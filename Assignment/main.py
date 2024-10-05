import cv2

cap = cv2.VideoCapture(0)  # ID: 0 | Webcam ID

# Set HD resolution for 1280 x 720
cap.set(3, 1280)
cap.set(4, 720)

while True:
    success, img = cap.read()
    cv2.imshow("Image", img)
    cv2.waitKey(1)

