# ADR-0001: GitHub organizasyonu ve çalışma kuralları

- **Durum:** Kabul edildi
- **Tarih:** 2026-11-25

## Bağlam

Ekip 8-12 kişilik, deneyim düzeyleri farklı. Herkesin kendi taslak sitesini yapması önerildi, ancak bu dağınıklık yaratır. Hocamız önce analiz ve tasarımı istedi. Ekipten birinin önceki benzer projesi; kapsam şişmesi, doğrudan `master`'a push, issue/PR kullanılmaması ve depoya üretilmiş dosyaların girmesi yüzünden başarısız oldu.

## Karar

- Tek organizasyon: `kopru-agi`. Depolar **herkese açık** (Free planda dal koruma kuralları yalnızca açık depolarda çalışır; depoda kişisel veri olmayacağı için sakıncası yok).
- Başlangıçta yalnızca `.github` ve `docs` depoları. Uygulama deposu analiz onayından sonra açılır.
- `main` korumalı: PR + 1 onay, squash merge, force push ve silme kapalı, CI yeşil olmalı.
- Her iş bir issue; proje board'u ile takip.
- Conventional Commits; PR başlığı CI'da kontrol edilir.
- Dokümanlar Türkçe, kod ve commit'ler İngilizce.
- 1 MB üstü dosya, `.env`, anahtar ve cache dosyaları CI'da reddedilir.

## Sonuçlar

- Herkes aynı süreci izler; inceleme zorunlu olduğu için bilgi ekibe yayılır.
- Başlangıçta yavaş gelebilir. Kurallar küçük PR'larla aşılır.
