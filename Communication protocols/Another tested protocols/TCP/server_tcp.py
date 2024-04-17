import socket
import json
from functions import *

 
localIP     = "192.168.148.154"
localPort   = 8000
bufferSize  = 1024

msgFromServer       = "Hello TCP Client"
bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

# Bind to address and ip
TCPServerSocket.bind((localIP, localPort))
print("TCP server up and listening")
TCPServerSocket.listen(1)

# Listen for incoming datagrams
print('waiting for a connection')
connection, client_address = TCPServerSocket.accept()

try:
    while(True):

        print('waiting for a message')
        bytesAddressPair = connection.recv(bufferSize)

        message = bytesAddressPair

        clientMsg = "Message from Client:{}".format(message)
        print(clientMsg)
        print(client_address)

        if is_json(message) :
            print("ES JSON")
            print("RESULTADO DE GUARDAR: {}".format(saveJson(message)))
        else :
            print("NO ES")
     
        # Sending a reply to client    
        connection.sendall(bytesToSend)

except KeyboardInterrupt:
    print("Closing TCP connection.")