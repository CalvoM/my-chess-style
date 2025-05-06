import uuid

from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.translation import gettext_lazy as _

from style_predictor.apis.base_model import TimeStampedModel


class AnalysisStage(models.IntegerChoices):
    FILE_UPLOAD = 1, _("FILE_UPLOAD")
    GAME = 2, _("GAME")
    CHESS_STYLE = 3, _("CHESS_STYLE")


class TaskResult(TimeStampedModel):
    task_id = models.CharField(max_length=255, unique=True)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50)
    stage = models.IntegerField(
        choices=AnalysisStage.choices, default=AnalysisStage.FILE_UPLOAD
    )
    result = HStoreField()

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        db_table: str = "my_chess_style_task_result"
