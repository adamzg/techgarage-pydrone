import cv2
from matcher import Matcher


matcher = Matcher([("number-3", "./templates/number-3.jpg"),
                   ("word-up", "./templates/word-up.jpg")
                  ])
positive_match = cv2.imread("./images/mm3.jpg", 0)
negative_match = cv2.imread("./images/mm6.jpg", 0)

print matcher.match(positive_match)
print matcher.match(negative_match)
