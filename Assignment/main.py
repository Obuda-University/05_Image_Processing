from cvzone.HandTrackingModule import HandDetector
from Keyboard import KeyBoard
import cv2


cap = cv2.VideoCapture(0)  # ID: 0 | Webcam ID

# Set HD resolution for 1280 x 720
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(staticMode=False, maxHands=4, detectionCon=0.8)  # To be more accurate

list_of_keys: list[list[str]] = [['Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P'],
                                 ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',],
                                 ['Y', 'X', 'C', 'V', 'B', 'N', 'M', ',',],
                                 ['space']]

keyboard = KeyBoard(list_of_keys)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)  # hands: List of Hand Landmarks

    img = keyboard.draw_keyboard(img)

    if hands:
        hand = hands[0]

        landmark_list = hand["lmList"]

        x_finger, y_finger = landmark_list[8][:2]
        pressed_key = keyboard.check_pressed_key(x_finger, y_finger)
        if pressed_key:
            print(f"Key pressed: {pressed_key}")

        bounding_box_info = hand["bbox"]

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
