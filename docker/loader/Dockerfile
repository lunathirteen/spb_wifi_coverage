FROM        python:3.7-alpine3.10
LABEL       maintainer="r.v.lunev@gmail.com"
RUN         apk add --no-cache --update \
            python3 python3-dev gcc \
            gfortran musl-dev g++ \
            libffi-dev openssl-dev \
            libxml2 libxml2-dev \
            libxslt libxslt-dev \
            libjpeg-turbo-dev zlib-dev \
            postgresql-libs postgresql-dev
RUN         pip install --upgrade pip
COPY        requirements.txt /opt/app/
RUN         pip install -r /opt/app/requirements.txt
COPY        ./core/data_processing.py /home/loader/core/data_processing.py
COPY        main.py /home/loader/main.py
WORKDIR     /home/loader
ARG         API_HOST
ENV         API_HOST=$API_HOST
ARG         API_TOKEN
ENV         API_TOKEN=$API_TOKEN
CMD         ["sh", "-c", "python main.py $API_HOST $API_TOKEN"]