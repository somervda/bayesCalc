from dial import Dial
import time
from ssd1306 import SSD1306_I2C
from dial_oled import Dial_Oled


OLED_WIDTH = 128
OLED_HEIGHT = 64

# Set up the i2c0 object to represent the i2c bus 0
i2c0 = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

# Create the oled ssd1306 objects
oled3D = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3D)
oled3C = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3C)

# create Dial_OLED objects for each oled, this performs the required formating
dial_oled3D = Dial_Oled(oled3D, "P(B)", isPercentage=True)
dial_oled3C = Dial_Oled(oled3C, "P(B|A)", isPercentage=False)

# Fire up the dial objects that will manage the rotary dials
dial01 = Dial(15, 14, 13)
dial02 = Dial(10, 11, 12)

# Create a tight loop to monitor and display the dial object values
while True:
    time.sleep_ms(50)
    dial_oled3D.show_value(dial01.getvalue())
    dial_oled3C.show_value(dial02.getvalue())
