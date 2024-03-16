from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_led import GroveLed
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
import paho.mqtt.client as mqtt
import random
import time
import json

CounterFitConnection.init('127.0.0.1', 5000)
led = GroveLed(5)
light_sensor = GroveLightSensor(0)

id = '<ID>'
client_telemetry_topic = id + '/telemetry'
client_name = id + 'nightlight_client'
server_command_topic = id + '/commands'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org') 
mqtt_client.loop_start()
print("MQTT connected!")

def handle_command(client, userdata, message):
        payload = json.loads(message.payload.decode())
        print("Message received:", payload)
    
        if payload['led_on']:
            led.on()
        else:
            led.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    light = light_sensor.light
    telemetry = json.dumps({'light' : light})

    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)