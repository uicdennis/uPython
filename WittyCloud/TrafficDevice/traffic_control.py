from machine import Pin, Timer
import utime
from mqtt_sub import start_mqtt, register_device, heartbeat, status_changed

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

hb_cfg = {"id": "abc", "sn": 1}
device_cfg = {"id": "Device0001", "uptime": "10:27:18", "date": "2026-09-09", "ip": "192.168.0.23", "data": "中山樹德", "rssi": 70}
status_cfg = {"id": "Device0001", "uptime": "10:27:18", "date": "2026-09-09", "rssi": 70, "color": "RED"}

led_status = OFFLINE
r_led = Pin(15, Pin.OUT)
g_led = Pin(12, Pin.OUT)
b_led = Pin(13, Pin.OUT)

leds = [r_led, g_led, b_led]
tim = 0
client = None
send_hearbeat = False

def led_off():
    for led in leds:
        led.off()

def led_change(led: int):
    global client

    print(f"led_change()  ==> led = {led}")
    led_off()
    if led == RED:
        r_led.on()
        status_cfg["color"] = "RED"
    elif led == YELLOW:
        r_led.value(1)
        g_led.value(1)
        status_cfg["color"] = "YELLOW"
    elif led == GREEN:
        g_led.value(1)
        status_cfg["color"] = "GREEN"
    led_status = led
    status_changed(client, status_cfg)

def tim_cb(x):
    global send_hearbeat

    send_hearbeat = True

def stop_heartbeat():
    global tim
    tim.deinit()
    print("  ---> Timer stopped !!!")

# Main traffic control function
# leds = [r_led, g_led, b_led]
#def traffic_test(leds, cfg):
#    r = cfg['red']
#    y = cfg['yellow']
#    g = cfg['green']
#
#    while True:
#        # red on
#        led_change(RED)
#        utime.sleep(r)
#        # green on
#        led_change(GREEN)
#        utime.sleep(g)
#        # yellow on
#        led_change(YELLOW)
#        utime.sleep(y)
#        utime.sleep(0.01)

def traffic_test(client, leds, cfg):
    global send_hearbeat

    r = cfg['red']
    y = cfg['yellow']
    g = cfg['green']

    # 交通燈狀態定義
    STATES = [
        {"color": RED, "duration": r},
        {"color": GREEN, "duration": g},
        {"color": YELLOW, "duration": y}
    ]

    current_state_idx = 0
    # 記錄上一次狀態切換的時間戳記
    last_switch_time = utime.ticks_ms()

    # 初始化：先切換到第一個狀態
    led_change(STATES[current_state_idx]["color"])

    while True:
        try:
            # 1. 每次迴圈都必須呼叫，用來維持 MQTT 連線與心跳
            client.check_msg()

            # 2. 檢查是否到達切換燈號的時間（非阻塞式計時）
            current_time = utime.ticks_ms()
            duration_ms = STATES[current_state_idx]["duration"] * 1000
            time_spent = utime.ticks_diff(current_time, last_switch_time)

            if time_spent >= duration_ms:
                # 切換到下一個狀態
                current_state_idx = (current_state_idx + 1) % len(STATES)
                last_switch_time = current_time

                # 改變 LED 狀態並發佈 MQTT 訊息
                new_color = STATES[current_state_idx]["color"]
                led_change(new_color)

            if send_hearbeat:
                heartbeat(client, hb_cfg["id"], hb_cfg)
                send_hearbeat = False

            # 3. 短暫休息避免 CPU 滿載，同時保持高頻率的 check_msg
            utime.sleep_ms(50)

        except OSError as e:
            print(f"MQTT 連線異常: {e}")
            try:
                client.connect()
            except Exception as reconnect_err:
                print(f"重連失敗，等待重試: {reconnect_err}")
                utime.sleep(5)

def start_light(did: str, ip: str, t):
    global tim, client

    led_off()
    print(f" ---> Enter start_light() - id = {did}")
    # Update Device ID
    hb_cfg["id"] = status_cfg["id"] = device_cfg["id"] = did
    device_cfg["ip"] = ip
    # 格式化日期與時間
    print(type(t))
    device_cfg["date"] = f"{t[0]}/{t[1]}/{t[2]}"
    device_cfg["uptime"] = f"{t[3]}:{t[4]}:{t[5]}"

    client = start_mqtt(did)
    try:
        client.check_msg()
    except OSError as e:
        print(f"MQTT --- 連線異常: {e}")
    register_device(client, device_cfg)

    #utime.sleep(1)

    tim = Timer(-1)
    tim.init(period=3000, mode=Timer.PERIODIC, callback=tim_cb)
    #heartbeat(client, hb_cfg["id"], hb_cfg)
    led_status = RED
    traffic_test(client, leds, led_cfg)
