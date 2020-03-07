#######################
import random
import schedule
from socket import *
import time# Create a UDP socket (notice the use of SOCK_DGRAM for UDP packets)
########################
serverSocket = socket(AF_INET, SOCK_DGRAM)# Assign IP address and a port number to socket
serverSocket.bind(('0.0.0.0', 12000))
blacklist=['localhost']
hits={}
############################
print("UDP Pinger Server is waiting for pings to pong!")
def refresh():
    global hits
    hits={}
schedule.every(5).seconds.do(refresh)
while True: # Generate random number in the range of 0 to 10
    schedule.run_pending()
    rand = random.randint(0, 10) # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(2046)
    if address[0] in hits.keys():
        if address[0] in blacklist:
            print("blacklisted IP Address")
            continue
        elif hits[address[0]] >= 10:
            blacklist.append(address[0])
            print("IP Blaclisted Now")
            continue
        elif hits[address[0]] < 10:
            hits[address[0]]+=1;
    else:
        hits.update({address[0]:1})# Capitalize the message from the client
    message = message.upper()# If rand is less is than 4, we consider the packet lost and do not respond
    if (rand < 3):
        continue  # Otherwise, the server responds
    delay=random.randint(300,500)
    time.sleep(delay/1000)
    serverSocket.sendto(message, address)
