# Arayüz Taslakları (Wireframe)

Köprü platformunun düşük çözünürlüklü, gri tonlu arayüz taslakları (v1). Taslaklar tasarım değildir: renk, yazı tipi ve görseller bilerek yer tutucu bırakılmıştır. Tüm kişi ve şirket adları uydurmadır.

- Mobil çerçeve: 390 px genişlik (uzun ekranlar dikey olarak uzatılmıştır).
- Masaüstü çerçeve: 1440 x 900 px.
- Her ekranın sol üst köşesinde ekran kodu yazar (ör. `W-06 Talep oluştur (mobil)`).

## Ekranlar

| Kod | Ekran | Görünüm | Aktör | Gereksinimler | Görsel | Kaynak |
|---|---|---|---|---|---|---|
| W-01 | Karşılama / nasıl çalışır | mobil | Ziyaretçi | FR-01, FR-14, NFR-07 | [PNG](png/w01-karsilama-mobil.png) | [HTML](src/w01-karsilama-mobil.html) |
| W-01 | Karşılama / nasıl çalışır | masaüstü | Ziyaretçi | FR-01, FR-14, NFR-07 | [PNG](png/w01-karsilama-masaustu.png) | [HTML](src/w01-karsilama-masaustu.html) |
| W-02 | Kayıt ve giriş (e-posta bağlantısı + GSM) | mobil | Üye | FR-01, FR-11 | [PNG](png/w02-kayit-giris-mobil.png) | [HTML](src/w02-kayit-giris-mobil.html) |
| W-03 | Referans davet et ve davet listesi | mobil | Üye | FR-02, FR-05, FR-14, NFR-07 | [PNG](png/w03-davet-mobil.png) | [HTML](src/w03-davet-mobil.html) |
| W-04 | Davet kabul: aydınlatma, açık rıza, bilgiler, doğrulama, bağ soruları | mobil | Referans | FR-03, FR-04, FR-11, NFR-07 | [PNG](png/w04-davet-kabul-mobil.png) | [HTML](src/w04-davet-kabul-mobil.html) |
| W-05 | Referans profili ve kriterleri | mobil | Referans | FR-04, FR-06, FR-13, NFR-07 | [PNG](png/w05-referans-profili-mobil.png) | [HTML](src/w05-referans-profili-mobil.html) |
| W-06 | Talep oluştur (kilitli durum) | mobil | İş arayan | FR-07, FR-14, FR-15, NFR-07 | [PNG](png/w06-talep-olustur-mobil.png) | [HTML](src/w06-talep-olustur-mobil.html) |
| W-06 | Talep oluştur (açık durum) | masaüstü | İş arayan | FR-07, FR-08, FR-14, FR-15, NFR-07 | [PNG](png/w06-talep-olustur-masaustu.png) | [HTML](src/w06-talep-olustur-masaustu.html) |
| W-07 | Gelen talep: Kabul et / Nazikçe reddet / Daha sonra | mobil | Referans | FR-08, FR-09, FR-13, NFR-07 | [PNG](png/w07-gelen-talep-mobil.png) | [HTML](src/w07-gelen-talep-mobil.html) |
| W-07 | Gelen talepler + kabul sonrası CV ve mesajlaşma | masaüstü | Referans | FR-08, FR-09, FR-10, FR-13, NFR-07 | [PNG](png/w07-gelen-talep-masaustu.png) | [HTML](src/w07-gelen-talep-masaustu.html) |
| W-08 | Taleplerim ve durumları | mobil | İş arayan | FR-09, FR-10, NFR-07 | [PNG](png/w08-taleplerim-mobil.png) | [HTML](src/w08-taleplerim-mobil.html) |
| W-09 | Hesabım: verimi indir, hesabımı sil, rıza kayıtları | mobil | Üye / Referans | FR-11, FR-12, NFR-03 | [PNG](png/w09-hesabim-mobil.png) | [HTML](src/w09-hesabim-mobil.html) |
| W-10 | Yönetici: dondurma ve itiraz kuyruğu | masaüstü | Yönetici | FR-12, FR-13, FR-11, NFR-07 | [PNG](png/w10-yonetici-masaustu.png) | [HTML](src/w10-yonetici-masaustu.html) |

## Gereksinim kodları

| Kod | Konu | Ekranlar |
|---|---|---|
| FR-01 | Kayıt / giriş | W-01, W-02 |
| FR-02 | Davet | W-03 |
| FR-03 | Davet kabul + rıza | W-04 |
| FR-04 | Doğrulama | W-04, W-05 |
| FR-05 | Davet silme (14 gün) | W-03 |
| FR-06 | Referans kriterleri | W-05 |
| FR-07 | Talep oluştur | W-06 |
| FR-08 | Bildirim / eşleştirme | W-06, W-07 |
| FR-09 | Kabul / ret | W-07, W-08 |
| FR-10 | Platform içi iletişim | W-07 (masaüstü), W-08 |
| FR-11 | Kayıt tutma | W-02, W-04, W-09, W-10 |
| FR-12 | Dondurma / itiraz | W-09, W-10 |
| FR-13 | Aktiflik | W-05, W-07, W-10 |
| FR-14 | Arama kilidi (referans eşiği) | W-01, W-03, W-06 |
| FR-15 | Arama kilidi (süre / katkı) | W-06 |
| NFR-03 | Veri indirme / silme | W-09 |
| NFR-07 | Gizlilik | W-01, W-03 – W-08, W-10 |

## Notlar

- W-04 tek uzun ekran olarak çizilmiştir. Uygulamada 4 adımlı bir sihirbaz olur; üstteki adım göstergesi 2. adımı gösterir.
- W-06 mobilde kilitli durumu (2/3 onaylı referans), masaüstünde açık durumu gösterir.
- İş arayan hiçbir ekranda kişi aramaz veya listelemez. Referans kimliği yalnızca "Kabul edildi" durumundan sonra görünür.

## Yeniden üretme

Kaynaklar tek dosyalık HTML'dir (satır içi CSS, dış kaynak yok). PNG'ler başsız Chrome ile alınır:

```
chrome.exe --headless=new --disable-gpu --hide-scrollbars --screenshot=<png yolu> --window-size=390,<yükseklik> file:///<html yolu>
```

Masaüstü için `--window-size=1440,900` kullanılır. Her PNG 1 MB altındadır.
