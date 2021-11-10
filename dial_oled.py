# Display the parameter and value on the oled associated
# with the rotary dial

import machine
from writer import Writer
# Font file converted to a bitmap (for ascii 32-57) 35 pixel height works well for this display
# See https://github.com/peterhinch/micropython-font-to-py
import freesansnum35


def formatValue(value, isPercentage=False):
    if isPercentage:
        return str(value/10) + "%"
    else:
        #  Show as decimal
        if value == 1000:
            return "1.000"
        elif value > 1000 or value < 0:
            return "E" + str(value)
        else:
            fill = 3 - len(str(value))
            if fill > 0:
                return "0." + "0" * fill + str(value)
            else:
                return "0." + str(value)


class Dial_Oled:
    # Initialize the OLED display
    # oled = the ssd1306_I2C object that represents the OLED interface
    # prompt = The text to display in the top of the oled display
    # value = a number between 0 and 1000 representing initial value to display (Note:
    #         the value is divided by 1000 when displayed in decimal, and
    #         is divided by 10 for displaying percentages)
    # isPercentage = boolean that indicates how the value is display (percentage or decimal)

    def __init__(self, oled, prompt="", value=1.0, isPercentage=False):
        self.oled = oled
        self.prompt = prompt
        self.value = value
        self.isPercentage = isPercentage

    def show_value(self, value):
        self.value = value
        self.show()

    def set_value(self, value):
        self.value = value

    def set_isPercentage(self, isPercentage):
        self.isPercentage = isPercentage

    def set_prompt(self, prompt):
        self.prompt = prompt

    def show(self):

        self.oled.line(0, 15, self.oled.width - 1, 15, 1)
        wri = Writer(self.oled, freesansnum35, verbose=False)
        Writer.set_textpos(self.oled, 0, 0)
        self.oled.text(self.prompt,  40, 0)
        Writer.set_textpos(self.oled, 25, 0)
        wri.printstring(formatValue(self.value, self.isPercentage))
        self.oled.show()
