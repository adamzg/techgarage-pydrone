import cv2

target_image = cv2.imread("./templates/sniper-target.png")
target_image_resized = None

camera = cv2.VideoCapture(0)
while True:
    (grabbed, image) = camera.read()
    if grabbed:
        if target_image_resized is None:
            target_image_resized = cv2.resize(camera, dsize = None,  fx=0.15,fy=0.15)
            cv2.imshow("Target", target_image_resized)
            cv2.waitKey(0)