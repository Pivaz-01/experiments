import threading

import cv2
from deepface import DeepFace 

class opt_matches:
    NONE = 0
    NO_EG = 1
    EG = 2

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_match = opt_matches.NONE

def detect_face(img):
    global face_match
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    try:
        if DeepFace.verify(frame, reference_img2.copy())['verified']: # copy to have no problems 
            face_match = opt_matches.EG
        elif DeepFace.verify(frame, reference_img.copy())['verified']: # copy to have no problems 
            face_match = opt_matches.NO_EG
        else: 
            face_match = opt_matches.NONE

    except ValueError:
        face_match = opt_matches.NONE

    if faces is ():
        return img
    
    for(x,y,w,h) in faces: 
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img

reference_img = cv2.imread("img.jpg")
reference_img2 = cv2.imread("img2.jpg")

cap = cv2.VideoCapture(0)
print(cap.isOpened())

counter = 0

while True:
    ret, frame = cap.read()
    frame = detect_face(frame)

    if ret:
        if counter % 1000 == 0:
            try: 
                threading.Thread(target=detect_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        if face_match == opt_matches.EG:
            cv2.putText(frame, "PIVAZ, WITH EYEGLASSES!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) 
        elif face_match == opt_matches.NO_EG:
            cv2.putText(frame, "PIVAZ, NO EYEGLASSES!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) 
        else: 
            cv2.putText(frame, "NOT PIVAZ!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow('Video Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()