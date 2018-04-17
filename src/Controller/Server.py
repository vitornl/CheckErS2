from socket import *
from ..ctx import codes
from .Game_Rules import Game_Rules

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("The server is ready to receive in port: {}".format(serverPort))
game = None
while 1:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024)
    print("Message Received")
    # message_code = message.code
    message_code = message
    response_code = codes['error']
    if message_code == codes['start_game']:
        game = Game_Rules()
        response_code = codes['ok']
    elif message_code == codes['select_piece']:
        pass
    elif message_code == codes['exit']:
        break
    response = response_code
    connectionSocket.send(response)
    connectionSocket.close()
serverSocket.shutdown()
serverSocket.close()