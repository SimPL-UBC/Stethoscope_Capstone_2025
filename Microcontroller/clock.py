from adafruit_ds3231 import DS3231
from busio import I2C
import board
import rtc
class Clock(DS3231):
    def __init__(self):
        i2c = I2C(board.D3,board.D2)
        super().__init__(i2c)
        r = rtc.RTC()
        r.datetime = self.datetime # Sets internal clock to be the same as the RTC
        
def init_clock():
    Clock()
        
        