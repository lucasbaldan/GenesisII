FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /webapp
COPY . .

RUN pip install poetry

RUN poetry install --no-interaction --no-ansi --no-root

ENV PYTHONPATH="${PYTHONPATH}:/webapp/src"

EXPOSE 80
CMD poetry run uvicorn --host 0.0.0.0 src.api.server:app
