import threading
import queue
import Adafruit_DHT
import time
class THSensor(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)        
        self.queue = queue
        self.stop_requested = False

    def stop(self):
        self.stop_requested = True

    def run(self):
        exit_flag = threading.Event()
        while not exit_flag.wait(timeout=1):
            print('read')
            if self.stop_requested:
                print('sensor cycle broke;')
                break
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
            if temperature is not None and humidity is not None:
                temperature = float(temperature)
                humidity = float(humidity)
                self.queue.put({"humidity": humidity, "temperature": temperature})
