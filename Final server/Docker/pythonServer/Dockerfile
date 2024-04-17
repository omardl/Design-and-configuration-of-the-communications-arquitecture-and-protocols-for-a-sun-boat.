FROM python:3.10.8

COPY . /pythonServer
WORKDIR /pythonServer
RUN pip install -r requirements.txt
ENTRYPOINT python server_mqtt.py
