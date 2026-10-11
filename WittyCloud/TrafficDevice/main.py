import os
from machine import Pin
#from traffic_control import led_test, led_test1, led_test2, led_test3
from wifi import wifi_connect
from traffic_control import start_light, stop_heartbeat
from mqtt_sub import start_mqtt

index = 0

def btn_irq(btn):
    stop_heartbeat()

if __name__ == "__main__":
    print("Witty Cloud Demo v.0.3 - Traffic Light show.")

    led_wifi = Pin(2, Pin.OUT)
    led_wifi.value(1)
    sta = wifi_connect(led_wifi)

    btn = Pin(4, Pin.IN, Pin.PULL_UP)
    btn.irq(handler=btn_irq, trigger=Pin.IRQ_RISING)

    device_id = start_mqtt()
    start_light(device_id)
