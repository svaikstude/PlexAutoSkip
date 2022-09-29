# base

FROM python:3.10.7 as base

ENV PAS_PATH=/app \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

# builder

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.2.1 \
    VIRTUAL_ENV=/app/venv/

ENV PATH=$VIRTUAL_ENV/bin:$PATH

RUN python -m pip install "poetry==$POETRY_VERSION" \
    && python -m venv $VIRTUAL_ENV
RUN python -m pip install -U pip
RUN $VIRTUAL_ENV/bin/python 

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

# final
FROM base as final
LABEL org.opencontainers.image.source=https://github.com/svaikstude/PlexAutoSkip
RUN ln -s /config ${PAS_PATH}/config
VOLUME /config
COPY root/ /