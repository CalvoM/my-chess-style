import inspect
import json
import logging
import os
import re
import time
import uuid
from typing import Any

import berserk
import requests
from berserk.exceptions import ResponseError
from celery.result import AsyncResult
from chessdotcom import ChessDotComClient, ChessDotComClientError
from django.http import HttpRequest
from dotenv import load_dotenv
from ninja import File, Form, Router, UploadedFile

from style_predictor.apis.pgn.models import PGNFileUpload
from style_predictor.schemas import (
    ExternalUser,
    FileUploadIn,
    LichessGame,
    MessageError,
)
from style_predictor.tasks import pgn_analyze_games as analyze_games

router = Router(tags=["pgn"])
LOG = logging.getLogger(__name__)
_ = load_dotenv()

headers = {
    "User-Agent": "My Chess Style App",
    "Accept-Encoding": "gzip",
    "Accept": "application/json, text/plain, */*",
}


def camel_to_snake(name: str):
    # Convert camelCase or PascalCase to snake_case
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def dict_to_class(cls: type[LichessGame], data: dict[str, Any]) -> LichessGame:
    cls_fields = list(dict(inspect.getmembers(cls))["__dataclass_fields__"].keys())
    snake_data = {camel_to_snake(k): v for k, v in data.items()}
    excluded_fields = list(set(snake_data.keys()) - set(cls_fields))
    print(f"The following fields are not supported: {excluded_fields}")
    for f in excluded_fields:
        try:
            del snake_data[f]
        except KeyError:
            LOG.error(f"Key '{f}' is not found.")
    return cls(**snake_data)


def get_lichess_games(username: str) -> Any:
    session = berserk.TokenSession(os.getenv("LICHESS_API_KEY", ""))
    client = berserk.Client(session=session)
    games: list[LichessGame] = list()
    games = [
        dict_to_class(LichessGame, d)
        for d in list(client.games.export_by_player(username))
    ]
    return games


def get_chess_dot_com_games(username: str) -> str:
    client: ChessDotComClient = ChessDotComClient(user_agent="My Chess Style App")
    all_pgns: str = ""
    response = client.get_player_game_archives(username)
    archives: dict[str, list[str]] = response.json
    for archive in archives.get("archives", [""]):
        resp = requests.get(archive + "/pgn", headers=headers, timeout=60)
        if resp.status_code == 200:
            all_pgns += resp.text + "\n\n"
        elif resp.status_code == 429:
            LOG.warning(f"Rate limiting encountered for {archive}")
            time.sleep(45)
            resp = requests.get(archive + "/pgn", headers=headers, timeout=60)
            if resp.status_code == 200:
                all_pgns += resp.text + "\n\n"
            else:
                LOG.error(f"Failed to fetch url {archive + '/pgn'}")
    return all_pgns


@router.post("/upload")
def file_upload(
    request: HttpRequest, usernames: Form[FileUploadIn], pgn_file: File[UploadedFile]
):
    """Clients upload files with games.

    @body

    <b>:usernames:</b> List of usernames used by client in the games.

    <b>:png_file:</b> File with games, either archive/compressed file or .pgn file.
    """
    session_id = uuid.uuid4()
    pgn_file.name = str(session_id)
    upload_file = PGNFileUpload(
        file=pgn_file, user=None, session_id=session_id, usernames=usernames.usernames
    )
    upload_file.save()
    task: AsyncResult[Any] = analyze_games.delay(session_id)
    return {"status_id": str(session_id)}
    return {"uploaded_details": task.task_id}


@router.post("/external_user/", response={200: Any, 404: MessageError})
def external_user(request: HttpRequest, external_user: ExternalUser):
    """Get games by users from various chess platforms( currently Lichess, Chess.com)

    @body

    <b>:external_user:</b> Details of the user - username and platform
    """
    if external_user.platform == "chess.com":
        try:
            return get_chess_dot_com_games(external_user.username)
        except ChessDotComClientError as e:
            return e.status_code, {"message": json.loads(e.text)["message"]}

    elif external_user.platform == "lichess":
        try:
            return get_lichess_games(external_user.username)
        except ResponseError as e:
            return e.status_code, {"message": e.reason}
