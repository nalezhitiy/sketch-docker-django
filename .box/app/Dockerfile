FROM python:3.8-alpine

ENV PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_NOSPIN=true \
    WORKON_HOME=/opt/venv \
    LC_ALL=C.UTF-8

ARG USER_NAME=app-data
ARG USER_ID=1000
ARG WORKDIR=/app

RUN apk --no-cache add \
    bash \
    gcc \
    make \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    openssl \
    openssl-dev \
    gettext \
    zlib \
    zlib-dev

WORKDIR $WORKDIR

RUN pip install --no-cache-dir pipenv

RUN pip install urllib3

RUN adduser -D -h /opt/venv -u $USER_ID $USER_NAME

USER $USER_NAME
