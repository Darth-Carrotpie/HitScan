from gpiozero import LED
import logger
class Control():
    def __init__(self, hs):
        self.run(hs)        #this starts the process at HS.py>start()
        self.led1 = LED(21)
        self.led1.on()
        self.led2 = LED(20)
        self.led2.on()
        
    def run(self, hs):
        tk = hs.root
        betweenBeats = 500
        if hs.started.get():
            #print('is cycling')
            bpm = hs.bpm.get()
            if bpm:
                betweenBeatsFlat = 60 / bpm
            else:
                betweenBeatsFlat = 1
            delay = betweenBeatsFlat * hs.delayPortion.get()
            wait = betweenBeatsFlat-delay
            betweenBeats = int(1000 * wait)
            #print(betweenBeats)
            self.cycle(hs)
        tk.after(betweenBeats, self.run, hs)          
        
    def cycle(self, hs):
        self.setState(hs, True)
        bpm = hs.bpm.get()
        if bpm:
            betweenBeatsFlat = 60 / bpm
        else:
            betweenBeatsFlat = 1
        delayFlat = betweenBeatsFlat * hs.delayPortion.get()
        delay = int(1000 * delayFlat)
        hs.root.after(delay)
        self.setState(hs, False)
        hs.logger.addHits(1)

    def setState(self, hs, extend):
        if extend:
            self.ledToggle(self.led2, self.led1, hs)
            self.fingerExtended = True;
        else:
            self.ledToggle(self.led1, self.led2, hs)
            self.fingerExtended = False;            
     
    def ledToggle(self, led, otherLed, hs):
        otherLed.on()
        led.off()
        hs.root.after(20)
        led.on()   
