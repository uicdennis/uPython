import os
from machine import Pin
#from traffic_control import led_test, led_test1, led_test2, led_test3
from wifi import wifi_connect
from traffic_control import start_light
from mqtt_sub import start_mqtt, heartbeat

index = 0

hb_cfg = {"id": "abc", "sn": 1}

def btn_irq(btn):
    print(f"sn = {hb_cfg["sn"]}")
    heartbeat("abc", hb_cfg)
    hb_cfg["sn"] = hb_cfg["sn"] + 1

if __name__ == "__main__":
    print("Witty Cloud Demo v.0.2 - Traffic Light show.")

    led_wifi = Pin(2, Pin.OUT)
    led_wifi.value(1)
    sta = wifi_connect(led_wifi)

    btn = Pin(4, Pin.IN, Pin.PULL_UP)
    btn.irq(handler=btn_irq, trigger=Pin.IRQ_RISING)

    device_id = start_mqtt()
    start_light(device_id)
