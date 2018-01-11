from pathlib import Path
import os
import datetime
import errno
import re
class SensorLogger():
    def __init__(self, hs):
        self.loggingPeriod = 60000
        self.logDaysToKeep = 10
        #read logger config file:
        self.configFile = open("/home/pi/Documents/HitScan/config", 'r+')
        lines = self.configFile.readlines()
        for i in range(0,len(lines)):
            if lines[i][0] is not "#":
                values = [int(s) for s in re.findall(r'\b\d+\b', lines[i])]
                if "days" in lines[i]:
                    self.logDaysToKeep = values[0]
                    print("Logging day storing is:",self.logDaysToKeep, 'days')
                if "period" in lines[i]:
                    self.loggingPeriod = values[0] * 1000
                    print("Logging period is:",values[0],'s')
            #else:
                #print(lines[i])
        #ready vars for file management:
        now = datetime.datetime.now()
        date = "{0}-{1}-{2}".format(now.year,now.month,now.day)
        self.pathToLogFolder = "/home/pi/Documents/HitScan/Logs/"
        self.pathToFile = "{0}{1}".format(self.pathToLogFolder, date)
        
        #delete old files:
        self.deleteOldLogs(self.pathToLogFolder)
        #today's log file reading:        
        self.logFile = self.readOrCreateFile(self.pathToFile)        
        
        self.voltageOutDataToAverage= 0.0
        self.voltageOutDataAdditions= 0
        self.voltageOutLow= 0.0
        self.voltageInDataToAverage= 0.0
        self.voltageInDataAdditions= 0
        self.voltageInLow= 0.0
        
        self.temperatureDataToAverage= 0.0
        self.temperatureDataAdditions= 0
        self.temperaturePeak = 0.0

        self.batTmpDataToAverage= 0.0
        self.batTmpDataAdditions= 0
        self.batTmpPeak = 0.0
        
        self.humidityDataToAverage = 0.0
        self.humidityDataAdditions = 0
        
        self.pDataToAverage = 0.0
        self.pDataAdditions = 0
        self.hitData = 0
        
        self.run(hs)

    def run(self, hs):
        now = datetime.datetime.now()
        dataToWrite = "{0}h:{1}m:{2}s*".format(now.hour,now.minute,now.second)
        dataToWrite+=' /Hits='
        dataToWrite +=self.formatLogNumber(self.hitData)
        dataToWrite+=' /Vo='
        dataToWrite +=self.formatLogNumber(self.voltageOutDataToAverage, self.voltageOutDataAdditions)
        dataToWrite+=' /VoLow='
        dataToWrite +=self.formatLogNumber(self.voltageOutLow)
        dataToWrite+=' /Vi='
        dataToWrite +=self.formatLogNumber(self.voltageInDataToAverage, self.voltageInDataAdditions)
        dataToWrite+=' /ViLow='
        dataToWrite +=self.formatLogNumber(self.voltageInLow)
        dataToWrite+='/Tmp='
        dataToWrite +=self.formatLogNumber(self.temperatureDataToAverage, self.temperatureDataAdditions)
        dataToWrite+=' /TmpPk='
        dataToWrite +=self.formatLogNumber(self.temperaturePeak)        
        dataToWrite+='/BtTemp='
        dataToWrite +=self.formatLogNumber(self.batTmpDataToAverage, self.batTmpDataAdditions)
        dataToWrite+=' /BtTmpPk='
        dataToWrite +=self.formatLogNumber(self.batTmpPeak)
        dataToWrite+=' /Humi='
        dataToWrite +=self.formatLogNumber(self.humidityDataToAverage, self.humidityDataAdditions)
        dataToWrite+=' /Prsr='
        dataToWrite +=self.formatLogNumber(self.pDataToAverage, self.pDataAdditions)

        self.write(dataToWrite)

        self.voltageOutDataToAverage= 0.0
        self.voltageOutDataAdditions= 0
        self.voltageOutLow= 0.0
        self.voltageInDataToAverage= 0.0
        self.voltageInDataAdditions= 0
        self.voltageInLow= 0.0
        
        self.temperatureDataToAverage= 0.0
        self.temperatureDataAdditions= 0
        self.temperaturePeak = 0.0

        self.batTmpDataToAverage= 0.0
        self.batTmpDataAdditions= 0
        self.batTmpPeak = 0.0
        
        self.humidityDataToAverage = 0.0
        self.humidityDataAdditions = 0
        
        self.pDataToAverage = 0.0
        self.pDataAdditions = 0
        self.hitData = 0
        hs.root.after(self.loggingPeriod, self.run, hs)
        
    def formatLogNumber(self, data, count=0):
        output=''
        if count > 0:
            output +="{0:0.2f}".format(data/count)
            #print(data/count)
        else:
            #for x in range(0, len(str(data))):
            if data == 0:
                output+='0.00'
            else:
                output+="{0:0.2f}".format(data)
        output+=''
        return output
    
    def addVoltageIn(self, data):
        self.voltageInDataToAverage += float(data)
        self.voltageInDataAdditions+=1
        if data < self.voltageInLow or self.voltageInLow == 0:
            self.voltageInLow = data
    def addVoltageOut(self, data):
        self.voltageOutDataToAverage += float(data)
        self.voltageOutDataAdditions+=1
        if data < self.voltageOutLow or self.voltageOutLow == 0:
            self.voltageOutLow = data
    def addTemperature(self, data):
        self.temperatureDataToAverage += float(data)
        self.temperatureDataAdditions+=1
        if data > self.temperaturePeak or self.temperaturePeak == 0:
            self.temperaturePeak = data
    def addBatTemperature(self, data):
        self.batTmpDataToAverage += float(data)
        self.batTmpDataAdditions+=1
        if data > self.batTmpPeak or self.batTmpPeak == 0:
            self.batTmpPeak = data
    def addHumidity(self, data):
        self.humidityDataToAverage += float(data)
        self.humidityDataAdditions+=1        
    def addPressure(self, data):
        self.pDataToAverage += float(data)
        self.pDataAdditions+=1
    def addHits(self, data):
        self.hitData+=data
    
    def write(self, data):
        self.logFile = open(self.pathToFile,'a+')
        dataAsString = str(data)
        #print(dataAsString)
        self.logFile.write(dataAsString)
        self.logFile.write('\n')
        self.logFile.close()
        
    def deleteOldLogs(self, path):
        files = self.getFiles(path)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for i in range(0,len(files)):
            #print(files[i])
            if i >= self.logDaysToKeep:
                print('removing old log file: ',files[i])
                os.remove(files[i])
    def getFiles(self, path):
        files = None
        for path, dirs, files in os.walk(path):
            dirs = sorted(dirs)
            break
        #print (len(files))
        files = [os.path.join(path, f) for f in files] # add path to each file
        return files
        
    def readOrCreateFile(self, path):
        try:
            file = open(path,'a+')
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                    raise        
        else:
            # exists! its fine, keep logging
            file = open(path,'a+')
        return file
        
    def __delete__(self, instance):
        self.logFile.close()
