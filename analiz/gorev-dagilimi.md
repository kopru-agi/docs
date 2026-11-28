# Görev Dağılımı (v1.0)

> Sorumlular **öneridir**. Ekip arkadaşları bir iş paketini GitHub'da ilgili issue'yu kendine atayarak üstlenir. Boş paketler "Gönüllü bekleniyor" olarak işaretlidir.
> Takip: [Köprü Yol Haritası board'u](https://github.com/orgs/kopru-agi/projects/1) · [Issue listesi](https://github.com/kopru-agi/docs/issues)

## 1. Roller

| Rol | Kişi | Sorumluluk |
|---|---|---|
| Proje koordinatörü / maintainer | Iliya Dindar | GitHub organizasyonu, süreç kuralları, PR incelemesi, issue triyajı, hocamızla iletişim |
| Analiz ve dokümantasyon sorumlusu | Gönüllü bekleniyor | Gereksinim ve use case dokümanlarının güncel tutulması |
| UI/UX sorumlusu | Gönüllü bekleniyor | Wireframe → yüksek çözünürlüklü tasarım, kullanılabilirlik testi |
| Veritabanı sorumlusu | Gönüllü bekleniyor | ER modeli, referans ağı tabloları, migration'lar |
| Backend sorumlusu | Gönüllü bekleniyor | Davet, rıza, talep, eşleştirme servisleri |
| Frontend sorumlusu | Gönüllü bekleniyor | Next.js sayfaları, form doğrulama, mobil uyum |
| Test sorumlusu | Gönüllü bekleniyor | Vitest ve Playwright testleri, pilot test planı |
| DevOps sorumlusu | Gönüllü bekleniyor | Sunucu, Coolify, CI/CD, yedekleme |
| KVKK ve hukuk sorumlusu | Gönüllü bekleniyor | Aydınlatma ve açık rıza metinleri, saklama politikası |
| Tanıtım sorumlusu | Gönüllü bekleniyor | Üniversite içi tanıtım, referans kazanımı, sosyal medya |

## 2. İş paketleri

Durum: ✅ tamamlandı · 🟡 devam ediyor · ⚪ bekliyor

| ID | İş paketi | Çıktı | Sorumlu | Hafta | Durum |
|---|---|---|---|---|---|
| İP-01 | GitHub organizasyonu ve çalışma kuralları | `kopru-agi` org, korumalı `main`, CI, şablonlar, board ([ADR-0001](../kararlar/0001-github-org-ve-calisma-kurallari.md)) | Iliya Dindar | H0 | ✅ |
| İP-02 | Ekip kararları için anketler | Depo açıklığı, dil, v1 kapsamı anketleri | Iliya Dindar | H0 | ✅ |
| İP-03 | Araştırma: KVKK, SMS/e-posta, graf, stack | [4 araştırma notu](../arastirma/) | Iliya Dindar | H0 | ✅ |
| İP-04 | Gereksinim analizi | [gereksinimler.md](gereksinimler.md) | Iliya Dindar | H0–H1 | 🟡 onayda |
| İP-05 | Use case diyagramları ve senaryolar | [4 diyagram](../diyagramlar/svg/), [senaryolar](use-case-senaryolari.md) | Iliya Dindar | H0–H1 | 🟡 onayda |
| İP-06 | Arayüz taslakları (wireframe) | [10 ekran](../wireframe/) | Iliya Dindar | H0–H1 | 🟡 onayda |
| İP-07 | İK / yönetici görüşmeleri | 5 görüşme özeti ([#5](https://github.com/kopru-agi/docs/issues/5)) | Gönüllü bekleniyor | H1–H2 | ⚪ |
| İP-08 | Kalıcı proje adı | Öneri + oylama ([#6](https://github.com/kopru-agi/docs/issues/6)) | Tüm ekip | H1 | ⚪ |
| İP-09 | KVKK metinleri | Aydınlatma metni, açık rıza metni, çerez politikası, saklama-imha politikası | Gönüllü bekleniyor | H2–H3 | ⚪ |
| İP-10 | Yüksek çözünürlüklü tasarım | Figma ekranları, bileşen kütüphanesi | Gönüllü bekleniyor | H2–H3 | ⚪ |
| İP-11 | Veri modeli | ER diyagramı, Drizzle şeması | Gönüllü bekleniyor | H2–H3 | ⚪ |
| İP-12 | Altyapı kurulumu | Uygulama deposu, sunucu, Coolify, CI/CD, staging | Gönüllü bekleniyor | H3 | ⚪ |
| İP-13 | Sprint 1: üyelik, davet, rıza | UC-01–UC-05, UC-16 | Backend + Frontend | H4–H5 | ⚪ |
| İP-14 | Sprint 2: talep ve eşleştirme | UC-06, UC-08, UC-09, UC-13 | Backend + Frontend + Veritabanı | H6–H7 | ⚪ |
| İP-15 | Sprint 3: yanıt, kurallar, KVKK hakları | UC-07, UC-10–UC-12, UC-14, UC-15, UC-17 | Backend + Frontend | H8–H9 | ⚪ |
| İP-16 | Test ve pilot | Uçtan uca testler, grup içi pilot (20–30 kişi) | Test sorumlusu + tüm ekip | H10 | ⚪ |
| İP-17 | Düzeltme ve yayına alma | Hata düzeltmeleri, canlı ortam, `security.txt` | DevOps + tüm ekip | H11–H12 | ⚪ |
| İP-18 | Tanıtım ve referans kazanımı | Tanıtım metni, afiş, ilk 100 referans hedefi | Tanıtım sorumlusu | H10–H12 | ⚪ |

## 3. Çalışma kuralları (özet)

- Her iş paketi GitHub'da bir veya daha fazla **issue**'ya bölünür. Bir issue en fazla birkaç günlük iştir.
- Değişiklikler **PR** ile gelir ve en az **1 onay** alır. `main` dalına doğrudan push kapalıdır.
- Haftalık kısa durum notu WhatsApp grubuna yazılır; kararlar `kararlar/` altında ADR olarak kaydedilir.
- Ayrıntı: [Katkı Rehberi](https://github.com/kopru-agi/.github/blob/main/CONTRIBUTING.md).
