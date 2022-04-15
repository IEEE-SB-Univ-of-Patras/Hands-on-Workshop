import socket
import cv2
import numpy as np
import mediapipe as mp
import itertools as it
from scipy.spatial import distance
import time


import sys







HEADERSIZE = 10

class Client():

    def __init__(self):

        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def serverConnect(self, ip, port):    
        try: 
            self.serverSocket.connect((ip, port))
            return True
        
        except socket.error:
            return False

    def sendMessage(self, message):
        
        dataString = "{}{}".format(str(len(message)).ljust(HEADERSIZE), message)
        self.serverSocket.send(dataString.encode("utf-8"))

    def getMessage(self):
        request_size = self.serverSocket.recv(HEADERSIZE).decode().strip()

        if request_size:
            server_data = self.serverSocket.recv(int(request_size)).decode()
            return server_data




#Find the distance between all the combinations of landmarks and calculate total distance.
def compare_landmark(x,y):
    pass


#Create all the combinations of points and append them to a list.
def landmark_dist(x):
    pass



def hand_init(client):

#   2 Initialize the hand tracker

#   1.1 Start capturing video from your camera





#   1.2 Read frame, flip it, find its shape and color convert it
#   1.3 (bonus) Apply edge detection to your video

#   3 Find and draw landmarks on frames


#   4 Score the landmarks

#   5 Send message to the robot





def main():

    IP = "192.168.43.40"
    PORT = 1234

    client = Client()
    
    client.serverConnect(IP, PORT)

    
    hand_init(client)

    # while True:
    #     msg = input("Enter a  message: ")
    #
    #     client.sendMessage("{}".format(msg))
    #     #print(client.getMessage())
    

if __name__ == "__main__":
    main()

