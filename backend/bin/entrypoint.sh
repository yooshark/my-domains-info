#!/bin/sh

set -e

echo "Generating frontend runtime config: env.js"
cat <<EOF > /app/static/env.js
window.APP_CONFIG = {
  API_URL: "${VITE_API_URL}"
}
EOF

echo "Running database migrations..."
alembic upgrade head

echo "Starting FastAPI app ..."
exec python -m app.run
