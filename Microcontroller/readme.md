# Microcontroller File Structure
The code written for the microcontroller is written in circuitpython version 9.2.6 for the RP2040. The majority of the libraries used can be found in the [Circuit Python Documentation](https://docs.circuitpython.org/en/latest/README.html)

## Main.py
This is the first file ran on startup. It initalizes an error checker class found in [error.py] and sets the next file to be ran to be record.py. It then waits until all the errors are clear and the switch is flipped, at which point it will reload and the file [record.py] will be ran. This file also initalizes the on board real time clock on the microcontroller by reading from the external RTC. This time will stay accurate through the time library for as long as the microcontroller has power, ie, even through a reload called by supervisor.reload() 

sudocode is below
```
while not (sd.inserted() and switch.onPosition()):
    pass
next_file = "recording.py"
reload()

```

## Record.py
This file creates a file on the sd card and writes to it a buffered bytearray of length 1024. where the first 1020 bytes are the values read from the analog pin A0, each 2 bytes giving a total of 510 readings per block. The last 4 bytes are a time value in miliseconds. you can use this to calculate the time it took for the last 510 values. This is done to maximize the recording frequency which on average is about 15kHz. 

sudo code below
```
while switch.onPosition()
    data = analog_read(1020)
    time = time.time()
    file.write(data)
    file.write(time)
file.close()
reload() # Goes back to main.py
```

## Liveplot
To have the data output to the serial console of the device, in main.py refer to the last lines of code and comment supervisor.set_next_code_file("record.py") out and uncomment supervisor.set_next_code_file("live_plot.py") to have the live plot file run after a reload. This simply initalizes the microphone the same way record.py does but outputs data to the serial console.



