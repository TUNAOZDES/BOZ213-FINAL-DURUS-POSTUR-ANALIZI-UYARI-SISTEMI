"""
Dosya Adı: main.py

Amaç:
Bu dosya, Duruş (Postür) Analiz Sisteminin ana
çalışma akışını yöneten merkez modüldür.

Bu dosyanın sorumlulukları:
- Kullanıcıdan analiz türü (canlı / statik) seçimini almak
- Gerekli modülleri başlatmak ve koordine etmek
- Analiz sürecini kontrol etmek
- Raporlama sürecini tetiklemek

Not:
Bu dosya doğrudan analiz veya hesaplama yapmaz.
Sadece sistem bileşenleri arasında koordinasyon sağlar.
"""

# Gerekli standart ve üçüncü parti kütüphaneler
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import cv2, time, winsound, numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from kamera_modulu import KameraYoneticisi
from goruntu_isleme import PosturHesaplayici
from arayuz_ozellikleri import ArayuzYoneticisi
from raporlama import RaporYoneticisi
from analiz_modu import AnalizModu

# --- AYARLAR VE RENKLER ---
# Analiz sonuçlarını değerlendirmek için kullanılan
# eşik değerler ve sistem durum değişkenleri.

SINIRLAR = {
    "omuz": {"sari": 3, "kirmizi": 8}, 
    "boyun": {"sari": 5, "kirmizi": 12}, 
    "yuz": {"sari": 4, "kirmizi": 10}, 
    "omurga": {"sari": 4, "kirmizi": 10}
}

rapor_tetiklendi = False
mod_secimi = None
secilen_dosya = None
tam_ad = ""

# Arayüzde kullanılan renk sabitleri
# Görsel tutarlılık ve okunabilirlik sağlamak amacıyla
# merkezi bir yapı altında tanımlanmıştır.

C_BG = "#0f172a"
C_CARD = "#1e293b"
C_PRIMARY = "#3b82f6"
C_SUCCESS = "#22c55e"
C_TEXT_MAIN = "#f8fafc"
C_TEXT_SUB = "#94a3b8"

def fare_olayi(event, x, y, flags, param):
    # Analiz ekranında kullanıcı etkileşimini yakalar.
    # Raporlama işlemini tetiklemek için kullanılır.
    global rapor_tetiklendi
    if event == cv2.EVENT_LBUTTONDOWN:
        ay = param
        if ay.btn_x1 <= x <= ay.btn_x2 and ay.btn_y1 <= y <= ay.btn_y2:
            rapor_tetiklendi = True

