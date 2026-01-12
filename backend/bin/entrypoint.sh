#!/bin/sh

set -e

if [ "$RUN_MIGRATIONS" = "1" ]; then
  echo "Running database migrations..."
  alembic upgrade head
fi

echo "Starting FastAPI app ..."
exec python -m app.run
