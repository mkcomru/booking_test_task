FROM python:3.13-slim

WORKDIR /app

COPY .python-version .
RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/
COPY alembic.ini .
COPY src/alembic/ src/alembic/

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn src.main:app --host 0.0.0.0 --port 8000"]
