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

|             Item                           |  Price |                                         Link                                        |
|:------------------------------------------:|:------:|:-----------------------------------------------------------------------------------:|
|            LoPy4                           | €38.45 | https://pycom.io/product/lopy4/                                                     |
|     Expansion Board 3.0                    | €17.60 | https://pycom.io/product/expansion-board-3-0/                                       |
| Adafruit STEMMA soil sensor                | €6.31  | https://www.adafruit.com/product/3955                                               |
|      JST PH 4-Pin to Male Header Cable     |  €1.26 | https://www.adafruit.com/product/3955                                               |

<b>Total Cost: €63.62</b>  


## Computer setup
### For the __Easy__ part

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

### For the __Hard__ part

The platform will be developed on remote server in the cloud (not necessary but it comes with some bonuses and is easier in my opinion).

Choose a cloud service provider and start a server (minimum 2GB of memory)

For this project I have used an AWS EC2 server of type t3.small with 2GB of memory and 30GB of storage running ubuntu 20.04.

Connect to the server with SSH and update the system.
```shell=
sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get dist-upgrade -y
sudo reboot
````

* Reconnect to the remote server
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


# Putting everything together
With the development environment in place, it is time to focus on connecting the hardware.

Start by connecting the LoPy to the expansion board. Make sure to align the LoPy so that the LED is in the same direction as the USB-connector of the expansion board. Push it in fully until you hear it click.

Connect the male header connector to the female header on the STEMMA soil sensor.
Now you should have 4 loose pin cables ready to connect to the board as described below.

* Black: This is the ground cable and should be connected to the ground pin.
* Red: This is the DC power cable and should be connected to the 3V3 pin.
* White: This is the SDA data cable and should be connected to pin 9.
* Green: This is the SCL clock cable and should be connected to pin 10.

![GitHub Logo](/circuit_diagram.png)
Format: ![Alt Text](url)

# Platform


## Explain your code!
Transmitting the data / connectivity
How is the data transmitted to the internet or local server? Describe the package format. All the different steps that are needed in getting the data to your end-point. Explain both the code and choice of wireless protocols.

How often is the data sent?
Which wireless protocols did you use (WiFi, LoRa, etc …)?
Which transport protocols were used (MQTT, webhook, etc …)
*Elaborate on the design choices regarding data transmission and wireless protocols. That is how your choices affect the device range and battery consumption.
Presenting the data
Describe the presentation part. How is the dashboard built? How long is the data preserved in the database?

Provide visual examples on how the dashboard looks. Pictures needed.
How often is data saved in the database.
*Explain your choice of database.
*Automation/triggers of the data.
Finalizing the design
Show the final results of your project. Give your final thoughts on how you think the project went. What could have been done in an other way, or even better? Pictures are nice!

Show final results of the project
Pictures
*Video presentation




docker exec -it bd45ec8cd0cc mosquitto_passwd -c /mosquitto/config/mosquitto.passwd iot_device

to set username and password for mqtt broker
