from cvzone.HandTrackingModule import HandDetector
import HandTracking
import numpy as np
import ctypes
import time
import cv2


class VirtualMouse:
    def __init__(self) -> None:
        self.present_time = 0
        self.CAMERA_WIDTH = 640
        self.CAMERA_HEIGHT = 480
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAMERA_HEIGHT)
        self.detector = HandDetector(staticMode=False, modelComplexity=0, maxHands=2, detectionCon=0.8, minTrackCon=0.5)
        self.screen_width = 1920
        self.screen_height = 1080
        self.frame_reduction = 100

    # TODO: Get the fingers [predefined gesture]
    # TODO: Check the gesture
    # TODO: Moving mode
    # TODO: Convert coordinates
    # TODO: Smoothen values
    # TODO: Move mouse
    # TODO: Clicking mode [predefined gesture]
    # TODO: Find distance [for gesture checking]
    # TODO: Click mouse

if __name__ == '__main__':
    app = VirtualMouse()
    app.run()
