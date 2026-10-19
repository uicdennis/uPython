import os
from machine import Pin, RTC
#from traffic_control import led_test, led_test1, led_test2, led_test3
from wifi import wifi_connect
from traffic_control import start_light, stop_heartbeat
import ubinascii
import machine
import time, ntptime

index = 0

def btn_irq(btn):
    stop_heartbeat()

if __name__ == "__main__":
    print("Witty Cloud Demo v.0.4 - Traffic Light show.")

    led_wifi = Pin(2, Pin.OUT)
    led_wifi.value(1)
    sta = wifi_connect(led_wifi)
    ip = sta.ifconfig()[0]

    # 取得NTP網路時間(同步NTP伺服器時間)
    try:
        rtc = RTC()
        print("Before synchronize RTC => ", rtc.datetime())
        ntptime.settime()
        print("NTP 時間同步成功！")
        print("RTC => ", rtc.datetime())
    except Exception as e:
        print("同步失敗:", e)

    # 轉換為本地時間（例如台灣時間為 UTC+8，需加上 8 小時 = 8 * 3600 秒）
    UTC_OFFSET = 8 * 3600
    actual_time = time.time() + UTC_OFFSET
    t = time.localtime(actual_time)

    btn = Pin(4, Pin.IN, Pin.PULL_UP)
    btn.irq(handler=btn_irq, trigger=Pin.IRQ_RISING)

    device_id = ubinascii.hexlify(machine.unique_id()).decode("utf-8")

    start_light(device_id, ip, t)
