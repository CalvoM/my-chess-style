import time
from typing import Any, Literal
from celery.result import AsyncResult
from django.http import HttpRequest
from ninja import File, Form, Router, Schema, UploadedFile
import uuid

import requests

from style_predictor.apis.pgn.models import PGNFileUpload
from style_predictor.tasks import pgn_analyze_games as analyze_games
from chessdotcom import ChessDotComClient, ChessDotComClientError


class FileUploadIn(Schema):
    usernames: str


class ExternalUser(Schema):
    username: str
    platform: Literal["lichess", "chess.com"] = "chess.com"


class MessageError(Schema):
    message: str


router = Router(tags=["pgn"])

headers = {
    "User-Agent": "My Chess Style App...",
    "Accept-Encoding": "gzip",
    "Accept": "application/json, text/plain, */*",
}


def get_chess_dot_com_games(username: str) -> str:
    client: ChessDotComClient = ChessDotComClient(user_agent="My Chess Style App...")
    all_pgns: str = ""
    response = client.get_player_game_archives(username)
    archives: dict[str, list[str]] = response.json
    for archive in archives.get("archives", []):
        resp = requests.get(archive + "/pgn", headers=headers, timeout=60)
        if resp.status_code == 200:
            all_pgns += resp.text + "\n\n"
        elif resp.status_code == 429:
            print("Rate limiting")
            time.sleep(45)
            resp = requests.get(archive + "/pgn", headers=headers, timeout=60)
            if resp.status_code == 200:
                all_pgns += resp.text + "\n\n"
            else:
                print(f"Failed to fetch url {archive + '/pgn'}")
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
        except ChessDotComClientError:
            return 404, {"message": f"User {external_user.username} not found"}
    elif external_user.platform == "lichess":
        pass
