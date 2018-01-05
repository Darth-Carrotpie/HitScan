#The HitScan project
This project is the Python scripting setup for controls of HitScan box inside the chamber.
The box is based on RPi, has multiple sensors, interface items and a small pneumatic system.

Required files:
Main application file: HS.py;
Module files: finger.py; sensors.py
Python Version 3+

Parts:
RPi2
Pressure sensor BMP180 Octopus
Temperature & humidity sensor Adafruit_DHT.AM2302

RPi pin data connections (gpiozero pinout):
4 Adafruit_DHT.AM2302
20 solenoid relay A
21 solenoid relay B