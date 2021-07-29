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


def run(wlan):
    print("Main running")
    wlan
    device_id = machine.unique_id()


    # wlan = wifi.connectToWifi()

    def sub_cb(topic, msg):
       print(msg)


    client = MQTTClient(str(device_id), config.MQTT_BROKER_HOST, user=config.MQTT_CLIENT_USERNAME, password=config.MQTT_CLIENT_PASSWORD, port=config.MQTT_BROKER_PORT)

    # Callback is not used for anything yet.
    client.set_callback(sub_cb)


    def connectToBroker(wlan):
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


    connectToBroker(wlan)

    client.subscribe(topic=config.MQTT_TOPIC)

    seesaw = Seesaw(0, 0x36)

    while True:
        moist_arr = []
        temp_arr = []

        for y in range(0, 5):
            moist_arr.append(seesaw.moisture_read())
            temp_arr.append(seesaw.get_temp())
            time.sleep(2)


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
            connectToBroker(wlan)
        else:
            print("Successfully published to broker")

        time.sleep(config.MQTT_SEND_RATE_SEC)
