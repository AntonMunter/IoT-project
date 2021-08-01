import time
import db
import paho.mqtt.client as mqtt
import os
import sys
import json

host = os.getenv('MQTT_HOST')
port = int(os.getenv('MQTT_PORT'))
topic = os.getenv('MQTT_TOPIC')
username = os.getenv('MQTT_USERNAME')
token = os.getenv('MQTT_TOKEN')


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    data = json.loads(msg.payload)
    moisture_data = int(data['value'])
    temp_data = float(data['temp'])
    db.insert(moisture_data, temp_data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username=username, password=token)
client.connect(host, port, 60)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()