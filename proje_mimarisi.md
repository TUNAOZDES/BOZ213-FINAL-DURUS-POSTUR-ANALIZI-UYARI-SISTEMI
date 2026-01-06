# 📐 Proje Mimarisi

Bu proje, Nesne Yönelimli Programlama (OOP) prensipleri temel alınarak,
modüler, okunabilir ve genişletilebilir bir mimari ile geliştirilmiştir.
Sistem; canlı analiz, statik analiz, görüntü işleme, kullanıcı arayüzü ve
raporlama katmanlarından oluşmaktadır.

---

## 🧱 Mimari Katmanlar

### 1️⃣ Giriş ve Kontrol Katmanı
**main.py**

Uygulamanın başlangıç noktasıdır. Kullanıcıdan analiz türü (canlı / statik)
alınır, gerekli modüller başlatılır ve sistemin genel çalışma akışı bu
dosya üzerinden koordine edilir.

---

### 2️⃣ Kamera ve Veri Girişi Katmanı
**kamera_modulu.py**

Kamera donanımı ile ilgili tüm işlemler bu modülde kapsüllenmiştir.
Kamera başlatma, kare okuma ve bağlantıyı güvenli şekilde kapatma işlemleri
bu katmanda gerçekleştirilir.

---

### 3️⃣ Analiz Katmanı
**analiz_modu.py**

Tüm analiz türleri için ortak bir soyut yapı tanımlar. Bu yapı sayesinde
analiz türleri birbirinden bağımsız olarak geliştirilebilir ve ana sistem,
analiz detaylarından soyutlanmış olur.

**canli_analiz.py**

Canlı (kamera tabanlı) analiz sürecini nesne yönelimli bir yapı altında
temsil eder. Gerçek zamanlı analiz mantığı bu modül üzerinden
genişletilebilir şekilde tasarlanmıştır.

---

### 4️⃣ Görüntü İşleme ve Hesaplama Katmanı
**goruntu_isleme.py**

MediaPipe kütüphanesi kullanılarak vücut eklem (landmark) noktaları tespit
edilir. Omuz, boyun, yüz ve omurga açıları matematiksel algoritmalar ile
hesaplanır ve analiz için gerekli ham veriler üretilir.

---

### 5️⃣ Kullanıcı Arayüzü Katmanı
**arayuz_ozellikleri.py**

Analiz sonuçlarının kullanıcıya görsel olarak sunulmasından sorumludur.
Açı değerleri, puanlama, seviye göstergeleri ve uyarılar bu modül
üzerinden ekrana çizilir.

---

### 6️⃣ Raporlama Katmanı
**raporlama.py**

Analiz süreci boyunca elde edilen verileri toplayarak kullanıcıya özel
HTML formatında rapor üretir. Analiz görüntüsü, puanlar, seviye bilgileri
ve sistem önerileri rapora entegre edilir.

---

## 🔄 Genel Veri Akışı

Kamera / Fotoğraf →  
Görüntü İşleme (MediaPipe) →  
Açı Hesaplama ve Puanlama →  
Postür Değerlendirmesi →  
Kullanıcı Arayüzü →  
Raporlama

Bu mimari yapı sayesinde sistem; sürdürülebilir, test edilebilir ve yeni
analiz türlerine açık bir şekilde tasarlanmıştır.
