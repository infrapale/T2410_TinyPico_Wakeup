'''
Pico U2U RTC SD  GPIO
'''
import board
import busio
import digitalio

TX0_PIN      = board.GP0
RX0_PIN      = board.GP1
TX1_PIN      = board.GP8
RX1_PIN      = board.GP9

I2C0_SDA_PIN = board.GP4
I2C0_SCL_PIN = board.GP5

I2C1_SDA_PIN = board.GP6
I2C1_SCL_PIN = board.GP7

RGB0         = board.GP10
RGB1         = board.GP11

PWR_SPI      = board.GP2
PWR_I2C      = board.GP3
EDOG_CLR     = board.GP12
VEXT_EN      = board.GP13
V33_EN       = board.GP14
EXT_CLR      = board.GP15

SPIO0_MISO   = board.GP16
SPIO0_CS     = board.GP17
SPIO0_SCK    = board.GP18
SPIO0_MOSI   = board.GP19

PWM2A        = board.GP20
PWM2B        = board.GP21

GP22         = board.GP22
GP26         = board.GP26
GP27         = board.GP27
GP28         = board.GP28

pwr_spi = digitalio.DigitalInOut(PWR_SPI)
pwr_spi.direction = digitalio.Direction.OUTPUT

pwr_i2c = digitalio.DigitalInOut(PWR_I2C)
pwr_i2c.direction = digitalio.Direction.OUTPUT

edog_clr = digitalio.DigitalInOut(EDOG_CLR)
edog_clr.direction = digitalio.Direction.OUTPUT

vext_en = digitalio.DigitalInOut(VEXT_EN)
vext_en.direction = digitalio.Direction.OUTPUT

v33_en = digitalio.DigitalInOut(V33_EN)
v33_en.direction = digitalio.Direction.OUTPUT

ext_clr = digitalio.DigitalInOut(EXT_CLR)
ext_clr.direction = digitalio.Direction.OUTPUT


# Power on I2C
#i2c_en = digitalio.DigitalInOut(EDOG_CLR)
#i2c_en.direction = digitalio.Direction.OUTPUT
#i2c_en.value = 1

i2c0 = busio.I2C(I2C0_SCL_PIN, I2C0_SDA_PIN, frequency=100000)
i2c1 = busio.I2C(I2C1_SCL_PIN, I2C1_SDA_PIN, frequency=10000)

