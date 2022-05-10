from socket import *
from bs4 import BeautifulSoup
from pathlib import Path
import os
import time
from datetime import datetime
import regex as re
import urllib.parse as urlparse

f = open("ecs152a.html", "a")
def retrieveHTML(server_name,server_port, file_size, clientSocket, request):
    
    if os.path.exists("ecs152a.html"):
        os.remove("ecs152a.html")

    f = open("ecs152a.html", "a")
    targetFileSize = 0
    totalResponse = ''
    clientSocket.send(request.encode('utf-8'))
    response = clientSocket.recv(4096)
    match = re.search(b'Content-length: [0-9]+',response)
    if match:
        ans = re.split(b': ',match.group())
        targetFileSize = int(ans[1])  

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
    atfPLT = datetime.now()
    time.sleep(2)
    rpsStart = datetime.now()
    for imagePath in imageList:
        
        totalResponse = b''

        if "http://" in imagePath:
            print(imagePath)
            path = urlparse.urlparse(imagePath)
            urlName = path.scheme+"://"+ path.netloc
            imageName = path.path.split("/")
            # print("This is the image name", imageName[len(imageName)-1])
            f = open(imageName[len(imageName)-1],"wb")

            imageSocket = socket(AF_INET, SOCK_STREAM)
            imageSocket.connect((path.netloc, 80))
            targetFileSize = 0
            request = "GET "+ path.path + " HTTP/1.1\r\nHost:"+ path.netloc+ "\r\nConnection: keep-alive\r\n\r\n"
            print("Request: ",request)
            imageSocket.send(request.encode('utf-8'))# Initial request for content length
            response = imageSocket.recv(4096)
            # print(response)
            content = response.split(b"\r\n\r\n")
            totalResponse+= content[1]
            fileSize = len(totalResponse)
            match = re.search(b'Content-Length: [0-9]+',response)
            if match:
                ans = re.split(b': ',match.group())
                targetFileSize = int(ans[1])
            # print(content[0])
            print("Target File size: ",targetFileSize)
            while fileSize < targetFileSize:
                response = imageSocket.recv(4096)
                # print(response)
                totalResponse += response
                # fileSize = os.path.getsize(os.path.join(current_directory,photoName))
                fileSize = len(totalResponse)
                if(fileSize >= targetFileSize):
                    break
            # print(content[0])
            # print(totalResponse)
            f.write(totalResponse)
            f.close()
            imageSocket.close()
            continue

        
        photoName = (imagePath.split("/"))[1]
        print("Downloading: ",photoName)
        f = open(imagePath,"wb")

        request = "GET /" + imagePath + " HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n\r\n"
        
        clientSocket.send(request.encode('utf-8'))# Initial request for content length
        response = clientSocket.recv(4096)
        content = response.split(b"\r\n\r\n")
        totalResponse+= content[1]
        fileSize = len(totalResponse)
        match = re.search(b'Content-length: [0-9]+',response)
        if match:
            ans = re.split(b': ',match.group())
            targetFileSize = int(ans[1])

        while fileSize < targetFileSize:
            response = clientSocket.recv(4096)
            
            totalResponse += response
            # fileSize = os.path.getsize(os.path.join(current_directory,photoName))
            fileSize = len(totalResponse)
            if(fileSize >= targetFileSize):
                break

        f.write(totalResponse)
        f.close()
    rpsEnd = datetime.now()
    clientSocket.close()
    return rpsEnd-rpsStart, atfPLT

def output(PLT, atfPLT,rps):
    size = os.get_terminal_size()
    print(size[0] * '*')
    print("HTTP Client Version: Persistent HTTP")
    print("Total PLT = {}".format(PLT.total_seconds()))
    print("Average Request Delay = {}".format("SOhan"))
    print("ATF PLT = {}".format(atfPLT.total_seconds()))
    print("RPS = {}".format(rps.total_seconds()))
    print(size[0] * '*')
    pass



server_name = "173.230.149.18"
server_port = 23662
file_size = 0
totalDelayTime = 0

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((server_name, server_port))

request = "GET /ecs152a.html HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n\r\n"


#Functions
startTime = datetime.now()
retrieveHTML(server_name,server_port, file_size, clientSocket, request)
imageList = parseHTML()
print("Images gathered : ",len(imageList))
rps,atfPLT = downloadPictures(imageList)
pltEnd = datetime.now()
PLT = pltEnd - startTime
atfPLT = atfPLT - startTime
output(PLT, atfPLT, rps)