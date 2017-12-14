import tkinter as tk
import threading
import queue
import random
import time
import Adafruit_DHT
class Example(object):
    def __init__(self):
        self.root = tk.Tk()
        self.sensor_vars = []

        self.root.grid_columnconfigure(1, weight=1)
        for row, i in enumerate(range(3)):
            var = tk.StringVar()
            self.sensor_vars.append(var)
            label = tk.Label(self.root, text="Sensor %d:" % i)
            value = tk.Label(self.root, textvariable=var, width=4)
            label.grid(row=row, column=0, sticky="e")
            value.grid(row=row, column=1, sticky="w")

        ledButton=tk.Button(self.root, text = 'Switch Blue', command = self.test, bg='bisque2', height=1, width=24)
        ledButton.grid(row=4, sticky=tk.NSEW)
        
        # create a queue for communication
        self.queue = queue.Queue()

        # create some sensors
        self.sensors = []
        for i in range(1):
            sensor = Sensor(self.queue, i)
            self.sensors.append(sensor)
            sensor.setName("Sensor %d" % i)

        # start polling the queue
        self.poll_queue()
    def test(self):
        print('click')
    def start(self):
        # start the sensors
        for sensor in self.sensors:
            sensor.start()

        # start the GUI loop
        self.root.mainloop()

        # wait for the threads to finish
        for sensor in self.sensors:
            sensor.stop()
            sensor.join()

    def poll_queue(self):
        if not self.queue.empty():
            message = self.queue.get()
            index = message["index"]
            self.sensor_vars[index].set(message["value"])

        self.root.after(100, self.poll_queue)

class Sensor(threading.Thread):
    def __init__(self, queue, index):
        threading.Thread.__init__(self)
        self.queue = queue
        self.index = index
        self.stop_requested = False

    def stop(self):
        self.stop_requested = True

    def run(self):
        for i in range(10):
            print('read')
            if self.stop_requested:
                break
            ##            value = random.randint(10, 100)
            humidity, value = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
            value = float(value)
            if value is not None:
                print('value is not none')
                self.queue.put({"index": self.index, "value": value})
            time.sleep(1)



if __name__ == "__main__":
    app = Example()
    app.start()
