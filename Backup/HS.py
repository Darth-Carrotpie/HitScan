import tkinter as tk
import threading
import queue
import time

from gpiozero import LED
import Sensors as sns
class Example(object):
    def __init__(self):
        self.root = tk.Tk()

##        self.root.grid_columnconfigure(3, weight=3)
        self.var = tk.StringVar()
        #self.varH = tk.StringVar()
        
        #label = tk.Label(self.root, text="Sensors:")
        value = tk.Label(self.root, textvariable=self.var, width=30)
        #humidity = tk.Label(self.root, textvariable=self.varH, width=20)

        #label.grid(row=0, column=0)
        value.grid(row=0, column=0)
        #humidity.grid(row=0, column=2) #, sticky="w"
        
        ledButton=tk.Button(self.root, text = 'Switch Blue', command = self.test, bg='bisque2', height=1, width=24)
        ledButton.grid(row=4, sticky=tk.NSEW)
        
        # create a queue for communication
        self.queue = queue.Queue()

        # create some sensors
        self.sensor = sns.THSensor(self.queue)
        self.sensor.setName("SensorT&H")

        # start polling the queue
        self.poll_queue()
    def test(self):
        print('click')
    def start(self):
        # start the sensors
        self.sensor.start()

        # start the GUI loop
        self.root.mainloop()

        # wait for the threads to finish
        self.sensor.stop()
        self.sensor.join()

    def poll_queue(self):
        if not self.queue.empty():
            message = self.queue.get()
            #output = 'Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(self.varT, self.varH)
            self.var.set('Temp={0:0.1f}*C   Humidity={1:0.1f}%'.format(message["temperature"], message["humidity"]))
            #self.varH.set(message["humidity"])
        self.root.after(100, self.poll_queue)


if __name__ == "__main__":
    app = Example()
    app.start()
