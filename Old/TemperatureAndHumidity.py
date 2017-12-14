#!/usr/bin/env python3
import Adafruit_DHT
import tkinter as tk

def Start(win, lbl):
    global window
    window = win
    global label
    label = lbl
    read_every_second

def READ():
    global temp
    try:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
        if humidity is not None and temperature is not None:
            temp = float(temperature)
            label.configure(text=str(temp))
            print(temp)
    except:
        print('TnH read exception!')
def read_every_second():
    print("read")
    READ()
    window.after(1000, read_every_second)

