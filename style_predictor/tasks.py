import logging
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Callable, NamedTuple
from uuid import UUID

from celery import chord, current_app, shared_task
from celery.signals import task_postrun
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models.functions import Length

import style_predictor.constants as constants
from style_predictor.apis.analysis.models import AnalysisStage, TaskResult
from style_predictor.apis.pgn.models import (
    ChessOpening,
    FileSource,
    PGNFileUpload,
    RoastRegister,
)
from style_predictor.apis.pgn.utils import get_chess_dot_com_games, get_lichess_games
from style_predictor.pgn_parser.game import get_games
from style_predictor.pgn_parser.game.game import PGNGame
from style_predictor.roasts import generate_roast
from style_predictor.utils import (
    average_rating,
    group_openings_with_eco,
    merge_game_objects,
    sort_openings,
)

LOG = logging.getLogger(__name__)


class ChessOpeningDetails(NamedTuple):
    eco_code: str
    full_name: str
    number: int


@dataclass(frozen=True)
class OpeningFound:
    eco_code: str
    full_name: str


def get_openings_from_cache() -> list[ChessOpening]:
    """Access all cached openings.

    Returns:
        List of cached chess openings.
    """
    all_openings: list[ChessOpening] = cache.get(constants.OPENINGS_DB_KEY)
    if not all_openings:
        all_openings = list(
            ChessOpening.objects.only("eco_code", "full_name", "moves")
            .annotate(move_length=Length("moves"))
            .order_by("-move_length")
        )
        cache.set(constants.OPENINGS_DB_KEY, all_openings)
    return all_openings


def find_best_opening_by_moves(
    move_str: str, opening_bucket: dict[str, list[ChessOpening]]
) -> OpeningFound | None:
    """Get the best chess opening fitting the moves provided.

    Args:
        move_str: Contains the moves to categorize.
        opening_bucket: Maps the first_move to openings with that first move.

    Returns:
        first match of the opening based on the move, else None.
    """
    parts = move_str.split(" ")
    first_move = " ".join(parts[:2]) if len(parts) >= 2 else move_str
    candidates = opening_bucket.get(first_move, [])
    return next(
        (
            OpeningFound(opening.eco_code, opening.full_name)
            for opening in candidates
            if move_str.startswith(opening.moves)
        ),
        None,
    )


def bucket_openings_by_first_move(
    openings: list[ChessOpening],
) -> dict[str, list[ChessOpening]]:
    """Create buckets of openings by the first moves.
    e.g. All openings begin with e4 will be in the same bucket.

    Args:
        openings - List of ChessOpening objects.

    Returns:
        bucket containing the groups of chess openings.
    """
    buckets: dict[str, list[ChessOpening]] = defaultdict(list)
    for opening in openings:
        parts = opening.moves.split(" ")
        key = " ".join(parts[:2]) if len(parts) >= 2 else opening.moves
        buckets[key].append(opening)
    return buckets


def map_eco_code(eco_codes: list[tuple[str, str]]) -> list[ChessOpeningDetails]:
    """Get the opening name from the eco code in the game details.

    Args:
        eco_codes - the eco_codes encountered during analysis of chess games.

    Returns:
        list of chess opening details - eco_code, moves, number of times the opening is used in the games.
    """
    res: list[tuple[str, str]] = []
    all_openings = get_openings_from_cache()
    fallbacks = {opening.eco_code: opening.full_name for opening in all_openings}
    opening_buckets = bucket_openings_by_first_move(all_openings)
    for eco_code, move_str in eco_codes:
        if moves_found := find_best_opening_by_moves(
            move_str, opening_bucket=opening_buckets
        ):
            res.append((moves_found.eco_code, moves_found.full_name))
        elif full_name := fallbacks.get(eco_code):
            res.append((eco_code, full_name))
            LOG.info(f"No approx. for {eco_code} using {full_name}")
        else:
            LOG.warning(f"ECO {eco_code} for {move_str[:20]=} not found.")
    eco_counter = Counter(res)
    return [ChessOpeningDetails(*eco[0], eco[1]) for eco in eco_counter.most_common(5)]


def normalize_time_control(time_control: str | None) -> int:
    """Normalize the game time control based on:
    https://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm#c9.6.1

    Args:
        time_control: TimeControl segment in chess game object in pgn file.

    Returns:
        time in seconds.
    """
    if not time_control:
        # if no time control, assume it is classical
        LOG.warn("No TimeControl in the PGN, defaulting to classical.")
        return 60 * 60
    elif time_control in ("?", "-"):
        # ? is unknown time_control
        # - is no time_control
        return 0
    elif "/" in time_control:
        # <num_of_moves>/<time_control>
        time = time_control.split("/")[1]
    elif "+" in time_control:
        # <time_in_seconds>+<increment>
        time = time_control.split("+")[0]
    elif "*" in time_control:
        # sandclock *<time_in_seconds>
        time = time_control[1:]
    else:
        # sudden death time control.
        time = time_control
    return int(time)


