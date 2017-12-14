#!/usr/bin/env python3
import tkinter as tk
import tkinter.font
from gpiozero import LED
import TemperatureAndHumidity as tah
from multiprocessing import Pool
win=tk.Tk()
win.title("Button Test")
myFont=tkinter.font.Font(family='Helvetica', size = 12, weight = "bold")
led1 = LED(21)
led1.on()   ##this is tu turn led off needed cause my MOSFETs invert signal
led2 = LED(20)
led2.on()
def ledToggle(led, otherLed):
    if led.is_lit:
        led.off()
##        ledButton["text"]="Turn Led ON"
##        print("switching off")
        otherLed.on()
    else:
        led.on()        
##        ledButton["text"]="Turn Led Off"


def exitProgram():
    win.quit()

ledButton=tk.Button(win, text = 'Switch Blue', font=myFont, command=lambda: ledToggle(led1, led2), bg='bisque2', height=1, width=24)
ledButton.grid(row=1, sticky=tk.NSEW)
ledButton=tk.Button(win, text = 'Switch Green', font=myFont, command=lambda: ledToggle(led2, led1), bg='bisque2', height=1, width=24)
ledButton.grid(row=2, sticky=tk.NSEW)
exitButton=tk.Button(win, text='Exit', font=myFont, command=exitProgram, bg='cyan', height=1, width=6)
exitButton.grid(row=3, sticky=tk.E)
## now stuff which is used for temperature and humidity reads and displays:
the_label = tk.Label (win, text="", fg="black", bg="white", font="36")
the_label.grid(row=0, column=0)

def startReadingTnH(window, label):
    print ('launched a process')
    tah.Start(window, label)
pool = Pool()
pool.map(startReadingTnH, args=(win,the_label))
tk.mainloop()
pool.close()
pool.join()
