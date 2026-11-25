# Köprü — Analiz ve Tasarım Dokümanları

Bu depo Köprü projesinin **kod öncesi** tüm çıktılarını tutar. Hocamızın istediği sıra:

1. Fonksiyonel ve fonksiyonel olmayan gereksinimler → [`analiz/gereksinimler.md`](analiz/gereksinimler.md)
2. Use case şeması → [`diyagramlar/`](diyagramlar/)
3. Arayüz taslakları → [`wireframe/`](wireframe/)
4. Onaydan sonra geliştirme

## Klasörler

| Klasör | İçerik |
|---|---|
| [`analiz/`](analiz/) | Gereksinim dokümanı (ISO/IEC/IEEE 29148 hafif şablon) |
| [`diyagramlar/`](diyagramlar/) | Use case, aktivite, ER diyagramları (PlantUML kaynak + SVG çıktı) |
| [`wireframe/`](wireframe/) | Ekran taslakları |
| [`kararlar/`](kararlar/) | ADR: verilmiş her önemli karar, gerekçesiyle |
| [`arastirma/`](arastirma/) | Araştırma notları (KVKK, SMS/e-posta, graf ve teşvik, stack ve hosting) |

## Kurallar

- Her değişiklik bir **issue** ve bir **PR** ile gelir. Ayrıntı: [Katkı Rehberi](https://github.com/kopru-agi/.github/blob/main/CONTRIBUTING.md).
- Diyagramların **kaynağı** (`.puml`, `.drawio`) depoya girer. Sadece görsel yüklemek yetmez.
- Dokümanlarda gerçek kişisel veri olmaz. Örnekler sahte isimlerle yazılır.

## Lisans

Bu depodaki dokümanlar [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.tr) lisansı ile paylaşılır.
