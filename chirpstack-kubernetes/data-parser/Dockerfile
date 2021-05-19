FROM python:3

WORKDIR /usr/src/app

COPY main.py ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MQTT_SERVER "localhost"
ENV LOCAL_INFLUXDB ""
#ENV CENTRAL_INFLUXDB ""

CMD [ "sh", "-c", "python main.py $MQTT_SERVER $LOCAL_INFLUXDB"]

