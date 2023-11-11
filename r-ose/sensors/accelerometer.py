#!/usr/bin/env python3

# ADXL345 Python library for Raspberry Pi 
#
# author:  Jonathan Williamson
# license: BSD, see LICENSE.txt included in this package
# 
# This is a Raspberry Pi Python implementation to help you get started with
# the Adafruit Triple Axis ADXL345 breakout board:
# http://shop.pimoroni.com/products/adafruit-triple-axis-accelerometer

# Packages
import smbus

# ADXL345 registers
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004

DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D

BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09

RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03

MEASURE             = 0x08
AXES_DATA           = 0x32

# Select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]

# ADXL345 class
class Accelerometer:

    def __init__(self, bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0), device_address = 0x53):        
        self.bus = bus

        self.device_address = device_address
        self._setBandwidthRate(BW_RATE_100HZ)
        self._setRange(RANGE_2G)
        self._enableMeasurement()

    def _enableMeasurement(self):
        self.bus.write_byte_data(self.device_address, POWER_CTL, MEASURE)

    def _setBandwidthRate(self, rate_flag):
        self.bus.write_byte_data(self.device_address, BW_RATE, rate_flag)

    # Set the measurement range for 10-bit readings
    def _setRange(self, range_flag):
        value = self.bus.read_byte_data(self.device_address, DATA_FORMAT)

        value &= ~0x0F;
        value |= range_flag;  
        value |= 0x08;

        self.bus.write_byte_data(self.device_address, DATA_FORMAT, value)
    
    # Returns the current reading from the sensor for each axis
    #   Gforce parameter:
    #       False (default): result is returned in m/s^2
    #       True           : result is returned in gs
    def getData(self, gforce = False):
        bytes = self.bus.read_i2c_block_data(self.device_address, AXES_DATA, 6)
        
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        return {"x": x, "y": y, "z": z}

if __name__ == "__main__":
    # if run directly we'll just create an instance of the class and output 
    # the current readings
    Accelerometer = Accelerometer()
    axes = Accelerometer.getData(gforce = False)
    print( "ADXL345 on address 0x%x:" % (Accelerometer.device_address))
    print( "x = %.5f" % ( axes['x'] ))
    print( "y = %.5f" % ( axes['y'] ))
    print( "z = %.5f" % ( axes['z'] ))
    print( (axes['x']**2 + axes['y']**2 + axes['z']**2)**(0.5))
