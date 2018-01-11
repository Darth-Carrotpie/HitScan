import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

CLK  = 26
MISO = 19
MOSI = 13
CS   = 16
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
#print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
#print('-' * 57)
# Main program loop.
def Read(pin):
    raspberryFeedReferanceVoltage = 3.318
    batteryNominalVoltage = 11.10
    maxVoltageInCircut = 11.1 / ((3900+10000)/float(3900))
    
    referanceAdjustment = raspberryFeedReferanceVoltage / maxVoltageInCircut
    fraction = (float(mcp.read_adc(pin)) / 1024)

    currentBatVoltage = float( batteryNominalVoltage * referanceAdjustment * fraction)
    #print(outputString)
    return currentBatVoltage
