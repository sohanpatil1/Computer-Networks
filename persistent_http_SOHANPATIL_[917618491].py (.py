from http import server
from pickle import FALSE
from socket import *
from matplotlib.cbook import ls_mapper
from bs4 import BeautifulSoup
from pathlib import Path
import os
import time

f = open("output.html", "a")
def retrieveHTML(server_name,server_port, targetFileSize, file_size, clientSocket, request):
    clientSocket.send(request.encode('utf-8'))

    while(file_size < targetFileSize):
        response = clientSocket.recv(4096)
        decodedResponse = response.decode('utf-8')
        decodedResponseLength = len(decodedResponse.encode('utf-8'))

        if(file_size + decodedResponseLength <= targetFileSize):
            percentageRecieved = (file_size + decodedResponseLength)/targetFileSize * 100
            print("received %: ",round(percentageRecieved))
            f.write(response.decode('utf-8'))
        else:
            break
        
        file_size = os.path.getsize('./output.html')
    print("The file size is : {}".format(file_size))

def parseHTML():
    with open("./output.html") as page:
        soup = BeautifulSoup(page, 'html.parser')
    imageList = []

    for img in soup.findAll('img'):
            imageList.append(img.get('src'))
    print(imageList)
    return imageList

def downloadPictures(imageList):
    current_directory = os.getcwd()
    print(current_directory)
    final_directory = os.path.join(current_directory, r'images')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
        print("Made a directory")
    
    time.sleep(2)
    for i in imageList:
        if "http" in i:
            continue
            httpSocket = socket(AF_INET, SOCK_STREAM)
            httpSocket.connect((server_name, server_port))
            request = "GET /" + i + " HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n"

        photoName = (i.split("/"))[1]
        f = open(os.path.join(current_directory,photoName), "wb")

        request = "GET /" + i + " HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n\r\n"
        
        clientSocket.send(request.encode('utf-8'))
        response = clientSocket.recv(4096)

        f.write(response)
        f.close()


        # print("This is i: ", i)
        # print("This is the request: \n", request)
        # print("This is the type of response: ", type(response))
        # print("This is the response: ", response)
        # print("Image: ",photoName," downloaded")


server_name = "173.230.149.18"
server_port = 23662
targetFileSize = 58533
file_size = 0

clientSocket = socket(AF_INET, SOCK_STREAM)

request = "GET /ecs152a.html HTTP/1.1\r\nHost:173.230.149.18:23662\r\nX-Client-project: project-152A-part2\r\nConnection: keep-alive\r\n\r\n"

clientSocket.connect((server_name, server_port))

#Functions
# retrieveHTML(server_name,server_port, targetFileSize, file_size, clientSocket, request)
imageList = parseHTML()
print("Images gathered : ",len(imageList))
downloadPictures(imageList)

clientSocket.close()