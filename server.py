import socket
import threading
from threading import Thread
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 35931))
serverSocket.listen(1337)

registeredNicks = {}
activeGamesList = {}

def registerNick(ip, nickName):
	global registeredNicks
	registeredNicks[ip] = nickName
	return '%s is now registered as: %s\n' % (ip, nickName)

def gamesList():
	return '\n'.join(activeGamesList)

def createGame(gameName):
	global activeGamesList
	try:
		gameName = ' '.join(gameName).strip('\n')
	except:
		gamename = gameName.strip('\n')

	if gameName.strip('\n') in activeGamesList:
		return '%s EXIST\n' % gameName
	else:
		activeGamesList[gameName] = gameName
		return '%s CREATED\n' % gameName
	
	return 'Failed to create game.\n'

def handleConnection():
	while True:
		receivedData = clientSocket.recv(1024)
		try:
			receivedData = receivedData.split()
			
			if receivedData[0] == 'NICK':
				clientSocket.send(registerNick(address[0], receivedData[1]))
			
			if receivedData[0] == 'LIST':
				global activeGamesList
				clientSocket.send(gamesList())
			
			if receivedData[0] == 'CREATE':
				if len(receivedData) > 1:
					tempData = createGame(receivedData[1:])
				else:
					tempData = createGame(receivedData[1])
				clientSocket.send(tempData)

		except:
			clientSocket.send('Failed parsing command.\n')
while 1:
    (clientSocket, address) = serverSocket.accept()
    thread = Thread(target = handleConnection)
    thread.start()
