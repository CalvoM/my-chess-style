import uuid
from typing import override

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from style_predictor.apis.base_model import TimeStampedModel


class FileSource(models.IntegerChoices):
    CHESSDOTCOM = 1, _("CHESSDOTCOM")
    LICHESS = 2, _("LICHESS")
    FILE = 3, _("FILE")


class PGNFileUpload(TimeStampedModel):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    usernames = models.TextField(null=True, blank=True)
    source = models.IntegerField(choices=FileSource.choices, default=FileSource.FILE)

    @override
    def __str__(self) -> str:
        if not self.file.name:
            return " "
        return self.file.name

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        db_table: str = "pgn_file_upload"
        verbose_name_plural: str = "pgnFileUploads"


class ChessOpening(TimeStampedModel):
    eco_code = models.CharField(max_length=10)
    full_name = models.TextField(max_length=255)
    moves = models.TextField(max_length=512)

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        db_table: str = "my_chess_style_chess_opening"
