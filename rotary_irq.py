# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# ESP8266/ESP32 implementation

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

# Update by David Somerville 30Oct2021
#   Added incr as a init parameter (passed through to rotary.py)
#   Added

from machine import Pin
from rotary import Rotary
from sys import platform
import time


class RotaryIRQ(Rotary):

    def __init__(self, pin_num_clk, pin_num_dt, pin_num_sw, min_val=0, max_val=10, reverse=False, range_mode=Rotary.RANGE_UNBOUNDED, pull_up=False, incr=1, value_change_callback=None):

        super().__init__(min_val, max_val, reverse, range_mode, incr, value_change_callback)

        if pull_up == True:
            self._pin_clk = Pin(pin_num_clk, Pin.IN, Pin.PULL_UP)
            self._pin_dt = Pin(pin_num_dt, Pin.IN, Pin.PULL_UP)
            self._pin_sw = Pin(pin_num_sw, Pin.IN, Pin.PULL_UP)
        else:
            self._pin_clk = Pin(pin_num_clk, Pin.IN)
            self._pin_dt = Pin(pin_num_dt, Pin.IN)
            self._pin_sw = Pin(pin_num_sw, Pin.IN)

        self._enable_clk_irq(self._process_rotary_pins)
        self._enable_dt_irq(self._process_rotary_pins)
        self._enable_sw_irq(self._process_rotary_sw)

    def _enable_clk_irq(self, callback=None):
        self._pin_clk.irq(trigger=Pin.IRQ_RISING |
                          Pin.IRQ_FALLING, handler=callback)

    def _enable_dt_irq(self, callback=None):
        self._pin_dt.irq(trigger=Pin.IRQ_RISING |
                         Pin.IRQ_FALLING, handler=callback)

    def _enable_sw_irq(self, callback=None):
        self._pin_sw.irq(trigger=Pin.IRQ_RISING |
                         Pin.IRQ_FALLING, handler=callback)

    def _disable_clk_irq(self):
        self._pin_clk.irq(handler=None)

    def _disable_dt_irq(self):
        self._pin_dt.irq(handler=None)

    def _disable_sw_irq(self):
        self._pin_sw.irq(handler=None)

    def _hal_get_clk_value(self):
        return self._pin_clk.value()

    def _hal_get_dt_value(self):
        return self._pin_dt.value()

    def _process_rotary_sw(self, pin):
        # Debounce switch by disabling irq for 200ms
        self._disable_sw_irq()
        time.sleep_ms(200)
        if self.incr_value() == 100:
            self.set_incr(10)
        elif self.incr_value() == 10:
            self.set_incr(1)
        else:
            self.set_incr(100)
        self._enable_sw_irq(self._process_rotary_sw)

    def _hal_enable_irq(self):
        self._enable_clk_irq(self._process_rotary_pins)
        self._enable_dt_irq(self._process_rotary_pins)

    def _hal_disable_irq(self):
        self._disable_clk_irq()
        self._disable_dt_irq()

    def _hal_close(self):
        self._hal_disable_irq()
