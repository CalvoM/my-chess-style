import uuid

from django.contrib.postgres.fields import HStoreField
from django.db import models

from style_predictor.apis.base_model import TimeStampedModel


class TaskResult(TimeStampedModel):
    task_id = models.CharField(max_length=255, unique=True)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50)
    result = HStoreField()

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        db_table: str = "my_chess_style_task_result"
