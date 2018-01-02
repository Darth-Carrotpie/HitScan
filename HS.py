import tkinter as tk
import tkinter.font
import threading
import queue
import time
from gpiozero import LED
import Sensors as sns
import finger as fng
class MainClass(object):

    def __init__(self):
        self.root = tk.Tk()
        self.started = tk.BooleanVar()
        self.started.set(False)
        
        myFont=tkinter.font.Font(family='Helvetica', size = 12, weight = "bold")
        
        #self.led1 = LED(21)
        #self.led1.on()
        #self.led2 = LED(20)
        #self.led2.on()
        
        self.var = tk.StringVar()
        
        value = tk.Label(self.root, textvariable=self.var, width=30)

        value.grid(row=0, column=0)

        self.fingerExtended = tk.BooleanVar()
        #Valve Manual Manipulation Buttons:
        ledButton=tk.Button(self.root, text = 'Pull', font=myFont, command=lambda:self.finger.setState(self, False), bg='bisque2', height=1, width=24)
        ledButton.grid(row=1, sticky=tk.NSEW)
        ledButton=tk.Button(self.root, text = 'Push', font=myFont, command=lambda:self.finger.setState(self, True), bg='bisque2', height=1, width=24)
        ledButton.grid(row=2, sticky=tk.NSEW)

        #Valve Auto
        autoAreaLabel = tk.Label(self.root, text = 'Set Automatic Hit Cycle:')
        autoAreaLabel.grid(row=3, column=0)


        self.bpm = tk.IntVar()
        self.bpm.set(60)
        self.delayPortion = tk.DoubleVar()
        self.delayPortion.set(1)
        
        self.startButton=tk.Button(self.root, text = 'Start Hitting', font=myFont, command=self.startButton, bg='bisque2', height=1, width=8)
        self.startButton.grid(row=4, sticky=tk.W)

        #App specific:
        exitButton=tk.Button(self.root, text='Exit', font=myFont, command=self.exitProgram, bg='cyan', height=1, width=6)
        exitButton.grid(row=5, sticky=tk.E)
        
        # create a queue for communication
        self.queue = queue.Queue()
        # create some sensors
        self.sensor = sns.THSensor(self.queue)
        self.sensor.setName("SensorT&H")
        #self.relayThread = threading.Thread(target=self.cycling, args=())
        # start polling the queue
        self.poll_queue()
        self.finger = fng.Control(self)

    #this loops the GUI    
    def refresh(self):
        self.root.update()
        self.root.after(100,self.refresh)
        
    def startButton(self):
        self.started = not self.started
        if self.started:
            self.startButton.grid(row=4, sticky=tk.E)
            self.startButton["text"] = 'Stop Hitting'
        else:
            self.startButton.grid(row=4, sticky=tk.W)
            self.startButton["text"] = 'Start Hitting'
            
    def start(self):
        self.refresh()
        #self.cycling()

        # start the sensors
        #self.sensor.start()
        #self.relayThread.start()
        # start the GUI loop
        self.root.mainloop()

        # wait for the threads to finish
        #self.sensor.stop()
        #self.sensor.join()
        
    def poll_queue(self):
        if not self.queue.empty():
            message = self.queue.get()
            self.var.set('Temp={0:0.1f}*C   Humidity={1:0.1f}%'.format(message["temperature"], message["humidity"]))
            self.root.after(100, self.poll_queue)
        
    def exitProgram(self):
        self.sensor.stop()
        self.root.quit()

if __name__ == "__main__":
    app = MainClass()
    app.start()


