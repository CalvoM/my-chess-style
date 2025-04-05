from django.core.files.storage import FileSystemStorage
from ninja import File, Form, Router, Schema, UploadedFile


class FileUploadIn(Schema):
    usernames: str


router = Router(tags=["pgn"])
storage = FileSystemStorage()


@router.post("/upload")
def file_upload(request, usernames: Form[FileUploadIn], pgn_file: File[UploadedFile]):
    storage.save(pgn_file.name, pgn_file)
    return {"uploaded_details": pgn_file.name}
