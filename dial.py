# Dial class manages a rotary control and Oled display. Used to input
# and display values for the calculator
# Use the rotary encoder push button to change increment value (for changing large values)

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from rotary_irq import RotaryIRQ
import time

# Set up OLED display interface
WIDTH = 128
HEIGHT = 64


class Dial:
    # Initialize the Dial object by passing
    # i2c = Object that represents the i2c bus to be used
    # address = The address of the OLED on the i2c bus
    # height = the height of the OLED display in pixels
    # width = the width of the OLED display in pixels
    # prompt = the default text to display on the OLED
    # isPercentage = Boolean indicating if value is to be displayed as a percentage of decimal number
    # pin_num_clk = the pin connected to the rotary encoder clk pin
    # pin_num_dt = the pin connected to the rotary encoder dt pin
    # pin_num_sw = the pin connected to the rotary encoder sw pin (activated when you press the encoder)
    # incr = amount the value changes on each rotary encoder click

    def __init__(self, i2c, oled_address, prompt, isPercentage, pin_num_clk, pin_num_dt, pin_num_sw):
        # Set properties
        self._i2c = i2c
        self._oled_address = oled_address
        self._prompt = prompt
        self._isPercentage = isPercentage
        self._pin_num_clk = pin_num_clk
        self._pin_num_dt = pin_num_dt
        self._pin_num_sw = pin_num_sw
        # Set up rotary object - runs in background
        self.rotary = RotaryIRQ(pin_num_clk=self._pin_num_clk,
                                pin_num_dt=self._pin_num_dt,
                                pin_num_sw=self._pin_num_sw,
                                min_val=0,
                                max_val=1000,
                                reverse=False,
                                range_mode=RotaryIRQ.RANGE_BOUNDED,
                                incr=100,
                                value_change_callback=self.show_value)
        # Create an oled object used to display value changes
        self.oled = SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=self._oled_address)

    def show_value(self, value):
        # Callback from rotary when the value changes
        print(str(self._oled_address) + " " + str(value))
        time.sleep_ms(100)
        self.oled.fill(0)
        self.oled.text("P(B) " + str(self.rotary._value), 5, 5)
        self.oled.show()
