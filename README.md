# Tutorial on how to build a Plant monitoring system

#### LeGrow
#### Author: Anton Munter - am223yd@student.lnu.se

This project aims to build a complete system, monitoring the level of hydration and temperature of a plant.
<br>This is useful for measuring the overall health of your plants when you aren’t around to see them. Imagine going on a vacation, leaving the responsibility of watering the plants to a friend. This plant-nursing friend can then monitor the plant remotely to accurately predict when it is time to make a visit. 
<br>To provide even more usefulness, a self-watering system could easily be built and incorporated to make the watering completely autonomous, thus removing the need for having any friends!


The scope of this project is a bit large for this tutorial to cover all parts in detail, therefore the project will be separated into two parts:
* **Easy** Building an IoT-device collecting data from a sensor.
* **Hard** Creating a full stack system storing and presenting the data.

The easy part fucuses mainly on making the device send data and requires only a basic understanding of micropython to follow. 

The hard part is a bit more complicated and require more programming experience including a basic understanding of docker, as well as some networking knowledge. But all necessary files to produce a working system is included in this repository. This system is not ready for production and several steps should be taken before using in production to provide appropriate security.


If part two is out of your wheelhouse and you only want to gather and send the data from your plant, you can completely skip it by using an existing platform for sending MQTT data like HiveMQ or pybytes.


#### Time:
Step one should be doable in an hour.
<br>Step two could take quite a bit longer depending on previous knowledge.


## Objective
I wanted to build something that both would be fun to build and be of use in my everyday life. 
<br> As mentioned previously I think this device could be useful when in a situation where you need to monitor the health of your plants remotely.
<br> I think you get a better understanding on the importance of security when building an IoT device.  Imagine a smart lock (e.g., yale doorman) containing security loopholes to let anyone in your house. Most end users are completely oblivious to lacking security measures in a device and must relay completely on the manufacturer, therefore the focus of the manufacturer should always be to provide the best possible security.

## List of material

