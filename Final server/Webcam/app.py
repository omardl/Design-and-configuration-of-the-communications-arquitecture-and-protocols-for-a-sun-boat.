import sys
from flask import Flask
from flask import render_template
from flask import Response
import cv2
import numpy as np
import socket
import pickle
import struct 
from threading import *
import time

app = Flask(__name__)

tcp = socket.SOCK_STREAM
afm = socket.AF_INET

usera_ip = "192.168.0.15"
usera_port = 1234

sa = socket.socket(afm,tcp)
sb = socket.socket(afm,tcp)

sa.bind((usera_ip,usera_port))

sa.listen()
session, addr = sa.accept()

print("reciviendo de ",addr)


def receive():
     data = b""
     payload_size = struct.calcsize("Q")
     print(payload_size)
     while True:
          while len(data) < payload_size:
               packet = session.recv(720) 
               if not packet:
                    break
               data+=packet
          packed_msg_size = data[:payload_size]
          data = data[payload_size:]
          msg_size = struct.unpack("Q",packed_msg_size)[0]
          while len(data) < msg_size:
               data += session.recv(720)
          frame_data = data[:msg_size]
          data  = data[msg_size:]
          frame = pickle.loads(frame_data)
          (flag, encodedImage) = cv2.imencode(".jpg", frame)
          if not flag:
               continue
          yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/")
def index():
     return render_template("index.html")


@app.route("/start")
def start():
     y= Response(receive(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")
     print('SOLICITUD')
     return y

if __name__ == "__main__":
     
     app.run(host="192.168.0.15",port="3015",debug=False)