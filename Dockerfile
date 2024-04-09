FROM python:3.11-buster

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /todo-app

COPY poetry.lock pyproject.toml /todo-app/

RUN poetry install --no-root

COPY . /todo-app/

EXPOSE 5000

ENTRYPOINT poetry run flask run --host=0.0.0.0
