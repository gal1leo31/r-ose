#!/usr/bin/env python3

# Packages
import sensors
import time

# Reusable Open Stratospheric Explorer flight program
Accelerometer = sensors.Accelerometer()
Altimeter = sensors.Altimeter()
Magnetometer = sensors.Magnetometer()

def _saveData(file_name = None):
    if file_name is None:
        file_name = time.strftime("%Y_%m_%d.csv")

    with open(f"../data/{file_name}","a") as f:
        f.write(f'{time.strftime("%Y,%m,%d,%H,%M,%S")},{Altimeter.temperature},{Altimeter.pressure},{Altimeter.altitude},{Accelerometer.x},{Accelerometer.y},{Accelerometer.z},{Magnetometer.heading}\n')

if __name__=="__main__":
    _saveData()
