import cv2

from bebop import Bebop
from matcher import Matcher


command = None
cnt = 0

def videoCallback( frame, drone, debug=False ):
   global cnt, command
   cnt = cnt + 1
   if isinstance(frame, tuple):
       print("h.264 frame - (frame# = %s, iframe = %s, size = %s)" % (frame[0],
                                                                      frame[1],
                                                                      len(frame[2])))
   else:
       cv2.imshow("image", frame)
       if (cnt % 10 == 0 and command is None):
           template_that_matches = matcher.match(frame)
           if template_that_matches == "techgarage-logo":
               command = "TAKEOFF"
           elif template_that_matches == "first-logo":
               command = "LAND"


       cv2.waitKey(10)


matcher = Matcher([("fau-logo", "../opencv/templates/fau-logo.png"),
                   ("first-logo", "../opencv/templates/first-logo.jpg"),
                   ("nextera-logo", "../opencv/templates/nextera-energy-logo.jpg"),
                   ("techgarage-logo", "../opencv/templates/techgarage-logo.png")
                   ], min_keypoints_pct_match=10)


print("Connecting to drone..")
drone = Bebop( metalog=None, onlyIFrames=False, jpegStream=True )
drone.videoCbk = videoCallback
drone.videoEnable()
print("Connected.")
for i in xrange(10000):
    if command is None:
        drone.update( );
    elif command == "TAKEOFF":
        print("Taking offf.........................")
        drone.takeoff()
        command = None
    elif command == "LAND":
        print("Landing ...........................")
        drone.land()
        command = None


print("Battery:", drone.battery)
