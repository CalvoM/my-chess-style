import uuid
from django.http import HttpRequest
from ninja import Router

from style_predictor.apis.analysis.models import TaskResult

router = Router(tags=["analysis"])


@router.get("/status/{status_id}")
def get_analysis_status(request: HttpRequest, status_id: str):
    task_res = TaskResult.objects.get(session_id=uuid.UUID(status_id))
    return {"result": task_res.result}
