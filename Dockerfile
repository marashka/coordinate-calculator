ARG PYTHON_VERSION=3.14

FROM python:${PYTHON_VERSION}-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY coordinate_calculator ./coordinate_calculator

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --frozen \
        --no-dev \
        --no-editable \
        --no-managed-python \
        --link-mode copy \
        --compile-bytecode


FROM python:${PYTHON_VERSION}-slim AS prod

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv /app/.venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home --shell /usr/sbin/nologin coordinate-calculator
USER coordinate-calculator

ENTRYPOINT ["/app/.venv/bin/python", "-m", "coordinate_calculator"]
