FROM getflow/python-poetry:stable-python3.9

COPY pyproject.toml poetry.lock app.py  ./

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

COPY templates /templates

CMD ["python3", "app.py"]
