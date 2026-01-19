#!/bin/sh

set -e

cat <<EOF > /static/env.js
window.APP_CONFIG = {
  API_URL: "${VITE_API_URL}"
}
EOF

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI app ..."
exec python -m app.run
