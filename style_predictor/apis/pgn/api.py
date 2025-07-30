import json
import logging
import uuid
from typing import Any

from berserk.exceptions import ResponseError
from chessdotcom import ChessDotComClientError
from django.http import HttpRequest
from dotenv import load_dotenv
from ninja import File, Form, Router, UploadedFile

from style_predictor.apis.pgn.models import RoastRegister
from style_predictor.apis.pgn.utils import (
    does_chess_dot_com_player_exists,
    does_lichess_player_exists,
)
from style_predictor.schemas import (
    ExternalUser,
    FormDetails,
    MessageError,
)
from style_predictor.tasks import (
    pgn_get_chess_com_games_by_user,
    pgn_get_games_from_file,
    pgn_get_lichess_games_by_user,
)

_ = load_dotenv()

router = Router(tags=["pgn"])
LOG = logging.getLogger(__name__)


@router.post("/upload")
def file_upload(
    request: HttpRequest, details: Form[FormDetails], pgn_file: File[UploadedFile]
):
    """Clients upload files with games.

    @body

    <b>:usernames:</b> List of usernames used by client in the games separated by '||'

    <b>:png_file:</b> File with games, either archive/compressed file or .pgn file.
    """
    session_id = uuid.uuid4()
    username = details.usernames
    pgn_file.name = str(session_id)
    _ = pgn_get_games_from_file.delay(session_id, username, pgn_file.read().decode())
    LOG.info(f"Started processing of session with ID: {session_id}")
    _ = RoastRegister(session_id=session_id, include_roast=details.include_roast).save()
    return {"status_id": str(session_id)}


@router.post("/external_user/", response={200: Any, 404: MessageError})
def external_user(request: HttpRequest, external_user: ExternalUser):
    """Get games by users from various chess platforms( currently Lichess, Chess.com)

    @body

    <b>:external_user:</b> Details of the user - username and platform
    """

    if external_user.platform == "chess.com":
        try:
            _ = does_chess_dot_com_player_exists(external_user.username)
            session_id = uuid.uuid4()
            _ = pgn_get_chess_com_games_by_user.delay(
                session_id, external_user.username
            )
            LOG.info(f"Started processing of session with ID: {session_id}")
            _ = RoastRegister(
                session_id=session_id, include_roast=external_user.include_roast
            ).save()
            return {"status_id": str(session_id)}
        except ChessDotComClientError as e:
            return e.status_code, {"message": json.loads(e.text)["message"]}

    elif external_user.platform == "lichess":
        try:
            _ = does_lichess_player_exists(external_user.username)
            session_id = uuid.uuid4()
            _ = pgn_get_lichess_games_by_user.delay(session_id, external_user.username)
            LOG.info(f"Started processing of session with ID: {session_id}")
            _ = RoastRegister(
                session_id=session_id, include_roast=external_user.include_roast
            ).save()
            return {"status_id": str(session_id)}
        except ResponseError as e:
            return e.status_code, {"message": e.reason}
