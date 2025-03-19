from collections import defaultdict, deque
import heapq
from typing import Dict, List, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

    def __lt__(self, other: 'Istasyon'):
        return self.idx < other.idx  # ID'ye göre karşılaştır

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar.get(istasyon1_id)
        istasyon2 = self.istasyonlar.get(istasyon2_id)
        if istasyon1 and istasyon2:
            istasyon1.komsu_ekle(istasyon2, sure)
            istasyon2.komsu_ekle(istasyon1, sure)

    def heuristik(self, istasyon1: Istasyon, hedef_id: str) -> int:
        return abs(int(istasyon1.idx[1]) - int(hedef_id[1]))  # Basit bir heuristik

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        pq = [(0 + self.heuristik(self.istasyonlar[baslangic_id], hedef_id), 0, self.istasyonlar[baslangic_id], [self.istasyonlar[baslangic_id]])]
        ziyaret_edildi = {}
        while pq:
            f, toplam_sure, mevcut, rota = heapq.heappop(pq)
            if mevcut.idx == hedef_id:
                return (rota, toplam_sure)
            if mevcut.idx in ziyaret_edildi and ziyaret_edildi[mevcut.idx] <= toplam_sure:
                continue
            ziyaret_edildi[mevcut.idx] = toplam_sure
            for komsu, sure in mevcut.komsular:
                yeni_sure = toplam_sure + sure
                heapq.heappush(pq, (yeni_sure + self.heuristik(komsu, hedef_id), yeni_sure, komsu, rota + [komsu]))
        return None

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        kuyruk = deque([(self.istasyonlar[baslangic_id], [self.istasyonlar[baslangic_id]])])
        ziyaret_edildi = set()
        while kuyruk:
            mevcut, rota = kuyruk.popleft()
            if mevcut.idx == hedef_id:
                return rota
            ziyaret_edildi.add(mevcut.idx)
            for komsu, _ in mevcut.komsular:
                if komsu.idx not in ziyaret_edildi:
                    kuyruk.append((komsu, rota + [komsu]))
        return None

if __name__ == "__main__":
    metro = MetroAgi()

    # İzmir Metro Hatları
    # Mavi Hat (Konak - Fahrettin Altay)
    metro.istasyon_ekle("K1", "Konak", "Mavi Hat")
    metro.istasyon_ekle("K2", "Basmane", "Mavi Hat")
    metro.istasyon_ekle("K3", "Çankaya", "Mavi Hat")
    metro.istasyon_ekle("K4", "Fahrettin Altay", "Mavi Hat")
    
    # Turuncu Hat (Halkapınar - Evka 3)
    metro.istasyon_ekle("T1", "Halkapınar", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Süleyman Demirel", "Turuncu Hat")
    metro.istasyon_ekle("T3", "Evka 3", "Turuncu Hat")
    
    # Bağlantılar ekleme
    metro.baglanti_ekle("K1", "K2", 3)
    metro.baglanti_ekle("K2", "K3", 5)
    metro.baglanti_ekle("K3", "K4", 7)
    metro.baglanti_ekle("T1", "T2", 6)
    metro.baglanti_ekle("T2", "T3", 8)
    
    # Hat aktarma bağlantısı
    metro.baglanti_ekle("K2", "T1", 4)

    # Ankara Metro Hatları
    # Kırmızı Hat (Kızılay - OSB)
    metro.istasyon_ekle("A1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("A2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("A3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("A4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat (AŞTİ - Gar)
    metro.istasyon_ekle("B1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("B2", "Kızılay", "Mavi Hat")
    metro.istasyon_ekle("B3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("B4", "Gar", "Mavi Hat")
    
    # Turuncu Hat (Batıkent - Keçiören)
    metro.istasyon_ekle("C1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("C2", "Demetevler", "Turuncu Hat")
    metro.istasyon_ekle("C3", "Gar", "Turuncu Hat")
    metro.istasyon_ekle("C4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    metro.baglanti_ekle("A1", "A2", 4)
    metro.baglanti_ekle("A2", "A3", 6)
    metro.baglanti_ekle("A3", "A4", 8)
    metro.baglanti_ekle("B1", "B2", 5)
    metro.baglanti_ekle("B2", "B3", 3)
    metro.baglanti_ekle("B3", "B4", 4)
    metro.baglanti_ekle("C1", "C2", 7)
    metro.baglanti_ekle("C2", "C3", 9)
    metro.baglanti_ekle("C3", "C4", 5)
    
    # Hat aktarma bağlantıları
    metro.baglanti_ekle("A1", "B2", 2)
    metro.baglanti_ekle("A3", "C2", 3)
    metro.baglanti_ekle("B4", "C3", 2)

    # İzmir Test Senaryoları
    print("\n=== İzmir Metro Test Senaryoları ===")
    print("\n1. Konak -> Fahrettin Altay")
    rota = metro.en_az_aktarma_bul("K1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("K1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n2. Basmane -> Halkapınar")
    rota = metro.en_az_aktarma_bul("K2", "T1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("K2", "T1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Ankara Test Senaryoları
    print("\n=== Ankara Metro Test Senaryoları ===")
    print("\n3. AŞTİ -> OSB")
    rota = metro.en_az_aktarma_bul("B1", "A4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("B1", "A4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n4. Demetevler -> Keçiören")
    rota = metro.en_az_aktarma_bul("C2", "C4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("C2", "C4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    print("\n5. Keçiören -> AŞTİ")
    rota = metro.en_az_aktarma_bul("C4", "B1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    sonuc = metro.en_hizli_rota_bul("C4", "B1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))