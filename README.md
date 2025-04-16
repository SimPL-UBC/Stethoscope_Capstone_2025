# Stethoscope_Capstone_2025
Repository for Wearable Miniaturized Stethoscope for Capstone 2024-2025  
This repository contains the following:
- Live Plotting: Code to have microcontroller write to serial and display live data for debugging
- Microcontroller: Code for microcontroller
- Sample Data: Sample of binary files with heartbeat data the Capstone team collected during testing
- Post Processing: Jupyter notebook that reads the binary file and filters data, then outputs plots, audio files, csv files, and calculated heartrate

## Post Processing Code
[SimPL Digital Stethoscope Post Processing (Updated for SD_New_Format)]  
It is recommended to run this code in a local development environment as most browser-based environments do not support the library _tkinter_ which is used to prompt the user for the file for analysis

The current post-processing code uses a band-pass range of 20-150 Hz. Adjustments to the sensitivity of the detected pulses can be made by altering the bandpass range, the noise threshold, or the parameters in the function _find_peaks_ used to find the variable _peaks_

The operation procedure for the post-processing software is as follows:
1. With the power to the stethoscope off and disconnected, use a 1.5mm hex key to unscrew  and remove the lid of the battery enclosure.
2. Remove the SD card from the SD card reader.
3. Connect the SD card to a computer with the post-processing software. This may require an adapter depending on the ports on the computer.
4. Load the software program on Visual Studio Code.
5. Run all cells of the program.
6. Enter session name when prompted, or skip by pressing “Enter” to use file name instead.
7. Select the file for analysis when prompted with the file explorer.
8. The software will generate plots and audio files and display heart rate data.

## Microcontroller File Structure
The code written for the microcontroller is written in circuitpython version 9.2.6 for the RP2040. The majority of the libraries used can be found in the [Circuit Python Documentation](https://docs.circuitpython.org/en/latest/README.html)

### Main.py
This is the first file ran on startup. It initalizes an error checker class found in [error.py] and sets the next file to be ran to be record.py. It then waits until all the errors are clear and the switch is flipped, at which point it will reload and the file [record.py] will be ran. This file also initalizes the on board real time clock on the microcontroller by reading from the external RTC. This time will stay accurate through the time library for as long as the microcontroller has power, ie, even through a reload called by supervisor.reload() 

sudocode is below
```
while not (sd.inserted() and switch.onPosition()):
    pass
next_file = "recording.py"
reload()

```

### Record.py
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

### Live_plot.py
To have the data output to the serial console of the device, in main.py refer to the last lines of code and comment supervisor.set_next_code_file("record.py") out and uncomment supervisor.set_next_code_file("live_plot.py") to have the live plot file run after a reload. This simply initalizes the microphone the same way record.py does but outputs data to the serial console.
#### plot_file.py and write_file.py
These files are ment to be ran on a PC connected to the device while it is running live_plot.py. write_file.py will continiously write the 1000 data entries to a file in the working directory called temp.txt. Leave this program running and in a seperate console on your pc run plot_file.py with the temp.txt file in the same directory. This will then plot the data in a easy to visualize way but please note, this does not save data. These files are simply ment for debugging or demonstration purposes. 

### Log File Format
The log files output is a binary file format. The device writes to this file in 510 blocks per write, where each block is 1020 bytes of data and a 4 byte timestamp. The method for decoding this data can be found under the decode_log in the post processing jupyter notebook. 

