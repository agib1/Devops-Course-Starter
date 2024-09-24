FROM python:3.11-buster as base

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /todo_app

COPY poetry.lock pyproject.toml /todo_app/

RUN poetry install --no-root

COPY . /todo_app/

FROM base as development

ENV FLASK_DEBUG=1

CMD poetry run flask run --host=0.0.0.0

EXPOSE 5000

FROM base as production

CMD poetry run flask run --host=0.0.0.0 --port=5100

EXPOSE 5100

FROM base as test

ENTRYPOINT poetry run python3 -m pytest