# see the image in the diferrent window using python script
import cv2

img = cv2.imread('/Users/neemiasbsilva/Downloads/Computer-Vision-with-Python/DATA/00-puppy.jpg')

while True:
    cv2.imshow('Puppy', img)
    
    # IF we've waited at Least 1 ms AND we've pressed the Esc
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.waitKey()

cv2.destroyAllWindows()
    