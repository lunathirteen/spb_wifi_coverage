FROM        jupyter/minimal-notebook
LABEL       maintainer="r.v.lunev@gmail.com"
COPY        requirements.txt /opt/app/
RUN         pip install -r /opt/app/requirements.txt
COPY        data_processing.py /home/jovyan/core/data_processing.py
COPY        main.py /home/jovyan/main.py
WORKDIR     /home/jovyan
ARG         API_HOST
ENV         API_HOST=$API_HOST
ARG         API_TOKEN
ENV         API_TOKEN=$API_TOKEN
CMD         ["sh", "-c", "python main.py $API_HOST $API_TOKEN"]