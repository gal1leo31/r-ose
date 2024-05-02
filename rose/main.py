#!/usr/bin/env python3

# Packages
import sensors
import time
import os
import csv

# Reusable Open Stratospheric Explorer flight program
Accelerometer = sensors.Accelerometer()
Altimeter = sensors.Altimeter()
Magnetometer = sensors.Magnetometer()

# Define PATH
PATH = "/var/data/"

def _saveData(file_name = None):
    """Saves in flight data to a csv file. Default file_name is year, month, day in csv format (YYYY-MM-DD.csv)."""
    if file_name is None:
        file_name = time.strftime("%Y-%m-%d.csv")

    if os.path.isfile(f"{PATH + file_name}") is False:
        with open(f"{PATH + file_name}","a") as f:
            writer = csv.writer(f)
            writer.writerow(["YYYY","MM","DD","hh","mm","ss","Altitude","Temperature","Pressure","x","y","z","Heading"])

    with open(f"{PATH + file_name}","a") as f:
        writer = csv.writer(f)
        writer.writerow(
            [time.strftime("%Y"),time.strftime("%m"),time.strftime("%d"),time.strftime("%H"),time.strftime("%M"),time.strftime("%S"),
            "{:.2f}".format(Altimeter.altitude),"{:.2f}".format(Altimeter.temperature),"{:.2f}".format(Altimeter.pressure),
            "{:.2f}".format(Accelerometer.x),"{:.2f}".format(Accelerometer.y),"{:.2f}".format(Accelerometer.z),
            "{:.2f}".format(Magnetometer.heading)]
            )

if __name__=="__main__":
    # Leave a couple sec for data to be usable
    # First off, need to reset offset of the accelerometer
    
    while True :
        _saveData()
