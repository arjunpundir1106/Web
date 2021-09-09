import serial
import time
import csv
import os
import minimalmodbus as mm
import datetime as dt


class Instrument:
    """
    Used to get and log data from Instruments rs485 CAN Hat
    
    
    address_sensor = The sensor needed
    
    Example:
    >>> sensor_1 = Instrument(address_sensor=1)
    >>> sensor_1.read_temp()
    98.6
    
    """
    
    def __init__(self, address_sensor=1, debug=False):
        self.instr = mm.Instrument('/dev/ttyS0', address_sensor, debug=debug)
        self.sensor = address_sensor
        self.instr.serial.baudrate=9600
        
        self.readings_map = {'pH' : 0x06,
                             'soil_moist' : 0x12,
                             'nitrogen' : 0x1e,
                             'potassium' : 0x20,
                             'phosphorus' : 0x1f,
                             'temp' : 0x07}
                             

    def log_data(self):

        while True:
            print(time.ctime())
            try:
                #self.instr.read_register(x,3) for x in range()
                with open(f'sensor_data_{address_sensor}.csv', 'a+') as f:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerrow([time.ctime(), decBytes])
                    
            except Exception as e:
                print(str(e))
                print("Keyboard Interrupt")
                break
            
            time.sleep(1)


    def read_pH(self) -> float:
        """
        Gets Soil pH Reading in pH
        """
        return self.instr.read_register(self.readings_map['pH'],2)
    
    
    

    def read_temp(self, fahren=True) -> float:
        """
        Gets Soil Moisture Reading in degrees
        default Fahrenheit
        """
        if fahren:
            return round(self.instr.read_register(self.readings_map['temp'], 2) * 1.8 + 32, 2)
        else:
            return self.instr.read_register(self.readings_map['temp'], 2)
        
    def read_npk(self) -> dict:
        """
        Gets Soil NPK Reading in mg/kg
        """
        return { x : self.instr.read_register(self.readings_map[x]) for x in
                 ['nitrogen','phosphorus','potassium']}
    
    def read_moisture(self) -> float:
        """
        Gets Soil Moisture Reading in %
        """
        return self.instr.read_register(self.readings_map['soil_moist'], 1)
    
    def read_all(self) -> dict:
        """
        Returns all readings in a dict
        """
        readings =  { 'Datetime' : dt.datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
                      'Temp' : self.read_temp(),
                      'pH' : self.read_pH(),
                      'EC' : self.read_ec(),
                      'Moisture' : self.read_moisture(),
                      'NPK' : self.read_npk()}
        return readings
                     
        
        
    
if __name__ == '__main__':
    import time

    
    npk = Instrument()
    x = 0
    while x < 5:
        print(npk.read_all())
        x += 1
        time.sleep(5)