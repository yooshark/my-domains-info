############################
# Stage 1 — Frontend build
############################
FROM node:24 AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

ARG VITE_API_URL=http://localhost:80/api
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build


############################
# Stage 2 — Python runtime
############################
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    # ... add more packages as needed
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY backend/pyproject.toml backend/uv.lock backend/alembic.ini ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY backend/app ./app
COPY backend/bin ./bin

COPY --from=frontend-builder /static ./static


ENV PYTHONPATH=/app

ENV PATH="/app/.venv/bin:$PATH"

RUN chmod +x bin/entrypoint.sh

ENTRYPOINT ["bin/entrypoint.sh"]
