from machine import Pin 
import utime 

OFFLINE = 0
RED = 1
YELLOW = 2
GREEN = 3

led_cfg = {
    "red": 10,
    "yellow": 5,
    "green": 15,
    "blink": 0
}

led_status = OFFLINE
r_led = Pin(15, Pin.OUT)
g_led = Pin(12, Pin.OUT)
b_led = Pin(13, Pin.OUT)

leds = [r_led, g_led, b_led]

def led_test():
    #global r_led, g_led, b_led
    i = 0
    while True:
        if i == 0:
            if r_led.value() == 0:
                r_led.on()
            else:
                r_led.off()
 
        if i == 1:
            if g_led.value() == 0:
                g_led.on()
            else:
                g_led.off()

        if i == 2:
            if b_led.value() == 0:
                b_led.on()
            else:
                b_led.off()

        i = i + 1
        if i == 3:
            i = 0

        utime.sleep(0.5)

def led_test1(leds):
    i = 0
    while True:
        leds[i].value(not leds[i].value())
 
        i = i + 1
        if i == 3:
            i = 0

        utime.sleep(0.5)

def led_test2(leds):
    while True:
        for i in range(0, 3):
            leds[i].value(not leds[i].value())
            utime.sleep(0.5)

def led_test3(leds):
    while True:
        for i in range(0, 3):
            leds[i].value(not leds[i].value())
            utime.sleep(0.5)
            leds[i].value(not leds[i].value())
            utime.sleep(0.5)

def led_off():
    for led in leds:
        led.off()

def led_change(led: int):
    print(f"led_change()  ==> led = {led}")
    led_off()
    if led == RED:
        r_led.on()
    elif led == YELLOW:
        r_led.value(1)
        g_led.value(1)
    elif led == GREEN:
        g_led.value(1)
    led_status = led

# Main traffic control function
# leds = [r_led, g_led, b_led]
def traffic_test(leds, cfg):
    r = cfg['red']
    y = cfg['yellow']
    g = cfg['green']
    
    while True:
        # red on
        led_change(RED)
        utime.sleep(r)
        # green on
        led_change(GREEN)
        utime.sleep(g)
        # yellow on
        led_change(YELLOW)
        utime.sleep(y)
        utime.sleep(0.01)

def start_light():
    led_off()

    led_status = RED
    traffic_test(leds, led_cfg)
    