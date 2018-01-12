#!/usr/bin/env python3
import tkinter as tk
import tkinter.font
import sensors as sns
import finger as fng
import voltmeter
import logger
import pygame
from PIL import Image, ImageTk
import os
import webbrowser

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
        
        #battery info:
        self.batteryFrame = tk.Frame(self.root, highlightbackground="yellow", highlightcolor="yellow", highlightthickness=2, width=100, height=100, bd=0)
        self.batteryFrame.grid(row=0, column=2, sticky=tk.NSEW)
        
        self.voltageInputVar = tk.StringVar()
        voltageInputLabel = tk.Label(self.batteryFrame, textvariable=self.voltageInputVar, font=textFont)
        voltageInputLabel.grid(row=0, column=0, sticky=tk.NSEW)

        self.voltageOutputVar = tk.StringVar()
        voltageOutputLabel = tk.Label(self.batteryFrame, textvariable=self.voltageOutputVar, font=textFont)
        voltageOutputLabel.grid(row=1, column=0, sticky=tk.NSEW)
        
        #altitude, sea level:
        self.extraDataVar = tk.StringVar()
        extraLabel = tk.Label(self.root, textvariable=self.extraDataVar, font=textFont)
        extraLabel.grid(row=5, column=1,sticky=tk.NSEW)
        
        self.fingerExtended = tk.BooleanVar()

        #self.frame1.pack_propagate(False)
        
        #Sensor button
        readSensorButton=tk.Button(self.root, text = 'Read Sensors', font=myFont, command=lambda:self.sensor.updateData(self), bg='DarkSeaGreen1', height=1, width=15)
        readSensorButton.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW)
        
        #Valve Manual Manipulation Buttons:
        ledButton=tk.Button(self.root, text = 'Pull', font=myFont, command=lambda:self.finger.setState(self, False), bg='DarkSeaGreen1', height=1, width=8)
        ledButton.grid(row=2, column=2, sticky=tk.NSEW)
        ledButton=tk.Button(self.root, text = 'Push', font=myFont, command=lambda:self.finger.setState(self, True), bg='DarkSeaGreen1', height=1, width=8)
        ledButton.grid(row=3, column=2, sticky=tk.NSEW)
        
        singleCycle=tk.Button(self.root, text = 'Single Hit', font=myFont, command=lambda:self.finger.cycle(self), bg='DarkSeaGreen1', height=2, width=15)
        singleCycle.grid(row=2, column=1, rowspan=2, sticky=tk.NSEW)

        #Valve Auto
        #autoAreaLabel = tk.Label(self.root, text = 'Set Automatic Hit Cycle:')
        #autoAreaLabel.grid(row=1, column=0)

        self.bpm = tk.DoubleVar()
        self.bpm.set(120)
        self.delayPortion = tk.DoubleVar()
        self.delayPortion.set(0.5)

        #Valve Auto Input
        self.inputFrame = tk.Frame(self.root, highlightbackground="green", highlightcolor="green", highlightthickness=2, width=100, height=100, bd=0)
        self.inputFrame.grid(row=2, column=0, rowspan=2, sticky=tk.NSEW)
        
        self.startButton=tk.Button(self.inputFrame, text = 'Start Hitting', font=myFont, command=self.startButton, bg='OliveDrab1', height=1, width=8)
        self.startButton.grid(row=0, columnspan=2, sticky=tk.NSEW)
        
        vcmd = (self.root.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        autoAreaLabel = tk.Label(self.inputFrame, text = 'BPM:', width=5)
        autoAreaLabel.grid(row=1, column=0)
        #autoAreaLabel.place(relx=.0, rely=.5, anchor="w")
        self.bpmInput = tk.Entry(self.inputFrame, textvariable=self.bpm, validate = 'key', validatecommand = vcmd, width=9)
        self.bpmInput.grid(row=1, column=1, sticky=tk.NSEW)
        
        autoAreaLabel = tk.Label(self.inputFrame, text = 'U/D:', width=5)
        autoAreaLabel.grid(row=1, column=2)        
        self.speedInput = tk.Entry(self.inputFrame, textvariable=self.delayPortion, validate = 'key', validatecommand = vcmd, width=9)
        self.speedInput.grid(row=1, column=3, sticky=tk.NSEW)
        
        #extras - audio, video, etc:
        pygame.mixer.init()
        self.extrasFrame = tk.Frame(self.root, highlightbackground="RoyalBlue1", highlightcolor="RoyalBlue1", highlightthickness=2, width=100, height=100, bd=0)
        self.extrasFrame.grid(row=4, column=0, rowspan=2, sticky=tk.NSEW)
        image = Image.open("/home/pi/Documents/HitScan/Resources/playstop.ico")
        image = image.resize((64, 64), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        audioPath = "/home/pi/Documents/HitScan/Audio"
        #get audio file list, take first, return path as string:
        audioFiles = self.getFiles(audioPath)
        #play button:
        playStopButton= tk.Button(self.extrasFrame, image=photo, font=myFont, command=lambda:self.playAudio(audioFiles[0]), bg='RoyalBlue1', height=64, width=64)
        playStopButton.grid(row=0, column=0) 
        playStopButton.image = photo # keep a reference!
        #playStopButton.pack()
        #video shortcut btn:
        imageVideo = Image.open("/home/pi/Documents/HitScan/Resources/camera.png")
        imageVideo = imageVideo.resize((64, 64), Image.ANTIALIAS)
        photoVideo = ImageTk.PhotoImage(imageVideo)
        
        url = 'http://docs.python.org/'
        chrome_path = '/usr/bin/google-chrome %s'
        videoButton = tk.Button(self.extrasFrame, image=photoVideo, font=myFont, command=lambda:self.openBrowserForVideo(), bg='RoyalBlue1', height=64, width=64)
        videoButton.grid(row=0, column=1) 
        videoButton.image = photoVideo # keep a reference!
        
        #App specific:
        exitButton=tk.Button(self.root, text='Exit', font=myFont, command=self.exitProgram, bg='CadetBlue4', height=1, width=3)
        exitButton.grid(row=5, column=2, sticky=tk.E)
        self.logger = logger.SensorLogger(self)

        self.sensor = sns.THSensor(self)
        self.finger = fng.Control(self)
    def openBrowserForVideo(self):
        url = "http://127.0.0.1/html/"
        chrome_path = "/usr/bin/chromium-browser %s"
        webbrowser.get(chrome_path).open(url)
        #os.system("sh /home/pi/RPi_Cam_Web_Interface/RPi_Cam_Web_Interface_Installer.sh")
        
    def playAudio(self, fullpath):
        print (pygame.mixer.music.get_volume())
        if not pygame.mixer.music.get_busy():
            print('playing: ',fullpath)
            pygame.mixer.music.load(fullpath)
            pygame.mixer.music.play() #loops=-1
        else:
            pygame.mixer.music.stop()        
        
    def getFiles(self, path):
        files = None
        for path, dirs, files in os.walk(path):
            dirs = sorted(dirs)
            break
        #print (len(files))
        files = [os.path.join(path, f) for f in files] # add path to each file
        return files
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
            self.startButton.grid(column=2)
            self.startButton["text"] = 'Stop Hitting'
            self.startButton["bg"] = 'tomato'
            if not self.bpm.get():
                self.bpm.set(120)
            if not self.delayPortion.get():
                self.delayPortion.set(0.5)
        else:
            self.startButton.grid(column=0)
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
