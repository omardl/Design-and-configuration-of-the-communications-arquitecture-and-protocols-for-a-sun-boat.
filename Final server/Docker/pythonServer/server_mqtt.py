import random
from paho.mqtt import client as mqtt_client
from datetime import datetime, timezone
import time


# remember change when necessary
#broker = "localhost"
broker= "192.168.0.15"
port = 5001

ultrasonic_topic = "rsfm/mqtt/ultrasonic"
pitch_topic = "rsfm/mqtt/pitch"
roll_topic = "rsfm/mqtt/roll"
location_topic = "rsfm/mqtt/location"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'



def connect_mqtt() -> mqtt_client:
 
    log = open("/pythonServer/server.log" , "a")
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!",file=log)
        else:
            print("Failed to connect, return code %d\n", rc,file=log)

    client = mqtt_client.Client(client_id)
    #
    time.sleep(2)
    log.close
    #

    #username and password
    client.username_pw_set("rapsberry2022", "raspberry2022")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):

    def on_message(client, userdata, msg):
        
       
        
        tiempo_llegada= datetime.now()
        log = open("/pythonServer/server.log", "a")
    
        
        msg_rx = msg.payload.decode('utf-8').split("|")

        if msg.topic == ultrasonic_topic:
            print("WARNING: You are %s cm from an object, you must change your route.\n" % msg_rx[0],file=log)
        
        elif msg.topic == pitch_topic:
            print("WARNING: pitch value is %s, you must change your speed.\n" % msg_rx[0],file=log)

        elif msg.topic == roll_topic:
            print("WARNING: roll value is %s, you must correct your route.\n" % msg_rx[0],file=log)

        elif msg.topic == location_topic:
            print("YOUR LOCATION IS: %s \n" % msg_rx[0],file=log)

        else:
            print("UNKNOWN ALERT",file=log)

        log.close
        tiempo_transmision = tiempo_llegada - datetime.strptime(msg_rx[1], '%Y-%m-%d %H:%M:%S.%f')

        file = open("/pythonServer/bbddTime.txt", "a")
        timestamp = ( "{}".format(tiempo_transmision) )
        file.write(timestamp)
        file.write("\n")
        file.close

        
    client.subscribe([(ultrasonic_topic, 0), (pitch_topic, 0), (roll_topic, 0), (location_topic, 0)])
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    try:
        run()


    except KeyboardInterrupt:
        print("Disconnected from MQTT Broker.")

