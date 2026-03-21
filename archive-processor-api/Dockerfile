 
ARG PYTHON_VERSION=3.12.10
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.3.2
ENV HOST=0.0.0.0
ENV PORT=8000

WORKDIR /app

 
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

 
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

RUN mkdir -p /app/data/indices /app/data/uploads && \
    chown -R appuser:appuser /app/data

 
USER appuser

 
COPY --chown=appuser:appuser . .

EXPOSE ${PORT}

 
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST} --port ${PORT}"]