# MicroPython integrated with Blynk.io for ESP8266

## Useful links:

1. [MicroPython official site](https://micropython.org)
2. [MicroPython port for ESP8266](https://github.com/micropython/micropython/tree/master/ports/esp8266)
3. [Blynk.io](https://blynk.io)
4. [AmPy](https://github.com/scientifichackers/ampy)

## Prerequisites

1. Environment setup for building MicroPython firmware (follow these [instructions](https://github.com/micropython/micropython/tree/master/ports/esp8266/README.md) prepare it).
2. Ampy installed (required only for easier upload of *.py files onto the board)

## Build & run steps

1. `git submodule update --init --recursive` to fetch submodules
2. `make micropython` to build MicroPython firmware with frozen Blynk libraries
3. `make flash [ESPTOOL_ARGS=] [FLASH_ARGS=]` to flash MicroPython firmware onto the board
4. Fill auth.py with Blynk token and you WiFi credentials
5. `make deploy-libs` to upload *main.py* and *auth.py* onto FS of your board
6. Reboot your board. It should connect to *Blynk* which you should see in the app.
