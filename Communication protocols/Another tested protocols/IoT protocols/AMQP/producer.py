import pika
from time import sleep
import serial
from datetime import datetime, timezone
import ntplib

def main():

    arduino = serial.Serial('/dev/ttyUSB0', 115200)

    ntp_client = ntplib.NTPClient()

    # RabitMQ broker IP
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.148.154',credentials=pika.PlainCredentials("raspberry2022", "raspberry2022")) )

    channel = connection.channel()

    channel.queue_declare(queue='sensor_alerts')

    try:

        while True:

            cadena = arduino.readline().decode('utf-8').strip()

            ntp_response = ntp_client.request("0.es.pool.ntp.org")
            ntp_response.offset

            channel.basic_publish(exchange="", routing_key="sensor_alerts", body= cadena + "|" + datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f'))

            print("Alerta enviada -> " + cadena)

    except ntplib.NTPException:
        print("Fallo al obtener el timestamp del servidor NTP.")
        
    except KeyboardInterrupt:
        print("Connection to broker closed.")
        connection.close()

if __name__ == "__main__":
    main()