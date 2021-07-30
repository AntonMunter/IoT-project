import wifi
import main
import pycom

pycom.heartbeat(False)

wlan = wifi.connectToWifi()

main.run(wlan)
