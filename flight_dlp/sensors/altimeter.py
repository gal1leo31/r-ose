#!/usr/bin/env python3

"""
    Distributed with a free-will license.
    Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
    MPL3115A2
    This code is designed to work with the MPL3115A2_I2CS I2C Mini Module available from ControlEverything.com.
    https://www.controleverything.com/products
"""

# Packages
import smbus
import time

# MPL3115A2 registers
register_ctrl = 0x26
register_data = 0x13

# MPL3115A2 class
class Altimeter:
    
    def __init__(self, bus = None, device_address = 0x60):
        if bus is None:
            # Select the correct i2c bus for this revision of Raspberry Pi
            revision = (
                [l[12:-1] for l in open('/proc/cpuinfo','r').readlines() \
                if l[:8]=="Revision"]+['0000']
            )[0]
            bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

        self.bus = bus
        
        self.device_address = device_address
         
        # Select control register, 0x26(38)
        # Active mode, OSR = 128, Altimeter mode
        bus.write_byte_data(device_address, register_ctrl, 0xB9)

        # Select data configuration register, 0x13(19)
        # Data ready event enabled for altitude, pressure, temperature
        bus.write_byte_data(device_address, register_data, 0x07)

        # Select control register, 0x26(38)
        # Active mode, OSR = 128, Barometer mode
        bus.write_byte_data(device_address, register_ctrl, 0x39)

    def _rawData(self, byte = None):
        # status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
        data = self.bus.read_i2c_block_data(self.device_address, 0x00, byte)

        return data

    def _temperature(self):
        # status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
        data = self.bus.read_i2c_block_data(self.device_address, 0x00, 6)
        
        # Convert the data to 20-bits
        temp_raw = ((data[4] * 256) + (data[5] & 0xF0)) / 16
        
        temperature = (temp_raw / 16.0) + 273.15 # K

        return {'temperature' : temperature}
    
    def _altitudeBarometer(self):
        # status, pressure MSB1, pressure MSB, pressure LSB
        data = self.bus.read_i2c_block_data(self.device_address, 0x00, 4)
        
        pressure_raw = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
        
        pressure = (pressure_raw / 4.0) / 1000.0 # kPa
        
        x = pressure / 101.326 
        altitude = (44330.77 * (1 - x**0.1902632))
        return {'pressure' : pressure, 'altitude' : altitude}

    def _getData(self):
        temperature_data = self._temperature()
        altitude_barometer_data = self._altitudeBarometer()
        
        return {'altitude' : altitude_barometer_data['altitude'], 'temperature' : temperature_data['temperature'], 'pressure' : altitude_barometer_data['pressure']}

    @property
    def altitude(self):
        return self._getData()['altitude']

    @property
    def temperature(self):
        return self._getData()['temperature']

    @property
    def pressure(self):
        return self._getData()['pressure']

if __name__=="__main__":
    Altimeter = Altimeter()

    print(
        "Pressure : %.4f kPa" % Altimeter.pressure,
        "Altitude : %.4f m" % Altimeter.altitude,
        "Temperature : %.4f K" % Altimeter.temperature
    )
