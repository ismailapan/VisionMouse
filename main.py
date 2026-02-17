import customtkinter as ctk
from GUI.ui_panel import VisionMouseUI
from core.vision_engine import VisionEngine
import os
import sys
import subprocess


# Windows DPI Ayarı
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def main():
    engine = VisionEngine()
    
    app = VisionMouseUI()

    
    def start_system():
        """Sistemi başlatır"""
        engine.start_thread()

    def on_pause():
        """Duraklat / Devam Et"""
        engine.is_paused = not engine.is_paused
        
        # Buton Görünümleri
        if engine.is_paused:
            engine.show_camera = True
            app.btn_pause.configure(text="▶", fg_color="#e67e22") # Turuncu
            app.status_canvas.itemconfig(app.led, fill="#f1c40f") # Sarı LED
        else:
            engine.show_camera = False
            app.btn_pause.configure(text="⏸", fg_color="#f39c12") # Normal
            app.status_canvas.itemconfig(app.led, fill="#2ecc71") # Yeşil LED

    def on_calibrate():
        """Kalibrasyon İşlemi"""
        engine.show_camera = True # Kamerayı aç
        app.status_canvas.itemconfig(app.led, fill="#3498db") # Mavi LED
        
        # 3 Saniye sonra kalibre et
        app.after(3000, perform_calibration)

    def perform_calibration():
        engine.calibrate()
        engine.show_camera = False # Kamerayı gizle
        app.status_canvas.itemconfig(app.led, fill="#2ecc71") # Yeşil LED
        print("Kalibrasyon Tamamlandı.")

    def on_keyboard():
        try:
            # 64-bit sistemlerde Sysnative klasörü üzerinden çağırmak gerekir
            osk_path = r"C:/Windows/Sysnative/osk.exe"
            if not os.path.exists(osk_path):
                osk_path = r"C:\Windows\WinSxS\amd64_microsoft-windows-osk_31bf3856ad364e35_10.0.26100.7824_none_465523d50a146704\osk.exe"
            
            subprocess.Popen(osk_path)
            print("Klavye Açıldı")
        except Exception as e:
            print(f"Klavye Hatası: {e}")

    def on_exit():
        engine.stop_thread()
        app.destroy()
        sys.exit()

    app.btn_pause.configure(command=on_pause)
    app.btn_calibrate.configure(command=on_calibrate)
    app.btn_keyboard.configure(command=on_keyboard)
    app.btn_exit.configure(command=on_exit)

    # 4. BAŞLAT
    start_system() 
    app.mainloop() 

if __name__ == "__main__":
    main()