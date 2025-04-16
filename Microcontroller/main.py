import os
import digitalio
import board
import supervisor
from error import ErrorChecker
from clock import init_clock

try: # initialize clock, this also sets the on board RTC to the correct time for future time.locatime() calls
    init_clock()
except:
    print("clock error, continuing")
    pass

# initialize switch
switch = digitalio.DigitalInOut(board.D9)
switch.switch_to_input()
switch.pull=digitalio.Pull.UP

#initialize LED
from neopixel import NeoPixel
np = NeoPixel(board.NEOPIXEL,1)

import asyncio
async def check_switch(): # Switch error check
    return not switch.value
        

async def check_sd(): #Sd error check
        from sdcard import init_sd
        return not init_sd(change_dir=False) 
        
def check_sd_mounted():
    try:
        dir_list = os.listdir("/sd")
        if len(dir_list) >  0:
            return True
        else: return False
    except OSError:
        return False

checker = ErrorChecker(np) #initialize error checker and attach to the RGB LED
checker.add_check("switch",check_switch,(255,0,0)) # Adds switch check
checker.add_check("SD Card",check_sd,(255,255,0)) # Adds SD card error check
asyncio.run(checker.run()) #Execution stops here until all checks are complete and there are no more errors



np.fill((0,255,0)) #turn LED Green to let user know there are no errors. 


while switch.value:
    pass
supervisor.set_next_code_file("record.py") # Sets next file to be ran as Record
# supervisor.set_next_code_file("live_plot.py") # for live plotting using provided python files

supervisor.reload() # Reloads into record.py