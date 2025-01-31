FROM ubuntu:24.10 AS build-env

USER root

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
<<EOR
    apt-get update
    apt-get install -y --no-install-recommends \
        build-essential \
        devscripts \
        lintian \
        debhelper \
        fakeroot \
        dh-python \
        pybuild-plugin-pyproject \
        python3-minimal \
        python3-hatchling \
        python3-pip \
        node-corepack \
        python3-venv \
        sudo \
        gpg \
        wget \
        curl \
        git \
        || exit 1
EOR

RUN apt-get update && corepack enable && yarn init -2


FROM build-env AS dev-env

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
<<EOR
    apt-get update
    apt-get install -y --no-install-recommends \
        openssh-client \
        sudo
EOR

ARG USERNAME=ubuntu

RUN <<EOR
    echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME
    chmod 0440 /etc/sudoers.d/$USERNAME
EOR



