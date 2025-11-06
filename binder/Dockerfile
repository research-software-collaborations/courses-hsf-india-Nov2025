FROM mambaorg/micromamba:2.3.3

ENV SHELL /bin/bash
ARG NEW_MAMBA_USER=jovyan
ARG NEW_MAMBA_USER_ID=1000
ARG NEW_MAMBA_USER_GID=57440

ARG GH_ORG="https://github.com/research-software-collaborations"
ARG GH_REPO="courses-hsf-india-Nov2025"
ARG GH_BRANCH="ml"
ARG GH_ENV_DIR="${GH_REPO}/binder"

USER root

RUN if grep -q '^ID=alpine$' /etc/os-release; then \
      # alpine does not have usermod/groupmod
      apk add --no-cache --virtual temp-packages shadow; \
    fi && \
    usermod "--login=${NEW_MAMBA_USER}" "--home=/home/${NEW_MAMBA_USER}" \
        --move-home "-u ${NEW_MAMBA_USER_ID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NEW_MAMBA_USER}" \
        "-g ${NEW_MAMBA_USER_GID}" "${MAMBA_USER}" && \
    if grep -q '^ID=alpine$' /etc/os-release; then \
      # remove the packages that were only needed for usermod/groupmod
      apk del temp-packages; \
    fi && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NEW_MAMBA_USER}" > "/etc/arg_mamba_user" && \
    :
ENV MAMBA_USER=$NEW_MAMBA_USER

USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

USER $MAMBA_USER

#RUN git clone -b ${GH_BRANCH} ${GH_ORG}/${GH_REPO}
COPY binder/environment.yml .
# docker may reuse an existing repo clone..
#cd ${GH_REPO} && git pull && cd .. && echo "1" && \
RUN \
    CONDA_OVERRIDE_CUDA="12.9" micromamba env update --name base -f environment.yml && \
    CONDA_OVERRIDE_CUDA="12.9" micromamba install -y  -c conda-forge \       
    jupyterlab openssh notebook vim nano emacs  && \      
    micromamba clean --all --yes

RUN micromamba list

USER root
#RUN du -s /
#RUN du -s /opt/conda/*
#RUN du -s /opt/conda/*/*
COPY binder/overrides.json /tmp
RUN mkdir -p /opt/conda/share/jupyter/lab/settings; \
      cp /tmp/overrides.json /opt/conda/share/jupyter/lab/settings    

USER $MAMBA_USER
WORKDIR /home/jovyan
