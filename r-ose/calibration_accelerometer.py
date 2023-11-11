#!/usr/bin/env python3

# Packages
import numpy as np
import csv
import time
from sensors import accelerometer, altimeter

# Functions
def computeStats(nb_executions = 100000):
    # Taken from
    # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance
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
        axes = Accelerometer.getData(gforce = False)
        current_temperature = Altimeter.getData()['temperature']
        aggregate_x = _update(aggregate_x, axes['x'])
        aggregate_y = _update(aggregate_y, axes['y'])
        aggregate_z = _update(aggregate_z, axes['z'])
        temperature_mean += (current_temperature - temperature_mean) / (i+1)
        
    mean_x, variance_x = _finalise(aggregate_x)
    mean_y, variance_y = _finalise(aggregate_y)
    mean_z, variance_z = _finalise(aggregate_z)

    return (temperature_mean, mean_x, np.sqrt(variance_x), mean_y, np.sqrt(variance_y), mean_z, np.sqrt(variance_z))

def output(nb_executions):
    print(f'Starting calibration ... \nDO NOT TOUCH SENSORS \nPlease wait for confirmation, before moving any sensor.')
    data = computeStats(nb_executions)
    
    with open("calibration_accelerometer1.csv","a") as f:
        f.write(f'{time.strftime("%Y,%m,%d,%H,%M,%S")},{nb_executions}')
        for values in data:
            f.write(f",{str(values)}")

    print(f'Calibration complete at {time.strftime("%H:%M:%S on %Y-%m-%d")}')
    
if __name__=="__main__":
    output(nb_executions = 100000)
