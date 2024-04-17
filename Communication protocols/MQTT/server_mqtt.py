import random
from paho.mqtt import client as mqtt_client
from datetime import datetime, timezone
from time import sleep

broker = "localhost"
port = 1883

ultrasonic_topic = "rsfm/mqtt/ultrasonic"
pitch_topic = "rsfm/mqtt/pitch"
roll_topic = "rsfm/mqtt/roll"
location_topic = "rsfm/mqtt/location"
home_topic = "rsfm/mqtt/home"

client_id = f'python-mqtt-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)

    client.username_pw_set("rapsberry2022", "raspberry2022")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        
        msg_rx = msg.payload.decode('utf-8')

        if msg.topic == ultrasonic_topic:
            print("WARNING: You are %s cm from an object, you must change your route.\n" % msg_rx)
        
        elif msg.topic == pitch_topic:
            print("WARNING: pitch value is %s, you must change your speed.\n" % msg_rx)

        elif msg.topic == roll_topic:
            print("WARNING: roll value is %s, you must correct your route.\n" % msg_rx)

        elif msg.topic == location_topic:
            print("YOUR LOCATION IS: %s \n" % msg_rx)

        else:
            print("UNKNOWN ALERT")
        
    client.subscribe([(ultrasonic_topic, 0), (pitch_topic, 0), (roll_topic, 0), (location_topic, 0)])
    client.on_message = on_message

    

def publish(client):

    subscribe(client)    
    msg = "hola"
    result = client.publish(home_topic, msg)
        
        

def run():
    client = connect_mqtt()
    publish(client)
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()

    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")

