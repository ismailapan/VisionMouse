# 👁️ VisionMouse: Yüz ve Mimik Tabanlı Engelsiz Erişim Arayüzü

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Prototype-orange)

> **"Teknoloji Engel Tanımaz: Gözlerinizle Dünyayı Yönetin."**

## 📖 Proje Hakkında

**VisionMouse**, fiziksel engelleri (ALS, MS, Felç, Ampütasyon vb.) nedeniyle standart fare ve klavye kullanamayan bireyler için geliştirilmiş, **yapay zeka destekli** ve **donanım bağımsız** bir erişilebilirlik projesidir.

Piyasadaki pahalı göz takip cihazlarının aksine, VisionMouse her dizüstü bilgisayarda bulunan standart bir web kamerasını kullanarak, **0 maliyetle** yüksek hassasiyetli bir bilgisayar kontrolü sağlar. Google MediaPipe teknolojisi ve özgün **Adaptif Yumuşatma Algoritması** sayesinde titremesiz ve akıcı bir deneyim sunar.

---

## 🚀 Temel Özellikler

* **👃 Burun ile Navigasyon:** Kafanızı çevirdiğiniz yöne mouse imleci hareket eder.
* **🎯 Adaptif Yumuşatma (Adaptive Smoothing):** İmleç titremesini (jitter) önleyen ve hıza göre hassasiyeti ayarlayan akıllı algoritma.
* **😉 Göz ile Tıklama:**
    * **Sol Göz Kırpma:** Sol Tık
    * **Sağ Göz Kırpma:** Sağ Tık
    * **İki Gözü Kısma:** Çift Tık (Double Click)
* **📜 Hands-Free Scroll Modu:** Ağzınızı açarak ("O" harfi) sayfayı aşağı-yukarı kaydırma özelliği.
* **💤 Uyku Modu (Güvenlik Kilidi):** Gözleri 3 saniye kapalı tutarak sistemi kilitleme ve yanlış hareketleri önleme.
* **🔒 Gizlilik Odaklı:** Görüntüler sunucuya gönderilmez, tamamen yerel bilgisayarda (On-Device) işlenir. KVKK uyumludur.

---

## 🛠️ Kurulum

Projeyi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Repoyu Klonlayın
```bash
git clone [https://github.com/ismailapan/VisionMouse.git](https://github.com/ismailapan/VisionMouse.git)
cd VisionMouse
