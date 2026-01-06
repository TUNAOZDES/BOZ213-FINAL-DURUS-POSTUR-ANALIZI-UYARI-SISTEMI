# Proje Mimarisi

Bu doküman, Duruş (Postür) Analiz Sistemi’nin
genel yazılım mimarisini ve modüller arasındaki
sorumluluk dağılımını açıklamak amacıyla hazırlanmıştır.

Proje, nesne yönelimli programlama (OOP) prensipleri
doğrultusunda modüler bir yapıda tasarlanmıştır.

---

## Genel Mimari Yaklaşım

Sistem, tek bir dosyada toplanmış karmaşık bir yapı yerine,
her biri belirli bir sorumluluğa sahip modüllerden oluşmaktadır.
Bu yaklaşım sayesinde:

- Kodun okunabilirliği artmıştır
- Bakım ve geliştirme kolaylaşmıştır
- OOP ilkeleri daha görünür hale gelmiştir

---

## Modül Bazlı Yapı

### main.py
- Uygulamanın giriş noktasıdır
- Kullanıcı etkileşimini başlatır
- Analiz modlarını koordine eder
- Diğer modüller arasında veri akışını sağlar

### goruntu_isleme.py
- MediaPipe kullanarak vücut landmark tespitini yapar
- Açı hesaplama algoritmalarını içerir
- Postür analizine ait matematiksel işlemleri gerçekleştirir

### kamera_modulu.py
- Kamera donanımına erişimi yönetir
- Kamera başlatma, kare okuma ve kapatma işlemlerini soyutlar
- Donanım bağımlılığını sistemin geri kalanından ayırır

### arayuz_ozellikleri.py
- Analiz sonuçlarının görsel olarak çizilmesini sağlar
- Açı değerleri, puanlama ve uyarı göstergelerini üretir
- Kullanıcıya geri bildirim sunar

### raporlama.py
- Analiz sonuçlarını kaydeder
- HTML formatında detaylı rapor üretir
- Hata analizi ve sağlık önerilerini oluşturur

### analiz_modu.py
- Tüm analiz türleri için soyut bir temel sınıftır
- Analiz süreçleri için ortak bir arayüz tanımlar
- Soyutlama ve çok biçimlilik ilkelerini gösterir

### canli_analiz.py
- AnalizModu sınıfından türetilmiştir
- Canlı kamera tabanlı analiz sürecini temsil eder
- İleride farklı analiz türlerinin eklenebilmesine olanak sağlar

---

## Nesne Yönelimli Programlama (OOP) Yapısı

Proje içerisinde aşağıdaki OOP prensipleri uygulanmıştır:

- **Kapsülleme (Encapsulation):**  
  Her modül yalnızca kendi sorumluluğundaki işlemleri içerir.

- **Soyutlama (Abstraction):**  
  AnalizModu soyut sınıfı ile analiz süreçleri için ortak bir yapı tanımlanmıştır.

- **Kalıtım (Inheritance):**  
  CanliAnaliz sınıfı, AnalizModu sınıfından türetilmiştir.

- **Çok Biçimlilik (Polymorphism):**  
  Farklı analiz modları, aynı arayüz üzerinden çalışabilecek şekilde tasarlanmıştır.

---

## Sonuç

Bu mimari yapı sayesinde proje;
- Modüler
- Genişletilebilir
- Akademik değerlendirme kriterlerine uygun

bir yazılım sistemi haline getirilmiştir.
