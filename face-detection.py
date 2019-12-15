# Face Recognition

# Import the libraries
import cv2

# Loading the cascades one for the eyes and
# one for the face
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Defining a function that will do the detections
def detect(gray, frame):
    # get the coordinates
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    
    # iteract for all the faces
    for (x, y, w, h) in faces:
        # draw to rectangle w is the width
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
        # region of interest
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eyeCascade.detectMultiScale(roi_gray, 1.7, 3)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
    return frame