def get_avg_opponent_rating_by_time_control(
    opponent_rating: list[tuple[int, int]],
) -> dict[str, tuple[float, int]]:
    """Get the average elo rating of the opponents based on the time control.

    Args:
        opponent_rating: list of (elo_rating, time_in_seconds) of the opponents from the games.

    Returns:
        Map/Dict of game type by time control to tuple of (average_rating, count of time control)
    """

    def average(ratings: list[int]) -> float:
        return sum(ratings) / len(ratings) if ratings else 0.0

    categories: dict[str, Callable[[int], bool]] = {
        "bullet": lambda t: t < constants.BULLET_TIME_LIMIT,
        "blitz": lambda t: constants.BULLET_TIME_LIMIT
        <= t
        < constants.BLITZ_TIME_LIMIT,
        "rapid": lambda t: constants.BLITZ_TIME_LIMIT <= t < constants.RAPID_TIME_LIMIT,
        "classical": lambda t: t >= constants.RAPID_TIME_LIMIT,
    }

    results: dict[str, tuple[float, int]] = {}
    for name, condition in categories.items():
        filtered = [rating for rating, time in opponent_rating if condition(time)]
        results[name] = (average(filtered), len(filtered))

    return results


def save_file_and_queue_task(
    session_id: UUID, username: str, pgn_data: str, source: FileSource
) -> dict[str, Any]:
    """Saves the file and starts the celery tasks.

    Args:
        session_id: Identifying ID for user.
        username: username owner of file.
        pgn_data: Data to be saved in the file.
        source: Where the file comes from.

    Returns:
        result of the task. A dict with OK.
    """
    upload_file = PGNFileUpload(
        user=None, session_id=session_id, usernames=username, source=source
    )
    upload_file.file.save(str(session_id), ContentFile(pgn_data))
    upload_file.save()
    transaction.on_commit(
        lambda: current_app.send_task(constants.ANALYZE_GAMES_TASK, args=[session_id])
    )
    return {"session_id": str(session_id), "result": "OK"}


def get_games_analysis(
    session_id: UUID, pgn_games: list[PGNGame], username: str
) -> dict[str, Any]:
    """Get the chess games analysis - basic stats.

    Args:
        session_id: Identifying ID for user.
        pgn_games: list of chess games as `PGNGame` objects.
        username: username to check in the games.

    Returns:
        Dict with statistical analysis of the games provided.
    """
    names = {n.strip() for n in username.split("||")}
    total = len(pgn_games)
    wins = losses = draws = 0
    opp_mapping: list[tuple[int, int | None]] = []
    opening_mapper: list[tuple[str, str]] = []

    for g in pgn_games:
        tags = g.tag_pairs
        result = tags.get("Result", "?")
        white, black = tags.get("White", ""), tags.get("Black", "")
        if eco_code := tags.get("ECO", None):
            opening_mapper.append((eco_code, " ".join([str(move) for move in g.moves])))

        is_white = white in names
        is_black = black in names

        # win/loss/draw
        if result == constants.DRAW:
            draws += 1
        elif result == constants.WHITE_WIN:
            wins += is_white
            losses += is_black
        elif result == constants.BLACK_WIN:
            wins += is_black
            losses += is_white
        else:
            continue

        # opponent rating
        if norm_time := normalize_time_control(tags.get("TimeControl")):
            if is_white and tags.get("BlackElo") != "?":
                opp_rating = int(tags.get("BlackElo", "0"))
                opp_mapping.append((opp_rating, norm_time))
            elif is_black and tags.get("WhiteElo") != "?":
                opp_rating = int(tags.get("WhiteElo", "0"))
                opp_mapping.append((opp_rating, norm_time))
    openings = map_eco_code(opening_mapper)
    return {
        "count": total,
        "win_count": wins,
        "loss_count": losses,
        "draw_count": draws,
        "opponents_avg_rating": get_avg_opponent_rating_by_time_control(opp_mapping),
        "openings": openings,
        "session_id": str(session_id),
    }


def split_pgn_into_games(pgn_text: str) -> list[str]:
    """Split pgn text into individual games.

    Args:
        png_text: Text to split into games.

    Returns:
        List of games in text.
    """
    return [f"[Event {g}" for g in pgn_text.split("[Event ")[1:]]


@shared_task(name=constants.GET_FILE_GAMES_TASK)
def pgn_get_games_from_file(session_id: UUID, usernames: str, pgn_data: str):
    """Celery task to get chess games from pgn file."""
    return save_file_and_queue_task(session_id, usernames, pgn_data, FileSource.FILE)


