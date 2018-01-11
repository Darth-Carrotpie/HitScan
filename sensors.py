import Adafruit_DHT.Raspberry_Pi_2 as Adafruit_DHT
import Adafruit_BMP.BMP085 as BMP085
import voltmeter
class THSensor():
    def __init__(self, hs):
        self.run(hs)        #this starts the process at HS.py>start()
        self.run2(hs)
        
    def run(self, hs):
        tk = hs.root
        period = 60000
        if not hs.started.get():
            period = 10000
        self.updateData(hs)
        tk.after(period, self.run, hs)
        
    def run2(self, hs):
        tk = hs.root
        period = 200
        self.updatePressureData(hs)
        self.updateVoltageData(hs)
        tk.after(period, self.run2, hs)
        
    def updateData(self, hs):
        #sensor = Adafruit_DHT.AM2302
        humidity, temperature = Adafruit_DHT.read(22, 4)
        if temperature is not None and humidity is not None:
            temperature = float(temperature)
            humidity = float(humidity)
            hs.var.set('BatTemp={0:0.1f}*C   Humidity={1:0.1f}%'.format(temperature,humidity))
            hs.logger.addHumidity(humidity)
            hs.logger.addBatTemperature(temperature)

    def updatePressureData(self, hs):
        sensor = BMP085.BMP085()
        pressure = sensor.read_pressure()
        temperature = sensor.read_temperature()
        if temperature is not None and pressure is not None:
            altitude = sensor.read_altitude()
            sealevel = sensor.read_sealevel_pressure()
            hs.pressureVar.set('Temp:{0:0.1f}*C   Pressure:{1:0.1f}Pa'.format(temperature,pressure))
            hs.extraDataVar.set('Alt:{0:0.1f}m SeaLvlP:{1:0.1f}Pa'.format(altitude,sealevel))
            hs.logger.addTemperature(temperature)
            hs.logger.addPressure(pressure)

    def updateVoltageData(self, hs):
        currentBatV = voltmeter.Read(0)
        #print(currentBatV)
        batString = 'Battery: {0:0.4f}V'.format(currentBatV)   
        hs.voltageInputVar.set(batString)
        hs.logger.addVoltageIn(currentBatV)
   
        currentOutputV = voltmeter.Read(3)
        outputString = 'Output: {0:0.4f}V'.format(currentOutputV)
        hs.voltageOutputVar.set(outputString)
        hs.logger.addVoltageOut(currentOutputV)     

