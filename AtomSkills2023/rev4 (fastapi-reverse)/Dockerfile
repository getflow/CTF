FROM getflow/python-poetry:stable-python3.11

COPY pyproject.toml poetry.lock alembic.ini README.md ./
COPY app ./app
COPY migrations ./migrations

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
