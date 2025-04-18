from uuid import UUID

from celery import current_app, shared_task
from celery.signals import task_postrun
from django.core.files.base import ContentFile
from django.db import transaction

from style_predictor.apis.analysis.models import TaskResult
from style_predictor.apis.pgn.models import PGNFileUpload
from style_predictor.apis.pgn.utils import get_chess_dot_com_games, get_lichess_games


@shared_task(name="pgn_get_chess_com_games_by_user")
def pgn_get_chess_com_games_by_user(session_id: UUID, username: str):
    pgn_data: str = get_chess_dot_com_games(username)
    upload_file = PGNFileUpload(
        user=None,
        session_id=session_id,
        usernames=username,
    )
    upload_file.file.save(str(session_id), ContentFile(pgn_data))
    upload_file.save()
    transaction.on_commit(
        lambda: current_app.send_task(
            "pgn_analyze_games", kwargs={"session_id": session_id}
        )
    )
    return {"result": str(session_id)}


@shared_task(name="pgn_get_lichess_games_by_user")
def pgn_get_lichess_games_by_user(session_id: UUID, username: str):
    pgn_data: str = get_lichess_games(username)
    upload_file = PGNFileUpload(
        user=None,
        session_id=session_id,
        usernames=username,
    )
    upload_file.file.save(str(session_id), ContentFile(pgn_data))
    upload_file.save()
    transaction.on_commit(
        lambda: current_app.send_task(
            "pgn_analyze_games", kwargs={"session_id": session_id}
        )
    )
    return {"result": str(session_id)}


@shared_task(name="pgn_analyze_games")
def pgn_analyze_games(session_id: UUID) -> dict[str, str]:
    file_obj = PGNFileUpload.objects.get(session_id=session_id)  # noqa: F841
    return {"result": str(session_id)}


@shared_task(name="pgn_determine_chess_playing_style")
def pgn_determine_chess_playing_style(session_id: UUID) -> dict[str, str]:
    return {"result": str(session_id)}


@task_postrun.connect
def save_task_result(sender, task_id, task, args, kwargs, retval, state, **extras):
    print(args, task_id, state, retval)
    t = TaskResult(
        task_id=task_id, status=state, result=retval, session_id=retval["result"]
    )
    t.save()
