import cv2
import numpy as np
import zbar
import PIL.Image as Image
from bebop import Bebop

cnt = 0

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

def videoCallback( frame, drone, debug=False ):
    global cnt
    cnt = cnt + 1
    print cnt
    if isinstance(frame, tuple):
        print "h.264 frame - (frame# = %s, iframe = %s, size = %s)" % (frame[0], frame[1], len(frame[2]))

    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tobytes()

        # wrap image data
        image = zbar.Image(width, height, 'Y800', raw)

        # scan the image for barcodes
        scanner.scan(image)

        # extract results
        for symbol in image:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', symbol.location, '"%s"' % symbol.data
            print symbol
            cv2.line(frame, symbol.location[0], symbol.location[1], color=(0, 0, 255), thickness=2)
            cv2.line(frame, symbol.location[1], symbol.location[2], color=(0, 0, 255), thickness=2)
            cv2.line(frame, symbol.location[2], symbol.location[3], color=(0, 0, 255), thickness=2)
            cv2.line(frame, symbol.location[0], symbol.location[3], color=(0, 0, 255), thickness=2)

        cv2.imshow("Drone feed", frame)
        cv2.waitKey(10)




print "Connecting to drone.."
drone = Bebop( metalog=None, onlyIFrames=False, jpegStream=True, fps = 0)
drone.videoCbk = videoCallback
drone.videoEnable()
drone.moveCamera(-90, 0)
print "Connected."
for i in xrange(10000):
    drone.update( );

print "Battery:", drone.battery