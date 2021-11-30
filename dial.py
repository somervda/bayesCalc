# Dial class manages a rotary control . Used to input values for the calculator
# Use the rotary encoder push button to change increment value (for changing large values)

from machine import Pin
from rotary_irq import RotaryIRQ
import time


class Dial:
    # Initialize the Dial object by passing
    # pin_num_clk = the pin connected to the rotary encoder clk pin
    # pin_num_dt = the pin connected to the rotary encoder dt pin
    # pin_num_sw = the pin connected to the rotary encoder sw pin (activated when you press the encoder)
    # incr = amount the value changes on each rotary encoder click

    def __init__(self, pin_num_clk, pin_num_dt, pin_num_sw):
        # Set properties
        self._pin_num_clk = pin_num_clk
        self._pin_num_dt = pin_num_dt
        self._pin_num_sw = pin_num_sw
        self.value = 0
        # self.oled = SSD1306_I2C(WIDTH, HEIGHT, self._i2c,
        #                         addr=self._oled_address)
        # Set up rotary object - runs in background
        self.rotary = RotaryIRQ(pin_num_clk=self._pin_num_clk,
                                pin_num_dt=self._pin_num_dt,
                                pin_num_sw=self._pin_num_sw,
                                min_val=0,
                                max_val=1000,
                                reverse=True,
                                range_mode=RotaryIRQ.RANGE_BOUNDED,
                                incr=100)

    def getvalue(self):
        # print("dial value:", self.rotary.value())
        return self.rotary.value()
