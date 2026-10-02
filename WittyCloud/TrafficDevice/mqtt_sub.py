import time
import machine
from umqtt.simple import MQTTClient
import ubinascii
import json

# mqtt_server = '192.168.0.20'
MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_ALIVE = 60
MQTT_PREFIX = "promath168/traffic/"
TRAFFIC_DEVICE_REGISTER_TOPIC = "promath168/traffic/cmd/registered"
TRAFFIC_DEVICE_HEARTBEAT_TOPIC = "promath168/traffic/+/heartbeat"
TRAFFIC_LIGHT_STATUS_TOPIC = "promath168/traffic/+/status"
TRAFFIC_LIGHT_CMD_TOPIC = "promath168/traffic/+/cmd"
mqtt_server = MQTT_SERVER
topic_sub = TRAFFIC_LIGHT_CMD_TOPIC

client = None

def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'notification' and msg == b'received':
        print('ESP received hello message')

def connect_and_subscribe(client_id: str) -> MQTTClient:
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

def publish_test(msg: dict):
    last_message = 0.0
    message_interval = 5.0
    counter = 1
    while True:
        try:
            client.check_msg()
            if (time.time() - last_message) > message_interval:
                msg = b'Hello #%d' % counter
                client.publish(topic_pub, msg)
                last_message = time.time()
                counter += 1
        except OSError as e:
            restart_and_reconnect()

def heartbeat(device_id: str, msg: dict):
    #topic = MQTT_PREFIX + device_id + "/heartbeat"
    topic = MQTT_PREFIX + msg["id"] + "/heartbeat"
    print(f"   Publish topic = {topic}")
    client.publish(topic, json.dumps(msg))

def start_mqtt():
    global client

    client_id = ubinascii.hexlify(machine.unique_id()).decode("utf-8")

    try:
        client = connect_and_subscribe(client_id)
    except OSError as e:
        restart_and_reconnect()
    
    return client_id
