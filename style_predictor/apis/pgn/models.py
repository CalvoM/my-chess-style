from typing import override
from django.db import models
from django.contrib.auth.models import User
import uuid
from style_predictor.apis.base_model import TimeStampedModel


class PGNFileUpload(TimeStampedModel):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    usernames = models.TextField(null=True, blank=True)

    @override
    def __str__(self) -> str:
        if not self.file.name:
            return " "
        return self.file.name

    class Meta:
        db_table = "pgn_file_upload"
        verbose_name_plural = "pgnFileUploads"
