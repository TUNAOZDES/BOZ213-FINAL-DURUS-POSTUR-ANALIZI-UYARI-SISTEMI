"""
Dosya Adı: raporlama.py

Amaç:
Bu modül, postür analiz sürecinde elde edilen tüm ölçüm
ve değerlendirme sonuçlarını kalıcı hale getirir.
Analiz verileri kullanılarak HTML formatında
detaylı ve görsel bir rapor üretilir.

Bu dosyanın sorumlulukları:
- Analiz sırasında oluşan puan ve seviye verilerini toplamak
- En sık karşılaşılan duruş problemini belirlemek
- Kullanıcıya özel sağlık önerileri üretmek
- Analiz görüntüsü ile birlikte HTML rapor oluşturmak

OOP Katkısı:
- Raporlama işlemlerinin tek bir sınıfta toplanması
- Veri yönetimi ve çıktı üretiminin kapsüllenmesi (Encapsulation)
- Ana sistemden rapor üretim detaylarının soyutlanması (Abstraction)

Not:
Bu modül yalnızca raporlama sürecinden sorumludur.
Analiz, görüntü işleme ve arayüz çizimi işlemleri
diğer modüller tarafından gerçekleştirilir.
"""

import os
import cv2
from datetime import datetime
from collections import Counter


