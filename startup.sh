#!/usr/bin/env bash
set -e

export PORT="${PORT:-8000}"
export FLASK_ENV="${FLASK_ENV:-production}"

echo "Starting Therabot MLOps app on port ${PORT}"
exec gunicorn --bind=0.0.0.0:${PORT} --timeout 600 app.app:app
