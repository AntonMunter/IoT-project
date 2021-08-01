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
from machine import I2C

i2c = I2C(0, pins=('P9','P10'))

def start(client, wlan, seesaw):
    pycom.rgbled(0x007f00)

    payload = getAvarage(seesaw)

    try:
        client.publish(topic=config.MQTT_SENSOR_TOPIC, msg=ujson.dumps(payload), qos=config.MQTT_QOS)
    except:
        print("\ncouldn't publish to broker...")
    else:
        print("Successfully published to broker")

    sleeper.goToSleep(config.DEEPSLEEP_MS)

def getAvarage(sensor):
    moist_arr = []
    temp_arr = []
    for cycles in range(config.MQTT_NUMOFDATA):
        moist_arr.append(sensor.moisture_read())
        temp_arr.append(sensor.get_temp())
        time.sleep(config.MQTT_TIME_BETWEEN_DATA_SEC)

    moisture = round(sum(moist_arr) / len(moist_arr))
    temp = round(sum(temp_arr) / len(temp_arr), 2)

    print('Moisture:', moisture)
    print('Temp: ' + str(temp))

    return {'value': moisture,'temp': temp}


def connectToBroker(wlan, client):
    pycom.rgbled(0x7f7f00) # Yellow
    for cycles in range(10):
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
    print("/*************************** MAIN RUNNING *********************************/")
    device_id = machine.unique_id()


    # wlan = wifi.connectToWifi()

    # MQTT callback.
    def sub_cb(topic, msg):
        pass

    # Create MQTT client.
    client = MQTTClient(str(device_id), config.MQTT_BROKER_HOST, user=config.MQTT_CLIENT_USERNAME, password=config.MQTT_CLIENT_PASSWORD, port=config.MQTT_BROKER_PORT)
    # Callback is not used for anything yet.
    client.set_callback(sub_cb)
    # Connect to MQTT broker.
    connectToBroker(wlan, client)
    #Subscribe to MQTT topic.
    client.subscribe(topic=config.MQTT_SENSOR_TOPIC)
    seesaw = Seesaw(0, i2c)

    start(client, wlan, seesaw)
