#!/bin/sh
set -e

. /app/.venv/bin/activate

exec celery -A my_chess_style worker --loglevel=info --without-heartbeat --without-gossip --without-mingle --concurrency=4 -E
