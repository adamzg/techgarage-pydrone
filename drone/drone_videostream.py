import sys
import numpy as np
import cv2

from bebop import Bebop
cnt = 0

def videoCallback( frame, robot=None, debug=False ):
    global  cnt
    cnt = cnt + 1
    f = open("./images/frame.h264", "wb", 0)
    f.write( frame[-1] )
    f.close()
    cap = cv2.VideoCapture("./images/frame.h264")
    ret, img = cap.read()
    cap.release()
    if ret:
       # cv2.imwrite("./images/" + str(cnt) + ".jpg", img)
        cv2.imshow('image', img)
        cv2.waitKey(10)

print "Connecting to drone.."
drone = Bebop( metalog=None, onlyIFrames=True )
drone.videoCbk = videoCallback
drone.videoEnable()
print "Connected."
for i in xrange(1000):
    drone.update( );

print "Battery:", drone.battery