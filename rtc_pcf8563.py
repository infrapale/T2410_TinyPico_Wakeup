from adafruit_pcf8563.pcf8563 import PCF8563

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def initialize(rtc_i2c):
    global rtc
    rtc = PCF8563(rtc_i2c)
    # Lookup table for names of days (nicer printing).


def set_time():
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2023, 9, 21, 19, 50, 0, 3, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t
    print()

 
def get_time():
    if rtc.datetime_compromised:
        print("RTC unset")
    else:
        pass
        # print("RTC reports time is valid")
    t = rtc.datetime
    return rtc.datetime

def get_date_str():
    t = get_time()
    return "{} {}/{}/{}".format(
            days[int(t.tm_wday)], t.tm_mday, t.tm_mon, t.tm_year)
    
def get_time_str():
    t = get_time()
    return "{}:{:02}:{:02}".format(t.tm_hour, t.tm_min, t.tm_sec)
    


def print_time():  
    
    print(get_date_str())
    print(get_time_str())     # uncomment for debugging