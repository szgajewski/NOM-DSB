# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
from retrying import retry

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 40
#MISO = 35
#MOSI = 38
#CS   = 36
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 1
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

class analogInput:
 @retry(stop_max_attempt_number = 3, wait_fixed=1000)
 def readAnalogInput(self, ID):
  actValue = mcp.read_adc(ID)
  #print(actValue)
  return actValue
 
 @retry(stop_max_attempt_number = 3, wait_fixed=1000)
 def analogInputLoop(self):
  print('Reading MCP3008 values, press Ctrl-C to quit...')
  # Print nice channel column headers.
  print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
  print('-' * 57)
  while True:
   values = [0]*8
   for i in range(8):
    values[i] = mcp.read_adc(i)
   print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
   time.sleep(2)  

#newInput = analogInput()
#newInput.readAnalogInput(0)
#newInput.analogInputLoop()

if __name__ == "__main__":
    analogInput().analogInputLoop()
