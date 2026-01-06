"""
Dosya Adı: goruntu_isleme.py

Amaç:
Bu modül, MediaPipe kütüphanesi kullanılarak insan vücudu üzerindeki
temel eklem (landmark) noktalarını tespit eder ve postür (duruş)
analizinde kullanılan açısal hesaplamaları gerçekleştirir.

Bu dosyanın sorumlulukları:
- Vücut eklem noktalarının (pose landmarks) algılanması
- Omuz ve baş eğim açılarını hesaplayan matematiksel işlemler
- Analiz için gerekli ham verilerin üst modüllere sunulması

OOP Katkısı:
- Görüntü işleme ve analiz algoritmalarının tek bir sınıfta toplanması
- Hesaplama detaylarının sistemin geri kalanından gizlenmesi (Encapsulation)
- Ana program için sade, okunabilir ve yeniden kullanılabilir bir arayüz sağlanması

Not:
Bu modül yalnızca analiz ve hesaplama işlemlerinden sorumludur.
Kamera yönetimi, arayüz çizimi ve raporlama işlemleri başka modüller
tarafından gerçekleştirilir.
"""

import cv2
import mediapipe as mp
import numpy as np


class PosturHesaplayici:
    """
    MediaPipe Pose modeli üzerinden insan vücudu eklem noktalarını analiz eden
    ve postür değerlendirmesinde kullanılan açıları hesaplayan sınıf.
    """

    def __init__(self):
        # MediaPipe Pose çözümleyicisi tanımlanır
        self.mp_pose = mp.solutions.pose

        # Pose modeli yapılandırılır:
        # - min_detection_confidence: ilk tespit hassasiyeti
        # - min_tracking_confidence: kareler arası takip güvenilirliği
        # - model_complexity: hız ve doğruluk dengesi
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
            model_complexity=1
        )

    def aci_hesapla(self, a, b):
        """
        İki nokta arasındaki açıyı hesaplar.

        Parametreler:
        - a, b: İki noktanın (x, y) koordinatları

        Dönüş:
        - 0–180 derece aralığında normalize edilmiş açı değeri
        """

        # Noktalar matematiksel işlem için numpy dizisine dönüştürülür
        a, b = np.array(a), np.array(b)

        # Arctan2 fonksiyonu ile iki nokta arasındaki yön açısı hesaplanır (radyan)
        radians = np.arctan2(b[1] - a[1], b[0] - a[0])

        # Radyan → derece dönüşümü yapılır
        aci = np.abs(radians * 180.0 / np.pi)

        # Açının 0–180 derece aralığında kalması sağlanır
        return 360 - aci if aci > 180.0 else aci

    def vucut_tara(self, frame):
        """
        Tek bir görüntü karesi üzerinde MediaPipe Pose analizi yapar.

        Parametre:
        - frame: OpenCV formatında alınmış görüntü karesi

        Dönüş:
        - OpenCV formatında işlenmiş görüntü
        - MediaPipe pose analiz sonuçları
        """

        # OpenCV görüntüsü MediaPipe için RGB formatına çevrilir
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Performans optimizasyonu için yazılabilirlik kapatılır
        image.flags.writeable = False

        # Pose modeli ile vücut landmark analizi yapılır
        sonuclar = self.pose.process(image)

        # Analiz sonrası tekrar yazılabilir hale getirilir
        image.flags.writeable = True

        # Görüntü tekrar OpenCV (BGR) formatına çevrilir
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR), sonuclar

    def detayli_analiz(self, landmarks, w, h):
        """
        Tespit edilen landmark noktalarından postür analizinde
        kullanılan açıları hesaplar.

        Parametreler:
        - landmarks: MediaPipe tarafından döndürülen landmark listesi
        - w, h: Görüntünün genişlik ve yükseklik değerleri

        Dönüş:
        - Omuz eğim açısı
        - Baş (yüz) eğim açısı
        - Landmark noktalarının piksel koordinatları
        """

        lm = {}

        # Analizde kullanılacak temel vücut noktaları
        kritik_noktalar = [
            0,   # Burun
            2, 5,  # Yüz yan noktaları
            7, 8,  # Kulaklar
            11, 12,  # Omuzlar
            13, 14,  # Dirsekler
            23, 24,  # Kalça
            25, 26,  # Dizler
            27, 28   # Ayak bilekleri
        ]

        # Seçilen landmark noktaları piksel koordinatlarına dönüştürülür
        for i in kritik_noktalar:
            lm[i] = [
                landmarks[i].x * w,
                landmarks[i].y * h
            ]

        # Omuzlar arasındaki eğim açısı hesaplanır
        ham_omuz = self.aci_hesapla(lm[11], lm[12])
        aci_omuz = abs(180 - ham_omuz) if ham_omuz > 90 else ham_omuz

        # Baş (yüz) eğim açısı hesaplanır
        ham_bas = self.aci_hesapla(lm[7], lm[8])
        aci_bas = abs(180 - ham_bas) if ham_bas > 90 else ham_bas

        # Hesaplanan değerler üst modüllere geri döndürülür
        return aci_omuz, aci_bas, lm
