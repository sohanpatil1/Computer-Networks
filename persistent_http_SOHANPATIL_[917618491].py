from http import server
from pickle import FALSE
from socket import *
from typing_extensions import final
from matplotlib.cbook import ls_mapper
from bs4 import BeautifulSoup
from pathlib import Path
import os
import time
import re

f = open("ecs152a.html", "a")
def retrieveHTML(server_name,server_port, file_size, clientSocket, request):
    
    targetFileSize = 58533

    clientSocket.send(request.encode('utf-8'))

    while(file_size < targetFileSize):
        response = clientSocket.recv(4096)
        decodedResponse = response.decode('utf-8')
        decodedResponseLength = len(decodedResponse.encode('utf-8'))

        if(file_size + decodedResponseLength <= targetFileSize):
            percentageRecieved = (file_size + decodedResponseLength)/targetFileSize * 100
            f.write(response.decode('utf-8'))
            print("received %: ",round(percentageRecieved))

        else:
            break
        file_size = os.path.getsize('./ecs152a.html')
        if(file_size >= targetFileSize):
            break
    
    print("The file size is : {}".format(file_size))

def parseHTML():
    with open("./ecs152a.html") as page:
        soup = BeautifulSoup(page, 'html.parser')
    imageList = []

    for img in soup.findAll('img'):
            imageList.append(img.get('src'))
    return imageList

def downloadPictures(imageList):
    current_directory = os.getcwd()
    # print(current_directory)
    final_directory = os.path.join(current_directory, r'images')
    # print(final_directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        print("Made a directory")
    
    time.sleep(2)
    for imagePath in imageList:
        if "http" in imagePath:
            continue
        
        photoName = (imagePath.split("/"))[1]
        f = open(imagePath,"wb")

        request = "GET /" + imagePath + " HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n\r\n"
        
        clientSocket.send(request.encode('utf-8'))# Initial request for content length
        totalResponse = b''
        response = clientSocket.recv(4096)

        fileSize = 0
        match = re.search(b'Content-length: [0-9]+',response)
        # print("Matched string: ",match.group())
        if match:
            # print("Header, size calculated")
            ans = re.split(b': ',match.group())
            targetFileSize = int(ans[1])
            # print("On splitting: ",targetFileSize)

        while fileSize < targetFileSize:
            response = clientSocket.recv(4096)
            f.write(response)
            totalResponse += response
            # fileSize = os.path.getsize(os.path.join(current_directory,photoName))
            fileSize = len(totalResponse)
            if(fileSize >= targetFileSize):
                break
            # print("Image Size for {} is {}".format(photoName, fileSize))
        break
    
        f.close()

        # print("This is i: ", i)
        # print("This is the request: \n", request)
        # print("This is the response: ", response)
        print("Image: ",photoName," downloaded")
    
    clientSocket.close()



server_name = "173.230.149.18"
server_port = 23662
file_size = 0

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_name, server_port))

request = "GET /ecs152a.html HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n\r\n"


#Functions
# retrieveHTML(server_name,server_port, file_size, clientSocket, request)
imageList = parseHTML()
print("Images gathered : ",len(imageList))
downloadPictures(imageList)