# Importations
from djitellopy import tello
import keyControl as kc
from time import sleep
import cv2 as cv
from ultralytics import YOLO
import math
import numpy as np

# Initializations and Variables
kc.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
drone.takeoff()

model = YOLO('path/to/your/yolo/weights') # Enter the path to your weights here
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

def getKeyboardInput():
    # initialize control variables for left-right, forward-back, up-down, and yaw velocity
    lr, fb, ud, yv = 0, 0, 0, 0

    # set movement speed
    speed = 50

    # Left-right control
    if kc.getKey("LEFT"): # check if 'LEFT' key is pressed
        lr = -speed # move left
    elif kc.getKey("RIGHT"): # check if 'RIGHT' key is pressed
        lr = speed # move right

    # Forward-back control
    if kc.getKey("UP"): # check if 'UP' key is pressed
        fb = speed # move forward
    elif kc.getKey("DOWN"): # check if 'DOWN' key is pressed
        fb = -speed # move backward

    # Up-down control
    if kc.getKey("w"): # check if 'w' key is pressed
        ud = speed # move up
    elif kc.getKey("s"): # check if 's' key is pressed
        ud = -speed # move down

    # Yaw control
    if kc.getKey("a"): # check if 'a' key is pressed
        yv = speed # yaw left
    elif kc.getKey("d"): # check if 'd' key is pressed
        yv = -speed # yaw right

    # Drone control keys
    if kc.getKey("q"): # check if 'q' key is pressed
        drone.land() # land the drone

    if kc.getKey("e"): # check if 'e' key is pressed
        drone.takeoff() # takeoff the drone

    # return the control commands
    return [lr, fb, ud, yv]



while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])


    # Accessing the drones cam(Frame)
    img = drone.get_frame_read().frame

    # Resizing the frame
    img = cv.resize(img, (640, 640))

    # Applying YOLO to drone stream
    img = model(img, stream=True)

    detections = np.empty((0, 5))

    # Working on the model result
    for i in img:
        boxes = i.boxes
        for box in boxes:
            # Bounding boxes
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Confidence
            conf = math.floor(box.conf[0] * 100) / 100

            # Classnames
            cls = int(box.cls[0])
            objectNames = classNames[cls]

            # Selecting the type of objects we want to detect
            if objectNames == 'person' and conf >= 0.3:
                currentDetection = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentDetection))

                cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), thickness=2)
                cv.putText(img, f'{conf}', (x1, y1), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), thickness=2)

    # Displaying the frames
    cv.imshow("img", img)
    cv.waitkey(1)
