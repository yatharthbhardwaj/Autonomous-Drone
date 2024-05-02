# Importations
from djitellopy import Tello
import cv2 as cv

# Tello obj and connection
tello = Tello()
tello.connect()

# Turning on tello stream
tello.streamon()

# Getting vid frame
frame_read = tello.get_frame_read()

# it's a continuous videoloop. its best to access it using a loop
while True:
    # Accessing the drones cam(Frame)
    img = tello.get_frame_read().frame

    # Resizing the frame
    img = cv.resize(img, (640, 640))

    # Displaying the frames
    cv.imshow("img", img)
    cv.waitkey(1)