# --- GİRİŞ PANELİ ---
class BiomechProPanel:
    """
    Kullanıcıdan analiz süreci için gerekli
    temel bilgileri alan giriş panelini temsil eder.

    Bu sınıf:
    - Kullanıcı adı ve soyadı bilgisini alır
    - Analiz türü seçimini sağlar
    - Ana analiz sürecini başlatır
    """
    def __init__(self, root):
        # Giriş paneli arayüzü ve pencere ayarları
        self.root = root
        self.root.title("Duruş (Postür) Analizi Uyarı Sistemi")
        self.root.geometry("1000x800")
        self.root.configure(bg=C_BG)

        # Arka plan canvas (ızgara ve merkezleme için)
        self.canvas = tk.Canvas(self.root, bg=C_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Merkez panel
        self.main_frame = tk.Frame(self.canvas, bg=C_BG)
        self.canvas.create_window(
            0, 0,
            window=self.main_frame,
            anchor="center",
            tags="centered_frame"
        )
        
        # Pencere yeniden boyutlandırma olayı
        self.canvas.bind("<Configure>", self.on_resize)

        # Başlık
        tk.Label(
            self.main_frame,
            text="DURUŞ (POSTÜR) ANALİZİ UYARI SİSTEMİ", 
            font=("Segoe UI", 28, "bold"),
            bg=C_BG,
            fg=C_TEXT_MAIN
        ).pack(pady=(0, 40))

        # Kullanıcı bilgileri
        name_frame = tk.Frame(self.main_frame, bg=C_BG)
        name_frame.pack(pady=(0, 40))

        # Kullanıcı adı ve soyadı giriş alanları
        tk.Label(
            name_frame,
            text="KİŞİNİN ADI:",
            font=("Segoe UI", 10, "bold"),
            bg=C_BG,
            fg=C_PRIMARY
        ).pack()

        self.entry_name = tk.Entry(
            name_frame,
            font=("Segoe UI", 13),
            width=40,
            bg=C_CARD,
            fg=C_TEXT_MAIN, 
            insertbackground="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#334155"
        )
        self.entry_name.pack(pady=(5, 20), ipady=5)
        
        tk.Label(
            name_frame,
            text="KİŞİNİN SOYADI:",
            font=("Segoe UI", 10, "bold"),
            bg=C_BG,
            fg=C_PRIMARY
        ).pack()

        self.entry_surname = tk.Entry(
            name_frame,
            font=("Segoe UI", 13),
            width=40,
            bg=C_CARD,
            fg=C_TEXT_MAIN, 
            insertbackground="white",
            bd=0,
            highlightthickness=1,
            highlightbackground="#334155"
        )
        self.entry_surname.pack(pady=5, ipady=5)
        
        # Analiz seçenek kartları
        cards_container = tk.Frame(self.main_frame, bg=C_BG)
        cards_container.pack()

        # Kart ve buton stil ayarları
        card_opts = {
            "bg": C_CARD,
            "padx": 35,
            "pady": 35,
            "highlightthickness": 1,
            "highlightbackground": "#334155"
        }
        
        btn_opts = {
            "font": ("Segoe UI", 11, "bold"),
            "width": 22,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "fg": "white"
        }

        # Canlı analiz kartı
        self.c_left = tk.Frame(cards_container, **card_opts)
        self.c_left.grid(row=0, column=0, padx=20)
        
        tk.Label(
            self.c_left,
            text="CANLI ANALİZ",
            font=("Segoe UI", 15, "bold"),
            bg=C_CARD,
            fg=C_SUCCESS
        ).pack(pady=(0, 10))
        
        tk.Label(
            self.c_left,
            text="Kamera üzerinden\ngerçek zamanlı ölçüm yapar.",
            font=("Segoe UI", 10),
            bg=C_CARD,
            fg=C_TEXT_SUB
        ).pack(pady=(0, 25))
        
        tk.Button(
            self.c_left,
            text="KAMERAYI BAŞLAT",
            bg=C_SUCCESS,
            activebackground="#16a34a",
            **btn_opts,
            command=self.start_cam
        ).pack()

        # Statik analiz kartı
        self.c_right = tk.Frame(cards_container, **card_opts)
        self.c_right.grid(row=0, column=1, padx=20)
        
        tk.Label(
            self.c_right,
            text="STATİK ANALİZ",
            font=("Segoe UI", 15, "bold"),
            bg=C_CARD,
            fg=C_PRIMARY
        ).pack(pady=(0, 10))
        
        tk.Label(
            self.c_right,
            text="Kayıtlı bir fotoğrafı\ndetaylıca analiz eder.",
            font=("Segoe UI", 10),
            bg=C_CARD,
            fg=C_TEXT_SUB
        ).pack(pady=(0, 25))
        
        tk.Button(
            self.c_right,
            text="FOTOĞRAF YÜKLE",
            bg=C_PRIMARY,
            activebackground="#2563eb",
            **btn_opts,
            command=self.start_file
        ).pack()

    def on_resize(self, event):
        """Pencere boyutu değiştikçe ızgarayı ve paneli merkezler."""
        # Pencere yeniden boyutlandığında arayüz düzenini korur
        w, h = event.width, event.height

        # Önce mevcut ızgara çizgileri temizlenir
        self.canvas.delete("grid_line")

        # Yeni pencere boyutuna göre arka plan ızgarası çizilir
        for i in range(0, w, 50):
            self.canvas.create_line(i, 0, i, h, fill="#1e293b", tags="grid_line")
        for i in range(0, h, 50):
            self.canvas.create_line(0, i, w, i, fill="#1e293b", tags="grid_line")

        # Ana panel her zaman pencerenin ortasında tutulur
        self.canvas.coords("centered_frame", w/2, h/2)
        

    def start_cam(self):
        # Canlı analiz modu seçildiğinde tetiklenir
        # Kamera tabanlı analiz akışını başlatır
        global mod_secimi, tam_ad

        ad = self.entry_name.get().strip()
        soyad = self.entry_surname.get().strip()
        tam_ad = f"{ad} {soyad}".strip() if ad or soyad else "Belirtilmedi"

        mod_secimi = 1;
        self.root.destroy()

    def start_file(self):
        # Statik analiz modu seçildiğinde tetiklenir
        # Seçilen görüntü dosyası analiz akışına aktarılır
        global mod_secimi, secilen_dosya, tam_ad
        
        ad = self.entry_name.get().strip()
        soyad = self.entry_surname.get().strip()
        tam_ad = f"{ad} {soyad}".strip() if ad or soyad else "Belirtilmedi"

        yol = filedialog.askopenfilename(
            filetypes=[("Resim Dosyaları", "*.jpg *.jpeg *.png")]
        )
        
        if yol:
            mod_secimi = 2;
            secilen_dosya = yol;
            self.root.destroy()

def sistem_baslat():
    """
    Sistem başlangıç noktasıdır.
    Analiz süreci, soyut AnalizModu yapısına
    uygun şekilde tasarlanmıştır.
    """
    # Ana uygulama akışı ve mod seçimi burada yönetilir
    global rapor_tetiklendi

    analiz_modu: AnalizModu | None = None

    # Giriş paneli (kullanıcıdan veri ve mod seçimi)
    root = tk.Tk()
    app = BiomechProPanel(root)
    root.mainloop()

    # Kullanıcı herhangi bir mod seçmeden çıktıysa
    if mod_secimi is None:
        return

    # Analiz sürecinde kullanılacak servis nesneleri
    beyin = PosturHesaplayici()
    arayuz = ArayuzYoneticisi()
    rapor_servisi = RaporYoneticisi()

    def renk_belirle(aci, tip):
        # Açı değerine göre görsel uyarı rengini belirler
        if aci < SINIRLAR[tip]["sari"]:
            return arayuz.RENK_CY_YESIL
        elif aci < SINIRLAR[tip]["kirmizi"]:
            return arayuz.RENK_CY_SARI
        else:
            return arayuz.RENK_CY_KIRMIZI

    def cizim_yap(img, lm, ao, ab, ay, aom):
        # Hesaplanan açı değerlerine göre eklem ve iskelet çizimleri yapar
        pts = {k: (int(v[0]), int(v[1])) for k, v in lm.items()}

        ry = renk_belirle(ay, "yuz")
        if 2 in pts and 5 in pts:
            arayuz.neon_cizgi(img, pts[2], pts[5], ry, 2)
            
        if 0 in pts and 9 in pts and 10 in pts:
            # Baş ve yüz hizasına ait merkez çizimleri
            ag_m = (
                (pts[9][0]+pts[10][0])//2,
                (pts[9][1]+pts[10][1])//2
            )
            arayuz.neon_cizgi(img, pts[0], ag_m, ry, 2)
            arayuz.neon_nokta(img, pts[0], arayuz.RENK_BEYAZ)
            
        rb = renk_belirle(ab, "boyun")
        if 0 in pts and 11 in pts and 12 in pts:
            om_m = (
                (pts[11][0] + pts[12][0]) // 2,
                (pts[11][1] + pts[12][1]) // 2
            )
            arayuz.neon_cizgi(img, pts[0], om_m, rb, 2)
            
        ro = renk_belirle(ao, "omuz")
        rom = renk_belirle(aom, "omurga")
        renk_belirle(aom, "omurga")
        
        if 11 in pts and 12 in pts:
            arayuz.neon_cizgi(img, pts[11], pts[12], ro, 4)
            
            if 23 in pts and 24 in pts:
                # Omuz ve kalça merkez noktaları
                om_m = (
                    (pts[11][0] + pts[12][0]) // 2,
                    (pts[11][1] + pts[12][1]) // 2
                )

                km_m = (
                    (pts[23][0] + pts[24][0]) // 2,
                    (pts[23][1] + pts[24][1]) // 2
                )
                
                # Omurga hizası çizimleri
                arayuz.neon_cizgi(img, om_m, km_m, rom, 3)
                arayuz.neon_cizgi(img, pts[23], pts[24], rom, 3)

                # Kol ve bacak bağlantı çizimleri
                for b in [
                    (11, 13), (13, 15),
                    (12, 14), (14, 16),
                    (23, 25), (25, 27),
                    (24, 26), (26, 28)
                ]:
                    if b[0] in pts and b[1] in pts:
                        arayuz.neon_cizgi(img, pts[b[0]], pts[b[1]], ro, 2)
        
    def hassas_puan_motoru(ao, ab, ay, aom):
        """
        Bölgesel açı sapmalarına göre
        genel duruş puanını ve risk seviyesini hesaplar.

        Parametreler:
        ao  -> omuz açısı
        ab  -> boyun açısı
        ay  -> yüz açısı
        aom -> omurga açısı
        """

        def ceza(aci, tip):
            """
            Verilen açı ve bölge tipine göre
            ceza puanını hesaplar.
            """
            sari = SINIRLAR[tip]["sari"]
            kirmizi = SINIRLAR[tip]["kirmizi"]

            # Sarı eşik altındaysa hafif ceza
            if aci < sari:
                return (aci / sari) * 4.5
            # Kırmızı eşik üstünde artan ceza
            else:
                return 5 + ((aci - sari) / (kirmizi - sari) * 18)

        # Her bölge için hesaplanan ceza değerleri
        cezalar = {
            "Omuz": ceza(ao, "omuz"),
            "Boyun": ceza(ab, "boyun"),
            "Yüz": ceza(ay, "yuz"),
            "Omurga": ceza(aom, "omurga")
        }

        # Toplam cezalara göre genel puan (0–100 arası)
        puan = int(max(0, 100 - sum(cezalar.values())))

        # Puana göre risk seviyesi belirleme
        if puan >= 80:
            seviye = 1          # İyi / Optimal
        elif puan >= 50:
            seviye = 2          # Orta / Dikkat
        else:
            seviye = 3          # Kötü / Kritik

        # En fazla sapma gösteren bölge
        en_kritik_bolge = max(cezalar, key=cezalar.get)

        return puan, seviye, f"{en_kritik_bolge} sapması saptandı."

    if mod_secimi == 1:
        # --- CANLI ANALİZ MODU (KAMERA) ---

        # Kamera başlatılır
        kamera = KameraYoneticisi(0)
        kamera.baslat()

        # Sesli uyarılar için zamanlayıcılar
        son_sari_uyari = time.time()
        son_kirmizi_uyari = time.time()
        
        # Tam ekran analiz penceresi
        cv2.namedWindow("Analiz", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "Analiz",
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

        # Mouse tıklamaları (rapor butonu) dinlenir
        cv2.setMouseCallback("Analiz", fare_olayi, arayuz)

        # Kamera kareleri okunur
        while True:
            ret, frame = kamera.kare_oku()
            if not ret:
                break

            # Görüntü üzerinde vücut tespiti yapılır
            img, sonuc = beyin.vucut_tara(frame)

            # Varsayılan değerler
            ao = ab = ay = aom = 0
            puan = 100
            seviye = 1
            
            # Eğer vücut landmarkları bulunduysa
            if sonuc.pose_landmarks:
                # Omuz ve yüz açısı hesaplanır
                ao, ay, lm = beyin.detayli_analiz(
                    sonuc.pose_landmarks.landmark,
                    frame.shape[1],
                    frame.shape[0]
                )

                # Omuz merkezi
                omuz_merkez = (
                    (lm[11][0] + lm[12][0]) / 2,
                    (lm[11][1] + lm[12][1]) / 2
                )

                # Boyun açısı
                ab = np.degrees(
                    np.arctan2(
                        abs(lm[0][0] - omuz_merkez[0]),
                        abs(lm[0][1] - omuz_merkez[1])
                    )
                )

                # Omurga açısı (kalça varsa)
                if 23 in lm and 24 in lm:
                    kalca_merkez = (
                        (lm[23][0] + lm[24][0]) / 2,
                        (lm[23][1] + lm[24][1]) / 2
                    )

                    aom = np.degrees(
                        np.arctan2(
                            abs(omuz_merkez[0] - kalca_merkez[0]),
                            abs(omuz_merkez[1] - kalca_merkez[1])
                        )
                    )

                # Genel puan ve seviye hesaplanır
                puan, seviye, msg = hassas_puan_motoru(
                    ao, ab, ay, aom
                )

                # Raporlama servisine veri eklenir
                rapor_servisi.veri_ekle(
                    puan, seviye, ao, ab, msg
                )

                # İskelet ve yardımcı çizimler
                cizim_yap(img, lm, ao, ab, ay, aom)

                # Sesli uyarılar
                simdi = time.time()

                # Sarı seviye: daha seyrek uyarı
                if seviye == 2 and simdi - son_sari_uyari > 1.0:
                    winsound.Beep(800, 150)
                    son_sari_uyari = simdi

                # Kırmızı seviye: sık uyarı
                if seviye == 3 and simdi - son_kirmizi_uyari > 0.4:
                    winsound.Beep(1000, 100)
                    son_kirmizi_uyari = simdi

            # Arayüz ve bilgi paneli çizilir
            final = arayuz.arayuzu_ciz(
                img, ao, ab, ay, aom, puan, seviye
            )

            cv2.imshow("Analiz", final)

            # Rapor oluşturma veya çıkış
            if cv2.waitKey(1) & 0xFF == ord("r") or rapor_tetiklendi:
                yol = rapor_servisi.raporu_kaydet(
                    final, puan, tam_ad
                )
                messagebox.showinfo(
                    "Bitti",
                    f"Kişi: {tam_ad}\nRapor: {yol}"
                )
                break

        # Kamera kapatılır
        kamera.kapat()

    elif mod_secimi == 2 and secilen_dosya:
        # --- STATİK ANALİZ MODU (FOTOĞRAF) ---

        # Fotoğraf dosyası okunur
        f_raw = cv2.imdecode(
            np.fromfile(secilen_dosya, dtype=np.uint8),
            cv2.IMREAD_UNCHANGED
        )

        # Orijinal boyutlar
        h_r, w_r = f_raw.shape[:2]

        # Analiz için boş tuval
        tuval = np.zeros((720, 1280, 3), dtype=np.uint8)

        # Fotoğrafı tuvale sığdırmak için ölçek hesaplanır
        olcek = min(1280 / w_r, 720 / h_r)
        yeni_w = int(w_r * olcek)
        yeni_h = int(h_r * olcek)

        # Fotoğraf yeniden boyutlandırılır
        f_resized = cv2.resize(f_raw, (yeni_w, yeni_h))

        # Fotoğraf tuvalin ortasına yerleştirilir
        tuval[
            (720 - yeni_h) // 2:(720 - yeni_h) // 2 + yeni_h,
            (1280 - yeni_w) // 2:(1280 - yeni_w) // 2 + yeni_w
        ] = f_resized

        # Vücut analizi yapılır
        img_islenmis, sonuc = beyin.vucut_tara(tuval)

        # Varsayılan değerler
        ao = ab = ay = aom = 0
        puan = 100
        seviye = 1
        msg = ""

        # Eğer landmarklar bulunduysa
        if sonuc.pose_landmarks:
            ao, ay, lm = beyin.detayli_analiz(
                sonuc.pose_landmarks.landmark,
                1280,
                720
            )

            # Omuz merkezi
            omuz_merkez = (
                (lm[11][0] + lm[12][0]) / 2,
                (lm[11][1] + lm[12][1]) / 2
            )

            # Boyun açısı
            ab = np.degrees(
                np.arctan2(
                    abs(lm[0][0] - omuz_merkez[0]),
                    abs(lm[0][1] - omuz_merkez[1])
                )
            )

            # Omurga açısı
            if 23 in lm and 24 in lm:
                kalca_merkez = (
                    (lm[23][0] + lm[24][0]) / 2,
                    (lm[23][1] + lm[24][1]) / 2
                )

                aom = np.degrees(
                    np.arctan2(
                        abs(omuz_merkez[0] - kalca_merkez[0]),
                        abs(omuz_merkez[1] - kalca_merkez[1])
                    )
                )

            # Puan ve seviye hesaplanır
            puan, seviye, msg = hassas_puan_motoru(
                ao, ab, ay, aom
            )

            # İskelet çizimleri
            cizim_yap(
                img_islenmis, lm, ao, ab, ay, aom
            )

        # Tam ekran analiz penceresi
        cv2.namedWindow("Analiz", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            "Analiz",
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )
        
         # Rapor butonu için mouse dinleyici
        cv2.setMouseCallback("Analiz", fare_olayi, arayuz)
        rapor_tetiklendi = False

        # Kullanıcı etkileşimi
        while True:
            final_foto = arayuz.arayuzu_ciz(
                img_islenmis.copy(),
                ao,
                ab,
                ay,
                aom,
                puan,
                seviye
            )

            cv2.imshow("Analiz", final_foto)

            # Rapor al veya çık
            if cv2.waitKey(1) & 0xFF == ord("r") or rapor_tetiklendi:
                rapor_servisi.veri_ekle(
                    puan, seviye, ao, ab, msg
                )

                yol = rapor_servisi.raporu_kaydet(
                    final_foto,
                    puan,
                    tam_ad
                )

                messagebox.showinfo(
                    "Bitti",
                    f"Kişi: {tam_ad}\nRapor: {yol}"
                )
                break

    # Tüm OpenCV pencereleri güvenli şekilde kapatılır
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sistem_baslat()
