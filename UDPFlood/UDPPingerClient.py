###################
# Required Packages
from socket import *
import time
from sys import argv
#####################
# Initilizing required variables
serverName = argv[1]
serverPort = int(argv[2])
clientSocket = socket(AF_INET, SOCK_DGRAM) # AF_INET is IPV4 & SOCK_DGRAM is udp socket or datagram socket
#clientSocket.bind(('',5432))
########################################
# User input to be sent to server
message = input('Input lowercase sentence:') 
timings=[]
for x in range(1,13):
	sendtime=time.time() # Calculating time in ms
	clientSocket.sendto(bytes(message+str(x),"utf_8"),(serverName, serverPort))
	clientSocket.settimeout(1)
	try:
		modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
		recvtime=time.time()
		print("Server {} : {} says: {}".format(serverAddress[0],serverAddress[1],str(modifiedMessage,"utf_8")))
		res = recvtime-sendtime
		timings.append(res)
		print("RTT : {:.4f} s".format(res))
	except Exception as e:
		print("Request Timeout")

sortedtimings = sorted(timings)
print("highest RTT: {:.4f}s".format(sortedtimings[-1]))
print("lowest RTT: {:.4f} s".format(sortedtimings[0]))
result=0;
for value in sortedtimings:
	result+=value;
print("Average RTT : {:.4f} s ".format(result/12))
loss = ((12-len(sortedtimings))/12)*100
print("Loss Rate : {:.2f}% ".format(loss))

clientSocket.close()


