from tkinter import *
from gpiozero import Servo
#import time
#rotation speeds in ms:
lowPeriod = 1.3
midPeriod = 1.5
highPeriod = 1.7
intervalTime = 20.0

servo = Servo (18, initial_value=0,
               min_pulse_width=lowPeriod/1000,
               max_pulse_width=highPeriod/1000,
               frame_width=intervalTime/1000)

def ArrowLeft(event):
    servo.min()
    print("left: servo.min()")

def ArrowRight(event):
    servo.max()
    print("right; servo.max()")

def ArrowDown(event):
    servo.mid()
    print("down; servo.mid()")

def ExitProgram(event):
    sys.exit()
root = Tk()
Label(root, text="Press a key (Escape key to exit):" ).grid()
root.bind('<Left>', ArrowLeft)
root.bind('<Right>', ArrowRight)
root.bind('<Down>', ArrowDown)
root.bind('<Escape>', ExitProgram)
root.mainloop()
