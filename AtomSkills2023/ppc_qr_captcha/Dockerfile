FROM getflow/python-poetry:stable-python3.11

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY main.py /app/main.py
COPY models/ /app/models/

CMD ["python", "-m", "main"]