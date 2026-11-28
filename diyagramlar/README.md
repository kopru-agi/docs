# Diyagramlar

Diyagramlar **koddan üretilir**. Böylece değişiklikler PR'da satır satır incelenebilir ve tüm diyagramlar aynı görünür.

| Dosya | İçerik |
|---|---|
| [`svg/uc-0-genel-bakis.svg`](svg/uc-0-genel-bakis.svg) | UC-0 Genel bakış: tüm aktörler ve ana kullanım durumları |
| [`svg/uc-1-is-arayan.svg`](svg/uc-1-is-arayan.svg) | UC-1 İş arayan ve üye |
| [`svg/uc-2-referans.svg`](svg/uc-2-referans.svg) | UC-2 Referans |
| [`svg/uc-3-yonetici-sistem.svg`](svg/uc-3-yonetici-sistem.svg) | UC-3 Yönetici ve sistem |
| [`svg/zaman-plani.svg`](svg/zaman-plani.svg) | Zaman planı (Gantt) |
| `er.svg` | Veritabanı ER diyagramı (İP-11, bekliyor) |

Her SVG'nin yanında rapor için `.png` kopyası vardır. Senaryolar: [`analiz/use-case-senaryolari.md`](../analiz/use-case-senaryolari.md).

## Nasıl değiştirilir?

1. Use case diyagramı için `uretici.py` içindeki `DIYAGRAMLAR` tanımını, zaman planı için `zaman_plani.py` içindeki `ISLER` listesini düzenleyin.
2. Betiği çalıştırın:
   ```
   python diyagramlar/uretici.py
   python diyagramlar/zaman_plani.py
   ```
3. PNG kopyasını güncelleyin (Chrome açıksa ayrı bir profil klasörü verin):
   ```
   chrome --headless=new --disable-gpu --hide-scrollbars --user-data-dir=<boş klasör> --force-device-scale-factor=2 --screenshot=<png yolu> --window-size=<genişlik>,<yükseklik> file:///<svg yolu>
   ```
4. Raporu yeniden üretin: `python rapor/olustur.py`
