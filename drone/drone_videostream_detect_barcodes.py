import cv2
import numpy as np
from bebop import Bebop
from bardecoder import Decoder
from bardecoder import Barcode

cnt = 0

decoder = Decoder()


def videoCallback( frame, drone, debug=False ):
    global decoder
    if isinstance(frame, tuple):
        print "h.264 frame - (frame# = %s, iframe = %s, size = %s)" % (frame[0], frame[1], len(frame[2]))

    else:
        barcodes = decoder.decode(frame)
        if len(barcodes) > 0:
            for barcode in barcodes:
                # do something useful with results
                print 'decoded', barcode.type, 'symbol', barcode.location, '"%s"' % barcode.value
                cv2.line(frame, barcode.location[0], barcode.location[1], color=(0, 0, 255), thickness=2)
                cv2.line(frame, barcode.location[1], barcode.location[2], color=(0, 0, 255), thickness=2)
                cv2.line(frame, barcode.location[2], barcode.location[3], color=(0, 0, 255), thickness=2)
                cv2.line(frame, barcode.location[0], barcode.location[3], color=(0, 0, 255), thickness=2)

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