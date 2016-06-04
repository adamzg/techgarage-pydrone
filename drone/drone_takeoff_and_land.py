import pygame
import sys
from commands import *
from bebop import Bebop


print ("Connecting to drone...")
drone = Bebop( metalog=None, onlyIFrames=True )
drone.trim()
print ("Connected.")


drone.takeoff()
drone.wait(5)
drone.land()