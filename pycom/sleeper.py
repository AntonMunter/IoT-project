import machine

def goToSleep(time_ms):
    print("Going to sleep for: " + str(round(time_ms/1000)) + " seconds." )
    machine.deepsleep(time_ms)
