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
        for i in range(10):
            print('read')
            if self.stop_requested:
                break
            ##            value = random.randint(10, 100)
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
            temperature = float(temperature)
            humidity = float(humidity)
            if temperature is not None and humidity is not None:
                print('values are not None')
                self.queue.put({"humidity": humidity, "temperature": temperature})
            time.sleep(1)
