import socket
import threading
import json
from threading import Thread

clientSocket = socket.socket()
clientSocket.connect(('127.0.0.1', 35931))

def socketSendData():
	userInput = raw_input()
	clientSocket.send(userInput)

def socketWaitForData():
	data = clientSocket.recv(1024)
	print data

while 1:
	thread = Thread(target = socketWaitForData)
	thread.start()
	socketSendData()