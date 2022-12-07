#!/usr/bin/python3

"""This client will first try to create a socket and connect it to the IP/port of the server.
	If successful, communication begins between server/client.
	Written by: Felipe Daniel Urzua-Alvarado"""

import socket
import sys
from struct import *

host = '192.168.0.127' 		#Change this
port = 7777			#If needed, change Port Number

"""Try to create and connect a socket at the known IP/port of server. If not possible, print the error"""

try:
    print("Trying to connect to the server...")
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.connect((host, port))

except socket.error as e:
    sys.exit(0)

"""If connection successful, communication between server/client starts"""

Response = ClientSocket.recv(1024)
print(f"\nConnection has been established, {Response.decode()}")

while True:
    NumDFloats = int(input("\nPlease enter how many numbers you would like: "))
    ClientSocket.send(str(NumDFloats).encode())					#Send variable of real numbers to set the correct Format Specifier to correctly unpack byte data stream on Server side.
    
    input_string = input("\nPlease enter the number of the operation\nyou want, along with your desired numbers: ")
    string = input_string.split() 						#Remove any whitespaces

    operation = int(string[0])  						#Operation as integer
    numbers = [float(i) for i in string[1:]]					#Convert string numbers to floats (exclude first value since this is the operation number and it must be type integer

    data_struct = Struct('<2i' + str(NumDFloats) + 'd')				#Set the Format Specifiers according to user
    sendBytes = data_struct.pack(NumDFloats, operation, *numbers)		#Pack expects two integers, and str(NumDFloats) numbers. * unpacks a list or tuple into position arguments.
    
    ClientSocket.send(sendBytes)						#Send Byte Data Stream
       
    """Result from the computation"""
    answer = ClientSocket.recv(1024) 
    print(f"\n{answer.decode()}")
    
    ClientSocket.close()
    sys.exit(0)
