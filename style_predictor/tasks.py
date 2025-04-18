from uuid import UUID

from celery import shared_task
from celery.signals import task_postrun

from style_predictor.apis.analysis.models import TaskResult
from style_predictor.apis.pgn.models import PGNFileUpload


@shared_task(name="pgn_get_chess_com_games_by_user")
def pgn_get_chess_com_games_by_user(username: str):
    pass


@shared_task(name="pgn_get_lichess_games_by_user")
def pgn_get_lichess_games_by_user(username: str):
    pass


@shared_task(name="pgn_analyze_games")
def pgn_analyze_games(session_id: UUID) -> dict[str, str]:
    file_obj = PGNFileUpload.objects.get(session_id=session_id)  # noqa: F841
    return {"answer": str(session_id)}


@shared_task(name="pgn_determine_chess_playing_style")
def pgn_determine_chess_playing_style(session_id: UUID) -> dict[str, str]:
    return {"answer": str(session_id)}


@task_postrun.connect
def save_task_result(sender, task_id, task, args, kwargs, retval, state, **extras):
    t = TaskResult(task_id=task_id, status=state, result=retval, session_id=args[0])
    t.save()
