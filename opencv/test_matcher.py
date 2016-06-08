import cv2
from matcher import Matcher


matcher = Matcher([("number-1", "./templates/animal_number_1.jpg"),
                   ("number-2", "./templates/animal_number_2.jpg"),
                   ("number-3", "./templates/animal_number_3.jpg"),
                   ("number-4", "./templates/animal_number_4.jpg"),
                   ("number-5", "./templates/animal_number_5.jpg"),
                   ("number-6", "./templates/animal_number_6.jpg"),
                   ("number-7", "./templates/animal_number_7.jpg"),
                   ("number-8", "./templates/animal_number_8.jpg"),
                   ("number-9", "./templates/animal_number_9.jpg")
                  ], mininum_matches=20)

positive_match = cv2.imread("./images/mm3.jpg", 0)
negative_match = cv2.imread("./images/mm6.jpg", 0)

print "Analyzing..."
print matcher.match(positive_match)
print matcher.match(negative_match)
