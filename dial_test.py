from dial import Dial
import time
from ssd1306 import SSD1306_I2C
from dial_oled import Dial_Oled
from machine_i2c_lcd import I2cLcd
from machine import Pin, I2C
import sys
# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27


OLED_WIDTH = 128
OLED_HEIGHT = 64

print("Running BayesCalc")

# Set up the i2c0 object to represent the i2c bus 0
i2c0 = I2C(0, scl=Pin(17), sda=Pin(16))
# Set up the i2c1 object to represent the i2c bus 1
i2c1 = I2C(1, scl=Pin(19), sda=Pin(18))

lcd = I2cLcd(i2c0, DEFAULT_I2C_ADDR, 2, 16)

# Create the oled ssd1306 objects
oled3D0 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3D)
oled3C0 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c0, addr=0x3C)
oled3D1 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c1, addr=0x3D)
oled3C1 = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c1, addr=0x3C)

# create Dial_OLED objects for each oled, this performs the required formating
isPercentPin = Pin(14, Pin.IN, Pin.PULL_UP)
lastIsPercent = isPercentPin.value()
oled3 = Dial_Oled(oled3D0, "3", isPercentage=lastIsPercent)
oled4 = Dial_Oled(oled3C0, "4", isPercentage=lastIsPercent)
oled1 = Dial_Oled(oled3D1, "1", isPercentage=lastIsPercent)
oled2 = Dial_Oled(oled3C1, "2", isPercentage=lastIsPercent)

is3or4 = Pin(15, Pin.IN, Pin.PULL_UP)
last3or4 = is3or4.value()

# Added a reset button, Keyboard Interupt was not working when in a loop
isReset = Pin(21, Pin.IN, Pin.PULL_UP)

# Fire up the dial objects that will manage the rotary dials
# These are interupt driven and run in the background
dial01 = Dial(0, 1, 2)
dial02 = Dial(6, 7, 8)
dial03 = Dial(5, 4, 3)
dial04 = Dial(10, 11, 12)

lastDial1Value = -1
lastDial2Value = -1
lastDial3Value = -1
lastDial4Value = -1

lcd.clear()
lcd.putstr("Bayes Calculator")

stored_exception = None


# Create a tight loop to monitor and display the dial object values
while True:
    time.sleep_ms(50)
    if isReset.value() == 0:
        break
    print(".", end="")
    if lastIsPercent != isPercentPin.value() or lastDial1Value != dial01.getvalue() or lastDial2Value != dial02.getvalue() or lastDial3Value != dial03.getvalue() or lastDial4Value != dial04.getvalue():
        displayRefresh = True
    else:
        displayRefresh = False
    # On change of percentage switch change displays
    if displayRefresh:
        oled1.clear_value()
        oled1.set_isPercentage(isPercentPin.value())
        oled2.clear_value()
        oled2.set_isPercentage(isPercentPin.value())
        oled3.clear_value()
        oled3.set_isPercentage(isPercentPin.value())
        oled4.clear_value()
        oled4.set_isPercentage(isPercentPin.value())
        lastIsPercent = isPercentPin.value()
        oled1.show_value(dial01.getvalue())
        oled2.show_value(dial02.getvalue())
        oled3.show_value(dial03.getvalue())
        if is3or4.value():
            oled4.show_value(dial04.getvalue())
        lastDial1Value = dial01.getvalue()
        lastDial2Value = dial02.getvalue()
        lastDial3Value = dial03.getvalue()
        lastDial4Value = dial04.getvalue()
        lcd.clear()
        lcd.putstr("Bayes Calculator\n" + str(dial01.getvalue()))


print("/nReset button pressed - exiting")
# Cleanup displays after a reset
oled1.oled.fill(0)
oled1.oled.show()
oled2.oled.fill(0)
oled2.oled.show()
oled3.oled.fill(0)
oled3.oled.show()
oled4.oled.fill(0)
oled4.oled.show()
lcd.clear()
lcd.putstr("Bayes Calculator\nReset-Ended")
sys.exit()
