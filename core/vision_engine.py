import mediapipe as mp
import numpy as np
import pyautogui
import cv2
import time
import threading
from helpersFunction.eye_ratio_func import eye_ratio, LEFT_EYE, RIGHT_EYE
from helpersFunction.mouth_ratio_func import mouth_ratio

class VisionEngine:
    def __init__(self):
        # --- SİSTEM DEĞİŞKENLERİ ---
        self.is_running = False
        self.show_camera = False 
        self.is_paused = False
        self.first_face_detected = False
        
        # Ekran ve Kamera
        self.screen_w, self.screen_h = pyautogui.size()
        self.cap = cv2.VideoCapture(0)
        self.cam_w = 640
        self.cam_h = 480
        self.cap.set(3, self.cam_w)
        self.cap.set(4, self.cam_h)

        # Mediapipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # --- SENİN DEĞİŞKENLERİN (nose_follow.py'den alındı) ---
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
        
        # Tıklama Sayaçları
        self.left_click = 0
        self.right_click = 0
        self.left_right_click = 0
        self.trig_left = False
        self.trig_right = False
        self.eyes_closed = False
        self.timer_start = 0
        self.timer_limit = 5.0 # Senin kodundaki limit
        self.double_clicked = False

        # --- KALİBRASYON / ROI ---
        self.roi_center_x = 320
        self.roi_center_y = 240 
        self.roi_w = 50
        self.roi_h = 50 
        self.update_roi()

        self.resume_timer = 0
        self.DWELL_TIME = 1.5

    def update_roi(self):
        #ROI Sınırlarını merkeze göre günceller.
        self.roi_x1 = self.roi_center_x - (self.roi_w // 2)
        self.roi_x2 = self.roi_center_x + (self.roi_w // 2)
        self.roi_y1 = self.roi_center_y - (self.roi_h // 2)
        self.roi_y2 = self.roi_center_y + (self.roi_h // 2)

    def calibrate(self):
        #--YENİ MERKEZ--

        if hasattr(self, 'current_nose'):
            self.roi_center_x, self.roi_center_y = self.current_nose
            self.update_roi()
            print(f"Kalibre Edildi! Yeni Merkez: {self.roi_center_x}, {self.roi_center_y}")

    def start_thread(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self._run_loop, daemon=True).start()

    def stop_thread(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()

    def _run_loop(self):
        """Ana Döngü - Senin Kodun Burada Çalışıyor"""
        while self.is_running and self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                continue

            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(image_rgb)

            if not self.is_paused:
                cv2.rectangle(image, (self.roi_x1, self.roi_y1), (self.roi_x2, self.roi_y2), (255, 0, 0), 2)

            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                
                nose = landmarks[4]
                nose_x = int(nose.x * self.cam_w)
                nose_y = int(nose.y * self.cam_h)
                self.current_nose = (nose_x, nose_y)

                ratio_left = eye_ratio(landmarks, LEFT_EYE)
                ratio_right = eye_ratio(landmarks, RIGHT_EYE)
                ratio_mouth = mouth_ratio(landmarks)

                if not self.first_face_detected:
                    self.calibrate()
                    self.first_face_detected = True
                    print("Sistem oto. kalibre edildi.")

                # --- PAUSE MODU ---
                if self.is_paused:
                    self._handle_pause_logic(image, ratio_left, ratio_right)
                
                # --- AKTİF MOD ---
                else:
                    self._process_active_mode(landmarks, nose, nose_x, nose_y, ratio_right,ratio_left, ratio_mouth)

            # --- DEBUG PENCERESİ ---
            if self.show_camera:
                cv2.imshow("MediaPipe Test", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    pass
            else:
                try:
                    cv2.destroyWindow("MediaPipe Test")
                except:
                    pass

    def _handle_pause_logic(self, image, ratio_left, ratio_right):
        if ratio_left < 0.25 and ratio_right < 0.25:
            
            if self.resume_timer == 0:
                self.resume_timer = time.time()
            
            elapsed = time.time() - self.resume_timer
            
            bar_width = int((elapsed / 3.0) * 300) 
            cv2.rectangle(image, (170, 300), (170 + bar_width, 340), (0, 255, 0), -1)
            cv2.rectangle(image, (170, 300), (470, 340), (255, 255, 255), 2)
            
            if elapsed > 3.0: 
                self.is_paused = False      # KİLİDİ AÇ
                self.show_camera = False    # KAMERAYI KAPAT
                self.resume_timer = 0       # SAYACI SIFIRLA
                print("Sistem Göz Hareketiyle Açıldı!")
        
        else:
            self.resume_timer = 0

    def _process_active_mode(self, landmarks, nose, nose_x, nose_y, ratio_left, ratio_right, ratio_mouth):

        # --- SCROLL MANTIĞI ---
        if ratio_mouth > 0.5:
            nose_y_pix = int(nose.y * self.cam_h)
            if nose_y_pix < 200:
                pyautogui.scroll(25)
            elif nose_y_pix > 280:
                pyautogui.scroll(-25)
        
        # --- MOUSE HAREKET MANTIĞI ---
        else:
            # MAPPING (Dinamik ROI sınırlarına göre interpolasyon)
            target_x = np.interp(nose_x, (self.roi_x1, self.roi_x2), (0, self.screen_w))
            target_y = np.interp(nose_y, (self.roi_y1, self.roi_y2), (0, self.screen_h))

            # MESAFE ÖLÇME & YUMUŞATMA
            distance = ((target_x - self.prev_x)**2 + (target_y - self.prev_y)**2)**0.5
            val = 130 / (1 + (distance * 0.1))
            dynamic_smooth = max(3, min(val, 130))

            # Jitter ÇÖZÜMÜ
            is_Clicking = ratio_left < 0.23 or ratio_right < 0.23

            if not is_Clicking:
                self.curr_x = self.prev_x + (target_x - self.prev_x) / dynamic_smooth
                self.curr_y = self.prev_y + (target_y - self.prev_y) / dynamic_smooth

                try:
                    pyautogui.moveTo(self.curr_x, self.curr_y)
                except:
                    pass

                self.prev_x, self.prev_y = self.curr_x, self.curr_y

            # --- TIKLAMA İŞLEMLERİ ---
            
            # SOL TIK
            if ratio_left < 0.19 and ratio_right > 0.20:
                self.left_click += 1
                if self.left_click == 3 and self.trig_left is False:
                    pyautogui.rightClick()
                    self.trig_left = True
            elif ratio_left > 0.20:
                self.left_click = 0
                self.trig_left = False

            # SAĞ TIK
            if ratio_right < 0.18 and ratio_left > 0.20:
                self.right_click += 1
                if self.right_click == 3 and self.trig_right is False:
                    pyautogui.leftClick()
                    self.trig_right = True
            elif ratio_right > 0.22:
                self.right_click = 0
                self.trig_right = False

            # ÇİFT TIK
            if ratio_left < 0.18 and ratio_right < 0.18:
                    self.left_right_click += 1
                    if self.left_right_click == 3:
                        pyautogui.doubleClick()
                        self.double_clicked = True
  
            else:
                self.double_clicked = False
                self.left_right_click = 0