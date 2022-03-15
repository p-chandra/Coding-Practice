import socket

print("Lets send some TCP packets :)")
#ipaddr = input("Enter the location address:")
#port = input("Enter the port number:")
message = input("Please enter a message:")
#10.66.100.195

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

MESSAGE = str.encode(message)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)
