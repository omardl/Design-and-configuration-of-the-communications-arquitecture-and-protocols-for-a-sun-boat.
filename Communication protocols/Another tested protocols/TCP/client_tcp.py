import socket
import json
from datetime import datetime, timezone
import serial
import ntplib

 
msgFromClient       = "Hello TCP Server"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("192.168.148.154", 8000)
bufferSize          = 1024

arduino = serial.Serial('/dev/ttyUSB0', 115200)
 

TCPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
TCPClientSocket.connect(serverAddressPort)


TCPClientSocket.sendall(bytesToSend)
msgFromServer = TCPClientSocket.recv(bufferSize)
msg = "Message from Server {}".format(msgFromServer)

print(msg)

ntp_client = ntplib.NTPClient()

try:

    while(True):

        cadena =  arduino.readline().decode('utf-8')

        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset

        if cadena.find("Ultrasonic") != -1:

            paquete={
                "Sensor": "Ultrasonic",
                "Distance_value_in_cm": cadena.replace("Ultrasonic: ", "").split(),
                "time_tx": datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_rx": ""
            }
        
        elif cadena.find("Pitch") != -1:

            paquete={
                "Sensor": "PitchRoll",
                "Pitch_value": cadena.replace("Pitch: ", "").split(),
                "time_tx": datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_rx": ""
            }


        elif cadena.find("Roll") != -1:

            paquete={
                "Sensor": "PitchRoll",
                "Roll_value": cadena.replace("Roll: ", "").split(),
                "time_tx": datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
                "time_rx": ""
            }

        elif cadena.find("Location") != -1:
            
            if cadena.find("Calculating") != -1:
                paquete={
                    "Sensor": "GPS",
                    "Location_value":  "",
                    "Longitude_value": "",
                    "time_tx": datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "time_rx": ""
                }

            else: 
                msg = cadena.replace("Location: ", "").strip().split(',')

                paquete={
                    "Sensor": "GPS",
                    "Location_value":  msg[0],
                    "Longitude_value": msg[1],
                    "time_tx": datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "time_rx": ""
                }
           
        new_string = bytearray(json.dumps(paquete),"UTF-8")
        TCPClientSocket.sendall(new_string)
        msgFromServer = TCPClientSocket.recv(bufferSize)
        msg = "Message from Server {}".format(msgFromServer)
        print(msg)

except ntplib.NTPException:
    print("Fallo al obtener el timestamp del servidor NTP.")

except KeyboardInterrupt:
    print("Closing TCP connection.")
