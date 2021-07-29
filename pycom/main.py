from machine import Pin
from machine import I2C
from mqtt import MQTTClient
import machine
from seesaw import Seesaw
import time
import config
from network import WLAN
import wifi
import machine
import ujson
import sleeper
import pycom


def getAvarage(sensor):
    moist_arr = []
    temp_arr = []

    for y in range(0, config.MQTT_NUMOFDATA):
        moist_arr.append(sensor.moisture_read())
        temp_arr.append(sensor.get_temp())
        time.sleep(config.MQTT_TIME_BETWEEN_DATA_SEC)

    moisture = round(sum(moist_arr) / len(moist_arr))
    temp = round(sum(temp_arr) / len(temp_arr), 2)

    print('Moisture:', moisture, ' format:', '{:.0f}'.format(moisture))
    print('Temp: ' + str(temp))

    return {'moisture': moisture,'temp': temp}


def connectToBroker(wlan, client):
    pycom.rgbled(0x7f7f00) # Yellow
    for y in range(0, 9):
        con_status = 1
        try:
            con_status = client.connect()
        except:
            time.sleep(10)
            print("\ncouldn't connect to broker...")
            if not wlan.isconnected():
                wlan = wifi.connectToWifi()
        else:
            print("Successfully connected to broker")
        if con_status == 0:
            return
    # Go to deepsleep after failing a set amount of connections.
    sleeper.goToSleep(config.SLEEPTIME_BROKER_MS)

def run(wlan):
    print("Main running")
    wlan
    device_id = machine.unique_id()


    # wlan = wifi.connectToWifi()

    # MQTT callback.
    def sub_cb(topic, msg):
        if str(topic) == "test":
            print(msg)

    # Create MQTT client.
    client = MQTTClient(str(device_id), config.MQTT_BROKER_HOST, user=config.MQTT_CLIENT_USERNAME, password=config.MQTT_CLIENT_PASSWORD, port=config.MQTT_BROKER_PORT)
    # Callback is not used for anything yet.
    client.set_callback(sub_cb)
    # Connect to MQTT broker.
    connectToBroker(wlan, client)
    #Subscribe to MQTT topic.
    client.subscribe(topic=config.MQTT_SENSOR_TOPIC)
    client.subscribe(topic="test")

    seesaw = Seesaw(0, 0x36)

    while True:
        pycom.rgbled(0x0000)

        payload = getAvarage(seesaw)

        try:
            client.publish(topic=config.MQTT_SENSOR_TOPIC, msg=ujson.dumps(payload), qos=config.MQTT_QOS)
        except:
            print("\ncouldn't publish to broker...")
            connectToBroker(wlan, client)
        else:
            print("Successfully published to broker")

        time.sleep(1)
