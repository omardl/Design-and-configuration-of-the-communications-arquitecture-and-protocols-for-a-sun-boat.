from ast import Break
from asyncore import write
from binhex import REASONABLY_LARGE
import json
from pdb import Restart
import time
import ntplib
from datetime import datetime, timezone

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def saveJson(myjson):

    ntp_client = ntplib.NTPClient()

    try:

        file = open('bbdd.json', "r")
        lines= (len(file.readlines())) 
        file.close()
        file = open('bbdd.json', "a")
        if not (lines==0):
            file.write(","+"\n")
            file.flush()

        jsonObject = json.loads(myjson)

        ntp_response = ntp_client.request("0.es.pool.ntp.org")
        ntp_response.offset
        jsonObject['time_rx']= datetime.fromtimestamp(ntp_response.tx_time, timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f')
        timestamp(jsonObject)

        json.dump(jsonObject, file,indent=4)

    except ntplib.NTPException:
        print("Fallo al obtener el timestamp del servidor NTP.")
        return False

    except ValueError as e:
        print(e)
        return False

    return True


def timestamp(jsonObject):
    try:
        
        fecha1 = jsonObject['time_tx']
        fecha2 = jsonObject['time_rx']
        res= datetime.strptime(fecha2, '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(fecha1, '%Y-%m-%d %H:%M:%S.%f')

        print(res)
        file = open('bbddTime.txt', "a")
        messg=("{}".format(res))
        file.write(messg)
        file.write("\n")
        file.close

      
    except ValueError as e:
        print(e)
        return False
    return True