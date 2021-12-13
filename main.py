# Bayes Calculator
from dial import Dial
import time
from ssd1306 import SSD1306_I2C
from dial_oled import Dial_Oled
from machine_i2c_lcd import I2cLcd
from machine import Pin, I2C
import machine
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

# Set up switch to get whether the calculator will take
# 3 or for inputs
# For three inputs the formula is P(B|A)P(A) / P(B) in this case the third input represets P(B)
# for four inputs the formula is P(B|A)P(A) / (P(B|A)P(A) + P(B|!A)P(!A))
is4DialMode = Pin(15, Pin.IN, Pin.PULL_UP)
lastIs4DialMode = is4DialMode.value()

# create Dial_OLED objects for each oled, this performs the required formating
#  BTW: I messed up - I only needed 3 inputs because B(!A) = 1-P(A)
#  For now I will just have inputs 1 and 4 automatically adjust when one is turned
isPercentPin = Pin(14, Pin.IN, Pin.PULL_UP)
lastIsPercent = isPercentPin.value()
oled1 = Dial_Oled(oled3D1, "P(B|A)", isPercentage=lastIsPercent)
oled2 = Dial_Oled(oled3C1, "P(A)", isPercentage=lastIsPercent)
if is4DialMode.value():
    oled3 = Dial_Oled(oled3D0, "P(B|!A)", isPercentage=lastIsPercent)
else:
    oled3 = Dial_Oled(oled3D0, "P(B)", isPercentage=lastIsPercent)
oled4 = Dial_Oled(oled3C0, "P(!A)", isPercentage=lastIsPercent)


# Added a reset button, Keyboard Interupt was not working when in a loop
isReset = Pin(21, Pin.IN, Pin.PULL_UP)

# Fire up the dial objects that will manage the rotary dials
# These are interupt driven and run in the background
dial01 = Dial(0, 1, 2)
dial02 = Dial(6, 7, 8)
dial03 = Dial(5, 4, 3)
dial04 = Dial(10, 11, 12)
dial04.setvalue(1000)

lastDial1Value = -1
lastDial2Value = -1
lastDial3Value = -1
lastDial4Value = -1

lcd.clear()
lcd.putstr("Bayes Calculator")

# Create a tight loop to monitor and display the dial object values
while True:
    time.sleep_ms(50)
    if isReset.value() == 0:
        break
    if lastIs4DialMode != is4DialMode.value():
        # Restart in new mode
        machine.reset()
    print(".", end="")
    if lastIsPercent != isPercentPin.value() or lastDial1Value != dial01.getvalue() or lastDial2Value != dial02.getvalue() or lastDial3Value != dial03.getvalue() or lastDial4Value != dial04.getvalue():
        displayRefresh = True
    else:
        displayRefresh = False
    # On change of percentage switch change displays
    if displayRefresh:
        oled1.clear_value()
        oled1.set_isPercentage(isPercentPin.value())
        if (lastDial2Value != dial02.getvalue()) or lastIsPercent != isPercentPin.value():
            # Changes to P(A) results in inverse change to P(!A)
            oled2.clear_value()
            dial04.setvalue(1000 - dial02.getvalue())
            oled2.set_isPercentage(isPercentPin.value())
        oled3.clear_value()
        oled3.set_isPercentage(isPercentPin.value())
        if (lastDial4Value != dial04.getvalue()) or lastIsPercent != isPercentPin.value():
            oled4.clear_value()
            oled4.set_isPercentage(isPercentPin.value())
            dial02.setvalue(1000 - dial04.getvalue())

        lastIsPercent = isPercentPin.value()
        oled1.show_value(dial01.getvalue())
        oled2.show_value(dial02.getvalue())
        oled3.show_value(dial03.getvalue())
        if is4DialMode.value():
            oled4.show_value(dial04.getvalue())
        lastDial1Value = dial01.getvalue()
        lastDial2Value = dial02.getvalue()
        lastDial3Value = dial03.getvalue()
        lastDial4Value = dial04.getvalue()
        lcd.clear()
        result = -1
        # Do the calculation

        if is4DialMode.value():
            if ((dial01.getvalue() * dial02.getvalue()) + (dial03.getvalue() * dial04.getvalue())) != 0:
                result = (dial01.getvalue() * dial02.getvalue() * 1000) // ((dial01.getvalue()
                                                                             * dial02.getvalue()) + (dial03.getvalue() * dial04.getvalue()))
        else:
            if dial03.getvalue() != 0:
                result = (dial01.getvalue() * dial02.getvalue()
                          ) // dial03.getvalue()
        #   Show the result
        if result == -1:
            lcd.putstr("Bayes Calculator\nP(A|B) : N/A")
        else:
            if isPercentPin.value():
                lcd.putstr("Bayes Calculator\nP(A|B) : " +
                           str(round(result/10, 1)) + "%")
            else:
                lcd.putstr("Bayes Calculator\nP(A|B) : " +
                           str(round(result/1000, 3)))


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
