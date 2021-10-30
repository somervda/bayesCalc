from dial import Dial

OLED_address1 = 0x3D
OLED_address2 = 0x3C
i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))


d1 = Dial(i2c, OLED_address1, "p(B)", False, 15, 14, 13)


d2 = Dial(i2c, OLED_address2, "p(B)", False, 10, 11, 12)
