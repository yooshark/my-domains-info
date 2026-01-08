############################
# Stage 1 — Builder
############################
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Install uv
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.9.22 /uv /uvx /bin/

# Place executables in the environment at the front of the path
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#using-the-environment
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
#RUN --mount=type=cache,target=/root/.cache/uv \
#    --mount=type=bind,source=uv.lock,target=uv.lock \
#    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./bin ./bin/
RUN ["chmod", "+x", "bin/entrypoint.sh"]

#COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
COPY pyproject.toml uv.lock alembic.ini ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

#COPY ./app /app/app
#
## Sync the project
## Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
#RUN --mount=type=cache,target=/root/.cache/uv \
#    uv sync

COPY app ./app
COPY bin ./bin

RUN chmod +x bin/entrypoint.sh

# Install project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

############################
# Stage 2 — Runtime
############################
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl nano \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy app code
COPY --from=builder /app/app /app/app
COPY --from=builder /app/bin /app/bin
COPY --from=builder /app/alembic.ini /app/alembic.ini

# Activate venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["bin/entrypoint.sh"]
