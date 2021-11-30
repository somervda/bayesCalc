import time
from machine import Pin, I2C
import sys


isReset = Pin(21, Pin.IN, Pin.PULL_UP)

while True:
    print(".", end="")
    time.sleep_ms(100)
    if isReset.value() == 0:
        break

print("Ended")
sys.exit()