class RaporYoneticisi:
    """
    Analiz sonuçlarını toplayan ve HTML rapor üreten sınıf.
    """

    def __init__(self):
        # Raporların kaydedileceği klasör
        self.klasor = "Raporlar"

        # Klasör yoksa oluşturulur
        if not os.path.exists(self.klasor):
            os.makedirs(self.klasor)

        # Analiz süresince toplanan puan ve seviye bilgileri
        self.veriler = []

        # Seviye > 1 olan durumlarda oluşan hata mesajları
        self.hatalar = []

    def veri_ekle(self, puan, seviye, omuz, boyun, en_buyuk_hata_mesaji):
        """
        Analiz sırasında elde edilen puan ve seviye bilgilerini kaydeder.
        """
        self.veriler.append({
            "puan": puan,
            "seviye": seviye
        })

        # Uyarı veya kritik seviyelerde hata mesajı kaydedilir
        if seviye > 1:
            self.hatalar.append(en_buyuk_hata_mesaji)

    def raporu_kaydet(self, analiz_goruntusu, final_puan, ad_soyad="Belirtilmedi"):
        """
        Toplanan analiz verilerine göre HTML rapor oluşturur.
        """

        # Veri yoksa rapor üretilemez
        if not self.veriler:
            return "Veri yok"

        # Zaman damgası oluşturulur
        zaman = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Analiz görüntüsü dosyaya kaydedilir
        resim_adi = f"Analiz_Gorseli_{zaman}.jpg"
        resim_yolu = os.path.join(self.klasor, resim_adi)
        cv2.imwrite(resim_yolu, analiz_goruntusu)

        # Puan seviyesine göre renk ve durum belirleme
        renk_skoru = "#00c853" if final_puan >= 80 else (
            "#ffd600" if final_puan >= 50 else "#ff1744"
        )
        durum = (
            "OPTIMUM (YEŞİL)" if final_puan >= 80
            else "DİKKAT (SARI)" if final_puan >= 50
            else "KRİTİK (KIRMIZI)"
        )

        # En sık görülen hata belirlenir
        ham_hata = (
            Counter(self.hatalar).most_common(1)[0][0]
            if self.hatalar else ""
        )

        # --- DİNAMİK HATA VE ÖNERİ MOTORU ---
        if final_puan >= 80:
            en_sik_hata = "Belirgin bir duruş bozukluğu saptanmadı."
            oneri = (
                "Duruşunuz mükemmel seviyede. "
                "Bu formu korumak için düzenli esneme hareketlerine devam edin."
            )

        elif 50 <= final_puan < 80:
            if "Omuz" in ham_hata:
                en_sik_hata = "Hafif Düzey Omuz Asimetrisi"
                oneri = (
                    "Omuzlarınızda hafif bir dengesizlik var. "
                    "Gün içinde omuzlarınızı geriye yuvarlayarak dik durmaya odaklanın."
                )
            elif "Boyun" in ham_hata:
                en_sik_hata = "Başlangıç Seviyesi Boyun Eğriliği"
                oneri = (
                    "Telefon ve bilgisayar kullanımında ekranı göz hizanıza getirmeye dikkat edin. "
                    "Hafif boyun egzersizleri faydalı olacaktır."
                )
            elif "Omurga" in ham_hata:
                en_sik_hata = "Düşük Riskli Omurga Sapması"
                oneri = (
                    "Sırt kaslarını güçlendiren hafif egzersizler "
                    "(pilates, yoga) ile bu durumu kontrol altına alabilirsiniz."
                )
            else:
                en_sik_hata = "Hafif Duruş Sapması"
                oneri = (
                    "Genel duruşunuzda ufak sapmalar var. "
                    "Çalışma alanınızın ergonomisini gözden geçirin."
                )

        else:
            if "Omuz" in ham_hata:
                en_sik_hata = "KRİTİK DÜZEY: İleri Derece Omuz Eğriliği"
                oneri = (
                    "Ciddi omuz asimetrisi saptandı. "
                    "Bu durum kronik ağrılara yol açabilir. "
                    "Bir fizyoterapist eşliğinde düzeltici egzersizler yapmanız önerilir."
                )
            elif "Boyun" in ham_hata:
                en_sik_hata = "KRİTİK DÜZEY: İleri Derece Boyun Eğilmesi"
                oneri = (
                    "Boyun bölgenizde aşırı yüklenme saptandı (Text-Neck Sendromu). "
                    "İleri düzey boyun fıtığı riski için acilen duruş rehabilitasyonu önerilir."
                )
            elif "Omurga" in ham_hata:
                en_sik_hata = "KRİTİK DÜZEY: Yüksek Skolyoz/Kifoz Riski"
                oneri = (
                    "Omurga hizasında belirgin bir deformasyon gözlenmektedir. "
                    "En kısa sürede bir ortopedi uzmanına muayene olmanız sağlığınız için kritiktir."
                )
            else:
                en_sik_hata = "Kritik Duruş Bozukluğu"
                oneri = (
                    "Biyomekanik dengenizde ciddi bozulmalar var. "
                    "Yaşam kaliteniz için profesyonel tıbbi destek almayı değerlendirmelisiniz."
                )

        # --------------------------------------------------
        # HTML rapor içeriği
        #
        # Bu bölüm:
        # - CSS stil tanımlarını
        # - Analiz puanı ve seviye bilgilerini
        # - Tespit edilen ana duruş problemini
        # - Sistem tarafından üretilen sağlık önerilerini
        # - Analiz görüntüsünü
        # içeren HTML rapor çıktısını oluşturur.
        #
        # NOT:
        # Bu alan bilinçli olarak tek parça tutulmuştur.
        # Okunabilirlik için bölünmemiştir.
        # --------------------------------------------------
        
        html_icerik = f"""
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <title>Duruş Analiz Raporu</title>
            <style>
                body {{ background-color: #0f0f0f; color: white; font-family: 'Segoe UI', sans-serif; text-align: center; padding: 20px; }}
                .container {{ background: #1a1a1a; border: 2px solid #ffffff; border-radius: 15px; display: inline-block; padding: 30px; max-width: 800px; }}
                h1 {{ color: #ffffff; margin-bottom: 5px; text-transform: uppercase; }}
                .kullanici {{ font-size: 18px; color: #ffffff; margin-bottom: 20px; font-weight: bold; }}
                .puan {{ font-size: 72px; font-weight: bold; color: {renk_skoru}; margin: 10px 0; }}
                .durum {{ font-size: 24px; color: {renk_skoru}; font-weight: bold; margin-bottom: 20px; }}
                .hata-kutusu {{ background: #252525; border-left: 5px solid {renk_skoru}; padding: 15px; text-align: left; margin: 20px auto; width: 90%; }}
                .oneri-kutusu {{ background: #1e293b; border: 1px dashed #3b82f6; padding: 15px; text-align: left; margin: 20px auto; width: 90%; border-radius: 8px; }}
                img {{ width: 100%; border-radius: 10px; margin-top: 20px; border: 1px solid #444; }}
                .footer {{ color: #666; font-size: 12px; margin-top: 30px; border-top: 1px solid #333; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>DURUŞ (POSTÜR) ANALİZ RAPORU</h1>
                <div class="kullanici">Analiz Edilen: {ad_soyad}</div>
                <p>Tarih: {zaman}</p>
                <hr style="border: 0; border-top: 1px solid #333;">
                <div class="puan">{final_puan:.2f}</div>
                <div class="durum">{durum}</div>
                
                <div class="hata-kutusu">
                    <strong style="color: {renk_skoru};">Saptanan Ana Sorun:</strong><br>
                    <span style="font-size: 18px;">{en_sik_hata}</span>
                </div>

                <div class="oneri-kutusu">
                    <strong style="color: #3b82f6;">Sistem Sağlık Önerisi:</strong><br>
                    <span style="font-size: 16px; color: #cbd5e1;">{oneri}</span>
                </div>

                <h3>Analiz Görüntüsü Kaydı</h3>
                <img src="{resim_adi}" alt="Postür Analiz Görüntüsü">
                
                <p class="footer">
                    Bu rapor Tuna Özdeş Duruş (Postür) Analiz Sistemi tarafından oluşturulmuştur.<br>
                    <strong>Uyarı:</strong> Bu rapor bilgilendirme amaçlıdır, tıbbi tanı yerine geçmez.
                </p>
            </div>
        </body>
        </html>
        """

        rapor_adi = f"Rapor_{zaman}.html"
        rapor_yolu = os.path.join(self.klasor, rapor_adi)

        with open(rapor_yolu, "w", encoding="utf-8") as f:
            f.write(html_icerik)

        return rapor_yolu
