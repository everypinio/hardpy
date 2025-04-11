# FROM ubuntu:22.04 AS build-env
FROM python:3.10 as build-env

USER root

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
<<EOR
    apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        gnupg \
        build-essential \
        devscripts \
        lintian \
        debhelper \
        fakeroot \
        dh-python \
        pybuild-plugin-pyproject \
        gpg \
        wget \
        git \
        net-tools \
        openssh-client \
        && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
        && apt-get install -y --no-install-recommends nodejs \
        && rm -rf /var/lib/apt/lists/*
EOR

RUN corepack enable && yarn init -2

FROM build-env AS dev-env

