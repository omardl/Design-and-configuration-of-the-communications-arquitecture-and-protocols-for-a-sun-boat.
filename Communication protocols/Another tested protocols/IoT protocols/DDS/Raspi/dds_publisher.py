import rticonnextdds_connector as rti
from time import sleep
import serial
import ntplib
from datetime import datetime, timezone

connector = rti.Connector("Participants::RSFM", "dds.xml")
outputUltrasonidos = connector.getOutput("Raspberry::TXUltrasonic")
outputPitchRoll = connector.getOutput("Raspberry::TXPitchRoll")
outputGPS = connector.getOutput("Raspberry::TXGPS")

arduino = serial.Serial('/dev/ttyUSB0', 115200)

ntp_client = ntplib.NTPClient()

try:
    while True:
        cadena = arduino.readline().decode('utf-8').strip()

        if cadena.find("Ultrasonic") != -1:
            outputUltrasonidos.instance.setNumber("distance", float(cadena.replace("Ultrasonic: ", "")))
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            outputUltrasonidos.instance.setString("timestamp", datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'))
            outputUltrasonidos.write()

        elif cadena.find("Pitch") != -1:
            outputPitchRoll.instance.setNumber("Pitch", float(cadena.replace("Pitch: ", "")))
            outputPitchRoll.instance.setNumber("Roll", 0)
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            outputPitchRoll.instance.setString("timestamp", datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'))
            outputPitchRoll.write()

        elif cadena.find("Roll") != -1:
            outputPitchRoll.instance.setNumber("Pitch", 0)
            outputPitchRoll.instance.setNumber("Roll", float(cadena.replace("Roll: ", "")))
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            outputPitchRoll.instance.setString("timestamp", datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'))
            outputPitchRoll.write()

        elif cadena.find("Location") != -1:
            localizacion = cadena.replace("Location: ", "")
            if cadena.find("Calculating") != -1:
                outputGPS.instance.setNumber("Latitude", 0)
                outputGPS.instance.setNumber("Longitude", 0)

            else:
                coord = localizacion.split(",")
                outputGPS.instance.setNumber("Latitude", float(coord[0]))
                outputGPS.instance.setNumber("Longitude", float(coord[1]))
            
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            outputGPS.instance.setString("timestamp", datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'))
            outputGPS.write()
    
        print(cadena)

except ntplib.NTPException:
    print("Fallo al obtener el timestamp del servidor NTP.")

except KeyboardInterrupt:
    print("Closing publisher.")