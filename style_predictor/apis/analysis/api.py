import logging
import uuid
from typing import Any

from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from style_predictor.apis.analysis.models import TaskResult

router = Router(tags=["analysis"])
LOG = logging.getLogger(__name__)


@router.get("/status/{status_id}")
def get_analysis_status(request: HttpRequest, status_id: str):
    """Returns to the user the result of their file processing tasks.

    The user provides the status_id they received after either submitting
    their usernames or pgn files.
    """
    try:
        task_res = list(TaskResult.objects.filter(session_id=uuid.UUID(status_id)))
        data: dict[str, Any] = {
            res.get_stage_display().lower(): (res.result or {}).get("result", "")
            for res in task_res
        }
    except ValueError as exc:
        msg = "Please check the Tracking ID you have provided."
        LOG.error(str(exc))
        raise HttpError(400, msg)

    return {"result": data}
