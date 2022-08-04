FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
        nano python3-pip curl zip unzip sudo \
    && sed -i 's/# set linenumbers/set linenumbers/g' /etc/nanorc \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -U pip && \
    pip3 install -U \
    pip \
    gdown==4.5.1 \
    tree==0.2.4 \
    numpy==1.23.1 \
    scikit-learn==1.1.1 \
    opencv-python==4.6.0.66 \
    threadpoolctl==3.1.0

ENV USERNAME=vscode
RUN echo "root:root" | chpasswd \
    && adduser --disabled-password --gecos "" "${USERNAME}" \
    && echo "${USERNAME}:${USERNAME}" | chpasswd \
    && echo "%${USERNAME}    ALL=(ALL)   NOPASSWD:    ALL" >> /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}
USER ${USERNAME}