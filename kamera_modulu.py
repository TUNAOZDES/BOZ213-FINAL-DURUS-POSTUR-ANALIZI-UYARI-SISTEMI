"""
Dosya Adı: kamera_modulu.py

Amaç:
Bu modül, sistemde kullanılan kamera donanımı ile ilgili
tüm işlemleri yönetir. Kamera başlatma, kare okuma ve
kapatma işlemlerini soyut bir yapı altında toplar.

Bu dosyanın sorumlulukları:
- Kamera bağlantısını başlatmak ve doğrulamak
- Kameradan görüntü (frame) okumak
- Kullanım sonunda kamerayı güvenli şekilde kapatmak

OOP Katkısı:
- Donanım soyutlaması (Abstraction)
- Tek sorumluluk prensibi (Single Responsibility Principle)
- Ana programdan kamera detaylarının gizlenmesi (Encapsulation)

Not:
Bu modül yalnızca kamera donanımı ile ilgilenir.
Görüntü işleme, analiz, arayüz ve raporlama işlemleri
diğer modüller tarafından gerçekleştirilir.
"""

import cv2


class KameraYoneticisi:
    """
    Kamera donanımını yöneten sınıf.

    Bu sınıf:
    - Kamerayı güvenli şekilde başlatır
    - Kare okuma işlemini gerçekleştirir
    - Kullanım sonunda kamerayı serbest bırakır
    """

    def __init__(self, kamera_id=0):
        """
        Kamera yöneticisi nesnesi oluşturur.

        Parametre:
        - kamera_id: Kullanılacak kamera indeksi (varsayılan: 0)
        """
        self.kamera_id = kamera_id
        self.cap = None

    def baslat(self):
        """
        Kamera bağlantısını başlatır ve çalışır durumda olup
        olmadığını kontrol eder.

        Dönüş:
        - True  → Kamera başarıyla başlatıldı
        - False → Kamera açılamadı
        """
        print(f"Kamera ({self.kamera_id}) bağlantısı kuruluyor...")
        self.cap = cv2.VideoCapture(self.kamera_id)

        if not self.cap.isOpened():
            print("HATA: Kamera açılamadı!")
            return False

        # Kamera çözünürlüğü ayarlanır (HD)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        print("Kamera başarıyla başlatıldı.")
        return True

    def kare_oku(self):
        """
        Kameradan tek bir görüntü karesi (frame) okur.

        Dönüş:
        - (True, frame)  → Okuma başarılı
        - (False, None)  → Okuma başarısız
        """
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                return True, frame

        return False, None

    def kapat(self):
        """
        Kamera bağlantısını güvenli bir şekilde sonlandırır.
        """
        if self.cap is not None:
            self.cap.release()
            print("Kamera kapatıldı.")
