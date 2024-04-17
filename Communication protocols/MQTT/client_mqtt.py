import random
from time import sleep
import serial
from paho.mqtt import client as mqtt_client
import json

broker = "5.224.43.188"  
port = 4040 

ultrasonic_topic = "rsfm/mqtt/ultrasonic"
ultrasonic_topic2 = "rsfm/mqtt/ultrasonic2"
pitch_topic = "rsfm/mqtt/pitch"
roll_topic = "rsfm/mqtt/roll"
pitch_topic2 = "rsfm/mqtt/pitch2"
roll_topic2 = "rsf,/mqtt/roll2"
location_topic = "rsfm/mqtt/location"
ship_topic = "rsfm/mqtt/ship"

client_id = f'python-mqtt-{random.randint(0, 1000)}'

arduino = serial.Serial('/dev/ttyUSB0', 115200)
arduino2 = serial.Serial('/dev/ttyACM0', 9600)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set("raspberry2022", "raspberry2022")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):

    subscribe(client)

    while True:

        cadena = arduino.readline().decode('utf-8').strip()

        if cadena.find("Ultrasonic") != -1:

            msg = cadena.replace("Ultrasonic: ", "")
            result = client.publish(ultrasonic_topic, msg)
        elif cadena.find("Pitch") != -1:

            msg = cadena.replace("Pitch: ", "")
            result = client.publish(pitch_topic, msg)
        elif cadena.find("Roll") != -1:

            msg = cadena.replace("Roll: ", "")
            result = client.publish(roll_topic, msg)
        elif cadena.find("Latitude") != -1:

            msg = cadena.replace("Location: ", "")
            result = client.publish(location_topic, msg)

        status = result[0]
        if status == 0:
            print(f"Send message: {cadena} ")
        else:
            print(f"Failed to send message.")

def subscribe(client):
    def on_message(client, userdata, msg):
        cadena = msg.payload.decode("utf-8")
        print(f"Received: {cadena}")

        if msg.topic == ultrasonic_topic2:

             print("a")
             arduino2.write(bytes("a", "utf-8"))
        elif msg.topic == pitch_topic2:
             print("b")
             arduino2.write(bytes("b", "utf-8"))
        elif msg.topic == roll_topic2:
             print("c")
             arduino2.write(bytes("c", "utf-8"))

    client.subscribe([(ship_topic,0),(roll_topic2, 0),(pitch_topic2, 0),(ultrasonic_topic2,0)])
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")