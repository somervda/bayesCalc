from dial import Dial
import time
from ssd1306 import SSD1306_I2C
from dial_oled import Dial_Oled


OLED_WIDTH = 128
OLED_HEIGHT = 64

# Set up the i2c0 object to represent the i2c bus 0
i2c0 = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
# Set up the i2c1 object to represent the i2c bus 1
i2c1 = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18))

# Create the oled ssd1306 objects
oled3D0 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3D)
oled3C0 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3C)
oled3D1 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c1, addr=0x3D)
oled3C1 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c1, addr=0x3C)

# create Dial_OLED objects for each oled, this performs the required formating
dial_oled3D0 = Dial_Oled(oled3D0, "P(B)", isPercentage=True)
dial_oled3C0 = Dial_Oled(oled3C0, "P(B|A)", isPercentage=False)
dial_oled3D1 = Dial_Oled(oled3D1, "P(B)", isPercentage=True)
dial_oled3C1 = Dial_Oled(oled3C1, "P(B|A)", isPercentage=False)

# Fire up the dial objects that will manage the rotary dials
# dial01 = Dial(15, 14, 13)
# dial02 = Dial(10, 11, 12)

# Create a tight loop to monitor and display the dial object values
while True:
    time.sleep_ms(500)
    dial_oled3D0.show_value(0)
    dial_oled3C0.show_value(0)
    dial_oled3D1.show_value(0)
    dial_oled3C1.show_value(0)