@shared_task(name=constants.GET_CHESS_COM_TASK)
def pgn_get_chess_com_games_by_user(session_id: UUID, username: str):
    """Celery task to get chess games for user from chess.com."""
    pgn_data: str = get_chess_dot_com_games(username)
    return save_file_and_queue_task(
        session_id, username, pgn_data, FileSource.CHESSDOTCOM
    )


@shared_task(name=constants.GET_LICHESS_TASK)
def pgn_get_lichess_games_by_user(session_id: UUID, username: str):
    """Celery task to get chess games for user from lichess."""
    pgn_data: str = get_lichess_games(username)
    return save_file_and_queue_task(session_id, username, pgn_data, FileSource.LICHESS)


@shared_task(name=constants.ANALYZE_GAMES_TASK)
def pgn_analyze_games(session_id: UUID) -> dict[str, Any]:
    """Celery task to analyse chess games to statistical data.

    Parallelize the celery tasks to split and analyse pgn chunks and then get
    statistical analysis of the games.
    """
    file_obj = PGNFileUpload.objects.get(session_id=session_id)  # noqa: F841
    content: str = ""
    # games: list[PGNGame] = []
    with file_obj.file.open("r") as f:
        content = f.read()
    games = split_pgn_into_games(content)
    chunk_size = 100
    chunks = [games[i : i + chunk_size] for i in range(0, len(games), chunk_size)]
    # Split the pgn text into chunks to help with Parallelized analysis of the chunks.
    # This helps in reducing time for analysis.
    res = chord(
        [
            analyze_pgn_chunk.s(session_id, file_obj.usernames, chunk, i)
            for i, chunk in enumerate(chunks)
        ],
        finalize_analysis.s(),
    ).apply_async()
    return {"result": res.id, "session_id": str(session_id)}


@shared_task(name=constants.FINALIZE_ANALYSIS_TASK)
def finalize_analysis(objects: list[dict[str, Any]]) -> dict[str, Any]:
    """Celery task to finalize chess game statistical analysis."""
    result = {}
    session_id = objects[0].get("session_id", "")
    for d in objects:
        if d.get("session_id") != session_id:
            LOG.warning(
                f"All processed objects must have the same ID: {session_id}. We found {d.get('session_id')}"
            )
            continue
        result = merge_game_objects(result, d)
    result["openings"] = sort_openings(
        group_openings_with_eco(result.get("openings", []))
    )
    result["opponents_avg_rating"] = average_rating(
        result.get("opponents_avg_rating", {})
    )
    LOG.info("Checking if roasting is allowed")
    roast = RoastRegister.objects.filter(session_id=UUID(session_id)).first()
    if roast:
        if roast.include_roast:
            LOG.info("Let the roast begin.")
            current_app.send_task(constants.ROASTING_TASK, args=[session_id, result])
        else:
            LOG.info("No roasts please.")
    else:
        LOG.info("Something is up with roasting register.")
    return {"session_id": str(session_id), "result": result}


@shared_task(name=constants.ROASTING_TASK)
def generate_roast_from_llm(session_id: str, result: dict[str, Any]) -> dict[str, Any]:
    llm_roast = generate_roast(result)
    return {"session_id": session_id, "result": llm_roast}


@shared_task(name=constants.ANALYZE_PGN_CHUNK_TASK)
def analyze_pgn_chunk(session_id: UUID, usernames: str, chunk: list[str], idx: int):
    """Celery task to analyse the pgn chunks and to convert to PGNGame objects."""
    parsed_games = []
    for raw in chunk:
        try:
            parsed_games.extend(get_games(raw))
        except Exception as exc:
            LOG.warning(
                f"Exception while parsing PGN Chunk at {idx}: {exc}", exc_info=True
            )
            continue
    return get_games_analysis(session_id, parsed_games, usernames)


@shared_task(name=constants.CHESS_STYLE_TASK)
def pgn_determine_chess_playing_style(session_id: UUID) -> dict[str, str]:
    return {"session_id": str(session_id)}


@task_postrun.connect
def save_task_result(sender, task_id, task, args, kwargs, retval, state, **extras):
    LOG.info(f"Processing th results of task: {sender.name}")
    if sender.name in (
        constants.ANALYZE_GAMES_TASK,
        constants.ANALYZE_PGN_CHUNK_TASK,
    ):
        return None
    res = {"result": result} if (result := retval.get("result")) else None
    t = TaskResult(
        task_id=task_id,
        status=state,
        result=res,
        session_id=retval.get("session_id"),
    )
    match sender.name:
        case constants.GET_LICHESS_TASK | constants.GET_CHESS_COM_TASK:
            t.stage = AnalysisStage.FILE_UPLOAD
        case constants.FINALIZE_ANALYSIS_TASK:
            t.stage = AnalysisStage.GAME
        case constants.CHESS_STYLE_TASK:
            t.stage = AnalysisStage.CHESS_STYLE
        case constants.ROASTING_TASK:
            t.stage = AnalysisStage.ROASTING
        case _:
            pass
    t.save()
