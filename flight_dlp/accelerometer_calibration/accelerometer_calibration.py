#!/usr/bin/env python3

# Packages
import numpy as np
import csv
import time
import os
from sensors import accelerometer, altimeter

# Define PATH
PATH = "/var/data/calibration_data/"

# Functions
def computeStats(nb_executions = 100000):
    """
    Taken from https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance.
    Iterative computing of the mean values coming from the three sensors (altimeter, accelerometer and magnetometer).
    The variance is also calculated for the accelerometer's data (x, y and z).
    """
    def _update(existing_aggregate, new_value):
        (count, mean, M2) = existing_aggregate
        count += 1
        delta = new_value - mean
        mean += delta / count
        delta2 = new_value - mean
        M2 += delta * delta2
        return (count, mean, M2)

    def _finalise(existing_aggregate):
        (count, mean, M2) = existing_aggregate
        return (mean, M2 / count)
    
    # Initialisation Accelerometer
    Accelerometer = accelerometer.Accelerometer()
    aggregate_x = (0, 0, 0)
    aggregate_y = (0, 0, 0)
    aggregate_z = (0, 0, 0)
    
    # Initialisation Altimeter
    Altimeter = altimeter.Altimeter()
    temperature_mean = 0
    
    for i in range(nb_executions):
        current_temperature = Altimeter.temperature

        aggregate_x = _update(aggregate_x, Accelerometer.x)
        aggregate_y = _update(aggregate_y, Accelerometer.y)
        aggregate_z = _update(aggregate_z, Accelerometer.z)
        temperature_mean += (current_temperature - temperature_mean) / (i+1)
        
    mean_x, variance_x = _finalise(aggregate_x)
    mean_y, variance_y = _finalise(aggregate_y)
    mean_z, variance_z = _finalise(aggregate_z)

    return (
        float("{:.2f}".format(temperature_mean)),
        mean_x, np.sqrt(variance_x),
        mean_y, np.sqrt(variance_y),
        mean_z, np.sqrt(variance_z)
        )

def output(nb_executions = 100000, file_name = "calibration_accelerometer.csv"):
    """Provides a data output for calibration sequences directly to a csv file."""
    print(f'Starting calibration sequence for the current angle at {time.strftime("%H:%M:%S on %Y-%m-%d")} ...\nDO NOT TOUCH SENSORS. Please wait for confirmation before moving any sensor.')
    data = computeStats(nb_executions)
    
    if os.path.isfile(f"{PATH + file_name}") is False:
        with open(f"{PATH + file_name}","a") as f:
            writer = csv.writer(f)
            writer.writerow(["YYYY","MM","DD","hh","mm","ss","nb_executions","temperature_mean","mean_x","gap_x","mean_y","gap_y","mean_z","gap_z"])
    
    with open(f"{PATH + file_name}","a") as f:
        writer = csv.writer(f)
        writer.writerow(
            [time.strftime("%Y"),time.strftime("%m"),time.strftime("%d"),time.strftime("%H"),time.strftime("%M"),time.strftime("%S"),
            nb_executions,data[0],data[1],data[2],data[3],data[4],data[5],data[6]]
            )

    print(f'Calibration complete at {time.strftime("%H:%M:%S on %Y-%m-%d")}.\n')
    
def terminate():
    """Takes keyboard input to allow the user to quit(Ctrl+C) or continue(enter). The keyboard python library requires root privileges to be used on linux distributions."""
    try :
        while True:
            if input() == "":
                break
    except KeyboardInterrupt:
        print()
        raise SystemExit

if __name__=="__main__":
    Altimeter = altimeter.Altimeter()
    print(
        "Before starting the calibration sequence for accelerometer sensor (ADXL345), make sure the module is stable and not moving.\n"+
        f"Press enter to continue or Ctrl+C to exit this program :"
        )
    
    terminate()

    start = time.strftime("%Y-%m-%d")
    environment_temperature = Altimeter.temperature
    print("Starting calibration session for accelerometer sensor (ADXL345) with an environment temperature of %.2f K." % environment_temperature)

    x = 1
    while True:
        print(f"Press enter to start a new sequence ({x}) or Ctrl+C to terminate this session :")
        terminate()
        output(nb_executions = 2000, file_name = start+"-"+"%.2fK.csv" % environment_temperature)
        
        x += 1