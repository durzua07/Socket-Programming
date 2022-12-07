#!/usr/bin/python3

"""This server is capable of four different computations. The server will first try
	to create a socket and bind it to a given IP/port. If successful, the server will start
	to listen for connections. Once a client decides to make contact, the server accepts the
	connection and communication begins between server/client.
	Written by: Felipe Daniel Urzua-Alvarado"""

import socket
import sys
import statistics #For mean
from struct import *


host = '192.168.0.127'							#Change this
port = 7777								        #If needed, change Port Number
operations = {'Sum':0, 'Mean':1, 'Min':2, 'Max':3}			#Assign unique key value to each operation

try:
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.bind((host, port))

except socket.error as e:
    sys.exit(0)
print("Waiting for a Connection..")
ServerSocket.listen(5)

while True:
    client, address = ServerSocket.accept()
    greeting = """This server is capable of four different computations:
    \t-Sum: 0\n\t-Mean: 1\n\t-Min: 2\n\t-Max: 3\n"""

    client.send(str.encode(f"welcome to the Server.\n{greeting}"))

    data_struct = client.recv(1024)					#Receive variable of real numbers. Will be used to construct the correct data structure to unpack the byte data stream.
    NumDFloats = data_struct.decode()
    
    rec_value = 8 + (int(NumDFloats) * 8)				#(int + int) + (NumDFloats * 8). One int = 4 bytes. One doublefloat = 8 bytes.
    data = client.recv(rec_value)					#Receive byte data stream and print it and it's length. Len should be the number of bytes the client is sending.
    print(f"\n\nLength of byte stream: {len(data)}")
    print(f"\nByte stream: {data}")
        
    data_struct = Struct('<2i' + (NumDFloats) + 'd')			#Set Format Specifiers according to user. Correct format specifier is needed for unpack() method.
    print(f"\n\nStruct Format: {data_struct.format}")
    print(f"Struct Size: {data_struct.size}")

    original_data_from_client = data_struct.unpack(data)		#Unpack data byte stream to perform the desired computation with desired real numbers.
    print(f"\n\nOriginal Data: {original_data_from_client}\n\n")    
    
    """Perform desired computation with desired real numbers according to client and send back the result"""   
    if original_data_from_client[1] == operations['Sum']:
    	print("The sum is: ", + sum(original_data_from_client[2:]))
        add = sum(original_data_from_client[2:])
        client.send(str.encode(f"The sum is: {add}"))
        
    elif original_data_from_client[1] == operations['Mean']:
        print("The mean is: ", + statistics.mean(original_data_from_client[2:]))
        meanR = statistics.mean(original_data_from_client[2:])               
        client.send(str.encode(f"The mean is: {meanR}"))
        
    elif original_data_from_client[1] == operations['Min']:
        print("The min is: ", +  min(original_data_from_client[2:]))
        minimum = min(original_data_from_client[2:])
        client.send(str.encode(f"The min is: {minimum}"))
        
    elif original_data_from_client[1] == operations['Max']:
        print("The max is: ", + max(original_data_from_client[2:]))
        maximum = max(original_data_from_client[2:])
        client.send(str.encode(f"The max is: {maximum}"))
            
ServerSocket.close()
sys.exit(0)
