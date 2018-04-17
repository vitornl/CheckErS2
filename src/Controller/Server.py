from socket import *
from ..ctx import codes
from .Message_Handler import Message_Handler

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
    response = Message_Handler(message)
    connectionSocket.send(response)
    connectionSocket.close()
serverSocket.shutdown()
serverSocket.close()