from time import sleep
import rticonnextdds_connector as rti
import ntplib
from datetime import datetime, timezone


connector = rti.Connector("Participants::RSFM", "dds.xml")
inputUltrasonido = connector.getInput("PCServer::RXUltrasonic")
inputPitchRoll = connector.getInput("PCServer::RXPitchRoll")
inputGPS = connector.getInput("PCServer::RXGPS")

ntp_client = ntplib.NTPClient()

try:

    while True:
        connector.wait()
    
        inputUltrasonido.take()

        for i in range (0, inputUltrasonido.samples.getLength()):
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

            distance_value = inputUltrasonido.samples.getNumber(i, "distance")
            timestamp = inputUltrasonido.samples.getString(i, "timestamp")
            print("WARNING: You are {} cm from an object, you must change your route.\n".format(distance_value))

            tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            file = open('bbddTime.txt', "a")
            timestamp = ( "{}".format(tiempo_transmision) )
            file.write(timestamp)
            file.write("\n")
            file.close

        	
        inputPitchRoll.take()

        for i in range (0, inputPitchRoll.samples.getLength()):
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

            pitch_value = inputPitchRoll.samples.getNumber(i, "Pitch")
            roll_value = inputPitchRoll.samples.getNumber(i, "Roll")
            timestamp = inputPitchRoll.samples.getString(i, "timestamp")
        
            if pitch_value > 45 or pitch_value < -45:
                print("WARNING: pitch value is {}, you must change your speed.\n".format(pitch_value))
            if roll_value > 45 or roll_value < -45:
                print("WARNING: roll value is {}, you must correct your route.\n".format(roll_value))
        

            tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            file = open('bbddTime.txt', "a")
            timestamp = ( "{}".format(tiempo_transmision) )
            file.write(timestamp)
            file.write("\n")
            file.close


        inputGPS.take()

        for i in range(0, inputGPS.samples.getLength()):
            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset
            tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

            latitude_value = inputGPS.samples.getNumber(i, "Latitude")
            longitude_value = inputGPS.samples.getNumber(i, "Longitude")
            timestamp = inputGPS.samples.getString(i, "timestamp")

            if longitude_value == 0 and latitude_value == 0:
                print("YOUR LOCATION IS: Calculating.\n")
            else:
                print("YOUR LOCATION IS: {}, {} \n".format(latitude_value, longitude_value))

            tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            file = open('bbddTime.txt', "a")
            timestamp = ( "{}".format(tiempo_transmision) )
            file.write(timestamp)
            file.write("\n")
            file.close


except ntplib.NTPException:
    print("Fallo al obtener el timestamp del servidor NTP.")

except KeyboardInterrupt:
    print("Closing subscriber.")
