# Duruş (Postür) Analiz Sistemi

Bu proje, Python programlama dili kullanılarak geliştirilen,
kamera tabanlı bir Duruş (Postür) Analiz ve Uyarı Sistemidir.

Sistem, MediaPipe kütüphanesi aracılığıyla insan vücudu üzerindeki
kritik eklem (landmark) noktalarını tespit eder, açısal hesaplamalar yapar
ve kullanıcının duruşunu analiz ederek görsel ve işitsel geri bildirimler sunar.

---

## Projenin Amacı

Bu projenin amacı;

- Nesne yönelimli programlama (OOP) prensiplerini gerçek bir uygulama üzerinde göstermek
- Görüntü işleme ve analiz süreçlerini modüler bir mimari ile gerçekleştirmek
- Kullanıcıya canlı (kamera) ve statik (fotoğraf) postür analizi sunmak
- Akademik değerlendirme kriterlerine uygun, düzenli ve sürdürülebilir bir yazılım geliştirmektir

---

## Temel Özellikler

- Canlı kamera tabanlı gerçek zamanlı postür analizi
- Statik görüntü (fotoğraf) üzerinden detaylı analiz
- Omuz, boyun, yüz ve omurga açı hesaplamaları
- Kritik duruşlarda sesli uyarı sistemi
- Skor tabanlı değerlendirme (optimum / dikkat / kritik)
- HTML formatında detaylı analiz raporu oluşturma

---

## Sistem Genel Yapısı (İnfografik)

Aşağıdaki infografik, geliştirilen Duruş (Postür) Analizi Uyarı Sisteminin
ana bileşenlerini, kullanılan teknolojileri ve sistemin genel işleyişini
görsel olarak özetlemektedir.

![Duruş (Postür) Analizi Uyarı Sistemi](infografik.png)

---

## Kullanılan Teknolojiler

- Python 3
- OpenCV
- MediaPipe
- Tkinter
- NumPy
- Pillow (PIL)

---

## Proje Dosya Yapısı

- main.py  
  Uygulamanın ana çalışma akışını yönetir ve tüm modüller arasında koordinasyon sağlar.

- goruntu_isleme.py  
  MediaPipe kullanarak vücut eklem noktalarını tespit eder ve açı hesaplamalarını yapar.

- kamera_modulu.py  
  Kamera donanımının başlatılması, kare okunması ve güvenli şekilde kapatılmasından sorumludur.

- arayuz_ozellikleri.py  
  Analiz sonuçlarının görsel arayüz üzerinde çizilmesini ve kullanıcıya sunulmasını sağlar.

- raporlama.py  
  Analiz sonuçlarını HTML formatında detaylı bir rapor haline getirir.

- analiz_modu.py  
  Analiz türleri için soyut (abstract) temel sınıfı tanımlar.

- canli_analiz.py  
  Canlı analiz modunun nesne yönelimli yapısını temsil eder.

- pair_programming.md  
  Pair programming sürecinin ve iş paylaşımının detaylı açıklamasını içerir.

- ai_usage.md  
  Yapay zeka asistanının proje sürecinde nasıl kullanıldığını açıklar.

- proje_mimarisi.md  
  Projenin genel mimari yapısını ve modüler tasarımını açıklar.

---

## Nesne Yönelimli Programlama (OOP) Kullanımı

Bu projede nesne yönelimli programlama prensipleri etkin ve bilinçli şekilde uygulanmıştır:

- Kapsülleme (Encapsulation):  
  Kamera yönetimi, görüntü işleme, arayüz çizimi ve raporlama işlemleri ayrı sınıflar altında toplanmıştır. Her sınıf yalnızca kendi sorumluluk alanına odaklanmakta ve sistemin geri kalanından bağımsız çalışabilmektedir.

- Soyutlama (Abstraction):  
  AnalizModu sınıfı ile analiz türleri için ortak bir soyut yapı oluşturulmuştur. Bu yapı sayesinde analiz türü değişse bile üst seviye sistem akışı değişmeden kalabilmektedir. Bu sayede sistem, analiz türünün iç detaylarını bilmeden analiz sürecini yönetebilmektedir.

- Kalıtım (Inheritance):  
  Canlı analiz ve statik analiz yapıları ortak soyut sınıflardan türetilmiştir. Bu sayede kod tekrarından kaçınılmış ve genişletilebilir bir yapı elde edilmiştir.

- Çok Biçimlilik (Polymorphism):  
  Farklı analiz modları aynı arayüzü kullanarak kendi iç işleyişlerine göre farklı davranışlar sergileyebilmektedir. Bu durum, sistemin esnekliğini artırmakta ve analiz türleri arasında geçişi sorunsuz hale getirmektedir.

---

## Pair Programming ve Yapay Zeka Asistanı Kullanımı

Bu proje, pair programming yaklaşımı benimsenerek geliştirilmiştir.
Geliştirme sürecinde öğrenci ve yapay zeka asistanı birlikte çalışmıştır.

- Proje mimarisi ve modüler yapı birlikte planlanmıştır
- Kod düzenleme, hata ayıklama ve iyileştirme süreçlerinde yapay zeka aktif olarak kullanılmıştır
- Akademik değerlendirme kriterlerine uygunluk sürekli kontrol edilmiştir

Bu sürece ait detaylı açıklamalar aşağıdaki dosyalarda yer almaktadır:
- pair_programming.md
- ai_usage.md
- proje_mimarisi.md

---

## Projeyi Çalıştırma

Bu proje Python 3 ortamında çalışacak şekilde geliştirilmiştir.

---

### Gerekli Kütüphanelerin Kurulumu

Projeyi çalıştırmadan önce aşağıdaki kütüphanelerin sisteme kurulu olması gerekmektedir:

pip install opencv-python mediapipe numpy pillow

---

### Uygulamanın Başlatılması

Tüm dosyalar aynı klasörde olacak şekilde proje dizinine girildikten sonra
aşağıdaki komut ile uygulama başlatılır:

python main.py

---

### Çalışma Akışı

- Uygulama açıldığında kullanıcıdan ad ve soyad bilgisi alınır
- Canlı analiz veya statik analiz modu seçilir
- Canlı analizde kamera üzerinden gerçek zamanlı ölçüm yapılır
- Statik analizde seçilen fotoğraf analiz edilir
- Analiz sonuçları ekranda görsel olarak gösterilir
- İstenildiğinde analiz raporu HTML formatında oluşturulur

Not: Canlı analiz modunda çalışabilmesi için sistemde aktif bir kamera bulunmalıdır.

---

## Akademik Proje Raporu

Bu projeye ait akademik rapor,
Computers and Informatics (Dergipark) dergisi yazım kurallarına uygun olarak
ayrı bir belge halinde hazırlanmıştır.

README.md dosyası, projenin teknik tanıtımı ve kullanımını açıklamak amacıyla hazırlanmıştır. 
