import pygame
import cv2
from commands import *
import logging
from bebop import Bebop

logging.basicConfig(level=logging.DEBUG)

wnd = None
def video_frame(frame):
    cv2.imshow("Drone", frame)
    cv2.waitKey(10)

def video_start():
    print("Starting video...")
    cv2.namedWindow("Drone")

def video_end():
    print("Ending video...")
    cv2.destroyWindow("Drone")
    # Have to send waitKey several times on Unix to make window disappear
    for i in range(1, 5):
        cv2.waitKey(1)

print("Connecting to drone..")
drone = Bebop()
drone.video_callbacks(video_start, video_end, video_frame)
drone.videoEnable()
print("Connected.")

pygame.init()
size = [100, 100]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Drone Teleop")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

if pygame.joystick.get_count() == 0:
    print("No joysticks found")
    done = True
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Initialized %s" % (joystick.get_name()))
    print("Number of buttons %d. Number of axis %d, Number of hats %d" %
          (joystick.get_numbuttons(), joystick.get_numaxes(),
           joystick.get_numhats()))


# -------- Main Program Loop -----------

MAX_SPEED = 50

while not done:
    try:
        # EVENT PROCESSING STEP
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        executing_command = False

        if joystick.get_button(0) == 1:
            executing_command = True
            print("Landing...")
            if drone.flyingState is None or drone.flyingState == 1: # if taking off then do emegency landing
                drone.emergency()
            drone.land()

        if joystick.get_button(1) == 1:
            executing_command = True
            drone.update(cmd=movePCMDCmd(True, 0, 0, MAX_SPEED, 0))
            print("Drone spinning clockwise.")

        if joystick.get_button(2) == 1:
            executing_command = True
            drone.update(cmd=movePCMDCmd(True, 0, 0, -1 * MAX_SPEED, 0))
            print("Drone spinning counterclockwise.")

        if joystick.get_button(3) == 1:
            executing_command = True
            print("Taking off..")
            drone.takeoff()

        if joystick.get_button(4) == 1:
            executing_command = True
            print("Descending...")
            drone.update(cmd=movePCMDCmd(True, 0, 0, 0, -1 * MAX_SPEED))

        if joystick.get_button(5) == 1:
            executing_command = True
            print("Asccending...")
            drone.update(cmd=movePCMDCmd(True, 0, 0, 0, MAX_SPEED))

        if joystick.get_button(6) == 1:
            executing_command = True
            print("Button 6 pressed")

        if joystick.get_button(7) == 1:
            executing_command = True
            print("Button 7 pressed")

        if abs(joystick.get_axis(0)) > 0.05 or abs(joystick.get_axis(1)) > 0.05:
            executing_command = True
            print("Left stick %f, %f" % (joystick.get_axis(0),
                                         joystick.get_axis(1)))
            drone.update(cmd=movePCMDCmd(True,  1 * joystick.get_axis(0) * MAX_SPEED, -1 * joystick.get_axis(1) * MAX_SPEED, 0, 0))

        if abs(joystick.get_axis(3)) > 0.05 or abs(joystick.get_axis(4)) > 0.05:
            executing_command = True
            print("Right stick %f, %f" % (joystick.get_axis(3),
                                          joystick.get_axis(4)))

        (hat_x, hat_y) = joystick.get_hat(0)
        if (hat_x != 0 or hat_y !=0):
            executing_command = True
            print("Hat %d, %d" % (hat_x, hat_y))

        # Limit to 20 frames per second
        clock.tick(20)

        if not executing_command:
            drone.update(cmd=movePCMDCmd(False, 0, 0, 0, 0))
            drone.update(cmd=None)
    except:
        print("Error")
        if drone.flyingState is None or drone.flyingState == 1: # if taking off then do emegency landing
            drone.emergency()
        drone.land()
        done = True


# Close the window and quit.
pygame.quit()
