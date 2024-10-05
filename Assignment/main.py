from cvzone.HandTrackingModule import HandDetector
import cv2


cap = cv2.VideoCapture(0)  # ID: 0 | Webcam ID

# Set HD resolution for 1280 x 720
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(staticMode=False, maxHands=4, detectionCon=0.8)  # To be more accurate

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)  # hands: List of Hand Landmarks

    if hands:
        hand = hands[0]

        landmark_list = hand["lmList"]
        bounding_box_info = hand["bbox"]

    cv2.imshow("Image", img)
    cv2.waitKey(1)

