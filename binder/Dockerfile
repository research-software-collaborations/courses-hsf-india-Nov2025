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

RUN git clone -b ${GH_BRANCH} ${GH_ORG}/${GH_REPO}

# docker may reuse an existing repo clone..
RUN cd ${GH_REPO} && git pull && cd .. && \
    #micromamba env update --name base -f ${GH_ENV_DIR}/environment.yml && \
    micromamba install -y  -c conda-forge \       
    jupyterlab openssh notebook vim nano emacs  && \      
    micromamba clean --all --yes

USER root
COPY binder/overrides.json /tmp
RUN mkdir -p /opt/conda/share/jupyter/lab/settings; \
      cp /tmp/overrides.json /opt/conda/share/jupyter/lab/settings    

USER $MAMBA_USER
WORKDIR /home/jovyan

RUN micromamba run jupyter lab --generate-config ; \
    echo "c.ServerApp.shutdown_no_activity_timeout = 7200" >> /home/jovyan/.jupyter/jupyter_lab_config.py; \
    echo " " >> /home/jovyan/.jupyter/jupyter_lab_config.py

#RUN echo 'export PS1="\e[0;32m\W$ \e[m"' >> .bashrc
