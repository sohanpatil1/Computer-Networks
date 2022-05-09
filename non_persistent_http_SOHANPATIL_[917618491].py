from asyncore import write
from http import server
from pickle import FALSE
from socket import *
from typing_extensions import final
from matplotlib.cbook import ls_mapper
from bs4 import BeautifulSoup
from pathlib import Path
import os
import time
import regex as re


def retrieveHTML(server_name,server_port, file_size, clientSocket, request):

    f = open("ecs152a.html", "a")    
    targetFileSize = 58533
    totalResponse = ''
    clientSocket.send(request.encode('utf-8'))
    response = clientSocket.recv(4096)
    content = response.decode('utf-8').split("\r\n\r\n")
    totalResponse+= content[1]
    file_size = len(totalResponse)
    while(file_size < targetFileSize):
        response = clientSocket.recv(4096)
        
        totalResponse += response.decode('utf-8')

        percentageRecieved = file_size/targetFileSize * 100
        print("received %: ",round(percentageRecieved))
        file_size = len(totalResponse)
        if(file_size >= targetFileSize):
            break
                
    f.write(totalResponse)
    percentageRecieved = file_size/targetFileSize * 100
    print("received %: ",round(percentageRecieved))
    
    print("The file size is : {}".format(file_size))
    f.close()

def parseHTML():
    with open("./ecs152a.html") as page:
        soup = BeautifulSoup(page, 'html.parser')
    imageList = []

    for img in soup.findAll('img'):
            imageList.append(img.get('src'))
    return imageList

def downloadPictures(imageList):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'images')
    
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        print("Made a directory")
    
    time.sleep(2)
    for imagePath in imageList:
        
        imageSocket = socket(AF_INET, SOCK_STREAM)
        imageSocket.connect((server_name, server_port))

        if "http" in imagePath:
            imageSocket.close()
            continue
        
        photoName = (imagePath.split("/"))[1]
        f = open(imagePath,"wb")

        request = "GET /" + imagePath + " HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: close\r\n\r\n"
        
        imageSocket.send(request.encode('utf-8'))# Initial request for content length
        totalResponse = b''
        response = imageSocket.recv(4096)
        content = response.split(b"\r\n\r\n")
        totalResponse+= content[1]
        fileSize = len(totalResponse)
        match = re.search(b'Content-length: [0-9]+',response)
        if match:
            ans = re.split(b': ',match.group())
            targetFileSize = int(ans[1])

        while fileSize < targetFileSize:
            response = imageSocket.recv(4096)
            
            totalResponse += response
            # fileSize = os.path.getsize(os.path.join(current_directory,photoName))
            fileSize = len(totalResponse)
            if(fileSize >= targetFileSize):
                break

        f.write(totalResponse)
        f.close()


        print("Image: ",photoName," downloaded")
        imageSocket.close()
        
    clientSocket.close()



server_name = "173.230.149.18"
server_port = 23662
file_size = 0

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_name, server_port))

request = "GET /ecs152a.html HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: close\r\n\r\n"


#Functions
# retrieveHTML(server_name,server_port, file_size, clientSocket, request)
imageList = parseHTML()
print("Images gathered : ",len(imageList))
downloadPictures(imageList)