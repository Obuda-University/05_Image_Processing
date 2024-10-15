from Assignment.HandTracking import HandTracking
import numpy as np
import time
import cv2


class VirtualMouse:
    def __init__(self, tracker: HandTracking) -> None:
        self.tracker = tracker

    # TODO: Get the fingers [predefined gesture]
    # TODO: Check the gesture
    # TODO: Moving mode
    # TODO: Convert coordinates
    # TODO: Smoothen values
    # TODO: Move mouse
    # TODO: Clicking mode [predefined gesture]
    # TODO: Find distance [for gesture checking]
    # TODO: Click mouse
