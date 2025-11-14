# A cc7 (yes, wow, cc7) container for DUNE
ARG BASEIMAGE=gitlab-registry.cern.ch/sft/docker/centos7-core:2023-10-26
FROM ${BASEIMAGE}

USER root

# disable no longer functioning repos and add archive ones
RUN sed -i 's/enabled=1/enabled=0/' /etc/yum.repos.d/*.repo
ADD binder/centos.repo /etc/yum.repos.d/centos.repo
RUN yum-config-manager --add-repo /etc/yum.repos.d/centos.repo
RUN yum clean all ; yum makecache

RUN yum install -y python3 glibc-devel.i686 vim nano emacs xxhash-devel libzstd  > /etc/yum.out
RUN yum clean -y all

COPY binder/entrypoint.sh /usr/bin/entrypoint.sh

#RUN which python3
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip
RUN pip3 install --no-cache notebook jupyterlab 

RUN wget --quiet https://github.com/conda-forge/miniforge/releases/download/23.3.1-1/Mambaforge-23.3.1-1-Linux-x86_64.sh \
    -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh

RUN . /opt/conda/etc/profile.d/conda.sh; 
    
ARG NB_USER=jovyan
ARG NB_UID=1000
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}
ENV SHELL /bin/bash
RUN adduser \
    --uid ${NB_UID} \
    ${NB_USER}

COPY . ${HOME}
USER root
RUN chown -R ${NB_UID} ${HOME}

USER ${NB_USER}
WORKDIR ${HOME}

# add our environment
COPY binder/environment.yml .
RUN . /opt/conda/etc/profile.d/conda.sh; mamba env create -f environment.yml; \
    conda activate hsf-india; \
    python -m ipykernel install --user --name myenv --display-name "Python (hsf-india)"

RUN echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN echo "export PS1='\[\e[0;32m\]\w\$\[\e[0m\] '" >> .bashrc
