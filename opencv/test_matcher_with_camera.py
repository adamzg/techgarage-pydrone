import time
import cv2
from matcher import Matcher



matcher = Matcher([("number-1", "./templates/animal_number_1.jpg")
#                   ("number-2", "./templates/animal_number_2.jpg"),
#                   ("number-3", "./templates/animal_number_3.jpg"),
#                   ("number-4", "./templates/animal_number_4.jpg"),
#                   ("number-5", "./templates/animal_number_5.jpg"),
#                   ("number-6", "./templates/animal_number_6.jpg"),
#                   ("number-7", "./templates/animal_number_7.jpg"),
#                   ("number-8", "./templates/animal_number_8.jpg"),
#                   ("number-9", "./templates/animal_number_9.jpg")
                  ], mininum_matches=20)

#img = cv2.imread("./images/0.jpg")
#print matcher.match(img)

cam = cv2.VideoCapture(0)

cnt = 0
while True:
    (grabbed, img) = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print matcher.match(gray)
    #cv2.imshow("Pic", img)
    #cv2.waitKey(10)
