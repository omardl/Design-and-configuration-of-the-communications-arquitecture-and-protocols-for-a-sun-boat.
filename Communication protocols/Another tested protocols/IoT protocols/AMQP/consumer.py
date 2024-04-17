import pika
from time import sleep
from datetime import datetime, timezone
import ntplib

def main():

    ntp_client = ntplib.NTPClient()

    # RabitMQ broker IP
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.148.154', credentials=pika.PlainCredentials("raspberry2022", "raspberry2022")))
    channel = connection.channel()

    channel.queue_declare(queue='sensor_alerts')

    def callback(ch, method, properties, body):

        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset    
        tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

        msg = body.decode('utf-8').split("|")

        if msg[0].find("Ultrasonic") != -1:
            print("WARNING: You are %s cm from an object, you must change your route." % msg[0].strip().replace("Ultrasonic: ", ""))

        elif  msg[0].find("Pitch") != -1:
            print("WARNING: pitch value is %s, you must change your speed." % msg[0].strip().replace("Pitch: ", ""))

        elif  msg[0].find("Roll") != -1:
            print("WARNING: roll value is %s, you must correct your route." % msg[0].strip().replace("Roll: ", ""))

        elif msg[0].find("Location") != -1:
            print("YOUR LOCATION IS: %s" % msg[0].strip().replace("Location: ", ""))

        else:
            print("UNKNOWN ALERT")

        tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(msg[1], '%Y-%m-%d %H:%M:%S.%f')
        

        file = open('bbddTime.txt', "a")
        timestamp = ( "{}".format(tiempo_transmision) )
        file.write(timestamp)
        file.write("\n")
        file.close

    channel.basic_consume(queue='sensor_alerts', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == "__main__":
    
    try:
        main()
    
    except ntplib.NTPException: 
        print("Fallo al obtener el timestamp del servidor NTP.")

    except KeyboardInterrupt:
        print("Connection to broker closed")