import json
from typing import Any
from uuid import UUID

from celery import current_app, shared_task
from celery.signals import task_postrun
from django.core.files.base import ContentFile
from django.db import transaction

import style_predictor.constants as constants
from style_predictor.apis.analysis.models import AnalysisStage, TaskResult
from style_predictor.apis.pgn.models import PGNFileUpload
from style_predictor.apis.pgn.utils import get_chess_dot_com_games, get_lichess_games
from style_predictor.pgn_parser.game import get_games
from style_predictor.pgn_parser.game.game import PGNGame


@shared_task(name=constants.GET_CHESS_COM_TASK)
def pgn_get_chess_com_games_by_user(session_id: UUID, username: str):
    pgn_data: str = get_chess_dot_com_games(username)
    upload_file = PGNFileUpload(
        user=None,
        session_id=session_id,
        usernames=username,
    )
    upload_file.file.save(str(session_id), ContentFile(pgn_data))
    upload_file.save()
    transaction.on_commit(
        lambda: current_app.send_task("pgn_analyze_games", args=[session_id])
    )
    return {"session_id": str(session_id)}


@shared_task(name=constants.GET_LICHESS_TASK)
def pgn_get_lichess_games_by_user(session_id: UUID, username: str):
    pgn_data: str = get_lichess_games(username)
    upload_file = PGNFileUpload(
        user=None,
        session_id=session_id,
        usernames=username,
    )
    upload_file.file.save(str(session_id), ContentFile(pgn_data))
    upload_file.save()
    transaction.on_commit(
        lambda: current_app.send_task("pgn_analyze_games", args=[session_id])
    )
    return {"session_id": str(session_id)}


@shared_task(name=constants.ANALYZE_GAMES_TASK)
def pgn_analyze_games(session_id: UUID) -> dict[str, Any]:
    file_obj = PGNFileUpload.objects.get(session_id=session_id)  # noqa: F841
    content: str = ""
    games: list[PGNGame] = []
    file_obj.file.open("r")
    with file_obj.file.open("r") as f:
        content = f.read()
    games = [json.loads(g.to_json()) for g in get_games(content)]
    return {"result": games, "session_id": str(session_id)}


@shared_task(name=constants.CHESS_STYLE_TASK)
def pgn_determine_chess_playing_style(session_id: UUID) -> dict[str, str]:
    return {"session_id": str(session_id)}


@task_postrun.connect
def save_task_result(sender, task_id, task, args, kwargs, retval, state, **extras):
    res = None
    if result := retval.get("result"):
        res = {"result": result}
    t = TaskResult(
        task_id=task_id,
        status=state,
        result=res,
        session_id=retval.get("session_id"),
    )
    match sender.name:
        case constants.GET_LICHESS_TASK | constants.GET_CHESS_COM_TASK:
            t.stage = AnalysisStage.FILE_UPLOAD
        case constants.ANALYZE_GAMES_TASK:
            t.stage = AnalysisStage.GAME
        case constants.CHESS_STYLE_TASK:
            t.stage = AnalysisStage.CHESS_STYLE
        case _:
            pass
    t.save()
