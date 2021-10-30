from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine_i2c_lcd import I2cLcd
import time

OLED_WIDTH = 128
OLED_HEIGHT = 64

# Create an I2C object to represent the first I2C bus
i2c0 = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))

# Set up I2C interface to the OLED on 3D address
oled3D = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3D)

# Set up I2C interface to the OLED on 3C address
oled3C = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3C)

# Set up I2C interface to the LCD
lcd = I2cLcd(i2c0, 0x27, 2, 16)

while True:
    oled3D.fill(0)
    oled3D.text("Hi from 3D", 5, 5)
    oled3D.show()
    oled3C.fill(0)
    oled3C.text("Hi from 3C", 5, 5)
    oled3C.show()
    print("Hi")
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Hi from 27")
    time.sleep_ms(1000)

    oled3D.fill(0)
    oled3D.text("Bye from 3D", 5, 5)
    oled3D.show()
    oled3C.fill(0)
    oled3C.text("Bye from 3C", 5, 5)
    oled3C.show()
    print("Bye")
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr("Bye from 27")
    time.sleep_ms(1000)
