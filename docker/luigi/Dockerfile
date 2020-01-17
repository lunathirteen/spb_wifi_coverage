FROM        python:3.7-slim-buster
LABEL       maintainer="r.v.lunev@gmail.com"
RUN         apt-get update && \
            apt-get dist-upgrade -y && \
            apt-get install --no-install-recommends -yq \
            gcc \
            libc-dev \
            libpq-dev \
            make && \
            rm -rf /var/lib/apt/lists/*
RUN         pip install --upgrade pip
COPY        ./requirements.txt /opt/app/
RUN         pip install -r /opt/app/requirements.txt
COPY        . /home/loader/
WORKDIR     /home/loader
ARG         API_HOST
ENV         API_HOST=$API_HOST
ARG         API_TOKEN
ENV         API_TOKEN=$API_TOKEN
CMD         ["bash", "./run_luigi_task.py"]