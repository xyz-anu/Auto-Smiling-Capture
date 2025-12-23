import cv2
import mediapipe as mp
import pyautogui
import os
x1 = 0
y1 = 0
x2 = 0
y2 = 0
os.system("afplay /System/Library/Sounds/Glass.aiff")
# face_mesh = mp.solutions.face_mesh.FaceMesh(refine_face_landmarks=True) #this function will help to detect face mesh
face_mesh = mp.solutions.face_mesh.FaceMesh()
camera = cv2.VideoCapture(0) #0 is the default camera when you have only 1 camera
while True:
    _ , image =camera.read() #this image is in brg format (blue, red, green)
    fh, fw, _ = image.shape
    image = cv2.flip(image,1) #to flip the image horizontally
    #we have to convert it into rgb format(red, green, blue)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_image)
    landmark_points = output.multi_face_landmarks
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks):
            x = int(landmark.x * fw)
            y = int(landmark.y * fh)
            if id == 43:
                x1 = x
                y1 = y
            if id == 287:
                x2 = x
                y2 = y
        dist = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
        print(dist)
        if dist > 140:
            print("smile detected")
            cv2.imwrite("smile.png",image)
            os.system("afplay /System/Library/Sounds/Glass.aiff")
            cv2.waitKey(10000)
    cv2.imshow("Smile Detector",image)
    key = cv2.waitKey(100)
    if key == 27: #27 is the ASCII code for the ESCAPE key
        break
camera.release()
cv2.destroyAllWindows()
