import serial
from collections import deque
import time

# === CONFIGURE SERIAL PORT ===
SERIAL_PORT = '/dev/tty.usbmodem101'  # Change as needed
BAUD_RATE = 115200

# Initialize serial and rolling buffer
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
data = deque(maxlen=1000)  # Start empty, but max size 100

with open('temp.txt', 'w') as f:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            data.append(line)
            if len(data) == 1000:
                f.seek(0)
                f.write('\n'.join(data))
                f.truncate()
