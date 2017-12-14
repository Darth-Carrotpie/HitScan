import Tkinter as tk
from Tkinter import *
import threading
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.AM2302
pin = 4

root = tk.Tk()
root.geometry("1200x720")
canvas = Canvas(width=1280, height=720, bg='black')
canvas.grid(rowspan=5, columnspan=8, sticky='W,E,N,S')

i_fan_slow = 18


# Input Fan Slow Temp
def is_minus_temp():
    global i_fan_slow
    if i_s_m["text"] == "-":
        i_fan_slow -= 1
        ifan_s.config(text=i_fan_slow)
        root.update_idletasks()


def is_plus_temp():
    global i_fan_slow
    if i_s_p["text"] == "+":
        i_fan_slow += 1
        ifan_s.config(text=i_fan_slow)
        root.update_idletasks()


# Maths
def maths():
    while 1:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temp = ("%02d" % temperature)
        if temperature is not None:
            c_temp.config(text=temp)
        if temperature >= i_fan_slow:
            gpio.config(text="On", bg='green')
            root.update_idletasks()
        if temperature < i_fan_slow:
            gpio.config(text="Off", bg='red')
            root.update_idletasks()
        time.sleep(1)


i_s_m = tk.Button(root, text="-", width=1, font=('aharoni', 30, 'bold'), command=is_minus_temp, bg='black', fg='white')
i_s_p = tk.Button(root, text="+", width=1, font=('aharoni', 30, 'bold'), command=is_plus_temp, bg='black', fg='white')
ifan_s = Label(root, text=i_fan_slow, width=4, font=('aharoni', 32, 'bold'), bg='black', fg='white')
ifan_s.grid(padx=5, pady=10, row=2, column=1, sticky='N')
i_s_m.grid(row=2, column=1, padx=15, pady=2, sticky="N,W")
i_s_p.grid(row=2, column=1, padx=15, pady=2, sticky="N,E")

c_temp = Label(root, text=" ", width=4, font=('aharoni', 32, 'bold'), bg='black', fg='white')
c_temp.grid(padx=5, pady=10, row=2, column=3, sticky='N')

gpio = Label(root, text="Off", width=4, font=('aharoni', 32, 'bold'), bg='red', fg='white')
gpio.grid(padx=5, pady=10, row=3, column=1, sticky='N')


t11 = threading.Thread(target=maths)
t11.daemon = True
t11.start()


root.mainloop()
