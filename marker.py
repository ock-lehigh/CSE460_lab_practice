import cv2
import cv2.aruco as aruco
import numpy as np
import os
from Motor import *            
PWM=Motor() 

def findArucoMarkers(img, markerSize = 6, totalMarkers=250, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    key = 10
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    # print(ids)
    if draw:
        aruco.drawDetectedMarkers(img, bboxs) 
    return [bboxs, ids]


cap = cv2.VideoCapture(0)
moving = 0
center = 0
direction = 1
while True:
    success, img = cap.read()
    arucofound = findArucoMarkers(img)
    
    
    
     # loop through all the markers and augment each one
    if  len(arucofound[0])!=0:
        moving = 0
        for bbox, id in zip(arucofound[0], arucofound[1]):
            #print(bbox)
            center = sum(bbox[0,:,0]) / 4
            size = (bbox[0,0,0]-bbox[0,2,0])*(bbox[0,0,0]-bbox[0,2,0])+(bbox[0,0,1]-bbox[0,2,1])*(bbox[0,0,1]-bbox[0,2,1])
            print(size)
            #print(sum(bbox[0,:,1]) / 4)
    else :
        moving += 1
    
    if moving > 3 :
        PWM.setMotorModel(-1200*direction,-1200*direction,1200*direction,1200*direction)
    elif center > 400 :
        direction = -1
        PWM.setMotorModel(1000,1000,-1000,-1000)
    elif center < 240 :
        direction = 1
        PWM.setMotorModel(-1000,-1000,1000,1000)
    elif size > 20000 :
        PWM.setMotorModel(-800,-800,-800,-800)
    elif size < 4000 :
        PWM.setMotorModel(800,800,800,800)
    else :
        PWM.setMotorModel(0,0,0,0)
        
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
PWM.setMotorModel(0,0,0,0)
cap.release()
cv2.destroyAllWindows()