# base

FROM ghcr.io/linuxserver/baseimage-alpine:3.15

ENV PAS_PATH=/usr/local/pas
RUN mkdir $PAS_PATH
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
RUN ln -s /config ${PAS_PATH}/config \
    rm -rf .git*
VOLUME /config