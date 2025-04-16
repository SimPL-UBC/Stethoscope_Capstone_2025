import digitalio
import board
import os
import supervisor
from sdcard import init_sd
# initialize switch
switch = digitalio.DigitalInOut(board.D9)
switch.switch_to_input()
switch.pull=digitalio.Pull.UP
# initialize LED

from neopixel import NeoPixel
np = NeoPixel(board.NEOPIXEL,1)

try: # initialize sd, if this fails, reload into main
    init_sd()
except:
    supervisor.reload()
    
# Create New File Name
files = [f for f in os.listdir() if "Log" in f]
new_index = len(files) + 1 # create new log
file_path = "Log"+str(new_index)


# Recording Loop
import analogbufio
import array
import time
rate = 50000 # recording frequency
buffer = bytearray(1020) # data array, 510 samples
adcbuf = analogbufio.BufferedIn(board.A0, sample_rate=rate)

try:
    with open(file_path,"wb",buffering=1024*1024) as file:
        np.fill((0,0,255)) # Turn light Blue
        start_time = time.monotonic()
        while not switch.value:
            adcbuf.readinto(buffer) # Read into buffer
            current_time = int(start_time-time.monotonic()*1000)
            current_time = current_time & 0xFFFFFFFF # logical to ensure time is 4 bytes 
            file.write(buffer) # write data
            file.write(current_time.to_bytes(4,byteorder="little")) # write time

        file.close() #Save file
        print(f"saved to {file_path}")
except Exception as e:
    print("Error In Recording: ",e)
    pass
supervisor.reload() #reloads into main.py