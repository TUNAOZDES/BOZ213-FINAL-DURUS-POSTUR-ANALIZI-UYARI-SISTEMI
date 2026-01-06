"""
Dosya Adı: arayuz_ozellikleri.py

Amaç:
Bu modül, postür analizinden elde edilen sonuçları kullanıcıya
görsel olarak sunmakla sorumludur. Açı değerleri, puanlama,
durum göstergeleri ve uyarılar bu dosyada çizilir.

Bu dosyanın sorumlulukları:
- Analiz sonuçlarını ekrana görsel olarak yansıtmak
- Kullanıcıya anlık geri bildirim sağlamak
- Puan, seviye ve uyarı durumlarını sezgisel biçimde göstermek

OOP Katkısı:
- Arayüz çizim sorumluluğunun ayrıştırılması
- Görselleştirme işlemlerinin tek bir sınıfta kapsüllenmesi
- Ana programdan arayüz detaylarının gizlenmesi (Encapsulation)

Not:
Bu modül yalnızca görselleştirme işlemlerini içerir.
Analiz, kamera yönetimi ve raporlama işlemleri diğer modüller
tarafından gerçekleştirilir.
"""

import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image


class ArayuzYoneticisi:
    """
    Analiz sonuçlarını ekrana çizen ve kullanıcı arayüzünü
    yöneten sınıf.
    """

    def __init__(self):
        # Sistem genelinde kullanılan renk paleti
        self.RENK_CY_SARI = (0, 215, 255)
        self.RENK_CY_YESIL = (50, 255, 50)
        self.RENK_CY_KIRMIZI = (50, 50, 255)
        self.RENK_BEYAZ = (255, 255, 255)
        self.RENK_GRI = (180, 180, 180)

        # Rapor butonunun başlangıç koordinatları
        self.btn_x1, self.btn_y1 = 40, 0
        self.btn_x2, self.btn_y2 = 280, 0

        # Font dosyaları yüklenir (yoksa varsayılan font kullanılır)
        try:
            self.font_buyuk = ImageFont.truetype("arialbd.ttf", 28)
            self.font_orta = ImageFont.truetype("arialbd.ttf", 20)
            self.font_kucuk = ImageFont.truetype("arial.ttf", 14)
        except IOError:
            self.font_buyuk = ImageFont.load_default()
            self.font_orta = ImageFont.load_default()
            self.font_kucuk = ImageFont.load_default()

    def neon_cizgi(self, img, pt1, pt2, renk, kalinlik=2):
        """
        İki nokta arasına neon efektli bir çizgi çizer.
        """
        # Arka plan parlama efekti
        cv2.line(
            img,
            pt1,
            pt2,
            (renk[0] // 5, renk[1] // 5, renk[2] // 5),
            kalinlik + 5
        )

        # Ana çizgi
        cv2.line(img, pt1, pt2, renk, kalinlik)

        # İnce beyaz vurgu çizgisi
        cv2.line(img, pt1, pt2, (255, 255, 255), 1)

    def turkce_yaz(self, img, text, pos, color, size="orta", ortala=False):
        """
        Türkçe karakter destekli, gölgeli ve net metin çizimi yapar.
        """
        pil_img = Image.fromarray(
            cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        )
        draw = ImageDraw.Draw(pil_img)

        # Font boyutu seçimi
        font = (
            self.font_buyuk if size == "buyuk"
            else self.font_kucuk if size == "kucuk"
            else self.font_orta
        )

        x, y = pos

        # Metni ortalama opsiyonu
        if ortala:
            bbox = draw.textbbox((0, 0), text, font=font)
            metin_genislik = bbox[2] - bbox[0]
            x -= metin_genislik // 2

        # Gölge efekti
        draw.text((x + 1, y + 1), text, font=font, fill=(0, 0, 0))
        draw.text((x, y), text, font=font, fill=color)

        return cv2.cvtColor(
            np.array(pil_img),
            cv2.COLOR_RGB2BGR
        )

    def arayuzu_ciz(
        self,
        image,
        aci_omuz,
        aci_boyun,
        aci_yuz,
        aci_omurga,
        puan,
        seviye
    ):
        """
        Analiz sonuçlarına göre ana kullanıcı arayüzünü çizer.
        """
        h, w = image.shape[:2]

        # Rapor butonunun dikey konumu güncellenir
        self.btn_y1, self.btn_y2 = h - 80, h - 30

        # Sol panel arka planı (yarı saydam)
        overlay = image.copy()
        cv2.rectangle(overlay, (0, 0), (320, h), (10, 10, 15), -1)
        image = cv2.addWeighted(overlay, 0.85, image, 0.15, 0)

        # Seviye durumuna göre renk ve metinler
        if seviye == 1:
            renk, baslik, alt = self.RENK_CY_YESIL, "OPTİMUM", "DENGE"
        elif seviye == 2:
            renk, baslik, alt = self.RENK_CY_SARI, "HAFİF", "SAPMA"
        else:
            renk, baslik, alt = self.RENK_CY_KIRMIZI, "KRİTİK", "DURUŞ"

        # OpenCV BGR → RGB dönüşümü
        rgb_renk = (renk[2], renk[1], renk[0])

        # Üst başlık
        image = self.turkce_yaz(
            image,
            "POSTÜR ANALİZİ",
            (20, 30),
            self.RENK_BEYAZ,
            "buyuk"
        )
        cv2.line(image, (20, 75), (300, 75), (80, 80, 90), 1)

        # Açı bilgileri
        image = self.turkce_yaz(image, "OMUZ EĞİMİ", (30, 95), self.RENK_GRI, "kucuk")
        image = self.turkce_yaz(image, f"{aci_omuz:.1f}°", (30, 115), self.RENK_BEYAZ, "buyuk")

        image = self.turkce_yaz(image, "BOYUN EĞİMİ", (180, 95), self.RENK_GRI, "kucuk")
        image = self.turkce_yaz(image, f"{aci_boyun:.1f}°", (180, 115), self.RENK_BEYAZ, "buyuk")

        image = self.turkce_yaz(image, "YÜZ EĞİMİ", (30, 165), self.RENK_GRI, "kucuk")
        image = self.turkce_yaz(image, f"{aci_yuz:.1f}°", (30, 185), self.RENK_BEYAZ, "buyuk")

        image = self.turkce_yaz(image, "OMURGA EĞİMİ", (180, 165), self.RENK_GRI, "kucuk")
        image = self.turkce_yaz(image, f"{aci_omurga:.1f}°", (180, 185), self.RENK_BEYAZ, "buyuk")

        # Merkezi puan göstergesi
        merkez_x, merkez_y = 160, 360
        cv2.circle(image, (merkez_x, merkez_y), 65, (40, 40, 50), 4)
        cv2.ellipse(
            image,
            (merkez_x, merkez_y),
            (65, 65),
            0,
            -90,
            -90 + (360 * (puan / 100)),
            renk,
            6
        )

        image = self.turkce_yaz(
            image,
            f"{int(puan)}",
            (merkez_x, merkez_y - 15),
            rgb_renk,
            "buyuk",
            ortala=True
        )

        # Durum metinleri
        image = self.turkce_yaz(image, baslik, (160, 470), rgb_renk, "buyuk", ortala=True)
        image = self.turkce_yaz(image, alt, (160, 505), rgb_renk, "buyuk", ortala=True)

        # Rapor butonu
        cv2.rectangle(
            image,
            (self.btn_x1, self.btn_y1),
            (self.btn_x2, self.btn_y2),
            (30, 35, 45),
            -1
        )
        cv2.rectangle(
            image,
            (self.btn_x1, self.btn_y1),
            (self.btn_x2, self.btn_y2),
            self.RENK_BEYAZ,
            2
        )

        image = self.turkce_yaz(
            image,
            "RAPORLA VE ÇIK",
            (160, self.btn_y1 + 15),
            self.RENK_BEYAZ,
            "orta",
            ortala=True
        )

        # Kritik durumda ekran çerçevesi
        if seviye == 3:
            cv2.rectangle(image, (0, 0), (w, h), self.RENK_CY_KIRMIZI, 15)

        return image
