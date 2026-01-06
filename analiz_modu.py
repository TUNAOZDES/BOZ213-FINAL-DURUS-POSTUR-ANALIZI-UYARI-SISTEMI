"""
Dosya Adı: analiz_modu.py

Amaç:
Bu dosya, sistemde kullanılabilecek tüm analiz türleri için
ortak bir çatı (arayüz) tanımlar.

Canlı analiz (kamera), statik analiz (fotoğraf) gibi
farklı analiz yaklaşımlarının tek bir standart altında
toplanmasını sağlar.

Bu sayede:
- Analiz türleri birbirinden bağımsız geliştirilir
- Sistemin genişletilebilirliği (scalability) artar
- Ana program analiz detaylarından soyutlanır

OOP Katkısı:
- Soyutlama (Abstraction)
- Çok Biçimlilik (Polymorphism)
- Açık/Kapalı Prensibi (Open–Closed Principle)

Not:
Bu sınıf doğrudan kullanılmaz.
Sadece diğer analiz sınıfları için bir şablon görevi görür.
"""

from abc import ABC, abstractmethod


class AnalizModu(ABC):
    """
    AnalizModu, sistemdeki tüm analiz modları için
    soyut (abstract) bir temel sınıftır.

    Canlı analiz ve statik analiz gibi tüm analiz türleri
    bu sınıftan türetilmelidir.

    Bu yapı sayesinde ana sistem, hangi analiz türünün
    kullanıldığını bilmeden analiz sürecini başlatabilir.
    """

    @abstractmethod
    def baslat(self):
        """
        Analiz sürecini başlatan zorunlu metottur.

        Bu metot:
        - Alt sınıflar tarafından mutlaka override edilmelidir
        - Analiz akışının nasıl çalışacağını belirler

        Örnek:
        - Canlı analizde kamera açma ve döngü başlatma
        - Statik analizde dosya okuma ve tek kare analizi
        """
        pass
