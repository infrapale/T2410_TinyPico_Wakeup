import busio
import digitalio
import time
import IO as IO
from rainbowio import colorwheel
import neopixel
import audiomp3
import audiopwmio


print("TinyPico Tests!")
# Select one only
TEST_UART        = False
TEST_LOAD_SWITCH = False
TEST_NEOPIXEL    = False
TEST_AUDIO       = False
TEST_RTC         = False
TEST_I2C0        = False
TEST_I2C_5V_LCD  = False
TEST_SD_CARD     = True

#*********************************************************************************
#  UART0 and UART1 Tests    
#*********************************************************************************

if TEST_UART:
    uart0 = busio.UART(IO.TX0_PIN, IO.RX0_PIN, baudrate=9600)
    uart1 = busio.UART(IO.TX1_PIN, IO.RX1_PIN, baudrate=9600)

    '''
    UART0 and UART1 Test
    Connect logic analyzer to UART0 and UART1 pins
    Connect TXRX0.TX - TXRX1.RX, TXRX1.TX - TXRX0.RX,
    '''
    s1 = "A"
    while(True):
        uart0.write(s1)
        s2 = uart1.read(4)
        s3 = s2 + "X"
        uart1.write(s3)
        s4 = uart0.read(4)
        s1 = s4 + "Y"
        
#*********************************************************************************
#  Load Switch Tests    
#*********************************************************************************
if TEST_LOAD_SWITCH:
    io_value = 0
    while True:
        
        IO.edog_clr.value = io_value
        time.sleep(0.01)
        IO.vext_en.value = io_value 
        time.sleep(0.01)
        IO.v33_en.value = io_value
        time.sleep(0.01)
        IO.ext_clr.value = io_value
        
        if (io_value == 0):
            io_value = 1
        else:
            io_value = 0
        time.sleep(0.1)
            
   

#*********************************************************************************
#  Neopixel Tests    
#*********************************************************************************
if TEST_NEOPIXEL:
    NUMPIXELS = 24  # Update this to match the number of LEDs.
    SPEED = 0.05  # Increase to slow down the rainbow. Decrease to speed it up.
    BRIGHTNESS = 0.2  # A number between 0.0 and 1.0, where 0.0 is off, and 1.0 is max.

    pixels = neopixel.NeoPixel(IO.RGB0, NUMPIXELS, brightness=BRIGHTNESS, auto_write=False)

    def rainbow_cycle(wait):
        for color in range(255):
            for pixel in range(len(pixels)):  # pylint: disable=consider-using-enumerate
                pixel_index = (pixel * 256 // len(pixels)) + color * 5
                pixels[pixel] = colorwheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

    while True:
        rainbow_cycle(SPEED)



#*********************************************************************************
#  Audio Tests    
#*********************************************************************************
if TEST_AUDIO:
    while True:   
        audio = audiopwmio.PWMAudioOut(IO.PWM2A)

        decoder = audiomp3.MP3Decoder(open("slow.mp3", "rb"))

        audio.play(decoder)
        while audio.playing:
            pass

        print("Done playing!")

#*********************************************************************************
#  RTC PCF85063 Tests    
#*********************************************************************************
if TEST_RTC:
    import pcf85063a

    rtc = pcf85063a.PCF85063A(IO.i2c0)

    # Lookup table for names of days (nicer printing).
    days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


    # pylint: disable-msg=using-constant-test
    if False:  # change to True if you want to set the time!
        #                     year, mon, date, hour, min, sec, wday, yday, isdst
        t = time.struct_time((2024, 10, 1, 7, 10, 0, 1, -1, -1))
        # you must set year, mon, date, hour, min, sec and weekday
        # yearday is not supported, isdst can be set but we don't do anything with it at this time
        print("Setting time to:", t)  # uncomment for debugging
        rtc.datetime = t
        print()
    # pylint: enable-msg=using-constant-test

    # Main loop:
    while True:
        t = rtc.datetime
        print(t)     # uncomment for debugging
        print(
            "The date is {} {}/{}/{}".format(
                days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year
            )
        )
        print("The time is {}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec))
        time.sleep(1)  # wait a second



if TEST_I2C0:

    from adafruit_neokey.neokey1x4 import NeoKey1x4

    # use default I2C bus
    #i2c_bus = board.I2C()

    # Create a NeoKey object
    neokey = NeoKey1x4(IO.i2c0, addr=0x30)

    print("Adafruit NeoKey simple test")
    IO.pwr_i2c.value = 0
    # Check each button, if pressed, light up the matching neopixel!
    while True:
        if neokey[0]:
            print("Button A")
            neokey.pixels[0] = 0xFF0000
        else:
            neokey.pixels[0] = 0x0

        if neokey[1]:
            print("Button B")
            neokey.pixels[1] = 0xFFFF00
        else:
            neokey.pixels[1] = 0x0

        if neokey[2]:
            print("Button C")
            neokey.pixels[2] = 0x00FF00
        else:
            neokey.pixels[2] = 0x0

        if neokey[3]:
            print("Button D")
            neokey.pixels[3] = 0x00FFFF
        else:
            neokey.pixels[3] = 0x0

if TEST_I2C_5V_LCD:
    import adafruit_character_lcd.character_lcd_i2c as character_lcd
    cols = 20
    rows = 4
    IO.pwr_i2c.value = 0
    lcd = character_lcd.Character_LCD_I2C(IO.i2c1, cols, rows, 0x27)

    while True:
        # Turn backlight on
        lcd.backlight = True
        #time.sleep(2)
        #lcd.backlight = False
        #time.sleep(2)


        # Print a two line message
        lcd.message = "Hello\nCircuitPython"
        # Wait 5s
        time.sleep(5)
        lcd.clear()
        # Print two line message right to left
        lcd.text_direction = lcd.RIGHT_TO_LEFT
        lcd.message = "Hello\nCircuitPython"
        # Wait 5s
        time.sleep(5)
        # Return text direction to left to right
        lcd.text_direction = lcd.LEFT_TO_RIGHT
        # Display cursor
        lcd.clear()
        lcd.cursor = True
        lcd.message = "Cursor! "
        # Wait 5s
        time.sleep(5)
        # Display blinking cursor
        lcd.clear()
        lcd.blink = True
        lcd.message = "Blinky Cursor!"
        # Wait 5s
        time.sleep(5)
        lcd.blink = False
        lcd.clear()
        # Create message to scroll
        scroll_msg = "<-- Scroll"
        lcd.message = scroll_msg
        # Scroll message to the left
        for i in range(len(scroll_msg)):
            time.sleep(0.5)
            lcd.move_left()
        lcd.clear()
        lcd.message = "Going to sleep\nCya later!"
        time.sleep(5)
        # Turn backlight off
        lcd.backlight = False
        time.sleep(2)


if TEST_SD_CARD:
    import busio
    import digitalio
    import adafruit_sdcard
    import storage
    
    spi = busio.SPI(IO.SPIO0_SCK, MOSI=IO.SPIO0_MOSI, MISO=IO.SPIO0_MISO)
    cs = digitalio.DigitalInOut(IO.SPIO0_CS)
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)

    print("TinyPico Test SD Card: Write & Read")

    storage.mount(vfs, "/sd")
    print("Write 3 Lines")
    with open("/sd/test.txt", "w") as f:
        f.write("Hello world!\r\n")
        f.write("Row 2\r\n")
        f.write("Rivi 3\r\n")
        
    print("Read all Lines")
    with open("/sd/test.txt", "r") as f:
        line = f.readline()
        while line != '':
            print(line)
            line = f.readline()
        