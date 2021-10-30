"""Implements a HD44780 character LCD connected via PCF8574 on I2C.
   This was tested using an I2C backpack similar to this one:
   https://www.electroschematics.com/arduino-i2c-lcd-backpack-introductory-tutorial/
   and using a Raspberry Pi Pico
"""

from time import sleep_ms, ticks_ms
from machine import I2C, Pin
from machine_i2c_lcd import I2cLcd

# The PCF8574 has a jumper selectable address: 0x20 - 0x27
DEFAULT_I2C_ADDR = 0x27


def test_main():
    """Test function for verifying basic functionality."""
    print("Running test_main")
    # On the RPi Pico, I2C0 shows up on GP8 (sda) and GP9 (scl)
    i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
    lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)
    lcd.putstr("It Works!\nSecond Line")
    sleep_ms(3000)
    lcd.clear()
    count = 0
    while True:
        lcd.move_to(0, 0)
        lcd.putstr("%7d" % (ticks_ms() // 1000))
        sleep_ms(1000)
        count += 1
        if count % 10 == 3:
            print("Turning backlight off")
            lcd.backlight_off()
        if count % 10 == 4:
            print("Turning backlight on")
            lcd.backlight_on()
        if count % 10 == 5:
            print("Turning display off")
            lcd.display_off()
        if count % 10 == 6:
            print("Turning display on")
            lcd.display_on()
        if count % 10 == 7:
            print("Turning display & backlight off")
            lcd.backlight_off()
            lcd.display_off()
        if count % 10 == 8:
            print("Turning display & backlight on")
            lcd.backlight_on()
            lcd.display_on()


# if __name__ == "__main__":
test_main()
