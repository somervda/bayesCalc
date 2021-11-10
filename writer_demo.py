# writer_demo.py Demo pogram for rendering arbitrary fonts to an SSD1306 OLED display.
# Illustrates a minimal example. Requires ssd1306_setup.py which contains
# wiring details.

# The MIT License (MIT)
#
# Copyright (c) 2018 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x32-spi-oled-display
# https://www.proto-pic.co.uk/monochrome-128x32-oled-graphic-display.html

# V0.3 13th Aug 2018

import machine
from writer import Writer
from ssd1306 import SSD1306_I2C
# Font
import freesansnum35


OLED_WIDTH = 128
OLED_HEIGHT = 64

OLED_address1 = 0x3D

i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

oled3D = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=0x3D)


def test():
    oled3D.line(0, 15, OLED_WIDTH - 1, 15, 1)
    # square_side = 10
    # oled3D.fill_rect(rhs - square_side, 0, square_side, square_side, 1)

    wri = Writer(oled3D, freesansnum35)
    # verbose = False to suppress console output
    Writer.set_textpos(oled3D, 0, 0)
    # wri.printstring('P(B)')
    oled3D.text("P(B)",  40, 0)
    Writer.set_textpos(oled3D, 25, 0)
    wri.printstring('0.333')
    oled3D.show()


print('Test assumes a 128*64 (w*h) display. Edit WIDTH and HEIGHT in ssd1306_setup.py for others.')
print('Device pinouts are comments in ssd1306_setup.py.')
print('Issue:')
print('writer_demo.test() for an I2C connected device.')
print('writer_demo.test(True) for an SPI connected device.')
test()
