# 👁️ VisionMouse: Yapay Zeka Destekli Engelsiz Erişim Arayüzü

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face%20Mesh-0099CC?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **"Teknoloji Engel Tanımaz: Bilgisayarınızı Gözlerinizle Yönetin."**

## 📖 Proje Hakkında

**VisionMouse**, fiziksel engelleri (ALS, MS, Felç, Ampütasyon vb.) nedeniyle standart fare ve klavye kullanamayan bireyler için geliştirilmiş, **yapay zeka destekli** ve **donanım bağımsız** bir erişilebilirlik çözümüdür.

Piyasadaki binlerce dolarlık göz takip cihazlarının aksine, VisionMouse her dizüstü bilgisayarda bulunan standart bir web kamerasını kullanarak, **0 maliyetle** yüksek hassasiyetli bir bilgisayar kontrolü sağlar. Gelişmiş **Multi-Thread (Çoklu İş Parçacığı)** mimarisi ve modern kullanıcı arayüzü ile donma yaşamadan akıcı bir deneyim sunar.

---

## 🎯 Projenin Amacı ve Sosyal Etki

Bu proje, teknolojinin herkes için eşit ve erişilebilir olması gerektiği inancıyla geliştirilmiştir.

* **Erişilebilirlik:** Ellerini kullanamayan bireylerin bilgisayar dünyasına tam katılımını sağlamak.
* **Bağımsızlık:** Başkasına ihtiyaç duymadan web'de gezinme, okuma ve iletişim kurma özgürlüğü sunmak.
* **Maliyet Avantajı:** Pahalı donanımlar yerine, halihazırda var olan kamera donanımını yapay zeka ile güçlendirerek ekonomik bir çözüm üretmek.


## 🚀 Temel Özellikler (v2.0)

### 🖱️ Hareket ve Kontrol
* **Hassas Burun Takibi:** Kafanızı çevirdiğiniz yöne mouse imleci milimetrik hassasiyetle hareket eder.
* **Adaptif Yumuşatma (Smart Smoothing):** İmleç titremesini (jitter) önleyen, hareket hızına göre dinamik tepki veren özel algoritma.
* **Göz ile Tıklama:**
    * **Sol Tık:** Sol göz kırpma.
    * **Sağ Tık:** Sağ göz kırpma.
    * **Çift Tık:** İki gözü hızlıca kırpma.
* **Hands-Free Scroll:** Ağzınızı hafifçe açarak ("O" harfi) sayfayı aşağı/yukarı kaydırma özelliği.

### 🖥️ Modern Arayüz ve Kullanıcı Deneyimi
* **Yüzen Kontrol Paneli (Floating Widget):** Ekranı kaplamayan, her zaman en üstte duran modern (CustomTkinter) kontrol çubuğu.
* **Otomatik Kalibrasyon:** Program açılışında kullanıcının duruşuna göre kendini otomatik olarak merkeze odaklar.
* **Sanal Klavye Entegrasyonu:** Tek tıkla Windows Ekran Klavyesi'ne erişim sağlar.
* **Akıllı Duraklatma (Smart Pause):** Kullanıcı yorulduğunda sistemi arayüzden tek tıkla duraklatabilir.
* **Temassız Başlatma (Hands-Free Resume):** **[Özgün Özellik]** Duraklatılan sistemi tekrar açmak için fiziksel bir etkileşime gerek yoktur. Kullanıcının **gözlerini 3 saniye kapalı tutması**, sistemi tekrar aktif etmek için yeterlidir.

## 🧰 Kullanılan Teknolojiler

Proje, yüksek performans ve düşük gecikme (low-latency) için optimize edilmiştir.

* **Dil:** Python 3.10+
* **Görüntü İşleme:** OpenCV, Google MediaPipe (Face Mesh - 468 Landmark)
* **Arayüz (GUI):** CustomTkinter (Modern UI Framework)
* **Otomasyon:** PyAutoGUI (İmleç Kontrolü)
* **Sistem:** Threading (Eşzamanlı İşleme), Subprocess
---

## 🏗️ Proje Mimarisi

VisionMouse, spagetti kod yapısından uzak, modüler ve ölçeklenebilir bir **Clean Architecture** (Temiz Mimari) yapısına sahiptir.

```text
VisionMouse/
├── core/                   # Sistemin Beyni (Görüntü İşleme Motoru)
│   └── vision_engine.py    # Multi-threaded Vision Class (Thread-Safe)
├── ui/                     # Kullanıcı Arayüzü (GUI)
│   └── ui_panel.py         # CustomTkinter Modern Panel
├── helpersFunction/        # Yardımcı Matematiksel Modüller
│   ├── eye_ratio_func.py   # EAR (Eye Aspect Ratio) Hesaplamaları
│   └── mouth_ratio_func.py # MAR (Mouth Aspect Ratio) Hesaplamaları
├── main.py                 # Uygulama Başlatıcı (Entry Point)
├── config.py               # Sistem Ayarları
└── requirements.txt        # Bağımlılıklar
