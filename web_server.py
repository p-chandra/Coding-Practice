from socket import *

def web_server():
    serverPort = 80
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print ("Web Server is up and listening...")
    while True:
        connectionSocket,addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            print(message)
            filename = message.split()[1]
            print(filename[1])
            print(filename,'||',filename[1])
            f = open(filename[1:])
            outputdata = f.read()
            print(outputdata)
            connectionSocket.send(outputdata.encode());            
            connectionSocket.close()
        except IOError:
            print("404 Not Found")
            response = 'HTTP/1.0 200 OK\n\n<html><head>404 Webpage not found </head></html>'
            connectionSocket.send(response.encode());
            pass
        break
    pass

if __name__ =="__main__":
    web_server()

