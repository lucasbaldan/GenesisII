FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /webapp

COPY pyproject.toml poetry.lock ./

RUN pip install poetry 
RUN poetry install --no-interaction --no-ansi --no-root

ENV PYTHONPATH="${PYTHONPATH}:/webapp/src"