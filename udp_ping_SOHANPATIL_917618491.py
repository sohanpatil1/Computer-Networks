from http import server
from socket import *
from datetime import datetime
import time
import math
import random

def expBack(timeoutcount):
    timeout_seconds=10
    timeoutcount += 1
    timeout_seconds = (timeout_seconds * math.pow(2,timeoutcount) + random.uniform(0,1))
    timeout_seconds = max(timeout_seconds, 600)
    return timeout_seconds,timeoutcount

def printall(storedRTT, recvcount):
    print("The program is done")
    print("Stored RTTs are: {}".format(storedRTT))
    print("Total number of succesful packets is: {}".format(recvcount))
    print("Max RTT: {} seconds".format(max(storedRTT)))
    print("Min RTT: {} seconds".format(min(storedRTT)))
    print("Sum of all RTTs is: {}".format(sum(storedRTT)))

    print("Average Round Trip Time is: {}".format(sum(storedRTT)/10))
    print("Total number of packet lost is: {}".format(10-recvcount))

    
    

server_name = "173.230.149.18"
server_port = 12000

# Create a UDP socket at client side
clientSocket = socket(AF_INET, SOCK_DGRAM)

request = "ping"
recvcount=0
sumRTT = 0
storedRTT = []
packetsDropped = 0

# Send 10 pings to the server using created UDP socket
for i in range(10):
    timeoutcount = 0
    while(True):
        clientSocket.sendto(request.encode('utf-8'), (server_name,server_port))
        print("The current time is {} and this is message number: {}".format(time.time(), i+1))
        sendingTime = datetime.now()
        if((datetime.now() - sendingTime).seconds > expBack(timeoutcount)[0]):
            print("Crossed Backoff iteration : {}".format(timeoutcount))
            clientSocket.sendto(request.encode('utf-8'), (server_name,server_port))
            sendingTime = datetime.now()
        else:
            break

    response,server_address = clientSocket.recvfrom(2048)
    recvTime = datetime.now()
    recvcount+=1
    
    print("Uppercase Message from the Server: {}".format(response.decode('utf-8')))
    
    RTTime = recvTime - sendingTime
    RTTime = RTTime.total_seconds()
    print("The Round Trip Time is: {} seconds".format(RTTime))

    storedRTT.append(RTTime)


printall(storedRTT, recvcount)
clientSocket.close()