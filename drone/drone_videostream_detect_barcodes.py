from email.iterators import body_line_iterator

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
        print("h.264 frame - (frame# = %s, iframe = %s, size = %s)" %
              (frame[0], frame[1], len(frame[2])))

    else:
        barcodes = decoder.decode(frame)
        if len(barcodes) > 0:
            for barcode in barcodes:
                # do something useful with results
                print('decoded', barcode.type, 'symbol', barcode.location,
                      '"%s"' % barcode.value)
                min_x = min(barcode.location[0][0], barcode.location[1][0], barcode.location[2][0], barcode.location[3][0])
                max_x = max(barcode.location[0][0], barcode.location[1][0], barcode.location[2][0], barcode.location[3][0])

                min_y = min(barcode.location[0][1], barcode.location[1][1], barcode.location[2][1], barcode.location[3][1])
                max_y = max(barcode.location[0][1], barcode.location[1][1], barcode.location[2][1], barcode.location[3][1])

                center_x = int( (min_x + max_x) * 0.5)
                center_y = int( (min_y + max_y) * 0.5)

                height, width, _ = frame.shape

                color = (0, 0 , 255)
                text = "Centered"
                if abs(width * 0.5 - center_x) < 50:
                    color = (0, 255, 0)
                elif center_x - width * 0.5 > 50:
                    color = (0, 0, 255)
                    text = "Go Right"
                elif center_x - width * 0.5 < 50:
                    color = (255, 0, 0)
                    text = "Go Left"

                cv2.line(frame, barcode.location[0], barcode.location[1], color=color, thickness=2)
                cv2.line(frame, barcode.location[1], barcode.location[2], color=color, thickness=2)
                cv2.line(frame, barcode.location[2], barcode.location[3], color=color, thickness=2)
                cv2.line(frame, barcode.location[0], barcode.location[3], color=color, thickness=2)
                cv2.circle(frame, (center_x, center_y), 3, color=color, thickness=2)
                cv2.putText(frame, org=(width - 100, height - 100), text=text, color=color, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,)
                break

        cv2.imshow("Drone feed", frame)
        cv2.waitKey(10)




print("Connecting to drone..")
drone = Bebop( metalog=None, onlyIFrames=False, jpegStream=True, fps = 0)
drone.videoCbk = videoCallback
drone.videoEnable()
drone.moveCamera(-90, 0)
print("Connected.")
for i in xrange(10000):
    drone.update( );

print("Battery:", drone.battery)
