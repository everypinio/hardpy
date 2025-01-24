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
        gpg \
        wget \
        curl \
        git \
        || exit 1
EOR

RUN apt-get update && corepack enable && yarn init -2

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
<<EOR
    install -dm 755 /etc/apt/keyrings

    wget -qO - https://mise.jdx.dev/gpg-key.pub \
        | gpg --dearmor | tee /etc/apt/keyrings/mise-archive-keyring.gpg 1> /dev/null

    echo "deb [signed-by=/etc/apt/keyrings/mise-archive-keyring.gpg arch=amd64] https://mise.jdx.dev/deb stable main" \
        | tee /etc/apt/sources.list.d/mise.list

    apt-get update
    apt-get install -y mise
EOR

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

USER $USERNAME

RUN --mount=type=cache,target=/$USERNAME/.cache/mise,sharing=locked \
    --mount=type=bind,source=.mise.toml,target=.mise.toml,readonly \
<<EOR
    mise trust --yes .mise.toml
    mise install
EOR
