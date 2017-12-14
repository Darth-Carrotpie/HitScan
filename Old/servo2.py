from Tkinter import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 666)
pwm.start(20)
#rotation speeds in ms:
lowPeriod = 1.3
midPeriod = 1.5
highPeriod = 1.7
intervalTime = 20.0
#speeds in freq:
lowFreq = 1/ (lowPeriod / 1000)
midFreq = 1/ (midPeriod / 1000)
highFreq = 1/(highPeriod / 1000)
#Duty cycles in percentages
lowDuty = (20 - lowPeriod) / 20
midDuty = (20 - midPeriod) / 20
highDuty = (20 - highPeriod) / 20

def ArrowLeft(event):
	pwm.ChangeFrequency(lowFreq)
	pwm.ChangeDutyCycle(lowDuty)
	print("left: ")
	print(lowFreq)
	print(lowDuty)
    #if (event.char == "0"):
    #    GPIO.output(led, 0)
def ArrowRight(event):
	pwm.ChangeFrequency(highFreq)
	pwm.ChangeDutyCycle(highDuty)
	print("right")
        print(highFreq)
	print(highDuty)
def ArrowDown(event):
	pwm.ChangeFrequency(midFreq)
	pwm.ChangeDutyCycle(midDuty)
	print("down")
        print(midFreq)
	print(midDuty)
def ExitProgram(event):
    pwm.stop()
    GPIO.cleanup()
    sys.exit()
root = Tk()
Label(root, text="Press a key (Escape key to exit):" ).grid()
root.bind('<Left>', ArrowLeft)
root.bind('<Right>', ArrowRight)
root.bind('<Down>', ArrowDown)
root.bind('<Escape>', ExitProgram)
root.mainloop()

GPIO.cleanup()
