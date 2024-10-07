from cvzone.HandTrackingModule import HandDetector
import numpy as np


class HandTracking:
    def __init__(self, max_hands: int = 4, detection_confidence: float = 0.8) -> None:
        self.detector = HandDetector(staticMode=False, maxHands=max_hands, detectionCon=detection_confidence)

    def detect_hands(self, frame: any) -> tuple[list, np.ndarray]:
        hands, frame = self.detector.findHands(frame, flipType=False)
        return hands, frame
