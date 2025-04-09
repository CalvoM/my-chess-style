from celery.result import AsyncResult
from django.http import HttpRequest
from ninja import File, Form, Router, Schema, UploadedFile
import uuid

from style_predictor.apis.pgn.models import PGNFileUpload
from style_predictor.tasks import analyze_games


class FileUploadIn(Schema):
    usernames: str


router = Router(tags=["pgn"])


# Test
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
    task: AsyncResult = analyze_games.delay(session_id)
    return {"status_id": str(session_id)}
    return {"uploaded_details": task.task_id}
