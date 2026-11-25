# Gereksinim Dokümanı (Taslak v0.1)

> Şablon: ISO/IEC/IEEE 29148 (hafif). Durum: **taslak**. Maddeler WhatsApp grubundaki hoca yönlendirmelerinden derlenmiştir. ⚠️ ile işaretli maddeler henüz ekipçe karara bağlanmadı.

## 1. Amaç

Öğrencilerin ve ailelerinin çevresindeki çalışan kişileri gönüllü **referans** olarak bir araya getirmek. İş arayan kişiye sahte ilanlar ve uzun süreçler yerine **doğrudan, referanslı başvuru** imkânı vermek.

## 2. Kapsam

**v1 kapsamında:** referans ağı, referanslı başvuru talebi, talep/dönüş kaydı, KVKK uyumlu rıza akışı.

**v1 kapsamı dışında (v2+):** topluluk iş ilanları, newsletter, yapay zekâ ile referans sıralaması, kimlik doğrulama (KYC), mobil uygulama. Bkz. [ADR-0002](../kararlar/0002-v1-yalnizca-referans.md).

## 3. Aktörler

| Aktör | Tanım |
|---|---|
| **Üye (öğrenci)** | Sisteme kayıt olan, referans davet eden ve gerektiğinde iş arayan kişi. |
| **İş arayan** | İş arama hakkını kullanan üye. Sektör ve pozisyon seçer. Kişiler üzerinde arama yapamaz. |
| **Referans** | Davet ile gelen, kendi şirket/sektör/pozisyon bilgisini giren ve onay veren çalışan kişi. |
| **Yönetici** | Hesap dondurma, itiraz inceleme, kötüye kullanım takibi yapan ekip üyesi. |
| **Sistem** | Eşleştirme, bildirim, kayıt ve süre takibini yapan otomatik süreçler. |

## 4. Fonksiyonel gereksinimler

| ID | Gereksinim | Öncelik | Kaynak | Durum |
|---|---|---|---|---|
| FR-01 | Üye e-posta ile kayıt olabilmeli ve giriş yapabilmelidir. | Must | Ekip | Taslak |
| FR-02 | Üye, referans olmasını istediği kişiye **davet** gönderebilmelidir. Davet için yalnızca telefon veya e-posta girilir. | Must | Hoca, KVKK araştırması | Taslak |
| FR-03 | Davet edilen kişi kendi şirket, sektör ve pozisyon bilgisini **kendisi** girer, aydınlatma metnini okur ve açık rıza verir. | Must | KVKK araştırması | Taslak |
| FR-04 | Referans, aktif olmadan önce e-posta ⚠️ ve SMS ⚠️ ile doğrulanmalıdır. Yalnızca TR GSM numaraları (+90 5xx) kabul edilir. | Must | Hoca | ⚠️ SMS sağlayıcı kararı açık |
| FR-05 | Onaylanmayan davetler N gün sonra kalıcı olarak silinmelidir. | Must | KVKK araştırması | ⚠️ N = 7 mi 14 mü |
| FR-06 | Referans kendi kriterlerini belirleyebilmelidir: hangi pozisyonlar, ne tür destek, ayda en fazla kaç talep. | Should | Ekip | Taslak |
| FR-07 | İş arayan yalnızca **sektör ve pozisyon** seçerek talep oluşturur. Referansların listesini veya kimliğini göremez. | Must | Hoca | Taslak |
| FR-08 | Sistem, talebe uygun referansa "böyle bir aday var" bildirimi gönderir. | Must | Hoca | Taslak |
| FR-09 | Referans talebi kabul veya reddedebilir. Kabul ederse adayın CV'sini görür. | Must | Hoca | Taslak |
| FR-10 | İletişim, aday ile referans arasındaki tanıdıklık bağı (zincir) üzerinden kurulur. | Must | Hoca | ⚠️ Zincir mi doğrudan mı |
| FR-11 | Her talep, dönüş ve sonuç kayıt altına alınır. | Must | Hoca | Taslak |
| FR-12 | Dönüş vermeyen veya olumsuz geri bildirim alan referans dondurulur. Dondurmadan önce uyarı ve itiraz hakkı verilir. | Should | Hoca, KVKK m.11 | ⚠️ Eşik değerleri açık |
| FR-13 | Kişinin aktiflik değeri, kendi ve referanslarının davranışı üzerinden hesaplanır ve izlenebilir. | Should | Hoca | ⚠️ Formül açık |
| FR-14 | İş aramak isteyen kişi en az 5 referans eklemiş olmalıdır. | Should | Hoca | ⚠️ "Eklemiş" mi "onaylanmış" mı |
| FR-15 | Yeni üye, katılımdan belirli bir süre sonra iş arayabilir. | Could | Hoca | ⚠️ 3 ay mı, katkıyla erken açılım mı |
| FR-16 | İşe yerleşmeye yardım eden kişi ek arama hakkı kazanır. | Could | Hoca | ⚠️ x2, devredilebilirlik açık |

## 5. Fonksiyonel olmayan gereksinimler

| ID | Kategori | Gereksinim | Durum |
|---|---|---|---|
| NFR-01 | KVKK | Kişisel veri yalnızca açık rıza ile işlenir. Aydınlatma metni ilk temasta gösterilir. | Taslak |
| NFR-02 | KVKK | Kişisel veri Türkiye'de barındırılır (yurt dışı aktarım yükümlülüğünden kaçınmak için). | ⚠️ Hosting kararı açık |
| NFR-03 | KVKK | Kullanıcı verisini indirebilir ve hesabını silebilir. | Taslak |
| NFR-04 | KVKK | CV ve kişisel veriler için saklama süresi tanımlanır ve periyodik imha yapılır. | Taslak |
| NFR-05 | Güvenlik | Tüm trafik HTTPS. Şifreler saklanmaz (e-posta bağlantısı / OTP ile giriş). | Taslak |
| NFR-06 | Güvenlik | Davet, OTP ve talep uç noktalarında hız sınırı (rate limit) uygulanır. | Taslak |
| NFR-07 | Gizlilik | İş arayan, referansların kimliğini kabulden önce göremez. | Taslak |
| NFR-08 | Kullanılabilirlik | Arayüz Türkçedir ve mobil uyumludur. | Taslak |
| NFR-09 | Erişilebilirlik | WCAG 2.2 AA hedeflenir. | Taslak |
| NFR-10 | Maliyet | Aylık işletme maliyeti hosting dahil hedef: 1.000 TL altı. | Taslak |
| NFR-11 | Bakım | Kritik akış (davet → onay → talep → kabul) uçtan uca test ile korunur. | Taslak |

## 6. Varsayımlar ve kısıtlar

- Proje ticari değildir; reklam ve ücret yoktur. Vergi hesaplaması gerekmez.
- Hosting giderini hocamız karşılar.
- Ekip gönüllü öğrencilerden oluşur; deneyim düzeyleri farklıdır.

## 7. Açık sorular

Bkz. ⚠️ işaretli maddeler. Her biri için bir **Karar önerisi (ADR)** issue'su açılacaktır.
