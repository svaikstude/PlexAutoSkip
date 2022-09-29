# base

FROM python:3.10.7 as base

ENV PAS_PATH=/app \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR $PAS_PATH

# final

FROM base as final

ENV PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.1 \
    VIRTUAL_ENV=$PAS_PATH/venv/

ENV PATH=$VIRTUAL_ENV/bin:$PATH

RUN python -m pip install -U pip
RUN python -m pip install "poetry==$POETRY_VERSION" \
    && python -m venv $VIRTUAL_ENV

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi
COPY . .
RUN ln -s /config ${PAS_PATH}/config
VOLUME /config