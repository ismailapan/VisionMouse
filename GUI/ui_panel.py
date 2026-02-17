import customtkinter as ctk
import tkinter as tk

# --- AYARLAR ---
ctk.set_appearance_mode("Dark")  # Koyu Mod
ctk.set_default_color_theme("blue")  # Tema Rengi

class VisionMouseUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. PENCERE AYARLARI (Modern ve Çerçevesiz)
        self.title("VisionMouse")
        
        # Ekran boyutlarını al
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Panel Boyutları
        panel_width = 70
        panel_height = 350
        
        # Konum: Ekranın SAĞ ORTASINA yasla
        x_pos = screen_width - panel_width - 10 # Sağdan 10px boşluk
        y_pos = (screen_height // 2) - (panel_height // 2)

        self.geometry(f"{panel_width}x{panel_height}+{x_pos}+{y_pos}")
        
        # Pencere Özellikleri
        self.overrideredirect(True) # Windows çerçevesini (çarpı, büyütme tuşu) kaldır
        self.attributes('-topmost', True) # Her zaman en üstte tut
        self.attributes('-alpha', 0.90)   # %10 Şeffaflık (Modern görünüm)
        self.configure(fg_color="#1a1a1a") # Arka plan rengi (Çok koyu gri)
        
        # Köşeleri yuvarlatmak için hile (Windows 11 destekler)
        try:
            from ctypes import windll, byref, sizeof, c_int
            dwmapi = windll.dwmapi
            DWMWA_WINDOW_CORNER_PREFERENCE = 33
            dwmapi.DwmSetWindowAttribute(windll.user32.GetParent(self.winfo_id()), 
                                         DWMWA_WINDOW_CORNER_PREFERENCE, 
                                         byref(c_int(2)), sizeof(c_int(2)))
        except:
            pass # Windows 10 veya altıysa sorun etme

        # --- ARAYÜZ ELEMANLARI (WIDGETS) ---
        self.setup_ui()

        # Pencereyi sürükleyebilmek için değişkenler
        self._drag_data = {"x": 0, "y": 0}

    def setup_ui(self):
        # 1. SÜRÜKLEME ALANI (Grip Handle)
        # Panelin en tepesindeki tutma yeri
        self.grip_frame = ctk.CTkFrame(self, height=30, fg_color="#2b2b2b", corner_radius=0)
        self.grip_frame.pack(fill="x", side="top")
        
        self.lbl_grip = ctk.CTkLabel(self.grip_frame, text="::: VM :::", font=("Arial", 10, "bold"), text_color="gray")
        self.lbl_grip.pack(pady=5)
        
        # Sürükleme olaylarını bağla
        self.grip_frame.bind("<Button-1>", self.start_move)
        self.grip_frame.bind("<B1-Motion>", self.do_move)
        self.lbl_grip.bind("<Button-1>", self.start_move)
        self.lbl_grip.bind("<B1-Motion>", self.do_move)

        # 2. DURUM LEDİ (Status)
        # Canvas ile yuvarlak çiziyoruz
        self.status_canvas = tk.Canvas(self, width=20, height=20, bg="#1a1a1a", highlightthickness=0)
        self.status_canvas.pack(pady=(15, 10))
        # Başlangıçta Kırmızı (Pasif)
        self.led = self.status_canvas.create_oval(2, 2, 18, 18, fill="#38c33c", outline="") 

        # 3. BUTONLAR GRUBU
        # Klavye Butonu
        self.btn_keyboard = ctk.CTkButton(self, text="⌨", width=40, height=40, 
                                          corner_radius=10, fg_color="#2980b9", hover_color="#3498db",
                                          font=("Arial", 20), command=self.toggle_keyboard)
        self.btn_keyboard.pack(pady=10)
        
        # Kalibrasyon Butonu
        self.btn_calibrate = ctk.CTkButton(self, text="🎯", width=40, height=40,
                                           corner_radius=10, fg_color="#27ae60", hover_color="#2ecc71",
                                           font=("Arial", 20), command=self.start_calibration)
        self.btn_calibrate.pack(pady=10)

        # Duraklat Butonu
        self.btn_pause = ctk.CTkButton(self, text="⏸", width=40, height=40,
                                       corner_radius=10, fg_color="#f39c12", hover_color="#f1c40f",
                                       font=("Arial", 20), command=self.toggle_pause)
        self.btn_pause.pack(pady=10)
        
        # 4. ÇIKIŞ BUTONU (En altta)
        self.btn_exit = ctk.CTkButton(self, text="✖", width=40, height=30,
                                      corner_radius=10, fg_color="#c0392b", hover_color="#e74c3c",
                                      font=("Arial", 14), command=self.close_app)
        self.btn_exit.pack(side="bottom", pady=20)

    # --- FONKSİYONLAR (Şimdilik Boş - Sonra Dolduracağız) ---
    def start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_move(self, event):
        deltax = event.x - self._drag_data["x"]
        deltay = event.y - self._drag_data["y"]
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    def toggle_keyboard(self):
        print("Klavye aç/kapa tıklandı")
        # Buraya osk.exe kodu gelecek

    def start_calibration(self):
        print("Kalibrasyon tıklandı")
        # Buraya kalibrasyon kodu gelecek

    def toggle_pause(self):
        print("Pause tıklandı")
        # Buraya pause kodu gelecek

    def close_app(self):
        self.destroy()
        # Buraya programı kapatma kodu gelecek

# --- TEST KODU ---
if __name__ == "__main__":
    app = VisionMouseUI()
    app.mainloop()