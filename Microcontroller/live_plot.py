#Live Plotting
import analogio
import board
from neopixel import NeoPixel
import digitalio
import supervisor

#initalize mic and LED to match main.py and Record.py
np = NeoPixel(board.NEOPIXEL,1)
mic_in = analogio.AnalogIn(board.A0)

switch = digitalio.DigitalInOut(board.D9)
switch.switch_to_input()
switch.pull=digitalio.Pull.UP
np.fill((0,0,255))


while not switch.value:
    print(mic_in.value) #print values to serial port
supervisor.reload() # Reloads into Main.py

