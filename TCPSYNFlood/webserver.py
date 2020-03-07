from socket import * #import socket module
import sys # sys module needed to terminate the program
##############################################
#Prepare a TCP server socket
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('',serverPort)) 
serverSocket.listen(1)
#################################################
while True:
	print('The server is ready to receive')# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	connectionSocket.settimeout(2)
# If an exception occurs during the execution of try clause, the rest of the clause is skipped, If the exception type matches the word after except, the except clause is executed
	try:# Receives the HTTP request message from the client
		message = connectionSocket.recv(1024)# Extract the path of the requested object from the message, The path is the second part of HTTP header, identified by [1]
		filename = message.split()[1] # Note: these are Python file operations
		print("File name is: {} ".format(str(filename[1:],"utf-8")))# Because the extracted path of the HTTP request includes a character '/', we read the path from the second character 
		infile = open(filename[1:])# Store the entire content of the requested file in a temporary buffer ,Send one HTTP response header line into socket
		connectionSocket.sendall(str.encode("HTTP/1.0 200 OK\n",'iso-8859-1'))
		connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
		connectionSocket.send(str.encode('\r\n'))	#Send the content of the requested file to the connection socket
		for line in infile.readlines():
			connectionSocket.sendall(str.encode(""+line+"",'iso-8859-1'))
		connectionSocket.close()
	except IOError:
	#Send HTTP response message for file not found
		connectionSocket.sendall(str.encode("HTTP/1.0 404 Not Found\n",'iso-8859-1'))
		connectionSocket.sendall(str.encode('Content-Type: text/html\n', 'iso-8859-1'))
		connectionSocket.send(str.encode('\r\n'))
		connectionSocket.sendall(str.encode("<h1> 404 Not Found </h1>",'iso-8859-1'))
		connectionSocket.close()
	except Exception as e:
		pass
serverSocket.close()
sys.exit()
