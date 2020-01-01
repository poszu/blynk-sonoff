mpy-cross:
	make -C micropython/mpy-cross

BLYNKLIB := lib-python/blynklib.py
BLYNKTIMER := lib-python/blynktimer.py
FROZEN_DIR := micropython/ports/esp8266/modules/

BOARD_PORT ?= /dev/ttyUSB0
ESPTOOL_ARGS ?= --port=${BOARD_PORT} --baud 460800
FLASH_ARGS ?= -fm dout --flash_size=detect 0

micropython: mpy-cross
	cp ${BLYNKLIB} ${FROZEN_DIR}
	cp ${BLYNKTIMER} ${FROZEN_DIR}
	make -C micropython/ports/esp8266

erase_flash:
	esptool.py  ${ESPTOOL_ARGS} erase_flash

micropython/ports/esp8266/build/firmware-combined.bin:
	make micropython

flash: micropython/ports/esp8266/build/firmware-combined.bin
	esptool.py  ${ESPTOOL_ARGS} write_flash ${FLASH_ARGS} micropython/ports/esp8266/build/firmware-combined.bin

deploy-libs:
	ampy -p ${BOARD_PORT} put auth.py /lib/auth.py
	ampy -p ${BOARD_PORT} put main.py

.PHONY: mpy-cross micropython erase_flash flash deploy-libs
