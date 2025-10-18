import json
import random
import time
import os
import paho.mqtt.client as mqtt

DEVICE_ID = "mbit-lab-01"
BROKER_HOST = os.getenv("MQTT_HOST", "100.118.141.104")
BROKER_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "lab/microbit/telemetry")

def sane_temp(value):
    return -10 <= value <= 60

def sane_light(value):
    return 0 <= value <= 255

client = mqtt.Client(client_id="simulador-microbit")
if MQTT_USER:
    client.username_pw_set(MQTT_USER, MQTT_PASS)

print(f"[MQTT] Conectando a {BROKER_HOST}:{BROKER_PORT} topic={MQTT_TOPIC}")
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_start()

SEQ = 0

while True:
    temp = random.randint(-15, 70)
    light = random.randint(-10, 300)
    ts = int(time.time() * 1000)

    # Determina estado
    status = []
    if not sane_temp(temp):
        status.append("temp_oob")
    if not sane_light(light):
        status.append("light_oob")
    if len(status) == 0:
        status = ["ok"]

    payload = {
        "deviceId": DEVICE_ID,
        "seq": SEQ,
        "ts_ms": ts,
        "temp_c": temp,
        "light_lvl": light,
        "status": status
    }

    # Publica al broker
    client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
    print(f"[PUB] {json.dumps(payload)}")

    SEQ += 1
    time.sleep(3)
