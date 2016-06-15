import cv2
import numpy as np

from bebop import Bebop

cnt = 0


def videoCallback( frame, drone, debug=False ):

   global cnt

   blueLower = np.array([100, 67, 0], dtype="uint8")
   blueUpper = np.array([255, 128, 50], dtype="uint8")

   if isinstance(frame, tuple):
       print "h.264 frame - (frame# = %s, iframe = %s, size = %s)" % (frame[0], frame[1], len(frame[2]))
   else:
       # determine which pixels fall within the blue boundaries
       # and then blur the binary image
       blue = cv2.inRange(frame, blueLower, blueUpper)
       blue = cv2.GaussianBlur(blue, (3, 3), 0)

       # find contours in the image
       a, cnts, hierarchy = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

       # check to see if any contours were found
       if len(cnts) > 0:
           # sort the contours and find the largest one -- we
           # will assume this contour correspondes to the area
           # of my phone
           cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

           # compute the (rotated) bounding box around then
           # contour and then draw it
           rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
           print (rect);

           cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)

       # show the frame and the binary image
       cv2.imshow("Tracking", frame)
       cv2.waitKey(10)
       cv2.imshow("Binary", blue)


print "Connecting to drone.."
drone = Bebop( metalog=None, onlyIFrames=False, jpegStream=True )
drone.videoCbk = videoCallback
drone.videoEnable()
print "Connected."
for i in xrange(10000):
    drone.update( );

print "Battery:", drone.battery