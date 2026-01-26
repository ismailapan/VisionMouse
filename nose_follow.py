import mediapipe as mp
import numpy as np
import pyautogui
import cv2
from eye_ratio_func import eye_ratio, LEFT_EYE, RIGHT_EYE
from mouth_ratio_func import mouth_ratio

cam_w = 640
cam_h = 480
screen_w, screen_h = pyautogui.size()
left_click = 0
right_click = 0
left_right_click = 0
trig_left = False
trig_right = False
trig_double = False
#cons_smooth = 20

prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces = 1,
    refine_landmarks = True,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.rectangle(image, (280,200), (370,290), (255,0,0), 2)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        nose = landmarks[4]
        ratio_left = eye_ratio(landmarks, LEFT_EYE)
        ratio_right = eye_ratio(landmarks, RIGHT_EYE)
        ratio_mouth = mouth_ratio(landmarks)

        if ratio_mouth > 0.5:
            nose_y_pix = int(nose.y * cam_h)

            if nose_y_pix < 200:
                pyautogui.scroll(25)
            elif nose_y_pix > 280:
                pyautogui.scroll(-25)
        
        else:
            nose_x = int(nose.x * cam_w)
            nose_y = int(nose.y * cam_h)

            #MAPPING
            target_x = np.interp(nose_x, (280,360), (0,screen_w))
            target_y = np.interp(nose_y, (200,280), (0,screen_h))

            #MESAFE ÖLÇME
            distance = ((target_x - prev_x)**2 + (target_y - prev_y)**2)**0.5
            if distance > 100:
                current_smooth = 2
            elif distance > 20:
                current_smooth = 5
            elif distance > 10:
                current_smooth = 10
            elif distance > 5:
                current_smooth = 15
            elif distance > 3:
                current_smooth = 20
            else:
                current_smooth = 40

            #Yumuşatma işlemi
            curr_x = prev_x + (target_x - prev_x) / current_smooth
            curr_y = prev_y + (target_y - prev_y) / current_smooth

            try:
                pyautogui.moveTo(curr_x, curr_y)
            except:
                pass

            prev_x, prev_y = curr_x, curr_y

            #Sol göz işlemleri
            if ratio_left < 0.19 and ratio_right > 0.20:
                left_click +=1

                if left_click == 3 and trig_left is False:
                    pyautogui.leftClick()
                    trig_left = True
            elif ratio_left > 0.20:
                left_click = 0
                trig_left = False

            #Sağ göz işlemleri
            if ratio_right < 0.18 and ratio_left > 0.20:
                right_click +=1

                if right_click == 3 and trig_right is False:
                    pyautogui.rightClick()
                    trig_right = True
            
            elif ratio_right > 0.22:
                right_click = 0
                trig_right = False

            #Sağ-Sol göz işlemleri
            if ratio_left < 0.18 and ratio_right < 0.18:
                left_right_click += 1

                if left_right_click == 3:
                    pyautogui.doubleClick()
                    trig_double = True
            
            else:
                left_right_click = 0
                trig_double = False
        
        #print(f"Sol Göz: {ratio_left:.2f} -- Sağ Göz: {ratio_right:.2f}")
        cv2.circle(image, (nose_x, nose_y), 5, (0,255,0), -1)

    cv2.imshow("MediaPipe Test", image)
    if cv2.waitKey(5) & 0xFF == ord("q"):
        break