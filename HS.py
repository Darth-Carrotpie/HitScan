#!/usr/bin/env python3
import tkinter as tk
import tkinter.font
import sensors as sns
import finger as fng
import voltmeter
import logger
class MainClass(object):

    def __init__(self):
        self.root = tk.Tk()
        self.started = tk.BooleanVar()
        self.started.set(False)
        
        myFont=tkinter.font.Font(family='Helvetica', size = 12, weight = "bold")
        textFont=tkinter.font.Font(family='Helvetica', size = 6, weight = "normal")
        
        self.var = tk.StringVar()
        value = tk.Label(self.root, textvariable=self.var, width=30, font=textFont)
        value.grid(row=0, column=1)
        
        self.pressureVar = tk.StringVar()
        pressureLabel = tk.Label(self.root, textvariable=self.pressureVar, font=textFont)
        pressureLabel.grid(row=1, column=1)

        self.voltageInputVar = tk.StringVar()
        voltageInputLabel = tk.Label(self.root, textvariable=self.voltageInputVar, font=textFont)
        voltageInputLabel.grid(row=4, column=1)

        self.voltageOutputVar = tk.StringVar()
        voltageOutputLabel = tk.Label(self.root, textvariable=self.voltageOutputVar, font=textFont)
        voltageOutputLabel.grid(row=5, column=1)
        
        self.extraDataVar = tk.StringVar()
        extraLabel = tk.Label(self.root, textvariable=self.extraDataVar, font=textFont)
        extraLabel.grid(row=6, column=1,sticky=tk.W)
        
        self.fingerExtended = tk.BooleanVar()

        #self.frame1.pack_propagate(False)
        
        #Sensor button
        readSensorButton=tk.Button(self.root, text = 'Read Sensors', font=myFont, command=lambda:self.sensor.updateData(self), bg='DarkSeaGreen1', height=1, width=15)
        readSensorButton.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)
        
        #Valve Manual Manipulation Buttons:
        ledButton=tk.Button(self.root, text = 'Pull', font=myFont, command=lambda:self.finger.setState(self, False), bg='DarkSeaGreen1', height=1, width=15)
        ledButton.grid(row=2, column=0, sticky=tk.NSEW)
        ledButton=tk.Button(self.root, text = 'Push', font=myFont, command=lambda:self.finger.setState(self, True), bg='DarkSeaGreen1', height=1, width=15)
        ledButton.grid(row=3, column=0, sticky=tk.NSEW)
        
        singleCycle=tk.Button(self.root, text = 'Single Hit', font=myFont, command=lambda:self.finger.cycle(self), bg='DarkSeaGreen1', height=2, width=15)
        singleCycle.grid(row=2, column=1, rowspan=2, sticky=tk.NSEW)

        #Valve Auto
        autoAreaLabel = tk.Label(self.root, text = 'Set Automatic Hit Cycle:')
        autoAreaLabel.grid(row=4, column=0)

        self.bpm = tk.DoubleVar()
        self.bpm.set(120)
        self.delayPortion = tk.DoubleVar()
        self.delayPortion.set(0.5)
        
        self.startButton=tk.Button(self.root, text = 'Start Hitting', font=myFont, command=self.startButton, bg='OliveDrab1', height=1, width=8)
        self.startButton.grid(row=5, sticky=tk.W)

        #Valve Auto Input
        self.inputFrame = tk.Frame(self.root, highlightbackground="green", highlightcolor="green", highlightthickness=2, width=100, height=100, bd=0)
        self.inputFrame.grid(row=6, column=0, sticky=tk.NSEW)
        
        vcmd = (self.root.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        autoAreaLabel = tk.Label(self.inputFrame, text = 'BPM:')
        autoAreaLabel.grid(row=0, column=0)
        #autoAreaLabel.place(relx=.0, rely=.5, anchor="w")
        self.bpmInput = tk.Entry(self.inputFrame, textvariable=self.bpm, validate = 'key', validatecommand = vcmd, width=7)
        self.bpmInput.grid(row=0, column=1, sticky=tk.NSEW)
        
        autoAreaLabel = tk.Label(self.inputFrame, text = 'U/D:')
        autoAreaLabel.grid(row=0, column=3)        
        self.speedInput = tk.Entry(self.inputFrame, textvariable=self.delayPortion, validate = 'key', validatecommand = vcmd, width=7)
        self.speedInput.grid(row=0, column=4, sticky=tk.NSEW)
        
        #App specific:
        exitButton=tk.Button(self.root, text='Exit', font=myFont, command=self.exitProgram, bg='CadetBlue4', height=1, width=3)
        exitButton.grid(row=6, column=1, sticky=tk.E)
        self.logger = logger.SensorLogger(self)

        self.sensor = sns.THSensor(self)
        self.finger = fng.Control(self)
    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except:
                return False
        else:
            return False
        
    #this loops the GUI    
    def refresh(self):
        self.root.update()
        self.root.after(100,self.refresh)
        
    def startButton(self):
        self.started.set (not self.started.get())
        #print(self.started.get())
        if self.started.get():
            self.startButton.grid(row=5, sticky=tk.E)
            self.startButton["text"] = 'Stop Hitting'
            self.startButton["bg"] = 'tomato'
            if not self.bpm.get():
                self.bpm.set(120)
            if not self.delayPortion.get():
                self.delayPortion.set(0.5)
        else:
            self.startButton.grid(row=5, sticky=tk.W)
            self.startButton["text"] = 'Start Hitting'
            self.startButton["bg"] = 'OliveDrab1'

            
    def start(self):
        self.refresh()
        # start the GUI loop
        self.root.mainloop()        
      
    def exitProgram(self):
        
        self.root.quit()

if __name__ == "__main__":
    app = MainClass()
    app.start()