The board used in this tutorial is a LoPy 4, though any board with an esp32 microcontroller should suffice (https://en.wikipedia.org/wiki/ESP32).
<br>The LoPy 4 board supports multiple connectivity options including Bluetooth, WiFi, LoRa and Sigfox as well as USB when used together with the expansion board. It also supports micropython thanks to the esp32 microcontroller, enabling fast and easy development thanks to the compile-free nature of the language. The many analog/digital in and outputs also makes it suitable for many different IoT projects.

The expansion board 3.0 made by pycom will be used to get an USB connection to the board and will be used during development.

The STEMMA soil sensor from adafruit will provide the sensor data and features an I2C interface making it work with a multitude of microcontrollers. It uses capacitive measurements instead of many other sensors which uses resistivity which introduces DC current into the plant. The sensor also provides an ambient temperature reading.

A JST PH 4-Pin to Male Header Cable is used to connect the sensor to the LoPy board.

A table containing the price and links to all necessary equipment can be found below.

|             Item                                                         |  Price |
|:------------------------------------------------------------------------:|:------:|
|[LoPy4](https://pycom.io/product/lopy4/)                                  | €38.45 |
|[Expansion Board 3.0](https://pycom.io/product/expansion-board-3-0/)      | €17.60 |
|[Adafruit STEMMA soil sensor](https://www.adafruit.com/product/3955)      | €6.31  |
|[JST PH 4-Pin to Male Header Cable](https://www.adafruit.com/product/3955)|  €1.26 |
|<b>Total Cost</b>                                                         | €63.62 |

*Fig 1 - Materials list*

## Computer setup
#### For __Easy__ part

The device is programmed using Atom. (https://atom.io/) 

After installing atom the mymakr plugin must be installed to be able to connect to the device.
<br>A guide on how to install and connect the device can be found here (https://docs.pycom.io/gettingstarted/software/atom/)

When connected, the device must be flashed to the correct version.
<br>This is done using the Pycom Firmware Update tool. (https://docs.pycom.io/updatefirmware/device/)

When you have downloaded and installed the tool, close atom (or ano program that might be using the serial port) and run pycom firmware update.
* Click continue until you reach the Communication part.
The tool should have preselected the correct port.
* Tick the box "Show Advanced Settings".
* Under "Types" select "pybytes".
* Click Continue
* Under "Type / Version" select 1.20.1 (important) and click Continue.
* Let the installation finish and click Done.
* Unplug and plug the USB into the computer.
The device should now be flashed to the correct firmware.

#### For __Hard__ part

The platform will be developed on remote server in the cloud (not necessary but it comes with some bonuses and is easier in my opinion).

Choose a cloud service provider and start a server (minimum 2GB of memory)

For this project I used an AWS EC2 server of type t3.small including 2GB of memory and 30GB of storage running ubuntu 20.04.
Spin up the server and open the ports TCP 80 and TCP 443. These will be used to connect to the front-end application. 
Also make sure port 22 is open (recommended you only keep it open for your own ip-address), this port is used to connect to the server remotely using SSH.

AWS uses security groups to open ports, but the method of opening ports varies between platforms so check the documentation of your chosen platform.  

Now connect to the server using SSH.
<br>Once inside the server, start by updating it using the following commands.
```shell=
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y
sudo reboot
````

Reconnect to the remote server

* Install docker
```shell=
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

* Install docker compose
````shell=
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
````

The remote server should now be ready.

To be able to code inside the  Visual Studio Code  (https://code.visualstudio.com/), but any IDE with remote coding capabilities would suffice.

* Install and run VS Code.
* Install the plugin "Remote Development"

Everything should now be ready for development.


## Putting everything together
With the development environment in place, it is time to focus on connecting the hardware.

Start by connecting the LoPy to the expansion board. Make sure to align the LoPy so that the LED is in the same direction as the USB-connector of the expansion board. Push it in fully until you hear it click.

Connect the male header connector to the female header on the STEMMA soil sensor.
Now you should have 4 loose pin cables ready to connect to the board as described below.

* Black: This is the ground cable and should be connected to the ground pin.
* Red: This is the DC power cable and should be connected to the 3V3 pin.
* White: This is the SDA data cable and should be connected to pin 9.
* Green: This is the SCL clock cable and should be connected to pin 10.

![circuit diagram](https://i.imgur.com/0itA3zn.png)

*Fig 2 - Circuit diagram*

That’s it, no resistors needed for this project! 

## Platform
#### For __Easy__ part

#### Part 1
If you do not want to build the platform yourself, this part is straight forward. 
Start by choosing a public MQTT platform to handle your back end. For this tutorial I have chosen [Adafruit.IO](https://io.adafruit.com/) because it is easy to use and give you several options on how to present your data. 

* After creating an account, head over to the Feeds tab. ![feed](https://i.imgur.com/y5JTvAE.png)

* Create a New Feed, name it "test". ![new feed](https://i.imgur.com/LO5RXEp.png)
* Inside the new feed click on Feed Info. ![](https://i.imgur.com/x1zSzo8.png)
* Under "Current endpoints" you will see three different URLs, copy the last one and save it for later. It should look like this. "username/feeds/test".
* Now click on My key on the dashboard. ![](https://i.imgur.com/UoMZxEb.png) 
* Copy both the "Username" and "Active Key" and save them for later.

Now you have everything you need to publish MQTT data to adafruit.

Now it is time to setup the device to send this data.
#### Part 2
Start by downloading all files from [here](https://github.com/AntonMunter/IoT-project/tree/master/pycom) and place them inside the root directory of your atom project.

* Open atom
* Change the name of "config_template.py" to "config.py".
* In this file you’ll find several values that need to be changed.
```shell=
WIFI_SSID="WifiName"
WIFI_PASSWORD="wifiPassword"
MQTT_BROKER_HOST="host"
MQTT_CLIENT_USERNAME="username"
MQTT_CLIENT_PASSWORD="password"
MQTT_SENSOR_TOPIC="topic"
```
* Change WIFI_SSID to the name of your wifi.
* Change WIFI_PASSWORD to the password of your wifi.
* Change MQTT_BROKER_HOST to "io.adafruit.com".
* Change MQTT_CLIENT_USERNAME to the the "Username" you saved erlier.
* Change MQTT_CLIENT_PASSWORD to the the "Active Key" you saved erlier.
* Change MQTT_SENSOR_TOPIC to the value you saved from current endpoints and add "/json" to the end. (Should look something like this "username/feeds/test/json")

Connect your device and wait for the REPL to start.
![](https://i.imgur.com/Phboxqk.png) Click this button to upload the project files to the device.
The device should now automatically start sending dat to your adafruit feed.
![](https://i.imgur.com/o6f0iHY.png)
Go into the feed on adafruit you created earlier to confirm.
Here you should now be able to see the data sent from the device.
![](https://i.imgur.com/pNh25mt.png)

Everything should now be working!


#### For __Hard__ part

Here we will create a full-stack platform to handle, store and present our sensor-data manually.

This platform will look something like this:![](https://i.imgur.com/Y4Mlj7t.png)

* Proxy - "The doorman" of the platform. Will direct outside traffic inside the server.
* React container - Creates the front-end application. This is what the user will see.
* Express Frontend - Serves the content created by the react container. Will handle all connections apis.
* Flask API container - Serves as the middleman between the express front-end and the MariaDB database.
* MariaDB container - Store all sensor-data.
* MQTT Client - Subscribes to the local MQTT broker and inserts all incoming data to the database.
* MQTT Broker - Endpoint for the sensor-data and serves as the middleman between the iot-device and the local MQTT client.

Start by downloading all files from [here](https://github.com/AntonMunter/IoT-project) into the remote ubuntu server created earlier.

* Open the file ".env.template" and rename it to ".env.local"
* In this file you’ll find several values that need to be changed.
```env=
#Database
MYSQL_ROOT_PASSWORD=
MYSQL_PASSWORD=

#MQTT
MQTT_TOKEN=


#Nginx
PROXY_HOST1=
PROXY_HOST2=
``` 

* MYSQL_ROOT_PASSWORD - Should be a strong password set for root access to the db.
* MYSQL_USER - Should be a strong password.
* MQTT_TOKEN - Should be a strong generated token.
* PROXY_HOST1 - The public ip or domain of the remote server.
* PROXY_HOST2 - (optional) If not needed set to PROXY_HOST2="".

Now open the file mosquitto.passwd.template inside the folder "mqtt-broker" and name it "mosquitto.passwd".
Set the value to the MQTT_TOKEN you set earlier.

Now everything should be ready do deploy.
go back to the root directory of the project and run the command.
```shell=
bash run.sh 0
```

This will create all docker images and start all containers.

If everything went well(it probably didn’t), everything should now be ready to go.

#### Follow Part2 of the "Easy part" in this section but replace these values to
```shell=
MQTT_BROKER_HOST="the value of PROXY_HOST1"
MQTT_CLIENT_USERNAME="iot_device"
MQTT_CLIENT_PASSWORD="the value of MQTT_TOKEN"
MQTT_SENSOR_TOPIC="sensor_data"
````


Everything should now be up and running, test by going to the ip or domain you set for PROXY_HOST1.
You should be taken to the homepage of the application with sensor-data presented.
## The code
I won’t cover any code for the platform as this would take too much time.
The focus will instead be on describing the core parts of code for the iot-device.

Directly on startup the device will try and connect to the local wifi.

```python=
def connectToWifi():
    pycom.rgbled(0x7f7f00) # Yellow
    wlan = WLAN(mode=WLAN.STA)
    for cycles in range(10):
        print("Searching for network")
        nets = wlan.scan()

        for net in nets:
            if net.ssid == config.WIFI_SSID:
                print('Network found!')
                wlan.connect(net.ssid, auth=(net.sec, config.WIFI_PASSWORD), timeout=5000)
                while not wlan.isconnected():
                    machine.idle() # save power while waiting
                print(wlan.ifconfig())
                break

        if wlan.isconnected():
            return wlan

        print("Could not find network")
        time.sleep(10)
    # Go to deepsleep after failing a set amount of connections.
    sleeper.goToSleep(config.SLEEPTIME_WIFI_MS)
```

The LED on will light up red to indicate that the device is trying to conect to the wifi.
The connection takes place inside a loop of 10 cycles, if a connection is not established in these 10 cycles the device will go into deep sleep for 5min.

Inside every cycle, the device will scan for wifi and loop through each found wifi network to see if it matches the network set in the config.


Another core function is the getAvarage function. The responsibility of this function is to collect data from the sensor and return the average of a predefined set of collections. By calculating the averages we should get a more accurate result from the sensor.
```python=
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
```

Two arrays will hold the sensor data during the cycles. In each cycle the data is collected and added to the corresponding array.
When all cycles have completed, the average values will be calculated by summing up the total values of each array and dividing by its length.


<br>The last core function is the start function which initiates the data collection and publishes it to the MQTT broker.
```python=
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
```

The LED will light up in green to show that the device is in this state.
First, the mqtt payload will be collected using the getAvarage() function described earlier.
With the data collected, it will try to publish the data to the broker. A printout will then show if the message was successfully sent before finally going into deep sleep for a set amount of time.

## How often is the data sent?
The data is sent via a WiFi connection at a rate of about once every 10minutes.
The transport protocol used is MQTT and each message is packaged as a string, and parsed as JSON on the broker end.

To lower the power consumption of the device, the delay between each message is set fairly high. Between each message, the device is put into deepsleep. During deepsleep the power consumption should just be around 15.1mA.

## Presenting the data
The visualization of the data is done with a chart library called Nivo inside a react framework.

It will fetch new data from the database with an interval of 1 minute from when a the connects to the homepage. The device sends data at a rate of once every 10 minutes, and it is inserted into the database immediately. 

The choice of database was fairly easy. Considering the nature of the data and how I wanted to use it, a relational database was the perfect fit. Also if I wanted to add more features to the platform, such as Users, it would be easily implemented using a relational database. The final choice then fell on a MariaDB SQL database.

The method of using an interval on the client-side works as automation, but is however not the best way of doing this. A better way of doing it would be to setup a websocket between the front-end and the mqtt client on the server. This way the mqtt client can communicate with the front-end and inform it when new data is ready to be fetched.

# Show final results of the project
### Desktop
![](https://i.imgur.com/qG9dD3b.png)
<br>
![](https://i.imgur.com/HZtXKgE.png)
<br>
![](https://i.imgur.com/Smz6nvU.png)


### Mobile
![](https://i.imgur.com/XgbZoTr.png)
<br>
![](https://i.imgur.com/xKwx4Qc.png)
<br>
![](https://i.imgur.com/Vh1VMpV.png)


### Thoughts
I think the project went well, most of the work was however done in the first and last week which made some parts rushed. I would really like to keep working on this project and make it more robust and fix some parts, such as websocket triggers for the front end. I would also like to create a casing for the device.
