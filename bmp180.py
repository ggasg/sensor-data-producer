"""
The vast majority of this code is an adaptation of the sample mentioned here:
https://www.theengineeringprojects.com/2023/06/how-to-interface-bmp180-air-pressure-sensor-with-pi-4.html"""

import time

class Sensor():
    def __init__(self, bus):
        # Perform initial calibrations
        data = bus.read_i2c_block_data(0x77, 0xAA, 22)
        
        self.AC1 = data[0] * 256 + data[1]
        if self.AC1 > 32767: self.AC1 -= 65535
        
        self.AC2 = data[2] * 256 + data[3]
        if self.AC2 > 32767: self.AC2 -= 65535
        
        self.AC3 = data[4] * 256 + data[5]
        if self.AC3 > 32767: self.AC3 -= 65535

        self.AC4 = data[6] * 256 + data[7]

        self.AC5 = data[8] * 256 + data[9]

        self.AC6 = data[10] * 256 + data[11]

        self.B1 = data[12] * 256 + data[13]
        if self.B1 > 32767: self.B1 -= 65535

        self.B2 = data[14] * 256 + data[15]
        if self.B2 > 32767: self.B2 -= 65535

        self.MB = data[16] * 256 + data[17]
        if self.MB > 32767: self.MB -= 65535

        self.MC = data[18] * 256 + data[19]
        if self.MC > 32767: self.MC -= 65535
        
        self.MD = data[20] * 256 + data[21]
        if self.MD > 32767: self.MD -= 65535

        # ---------- Set up the sensor
        # BMP180 address, 0x77(119)
        # Select measurement control register, 0xF4(244)
        # 0x2E(46) Enable temperature measurement
        bus.write_byte_data(0x77, 0xF4, 0x2E)
        time.sleep(0.5)
        # BMP180 address, 0x77(119)
        # Select measurement control register, 0xF4(244)
        # 0x74(116) Enable pressure measurement, OSS = 1
        bus.write_byte_data(0x77, 0xF4, 0x74)
        time.sleep(0.5)
        # -----------
    # Read Temperature
    def get_temperature(self):
        data = self.bus.read_i2c_block_data(0x77, 0xF6, 2)
        temp = data[0] * 256 + data[1]
        # Extra calibrations
        X1 = (temp - self.AC6) * self.AC5 / 32768.0
        X2 = (self.MC * 2048.0) / (X1 + self.MD)
        B5 = X1 + X2
        cTemp = ((B5 + 8.0) / 16.0) / 10.0
        fTemp = cTemp * 1.8 + 32
        return (cTemp, fTemp)
    # Read Pressure
    def get_pressure(self):
        data = self.bus.read_i2c_block_data(0x77, 0xF6, 3)
        pres = ((data[0] * 65536) + (data[1] * 256) + data[2]) / 128
        B6 = self.B5 - 4000
        X1 = (self.B2 * (B6 * B6 / 4096.0)) / 2048.0
        X2 = self.AC2 * B6 / 2048.0
        X3 = X1 + X2
        B3 = (((self.AC1 * 4 + X3) * 2) + 2) / 4.0
        X1 = self.AC3 * B6 / 8192.0
        X2 = (self.B1 * (B6 * B6 / 2048.0)) / 65536.0
        X3 = ((X1 + X2) + 2) / 4.0
        B4 = self.AC4 * (X3 + 32768) / 32768.0
        B7 = ((pres - B3) * (25000.0))
        
        pressure = 0.0
        
        if B7 < 2147483648:
            pressure = (B7 * 2) / B4
        else:
            pressure = (B7 / B4) * 2
            
        X1 = (pressure / 256.0) * (pressure / 256.0)
        X1 = (X1 * 3038.0) / 65536.0
        X2 = ((-7357) * pressure) / 65536.0
        pressure = (pressure + (X1 + X2 + 3791) / 16.0) / 100

        altitude = 44330 * (1 - ((pressure / 1013.25) ** 0.1903))

        return (pressure, altitude)


def annoy_me(msg, stop):
    while (True):
        print(msg)
        time.sleep(5)
        if stop():
            print('Ok now leaving')
            break
    print('Thread signing off')
