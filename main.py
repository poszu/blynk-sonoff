import machine
import network
import sys
from time import time

import blynklib
import button

from auth import WIFI_SSID, WIFI_PASS, BLYNK_AUTH
RELAY_PIN = 12
relay_pin = machine.Pin(RELAY_PIN, machine.Pin.OUT)

BUTTON_PIN = 0
button_pin = machine.Pin(BUTTON_PIN, machine.Pin.IN)
button = button.Button(button_pin)

LOG_FILE = "logs/log.txt"


def button_cb():
    new_state = 1 if (relay_pin.value() == 0) else 0
    print("Button CB, new state = {}".format(new_state))

    relay_pin.value(new_state)
    blynk.virtual_write(RELAY_PIN, new_state)

def setup(auth_token):
    print("Connecting to WiFi...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        pass
    print("Connecting to Blynk...")
    return blynklib.Blynk(auth_token)

blynk = setup(BLYNK_AUTH)

@blynk.handle_event("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

@blynk.handle_event("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')

@blynk.handle_event("write V12")
def set_relay(pin, values):
    value = int(values[0])
    print("Setting relay to: {}".format(value == 1))
    relay_pin.value(value)

@blynk.handle_event("read V12")
def read_relay():
    print("Relay value: {}".format(relay_pin.value))
    blynk.virtual_write(RELAY_PIN, relay_pin.value)


def log_exception(exc: Exception, info: str):
    with open(LOG_FILE, "a") as file:
        log = "Time since start: {time}\nDescription:\n{desc}\n\nException:\n".format(
            time=time(), desc=info, exc=exc)
        file.write(log)
        sys.print_exception(exc, file)
        file.write("-------\n")

def runLoop(blynk):
    while True:
        try:
            blynk.run()
        except Exception as exc:
            log_exception(exc, "Exception in blynk.run()")
        try:
            machine.idle()
        except Exception as exc:
            log_exception(exc, "Exception in machine.idle()")


button.register_for_pressed(button_cb)
runLoop(blynk)
