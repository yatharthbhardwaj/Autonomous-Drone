# Importations
from djitellopy import Tello
import cv2 as cv

# Tello obj and connection
tello = Tello()
tello.connect()

# Turning on tello stream
tello.streamon()

# Getting vid frame
freame_read = tello.get_frame_read()
