import asyncio
from aiocoap import *
from time import sleep
import serial
import ntplib
from datetime import datetime, timezone

#Eliminamos con estas dos lineas un deprecation warning que nos salta al tratar de usar get_event_loop(). 
#El programa nos avisa de que no existe ningun event_loop() en ese momento, aunque funciona correctamente ya que la propia funcion lo crea si no existe
from warnings import filterwarnings
filterwarnings("ignore", category=DeprecationWarning)

ntp_client = ntplib.NTPClient()

async def main():

    arduino = serial.Serial('/dev/ttyUSB0', 115200)

    context = await Context.create_client_context()

    try:
        while True:

            cadena = arduino.readline().decode('utf-8').strip()


            if cadena.find("Ultrasonic") != -1:
                ntp_response = ntp_client.request("0.es.pool.ntp.org")
                ntp_response.offset
                msg = cadena.replace("Ultrasonic: ", "") + "|" + datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
                payload = bytes(msg, 'utf-8')
                request = Message(code=PUT, payload=payload, uri="coap://192.168.148.154/ultrasonic")
                response = await context.request(request).response
                print("Sending message --> Ultrasonic: {}".format(msg))
            
            elif cadena.find("Pitch") != -1:
                ntp_response = ntp_client.request("0.es.pool.ntp.org")
                ntp_response.offset
                msg = cadena.replace("Pitch: ", "") + "|" + datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
                payload = bytes(msg, 'utf-8')
                request = Message(code=PUT, payload=payload, uri="coap://192.168.148.154/pitch")
                response = await context.request(request).response
                print("Sending message --> Pitch: {}".format(msg))
            
            elif cadena.find("Roll") != -1:
                ntp_response = ntp_client.request("0.es.pool.ntp.org")
                ntp_response.offset
                msg = cadena.replace("Roll: ", "") + "|" + datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
                payload = bytes(msg, 'utf-8')
                request = Message(code=PUT, payload=payload, uri="coap://192.168.148.154/roll")
                response = await context.request(request).response
                print("Sending message --> Roll: {}".format(msg))

            elif cadena.find("Location") != -1:
                ntp_response = ntp_client.request("0.es.pool.ntp.org")
                ntp_response.offset
                msg = cadena.replace("Location: ", "").strip() + "|" + datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
                payload = bytes(msg, 'utf-8')
                request = Message(code=PUT, payload=payload, uri="coap://192.168.148.154/gps")
                response = await context.request(request).response
                print("Sending message --> Location: {}".format(msg))

            

    except ntplib.NTPException:
        print("Fallo al obtener el timestamp del servidor NTP.")

    except KeyboardInterrupt:
        print("Closing connection.")


        
                     
if __name__ == "__main__":

    try: 
        asyncio.get_event_loop().run_until_complete(main())
        
    except:  
        print("Can't connect to server.")