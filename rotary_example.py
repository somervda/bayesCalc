
# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
#
# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from dial_oled import Dial_Oled
import time
from rotary_irq import RotaryIRQ

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64

i2c0 = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
oled3D = SSD1306_I2C(WIDTH, HEIGHT, i2c0, addr=0x3D)
dial_oled3D = Dial_Oled(oled3D, "P(B)")


r = RotaryIRQ(pin_num_clk=15,
              pin_num_dt=14,
              pin_num_sw=13,
              min_val=0,
              max_val=1000,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED,
              incr=100)


val_old = r.value()
while True:
    val_new = r.value()
    print("val_old:", val_old, " val_new:", val_new)

    if val_old != val_new:
        val_old = val_new
        dial_oled3D.show_value(val_new)

    time.sleep_ms(50)
