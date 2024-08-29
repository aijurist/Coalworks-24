import uuid
import cv2
import os

TRUE_PATH=os.path.join('images','true_images')
FALSE_PATH=os.path.join('images','false_images')
INPUT_PATH=os.path.join('images','input_images')

capture=cv2.VideoCapture(0)
while capture.isOpened():
    ret, frame = capture.read()
    frame=cv2.resize(frame, (500,500))
    
    if cv2.waitKey(1) & 0xFF== ord('i'):
        print('Capturing image, ready for click')
        path=os.path.join(INPUT_PATH, f"{uuid.uuid1()}.jpg")
        cv2.imwrite(path, frame)
        print('clicked image')
    
    if cv2.waitKey(1) & 0xFF== ord('t'):
        print("ready for click t!")
        path = os.path.join(TRUE_PATH,f"{uuid.uuid1()}.jpg")
        cv2.imwrite(path,frame)
        print('clicked t')

    cv2.imshow('Image Collection', frame)

    if cv2.waitKey(1) & 0XFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()