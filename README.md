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
