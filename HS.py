import tkinter as tk
import tkinter.font
import threading
import queue
import time
from gpiozero import LED
import Sensors as sns

class MainClass(object):

    def __init__(self):
        self.root = tk.Tk()
        myFont=tkinter.font.Font(family='Helvetica', size = 12, weight = "bold")
        led1 = LED(21)
        led1.on()   ##this is tu turn led off needed cause my MOSFETs invert signal
        led2 = LED(20)
        led2.on()
        
##        self.root.grid_columnconfigure(3, weight=3)
        self.var = tk.StringVar()
        #self.varH = tk.StringVar()
        
        #label = tk.Label(self.root, text="Sensors:")
        value = tk.Label(self.root, textvariable=self.var, width=30)
        #humidity = tk.Label(self.root, textvariable=self.varH, width=20)

        #label.grid(row=0, column=0)
        value.grid(row=0, column=0)
        #humidity.grid(row=0, column=2) #, sticky="w"

        #Valve Manual Manipulation Buttons Testing:
        ledButton=tk.Button(self.root, text = 'Switch Blue', font=myFont, command=lambda: self.ledToggle(led1, led2), bg='bisque2', height=1, width=24)
        ledButton.grid(row=1, sticky=tk.NSEW)
        ledButton=tk.Button(self.root, text = 'Switch Green', font=myFont, command=lambda: self.ledToggle(led2, led1), bg='bisque2', height=1, width=24)
        ledButton.grid(row=2, sticky=tk.NSEW)

        #Valve Auto
        autoAreaLabel = tk.Label(self.root, text = 'Set Automatic Hit Cycle:')
        autoAreaLabel.grid(row=3, column=0)

        self.started = tk.BooleanVar()

        startButton=tk.Button(self.root, text = 'Start Hitting', font=myFont, command=lambda: self.startButton(), bg='bisque2', height=1, width=12)

        if self.started:
            startButton.grid(row=4, sticky=tk.E)
            #StartButton.text = 'Stop Hitting'
        else:
            startButton.grid(row=4, sticky=tk.W)
            #startButton.text = 'Start Hitting'
        
        #App specific:
        exitButton=tk.Button(self.root, text='Exit', font=myFont, command=self.exitProgram, bg='cyan', height=1, width=6)
        exitButton.grid(row=5, sticky=tk.E)
        
        # create a queue for communication
        self.queue = queue.Queue()

        # create some sensors
        self.sensor = sns.THSensor(self.queue)
        self.sensor.setName("SensorT&H")

        # start polling the queue
        self.poll_queue()
        
    def startButton(self):
        self.started = not self.started
        
    def ledToggle(self, led, otherLed):
        if led.is_lit:
            led.off()
            otherLed.on()
        else:
            led.on()
            
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
        self.root.after(500, self.poll_queue)
    def exitProgram(self):
        self.root.quit()

if __name__ == "__main__":
    app = MainClass()
    app.start()
