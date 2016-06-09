import cv2

from bebop import Bebop

def videoCallback( frame, drone, debug=False ):
   if isinstance(frame, tuple):
       print "h.264 frame - (frame# = %s, iframe = %s, size = %s)" % (frame[0], frame[1], len(frame[2]))
   else:
       cv2.imshow("image", frame)
       cv2.waitKey(10)


print "Connecting to drone.."
drone = Bebop( metalog=None, onlyIFrames=False, jpegStream=True )
drone.videoCbk = videoCallback
drone.videoEnable()
print "Connected."
for i in xrange(10000):
    drone.update( );

print "Battery:", drone.battery