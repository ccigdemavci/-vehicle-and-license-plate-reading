 🚛 Akıllı Araç Kapısı: Kamyon Tanıma ve Plaka Doğrulama Sistemi

Bu projede, bir kapıya yaklaşan araçların kamera görüntüsü üzerinden türü (kamyon/tır veya otomobil) ve plakası tespit edilerek, **önceden belirlenen kurallara göre Arduino üzerinden fiziksel bir kapı kontrolü** gerçekleştirilmiştir. 

Görüntü işleme ile tespit edilen **kamyon/tır** araçlarının plakaları, sistemde kayıtlı olan plakalarla karşılaştırılmıştır. Eğer plaka kayıtlı ise **Arduino üzerinden bir kapı açma sinyali** gönderilmiş, aksi takdirde ya da araç tipi uygun değilse **Arduino üzerindeki buzzer ile uyarı verilmiştir**.

Uygulama, Flask web çatısı kullanılarak geliştirilmiştir. Sistem, hem bilgisayar kamerası hem de mobil cihaz kamerası (IP üzerinden) ile çalışabilecek şekilde tasarlanmıştır.

---

## 🎯 Projenin Amacı

Bu projenin amacı; bir kapının önüne gelen araçların görsel olarak analiz edilerek, yalnızca **kamyon/tır tipi araçlardan yetkili olanların** içeri alınmasını sağlamak, diğer araçlar için ise bir uyarı sistemi oluşturmaktır. 

Geliştirilen sistem sayesinde hem güvenlik artırılmış hem de insan müdahalesine gerek kalmadan araç geçişi otomatik hale getirilmiştir.

---

## ⚙️ Sistemin Genel İşleyişi

1. Kapıya yaklaşan araç, sistemin kamerası tarafından görüntülenir.
2. Görüntü, YOLOv8 modeli kullanılarak analiz edilir:
   - Aracın türü (kamyon/tır veya otomobil) tespit edilir.
   - Eğer kamyon veya tır tespit edilmişse, araçtaki plaka bölgesi tanınır.
3. Tespit edilen plaka, SQLite veritabanında kayıtlı plakalarla karşılaştırılır.
4. Sonuca göre:
   - Eğer **kamyon/tır** tespit edilmiş ve plaka **veritabanında kayıtlıysa**, Arduino üzerinden **kapı açma komutu** gönderilir.
   - Eğer araç tipi **otomobil** ise veya plaka **veritabanında kayıtlı değilse**, Arduino üzerindeki **buzzer devreye alınır**.
5. Tüm bu işlemler canlı olarak bir web arayüzü üzerinden izlenebilir.

---

## 🧱 Sistem Bileşenleri

- **Görüntü İşleme:** YOLOv8 modeli ile araç tipi ve plaka bölgesi tespiti yapılmaktadır.
- **Veritabanı:** Kayıtlı plakalar bir SQLite veritabanında tutulmaktadır.
- **Web Arayüzü:** Flask kullanılarak oluşturulan arayüz ile kamera görüntüsü izlenmekte ve plaka ekleme işlemleri yapılmaktadır.
- **Donanım:** Arduino kullanılarak kapı açma ve buzzer kontrolü sağlanmaktadır.
- **Kamera:** Bilgisayar kamerası ya da mobil cihaz kamerası (örneğin IP Webcam uygulaması) kullanılmaktadır.

---

## 📌 Geliştirme Süreci

### 1. **Veri Toplama**
- 300 adet kamyon/tır ve 300 adet otomobil görüntüsü toplanmıştır.

### 2. **Veri Etiketleme ve İlk Eğitim**
- Görüntüler Roboflow platformuna yüklenmiş ve hem araç türleri hem de plaka bölgeleri bounding box ile manuel olarak etiketlenmiştir.
- Etiketli verilerle Roboflow üzerinden ilk nesne tanıma modeli eğitilmiştir.

### 3. **Otomatik Etiketleme ve YOLO Eğitimi**
- Eğitilen model, kalan görüntüleri otomatik etiketlemek için kullanılmıştır.
- Elde edilen veri kümesiyle YOLOv8 modeli yerel olarak eğitilmiştir.

### 4. **Test Süreci**
- Eğitimli YOLO modeli ile 3 dakikalık gerçek ortam videosu kullanılarak test yapılmıştır.
- Doğru sınıflandırma ve tepki kontrolleri gözlemlenmiştir.

### 5. **Web Uygulaması ve Arduino Entegrasyonu**
- Flask tabanlı bir arayüz geliştirilmiş, canlı kamera görüntüsü ile entegre edilmiştir.
- Plaka veritabanı için giriş ekranı eklenmiştir.
- Arduino üzerinden, plaka ve araç türüne göre kapı açma ya da buzzer aktif etme işlemleri gerçekleştirilmiştir.

---

## 🖥️ Web Arayüz Özellikleri

- **Canlı Kamera Görüntüsü**: Anlık olarak kamera akışı izlenebilir.
- **Uyarılar**: 
  - “Kamyon tespit edildi”
  - “Araç içeri alınıyor”
  - “Yetkisiz araç tespit edildi”
- **Plaka Ekleme Sayfası**: Kullanıcılar yeni plakaları arayüz üzerinden sisteme kaydedebilir.

---

## 🔧 Kurulum ve Kullanım

### Gereksinimler

- Python 3.8+
- Arduino (USB üzerinden bağlı)
- Eğitilmiş YOLOv8 modeli (`best.pt`)
- IP kamera uygulaması veya bilgisayar kamerası

### Kurulum Adımları

```
pip install flask opencv-python pyserial ultralytics
```

### Uygulamanın Çalıştırılması

```
python app.py
```

Tarayıcıdan şu adres ile erişim sağlanabilir:

```
http://localhost:5000
```

---

## 📁 Proje Klasör Yapısı

```
arac_kapi_sistemi/
│
├── app.py                  # Flask uygulaması
├── detect.py               # YOLO modeli ile tespit
├── yolov8/
│   └── best.pt             # Eğitilmiş YOLOv8 modeli
├── plates.db               # Plaka veritabanı (SQLite)
├── templates/
│   ├── index.html          # Canlı kamera sayfası
│   └── add_plate.html      # Plaka ekleme formu
├── static/
│   └── style.css           # Stil dosyası
├── test_video.mp4          # Test videosu (3 dakika)
└── README.md               # Açıklama dosyası
```

---

## 👤 Geliştirici Bilgisi

Bu proje, 21 yaşındaki bir bilgisayar mühendisliği öğrencisi olarak bireysel olarak geliştirilmiştir. Görüntü işleme, gömülü sistemler ve web teknolojileri bir araya getirilmiştir.

**Geliştiren:** Çiğdem Avcı  
**E-posta:** cigdemavci@example.com  
**GitHub:** [github.com/cigdemavci](https://github.com/cigdemavci)
