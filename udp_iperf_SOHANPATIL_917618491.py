from http import server
from socket import *
import os
from datetime import datetime
from time import time

server_name = "173.230.149.18"
server_port = 5006

# Create a UDP socket at client side
clientSocket = socket(AF_INET, SOCK_DGRAM)

request = "ping"
targetFileSize = 1300000

if os.path.exists("./clientOutput.txt"):
    os.remove("./clientOutput.txt")
else:
    print("File Doesn't exist")

f = open("clientOutput.txt", "a")

# Send to server using created UDP socket
file_size = 0
startTime = datetime.now()

clientSocket.sendto(request.encode('utf-8'), (server_name,server_port))

while(file_size < targetFileSize):
    response,server_address = clientSocket.recvfrom(4096)
    decodedResponse = response.decode('utf-8')
    decodedResponseLength = len(decodedResponse.encode('utf-8'))

    if(file_size + decodedResponseLength <= targetFileSize):
        percentageRecieved = (file_size + decodedResponseLength)/targetFileSize * 100
        print("received %: ",round(percentageRecieved))
        f.write(response.decode('utf-8'))
    else:
        break
file_size = os.path.getsize('./clientOutput.txt')

endTime = datetime.now()
timeElapsed = (endTime-startTime).total_seconds()
print("break")
print("Time Elapsed: {} seconds".format(timeElapsed))
f.close()

file_size = os.path.getsize('./clientOutput.txt')
print("Size of file is {} bytes".format(file_size))
throughput = file_size/timeElapsed
print("Throughput: {} bps\nFile Downloaded".format(throughput))
clientSocket.close()