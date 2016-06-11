import cv2
from imutils.video import VideoStream

left_camera = cv2.VideoCapture(0)
left_camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
left_camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

right_camera = cv2.VideoCapture(1)
right_camera.set(cv2.CAP_PROP_FRAME_WIDTH,320)
right_camera.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# VideoStream(usePiCamera=False, src=0, framerate=10, resolution=(320, 240)).start()
#right_camera = VideoStream(usePiCamera=False, src=1, framerate=5).start()

cnt = 0
while True:
    g1, left_image = left_camera.read()
    g2, right_image = right_camera.read()

    cv2.imshow("Left", left_image)
    cv2.imshow("Right", right_image)

    cv2.waitKey(10)
  #  if key == ord('q'):
  #     break