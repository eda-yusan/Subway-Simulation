# Metro Simülasyonu

Bu proje, İzmir ve Ankara metro ağlarında iki istasyon arasında en hızlı rotayı (A* algoritması ile) ve en az aktarmalı rotayı (BFS algoritması ile) bulan bir Python uygulamasıdır. Metro istasyonları, hatlar ve bağlantılar bir graf yapısı olarak modellenmiş, ardından yol bulma algoritmaları ile kullanıcıya optimum çözümler sunulmuştur.

---

## 📌 Kullanılan Teknolojiler ve Kütüphaneler

Bu proje, Python programlama dili ile geliştirilmiştir ve aşağıdaki kütüphaneleri kullanır:

- **`collections`**: 
  - `defaultdict`: Hatlara bağlı istasyonları otomatik bir liste ile eşlemek için kullanılır.
  - `deque`: BFS algoritmasında kuyruk yapısı olarak, ilk giren ilk çıkar (FIFO) mantığıyla çalışır.
- **`heapq`**: A* algoritması için öncelik kuyruğu (min-heap) sağlar. En düşük maliyetli rotayı hızlıca seçmek için kullanılır.
- **`typing`**: Kodun okunabilirliğini artırmak ve tip kontrolü sağlamak için `Dict`, `List`, `Tuple`, `Optional` gibi tip tanımlamaları içerir.

Ek bir bağımlılık yoktur; standart Python kütüphaneleri ile çalışır.

---

## 🧠 Algoritmaların Çalışma Mantığı

### BFS (Breadth-First Search - Genişlik Öncelikli Arama)
- **Nasıl Çalışır?**
  - Bir kuyruk (`deque`) kullanarak başlangıç istasyonundan başlar ve tüm komşuları genişlik öncelikli olarak keşfeder.
  - Her seviye tamamlanmadan bir sonraki seviyeye geçmez, böylece en az aktarma gerektiren rotayı ilk bulan algoritmadır.
  - Süreyi dikkate almaz, sadece istasyon geçiş sayısını (düğüm sayısını) optimize eder.
- **Kullanım Yeri:** `en_az_aktarma_bul` fonksiyonunda, kullanıcıya aktarma sayısını minimize eden rota sunar.

### A* (A Yıldız) Algoritması
- **Nasıl Çalışır?**
  - Maliyet (`g(n)`: başlangıçtan mevcut noktaya süre) ve sezgisel tahmin (`h(n)`: hedeften tahmini süre) toplamını (`f(n) = g(n) + h(n)`) hesaplar.
  - Öncelik kuyruğu (`heapq`) ile her zaman en düşük `f(n)` değerine sahip yolu seçer.
  - Basit bir heuristik olarak istasyon kimlik numaralarının farkını (`abs(idx1 - idx2)`) kullanır.
- **Kullanım Yeri:** `en_hizli_rota_bul` fonksiyonunda, en kısa sürede hedefe ulaşan rotayı bulur.

### Neden Bu Algoritmalar?
- **BFS:** En az aktarma ile rota bulmak için idealdir çünkü grafın derinliğine değil genişliğine odaklanır ve ilk bulduğu çözüm minimum düğüm geçişini garanti eder.
- **A star:** Süre optimizasyonu için uygundur; sezgisel tahminle gereksiz yolları eleyerek Dijkstra’dan daha hızlı çalışır ve optimal sonuç verir (heuristik uygun olduğu sürece).

---

## ✅ Örnek Kullanım ve Test Sonuçları

Proje, İzmir ve Ankara metro ağları için test senaryoları içerir. Aşağıda bazı örnekler ve çıktılar yer alıyor:

### İzmir Metro
1. **Konak → Fahrettin Altay**
   - **En Az Aktarmalı Rota:** `Konak -> Basmane -> Çankaya -> Fahrettin Altay`
   - **En Hızlı Rota:** `Konak -> Basmane -> Çankaya -> Fahrettin Altay (15 dakika)`
2. **Basmane → Halkapınar**
   - **En Az Aktarmalı Rota:** `Basmane -> Halkapınar`
   - **En Hızlı Rota:** `Basmane -> Halkapınar (4 dakika)`

### Ankara Metro
3. **AŞTİ → OSB**
   - **En Az Aktarmalı Rota:** `AŞTİ -> Kızılay -> OSB`
   - **En Hızlı Rota:** `AŞTİ -> Kızılay -> OSB (15 dakika)`
4. **Keçiören → AŞTİ**
   - **En Az Aktarmalı Rota:** `Keçiören -> Gar -> AŞTİ`
   - **En Hızlı Rota:** `Keçiören -> Gar -> AŞTİ (11 dakika)`
  
---
     
## 💡 Projeyi Geliştirme Fikirleri

- **Daha İyi Heuristik Fonksiyon:** Şu anki basit `abs(idx farkı)` yerine, gerçek coğrafi mesafeler veya hat bazlı tahminler eklenebilir.
- **Aktarma Maliyeti:** Hat değiştirme sürelerini (örneğin 2 dakika ek süre) modele dahil ederek daha gerçekçi rotalar sunulabilir.
- **Kullanıcı Arayüzü:** Terminal çıktısı yerine bir GUI (örneğin Tkinter ile) veya web arayüzü (Flask/Django) eklenebilir.
- **Dinamik Veri:** Gerçek zamanlı metro verilerini (sefer saatleri, gecikmeler) entegre etmek için bir API bağlanabilir.
