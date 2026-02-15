# 📄 VisionMouse - Faz 2 Ürün Gereksinim Dokümanı (PRD)

| **Proje Adı** | VisionMouse (Yüz ve Mimik Tabanlı Engelsiz Erişim) |
| :--- | :--- |
| **Versiyon** | 2.0 (Release Candidate for Jury) |
| **Tarih** | 15.02.2026 |
| **Durum** | Geliştirme (Faz-2 UI/UX Entegrasyonu) |
| **Hazırlayan** | İsmail Apan & AI Mentor |

---

## 1. Giriş ve Amaç
Bu fazın temel amacı, çalışan "Çekirdek Algoritmayı" (Core Engine), son kullanıcının (özellikle motor fonksiyon kaybı yaşayan bireylerin) yardım almadan yönetebileceği, hataya toleranslı ve modern bir masaüstü ürününe dönüştürmektir.

**Temel Hedef:** Projeyi bir "Python Betiği" görünümünden çıkarıp, **"Ticarileşmeye Hazır Ürün"** algısına taşımak ve sürdürülebilir bir kullanıcı deneyimi sunmaktır.

---

## 2. Kullanıcı Arayüzü (UI) Tasarımı

Arayüz, kullanıcının ana ekranını işgal etmeyen, **"Yüzen Araç Çubuğu" (Floating Toolbar)** mimarisinde tasarlanacaktır.

### 2.1. Tasarım Dili (Style Guide)
* **Tema:** Koyu Mod (Dark Mode) - Göz yorgunluğunu minimize etmek için.
* **Renk Paleti:**
    * Arka Plan: `#2C3E50` (Midnight Blue)
    * Yazı Tipi: Segoe UI veya Roboto (Okunabilir, sans-serif)
    * Vurgu Renkleri: 
        * 🔴 Hata/Kapalı: `#E74C3C`
        * 🟢 Aktif: `#2ECC71`
        * 🟡 Bekleme/Pause: `#F1C40F`
* **Pencere Davranışı:** `Always On Top` (Her zaman en üstte) ve `Frameless` (Çerçevesiz/Modern).

### 2.2. Arayüz Bileşenleri (Widget'lar)
Panel, yukarıdan aşağıya şu fonksiyonel butonları içerecektir:

1.  **Sürükleme Alanı (Drag Handle):** Panelin taşınmasını sağlar.
2.  **Durum LED'i (Status Indicator):** Sistemin o anki durumunu (Yüz Takibi, Pause, Hata) renklerle bildirir.
3.  **Aksiyon Butonları:**
    * `[ ⌨ KLAVYE ]`: Windows Sanal Klavyesini (`osk.exe`) açar/kapatır.
    * `[ 🎯 KALİBRE ET ]`: Otomatik merkezleme (Auto-Centering) işlemini başlatır.
    * `[ ⏸ DURAKLAT ]`: Sistemi kilitler ve "Sanal İğne" modunu aktif eder.
4.  **Hassasiyet Ayarı (Slider):** Kullanıcının kafa hareketi ile imleç hızı arasındaki çarpanı (`0.1` - `1.0`) anlık olarak değiştirir.
5.  **Kamera Önizleme (Gizli Mod):** Varsayılan olarak kapalıdır. Sadece kalibrasyon sırasında açılır.

---

## 3. Fonksiyonel Gereksinimler (Sistem Mantığı)

### 3.1. Dinamik Kalibrasyon (Auto-Centering)
**Sorun:** Sabit kodlanmış koordinatlar (`295-345`), farklı ekran ve oturma pozisyonlarında çalışmamaktadır.
**Çözüm Akışı:**
1.  Kullanıcı **"Kalibre Et"** butonuna basar.
2.  Ekranda kamera önizlemesi açılır, 3 saniyelik geri sayım başlar.
3.  Süre dolduğunda o anki `nose_x` ve `nose_y` değerleri `CENTER` noktası olarak kaydedilir.
4.  Algoritma sınırları (ROI) bu merkeze göre (+/- 60px) yeniden hesaplanır.

### 3.2. Durdurma ve Devam Ettirme (Sanal İğne Yöntemi)
**Sorun:** Kullanıcı sistemi durdurduğunda mouse donar, bu yüzden "Başlat" butonuna tıklayamaz.
**Çözüm:**
* **Durdurma (Pause):** Panelden **[DURAKLAT]** butonuna tıklanır. `pyautogui` devre dışı kalır. Ekrana yarı saydam bir "Kilit Ekranı" ve ortada kırmızı bir **"BAŞLAT"** hedefi iner.
* **Devam Ettirme (Resume):** Kullanıcı başını hareket ettirerek burnunu sanal "BAŞLAT" hedefinin üzerine getirir (Hover). Hedef yeşile döner ve dolmaya başlar (Progress Bar). **1.5 saniye** hedefte kalınırsa kilit açılır.

### 3.3. Görsel Geri Bildirim (HUD)
Kullanıcıya eylem öncesi geri bildirim verilmelidir:
* **Tıklama Hazırlığı:** Gözler kısılmaya başladığında (Threshold altı) arayüzde sarı uyarı veya imleç etrafında görsel belirteç.
* **Scroll Modu:** Ağız açıldığında ekranda "SCROLL MODU" bildirimi.

---

## 4. Teknik Mimari

Proje, arayüzün donmaması için **Multi-Threading** yapısına geçirilmelidir.

### 4.1. İş Parçacığı Yapısı
1.  **Main Thread (UI):** `tkinter.mainloop()` döngüsünü çalıştırır.
2.  **Worker Thread (Vision Core):** `cv2` ve `mediapipe` işlemlerini yapar. UI thread'i ile değişkenler üzerinden haberleşir.

### 4.2. Dosya Yapısı (Önerilen)
```text
VisionMouse/
├── main.py             # Başlatıcı (Thread yönetimini yapar)
├── ui_panel.py         # Tkinter Arayüz Sınıfı
├── vision_core.py      # Görüntü İşleme ve Mouse Kontrol Sınıfı
├── utils/
│   ├── one_euro.py     # Filtre Algoritması
│   └── helpers.py      # Matematiksel Hesaplamalar
└── assets/             # İkonlar ve Görseller