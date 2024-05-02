#!/usr/bin/env python3

"""
    Find Heading by using HMC5883L interface with Raspberry Pi using Python
	http://www.electronicwings.com
"""

# Packages
import smbus
import math
import numpy as np

# Some MPU6050 Registers and their Address
register_a     = 0x0b           # Address of Configuration register A
register_b     = 0x09           # Address of configuration register B
#register_mode  = 0x02           # Address of mode register

# Select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]

# MPU6050 class
class Magnetometer:
        
        def __init__(self, bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0), device_address = 0x0d, x_axis_h = 0x00, y_axis_h = 0x02, z_axis_h = 0x04):
                if bus is None:
                # Select the correct i2c bus for this revision of Raspberry Pi
                        revision = (
                                [l[12:-1] for l in open('/proc/cpuinfo','r').readlines() \
                                if l[:8]=="Revision"]+['0000']
                        )[0]
                        bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)
                
                self.bus = bus
                
                # HMC5883L magnetometer device address
                self.device_address = device_address

                # Write to Configuration Register A
                bus.write_byte_data(device_address, register_a, 0x01)

                # Write to Configuration Register B for gain
                bus.write_byte_data(device_address, register_b, 0x1d)

                # Write to mode Register for selecting mode
                #bus.write_byte_data(device_address, register_mode, 0)

                # Axis
                self.x_axis = self._rawData(x_axis_h)
                self.y_axis = self._rawData(y_axis_h)
                self.z_axis = self._rawData(z_axis_h)

        def _rawData(self, address):
                # Read raw 16-bit value
                high = self.bus.read_byte_data(self.device_address, address)
                low = self.bus.read_byte_data(self.device_address, address + 1)
                print(high,low)
                # Concatenate higher and lower value
                value = ((high << 8) | low)

                # Get signed value from module
                if(value > 32768):
                        value = value - 65536
                
                return value

        def _getData(self):
                # Read Accelerometer raw value
                x = self.x_axis
                y = self.y_axis
                z = self.z_axis
                print(x,y,z)
                heading = math.atan2(y, x)

                # Due to declination check for > 360 degree
                if(heading > 2 * (np.pi)):
                        heading = heading - 2 * (np.pi)

                # Check for sign
                if(heading < 0):
                        heading = heading + 2 * (np.pi)

                # Convert into angle
                heading_angle = heading * 180/(np.pi) # int(heading * 180/(np.pi))

                return {'heading' : heading_angle}

        @property
        def heading(self):
                return self._getData()['heading'] 

if __name__=="__main__":
        Magnetometer = Magnetometer()
        
        print("Heading angle = %.4f degrees" % Magnetometer.heading)
