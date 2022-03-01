import numpy as np
import cv2
import time
from Motor import *            
PWM=Motor() 


# Video source - can be camera index number given by 'ls /dev/video*
# or can be a video file, e.g. '~/Video.avi'
cap = cv2.VideoCapture(0)
start_moving = 0
start_forwarding = 0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Filter
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    result = cv2.bitwise_and(frame, frame, mask = mask)       
    
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5) 
    
    rows = gray.shape[0]
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, rows / 8,
                               param1=100, param2=15,
                               minRadius=1, maxRadius=200)
    

    if circles is None:
        start_moving = start_moving +1
    
    if start_moving > 5:
        PWM.setMotorModel(950,950,-950,-950)

    if circles is not None:
        start_moving = 0
        PWM.setMotorModel(0,0,0,0)
        circles = np.uint16(np.around(circles))
        biggest = circles[0, 0]
        for i in circles[0, :]:
            if i[2] > biggest[2] :
                biggest = i
                
        center = (biggest[0], biggest[1])
        # circle center
        cv2.circle(gray, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = biggest[2]
        cv2.circle(gray, center, radius, (255, 0, 255), 3)
        print(radius, center)
        
        if radius < 80 :
            start_forwarding = start_forwarding - 1
        else:
            start_forwarding = -1
        
        if start_forwarding >= 3:
            speed = -600
            PWM.setMotorModel(speed,speed,speed,speed)
        elif start_forwarding <= -3:
            speed = 600
            PWM.setMotorModel(speed,speed,speed,speed)
        else :
            PWM.setMotorModel(0,0,0,0)
            
    # Display the resulting frame
    cv2.imshow('frame',gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        PWM.setMotorModel(0,0,0,0)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()