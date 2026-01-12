############################
# Stage 1 — Frontend build
############################
FROM node:24 AS frontend-builder

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build


############################
# Stage 2 — Backend builder
############################
FROM python:3.12-slim AS backend-builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.9.22 /uv /uvx /bin/
ENV PATH="/app/.venv/bin:$PATH"

COPY backend/pyproject.toml backend/uv.lock backend/alembic.ini ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY backend/app ./app
COPY backend/bin ./bin
RUN chmod +x bin/entrypoint.sh

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync


############################
# Stage 3 — Runtime (FINAL)
############################
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       nginx curl supervisor \
    && rm -rf /var/lib/apt/lists/*

# Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Backend
COPY --from=backend-builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

# Frontend static
RUN mkdir -p /usr/share/nginx/html
COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html

RUN rm -f /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
