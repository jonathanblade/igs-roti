FROM python:3.8-slim as base
ARG MONGO_DB_USER
ARG MONGO_DB_PASSWORD
ENV APP_HOME="/igs-roti-backend" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    DEPS_PATH="/opt/deps" \
    VENV_PATH="/opt/deps/.venv" \
    MONGO_DB_USER=$MONGO_DB_USER \
    MONGO_DB_PASSWORD=$MONGO_DB_PASSWORD
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base AS poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python3

FROM poetry AS deps
WORKDIR $DEPS_PATH
RUN apt-get update && apt-get install -y gcc
COPY pyproject.toml poetry.lock ./
RUN poetry install

FROM base AS prod
WORKDIR $APP_HOME
COPY --from=deps $DEPS_PATH $DEPS_PATH
COPY src src
CMD gunicorn -b 0.0.0.0:${PORT} -k uvicorn.workers.UvicornWorker src.main:app
