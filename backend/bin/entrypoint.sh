#!/bin/sh

set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI app ..."
exec python -m app.run
