
# AI Destekli El Hareketiyle Çiçek Kontrolü

Bu proje, MediaPipe ve OpenCV kütüphanelerini kullanarak el hareketleriyle gerçek zamanlı etkileşime girebilen bir "çiçek açtırma" simülasyonudur. Kullanıcı elini açtıkça çiçek büyüme evrelerinden geçer ve gelişir.

## Özellikler
* **Gerçek Zamanlı El Takibi:** MediaPipe Hands modülü ile 21 nokta üzerinde hassas takip.
* **Etkileşimli Kontrol:** Elin bilek ve parmak ucu arasındaki mesafe (öklid uzaklığı) baz alınarak dinamik seviye kontrolü.
* **Esnek Çalışma Modları:** * `main.py`: Standart OpenCV penceresi ile doğrudan uygulama çalıştırıcı.
    * `streamlit_main.py`: Web arayüzü üzerinden kamera görüntüsünü ve çiçek panelini aynı anda izleme imkanı.
* **Gelişmiş Görüntü İşleme:** Alpha kanalı (şeffaflık) yönetimi ile pürüzsüz görselleştirme.

## Gereksinimler
Projenin çalışması için bilgisayarınızda bir web kamerası bulunmalıdır.

## Kurulum

1. **Depoyu Klonlayın:**
   ```bash
   git clone [https://github.com/kullanici_adiniz/proje_adi.git](https://github.com/kullanici_adiniz/proje_adi.git)
   cd proje_adi

`

2. **Gerekli Kütüphaneleri Yükleyin:**
```bash
pip install -r requirements.txt

```



## Kullanım

### 1. Standart Mod (OpenCV)

Eğer sadece yerel bir pencerede denemek isterseniz:

```bash
python main.py

```

### 2. Web Arayüzü Modu (Streamlit)

Tarayıcı üzerinden etkileşimli bir deneyim için:

```bash
streamlit run streamlit_main.py

```

## Proje Yapısı

* `assets/`: Çiçeğin büyüme evrelerini temsil eden `C1.png` - `C10.png` dosyalarını içermelidir.
* `main.py`: OpenCV tabanlı temel çalışma scripti.
* `streamlit_main.py`: Streamlit arayüz entegrasyonuna sahip gelişmiş script.

## Teknolojiler

* Python
* OpenCV (Görüntü işleme)
* MediaPipe (El iskeleti tespiti)
* Streamlit (Web Arayüzü)
* NumPy (Matematiksel hesaplamalar)

