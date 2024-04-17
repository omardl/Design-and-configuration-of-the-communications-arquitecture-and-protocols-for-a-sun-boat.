import aiocoap.resource as resource
import aiocoap
import asyncio
import ntplib
from datetime import datetime, timezone

from warnings import filterwarnings
filterwarnings("ignore", category=DeprecationWarning)

ntp_client = ntplib.NTPClient()

class UltrasonicResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.content = ""
    
    async def render_put(self, request):
        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset
        tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

        self.content = request.payload
        msg = self.content.decode('utf-8').split("|")
        print("WARNING: You are %s cm from an object, you must correct your route." % msg[0].strip())
        payload = b"payload"

        tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(msg[1], '%Y-%m-%d %H:%M:%S.%f')

        file = open('bbddTime.txt', "a")
        timestamp = ( "{}".format(tiempo_transmision) )
        file.write(timestamp)
        file.write("\n")
        file.close

        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)
        

        
class PitchResource(resource.Resource):
    
    def __init__(self):
        super().__init__()
        self.content = ""
    
    async def render_put(self, request):
        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset
        tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

        self.content = request.payload
        msg = self.content.decode('utf-8').split("|")
        print("WARNING: pitch value is %s, you must change your speed." % msg[0].strip())  
        payload = b"payload"

        tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(msg[1], '%Y-%m-%d %H:%M:%S.%f')

        file = open('bbddTime.txt', "a")
        timestamp = ( "{}".format(tiempo_transmision) )
        file.write(timestamp)
        file.write("\n")
        file.close

        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)
        

        
class RollResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.content = ""
        
    async def render_put(self, request):
        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset
        tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

        self.content = request.payload
        msg = self.content.decode('utf-8').split("|")
        print("WARNING: roll value is %s, you must changew your route." % msg[0].strip())
        payload = b"payload"

        tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(msg[1], '%Y-%m-%d %H:%M:%S.%f')

        file = open('bbddTime.txt', "a")
        timestamp = ( "{}".format(tiempo_transmision) )
        file.write(timestamp)
        file.write("\n")
        file.close

        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)



class GPSResource(resource.Resource):

    def __init__(self):
        super().__init__()
        self.content = ""

    async def render_put(self, request):
        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset
        tiempo_llegada = datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')

        self.content = request.payload
        msg = self.content.decode('utf-8').split("|")
        print("YOUR LOCATION IS: %s" % msg[0].strip())
        payload = b"payload"

        tiempo_transmision = datetime.strptime(tiempo_llegada, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(msg[1], '%Y-%m-%d %H:%M:%S.%f')

        file = open('bbddTime.txt', "a")
        timestamp = ( "{}".format(tiempo_transmision) )
        file.write(timestamp)
        file.write("\n")
        file.close

        return aiocoap.Message(code=aiocoap.CHANGED, payload=payload)

def main():

    root = resource.Site()
    
    root.add_resource(['ultrasonic'], UltrasonicResource())
    
    root.add_resource(['pitch'], PitchResource())
    
    root.add_resource(['roll'], RollResource())

    root.add_resource(['gps'], GPSResource())
    
    asyncio.Task(aiocoap.Context.create_server_context(root, bind=('192.168.148.154', 5683)))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":

    try:
        main()

    except ntplib.NTPException:
        print("Fallo al obtener el timestamp del servidor NTP.")

    except KeyboardInterrupt:
        print("Closing connection")

    
    
