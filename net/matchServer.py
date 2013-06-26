import socket
from threading import Thread
import threading

matchServer = socket.socket()
matchServer.bind(('0.0.0.0', 13373))
matchServer.listen(1337)

activeGames = [['default', 'default', 'default']]

def checkExistance(commandData):
	global activeGames
	commandData = commandData.split()
	gameName = ' '.join(commandData[1:])
	for i in range(len(activeGames)):
		if gameName in activeGames[i][0]:
			return 'EXIST'
	return 'AVAILABLE'

def createGame(gameName):
	activeGames.append([' '.join(gameName), 1, 'obnoxious'])
	matchServer.sendall('GAME %s' % str(' '.join(gameName)))
	return 'MATCH CREATED\n'

def handleConnection():
	while True:
		command = clientSocket.recv(1024)
		commandSplit = command.split()
		try:
			if commandSplit[0] == 'LIST':
				global activeGames
				clientSocket.send(str(activeGames) + '\n')

			if commandSplit[0] == 'CREATE':
				if checkExistance(command) == 'AVAILABLE':
					clientSocket.send(createGame(commandSplit[1:]))
				else:
					clientSocket.send('GAME NAME TAKEN\n')
		except:
			clientSocket.send('FAIL\n')

while 1:
	(clientSocket, address) = matchServer.accept()
	thread = Thread(target = handleConnection)
	thread.start() 