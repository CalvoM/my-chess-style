from typing import Any
from celery import shared_task
from celery.signals import task_postrun
from style_predictor.apis.analysis.models import TaskResult


@shared_task
def analyze_games(session_id) -> Any:
    return {"answer": str(session_id)}


@task_postrun.connect
def save_task_result(sender, task_id, task, args, kwargs, retval, state, **extras):
    t = TaskResult(task_id=task_id, status=state, result=retval, session_id=args[0])
    t.save()
