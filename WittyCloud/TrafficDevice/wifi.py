import network
import json

def wifi_connect(led):
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    with open('config.json', 'rt') as f:
        cfg = json.load(f)
        wifi.connect(cfg['ssid'], cfg['password'])
    while wifi.isconnected() == False:
        pass

    led.value(0)
    print(wifi.ifconfig())
    return wifi
