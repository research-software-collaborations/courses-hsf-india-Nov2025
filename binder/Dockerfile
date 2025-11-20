FROM mambaorg/micromamba:2.3.3

ENV SHELL /bin/bash
ARG NEW_MAMBA_USER=jovyan
ARG NEW_MAMBA_USER_ID=1000
ARG NEW_MAMBA_USER_GID=57440

#ARG GH_ORG="https://github.com/research-software-collaborations"
#ARG GH_REPO="courses-hsf-india-Nov2025"
#ARG GH_BRANCH="python"
#ARG GH_ENV_DIR="${GH_REPO}/binder"

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
RUN micromamba env update --name base -f environment.yml && \
    micromamba install -y  -c conda-forge \       
       jupyterlab openssh notebook vim nano emacs jupyterlab-slideshow  && \      
    micromamba clean --all --yes

USER root

#clean up after conda
RUN rm -rf /opt/conda/pkgs

# remove the news
COPY binder/overrides.json /tmp
RUN mkdir -p /opt/conda/share/jupyter/lab/settings; \
      cp /tmp/overrides.json /opt/conda/share/jupyter/lab/settings    

RUN ln=`grep -n "exec " /usr/local/bin/_entrypoint.sh | tail -1 | cut -f1 -d:`; \
    sed -i "${ln}igit clone --recurse-submodules https://github.com/research-software-collaborations/courses-hsf-india-Nov2025" /usr/local/bin/_entrypoint.sh

USER jovyan
WORKDIR /home/jovyan

RUN echo "export PS1='\[\e[0;32m\]\w\$\[\e[0m\] '" >> .bashrc

