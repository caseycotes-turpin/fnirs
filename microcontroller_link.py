# -*- coding: utf-8 -*-
"""
Created on Fri May 16 12:08:22 2025

@author: Casey Côtes-Turpin, Laboratoire de Motion Capture de l'UQAT

Prereq : pip install pyserial
"""

import serial
import pandas as pd
import datetime
import time


# Generation of session ID for file name
def session_ID_gen():
    t = datetime.datetime.now()
    return t.strftime("%Y%m%d_%H%M%S_%f")  # microseconds for uniqueness


# Connection to microcontroller setup
port = 'COMX'  # change X for the right port and reserve the port to your device manager
baud_rate = 9600
is_connected = False
dataset_output = "fnirs_" + session_ID_gen() + ".csv"

data_rows = []  


# Connection attempt
try:
    sp = serial.Serial(port, baud_rate)
    is_connected = True
    print(f"Connected to {port} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Connection error: {e}")
    is_connected = False

time.sleep(2)  # wait for Arduino to reset

# Reading Data
try:
    while is_connected:
        line = sp.readline().decode('utf-8').strip()
        if line:
            parts = line.split(',')
            if len(parts) == 2:
                try:
                    hb = int(parts[0])
                    hbo = int(parts[1])
                    unix_ts = time.time()
                    readable_ts = datetime.datetime.now().isoformat(sep=' ', timespec='microseconds')
                    row = [unix_ts, readable_ts, hb, hbo]
                    print(row)
                    data_rows.append(row)  
                except ValueError:
                    print(f"Invalid integer values: {parts}")
            else:
                print(f"Unexpected format: {line}")
except KeyboardInterrupt:
    print("\nStopping data collection.")
finally:
    if is_connected:
        sp.close()
        

# Save to CSV if data collected
if data_rows:
    df = pd.DataFrame(data_rows, columns=['unix_timestamp', 'datetime', 'HB', 'HBo'])
    df.to_csv(dataset_output, index=False)
    print(f"Data saved to {dataset_output}")
else:
    print("No data collected.")
    print("\nStop the datacollection")




