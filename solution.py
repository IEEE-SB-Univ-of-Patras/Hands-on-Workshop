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





def compare_landmark(x,y):
    landmark = landmark_dist(y)
    return np.sum((landmark-x)**2)/1000

def landmark_dist(x):
    landmark = []
    for x,y in it.combinations(x,2):
        landmark.append(distance.euclidean(x,y))

    return np.array(landmark)



def hand_init(client):
    mpHands = mp.solutions.hands
    hands  = mpHands.Hands(max_num_hands=1,min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    saved_landmarks = []

    cap = cv2.VideoCapture(0)
    msg = ''
    while True:
        scores = []

        _, frame  = cap.read()
        frame = cv2.flip(frame,1)
        x,y,c = frame.shape

        temp = np.zeros((x,y,c))
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(framergb)
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])
                # Drawing landmarks on frames

                mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        if cv2.waitKey(1) == ord('s'):
            saved_landmarks.append(landmark_dist(landmarks))

        if cv2.waitKey(1) == ord('g'):
            client.sendMessage(msg)

        for i in saved_landmarks:
            scores.append(compare_landmark(i,landmarks))

        for i in range(len(scores)):
            if scores[i]<60:
                msg = str(i)
                print(i,msg)

        print(scores)
        cv2.imshow("Handy", frame)




    ##### PNG #############
        # temp = np.float32(temp)
        # temp = cv2.cvtColor(temp,cv2.COLOR_RGB2RGBA)
        # temp[:,:,3] = np.logical_and(temp[:,:,0],temp[:,:,3])*255
        #
        #
        # cv2.imshow('Workshop',temp[:,:,3])
        #
        # if cv2.waitKey(1) == ord('s'):
        #     cv2.imwrite("Temp.png",temp)
        #


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

