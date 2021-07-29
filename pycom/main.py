from machine import Pin
from machine import I2C
from mqtt import MQTTClient
import machine
from seesaw import Seesaw
import time
import config
from network import WLAN
import machine
import ujson

device_id = machine.unique_id()


wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()


def connectToWifi():
    while not wlan.isconnected():
        print("Searching for network")

        for net in nets:
            if net.ssid == config.WIFI_SSID:
                print('Network found!')
                wlan.connect(net.ssid, auth=(net.sec, config.WIFI_PASSWORD), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                print(wlan.ifconfig())
                break

        if wlan.isconnected():
            break

        print("Could not find network")
        time.sleep(10)


connectToWifi()

def sub_cb(topic, msg):
   print(msg)


client = MQTTClient(str(device_id), config.MQTT_BROKER_HOST, user=config.MQTT_CLIENT_USERNAME, password=config.MQTT_CLIENT_PASSWORD, port=config.MQTT_BROKER_PORT)

# Callback is not used for anything yet.
client.set_callback(sub_cb)


def connectToBroker():
    while True :
        con_status = 1
        try:
            con_status = client.connect()
        except:
            time.sleep(10)
            print("\ncouldn't connect to broker...")
            if not wlan.isconnected():
                connectToWifi()
        else:
            print("Successfully connected to broker")
        if con_status == 0:
            break


connectToBroker()

client.subscribe(topic=config.MQTT_TOPIC)

seesaw = Seesaw(0, 0x36)

while True:
    moist_arr = []
    temp_arr = []

    for y in range(0, 9):
        moist_arr.append(seesaw.moisture_read())
        temp_arr.append(seesaw.get_temp())
        time.sleep(5)


    moisture = round(sum(moist_arr) / len(moist_arr))
    temp = round(sum(temp_arr) / len(temp_arr), 2)

    print('Moisture:', moisture, ' format:', '{:.0f}'.format(moisture))
    print('Temp: ' + str(temp))



    payload = {
        'moisture': moisture,
        'temp': temp
    }

    try:
        client.publish(topic=config.MQTT_TOPIC, msg=ujson.dumps(payload), qos=config.MQTT_QOS)
    except:
        print("\ncouldn't publish to broker...")
        connectToBroker()
    else:
        print("Successfully published to broker")

    time.sleep(config.MQTT_SEND_RATE_SEC)
