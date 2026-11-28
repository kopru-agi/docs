# Gereksinim Analizi (v1.0)

> Şablon: ISO/IEC/IEEE 29148 (hafif). Tarih: 28.11.2026. Durum: **hocalarımızın onayına sunuldu**.
> Kaynaklar: WhatsApp grubundaki hoca yönlendirmeleri, ekip anketleri, [araştırma notları](../arastirma/).

## 1. Amaç

Öğrencilerin ve ailelerinin çevresindeki çalışan kişileri gönüllü **referans** olarak bir araya getirmek. İş arayan kişiye sahte ilanlar ve uzun süreçler yerine **doğrudan, referanslı başvuru** imkânı vermek. Sistemin motoru iyiliktir: referanslar gönüllüdür, platform ücretsizdir.

## 2. Kapsam

| v1 kapsamında | v2 ve sonrası |
|---|---|
| Üyelik, referans daveti, KVKK uyumlu rıza akışı | Topluluk iş ilanları |
| Referans kriterleri ve bağ gücü | Newsletter |
| Sektör + pozisyon ile referanslı talep | Yapay zekâ ile referans sıralaması |
| Ağ içinde eşleştirme (en fazla 3 adım) | x2 arama hakkı (kredi) sistemi |
| Platform içi iletişim, talep/dönüş kaydı | SMS doğrulama (kurum hesabı bulununca) |
| Dondurma, itiraz, aktiflik değeri | Kimlik doğrulama (KYC) |
| KVKK hakları: veri indirme, hesap silme | Mobil uygulama |

Kapsam kararı ekip anketiyle alındı (10 oy, 0 karşı): "V1 sadece referanslardan oluşacak, kalan idealler v2'ye girecek."

## 3. Aktörler

| Aktör | Tanım |
|---|---|
| **Ziyaretçi** | Siteyi gezen, henüz üye olmayan kişi. |
| **Üye** | Kayıt olan öğrenci veya davetle gelen kişi. Referans davet edebilir. |
| **İş arayan** | Arama kilidi açılmış üye. Yalnızca sektör ve pozisyon seçer; kişiler üzerinde arama yapamaz. |
| **Referans** | Daveti kabul eden, kendi şirket/sektör/pozisyon bilgisini giren ve açık rıza veren çalışan. |
| **Yönetici** | Dondurma ve itirazları inceleyen ekip üyesi. |
| **Sistem** | Eşleştirme, bildirim, süre takibi ve veri imhasını yapan otomatik süreçler. |

## 4. Fonksiyonel gereksinimler

Öncelik: **M** = Must (olmazsa olmaz), **S** = Should (önemli), **C** = Could (olsa iyi olur).

### 4.1 Üyelik ve davet

| ID | Gereksinim | Öncelik |
|---|---|---|
| FR-01 | Kullanıcı e-posta ile kayıt olur ve şifresiz **e-posta bağlantısı** ile giriş yapar. Kayıtta TR GSM numarası (+90 5xx) zorunludur ve biçimi doğrulanır. | M |
| FR-02 | Üye, referans olmasını istediği kişiye **davet** gönderir. Davet için yalnızca bir telefon **veya** e-posta ve yakınlık türü girilir. Davet edilen kişi hakkında başka bilgi girilmez. | M |
| FR-03 | Davet edilen kişi bağlantıyı açınca **aydınlatma metnini** görür, **açık rıza** verir (işaretli gelmeyen onay kutusu) ve şirket, sektör, pozisyon bilgisini **kendisi** girer. | M |
| FR-04 | Referans, aktif olmadan önce e-posta adresini doğrular. İsterse **iş e-postasını** da doğrular ve "Doğrulanmış iş e-postası" rozeti alır. | M |
| FR-05 | 14 gün içinde onaylanmayan davetler ve bu davetlere ait iletişim bilgisi **kalıcı olarak silinir**. | M |
| FR-06 | Referans kendi kriterlerini belirler: referans olabileceği pozisyonlar, destek türü (CV'ye göz atma, şirket içi yönlendirme, bilgi verme), ayda en fazla kaç talep alacağı (1/3/5). | S |
| FR-17 | Davet kabul edilirken iki taraf da 3 kısa **bağ gücü** sorusunu yanıtlar: yakınlık türü, tanışma süresi, görüşme sıklığı. Düşük olan yanıt geçerli sayılır. | S |

### 4.2 Talep ve eşleştirme

| ID | Gereksinim | Öncelik |
|---|---|---|
| FR-07 | İş arayan yalnızca **sektör ve pozisyon** seçer, PDF CV yükler ve kısa not yazar. Referans listesini veya kimliklerini **göremez**. | M |
| FR-08 | Sistem talebe uygun referansları ağ içinde **en fazla 3 adım** uzaklıkta arar, yakın ve orta güçteki bağları öne alır ve seçilen referansa "Böyle bir aday var" bildirimi gönderir. Bildirimde adayla **nasıl bağlantılı** olduğu gösterilir. | M |
| FR-09 | Referans talebi **kabul eder**, **nazikçe reddeder** veya erteler. Ret de bir yanıt sayılır. CV yalnızca kabulden sonra görünür. | M |
| FR-10 | Kabulden sonra iletişim **platform içi mesajlaşma** ile kurulur. Telefon ve e-posta paylaşılmaz. Aradaki tanıdıklar talepten haberdar edilir; onayları beklenmez. | M |
| FR-11 | Her talep, yanıt, sonuç ve geri bildirim zaman damgasıyla kaydedilir. İş arayan talebinin durumunu izler: Gönderildi, Görüldü, Kabul edildi, Reddedildi, Süresi doldu. | M |

### 4.3 Güven ve kurallar

| ID | Gereksinim | Öncelik |
|---|---|---|
| FR-12 | 30 gün içinde 3 talebi yanıtsız bırakan referansa **uyarı** gider. 14 gün daha yanıt yoksa **yönetici** dondurma kararı verir. Olumsuz geri bildirim otomatik dondurma yapmaz; yöneticiye düşer. Kullanıcı her karara **itiraz** edebilir. | S |
| FR-13 | Kişinin **aktiflik değeri**, kendi davranışı ve davet ettiği referansların yanıt oranı üzerinden hesaplanır ve profilinde görünür. | S |
| FR-14 | Arama yapabilmek için en az **3 onaylı referans** gerekir (pilot dönem; 5 davetten 3'ü). Pilot sonrası eşik 5 onaylı referansa çıkar. Onaylanmamış davetler sayılmaz. | M |
| FR-15 | Yeni üyenin arama kilidi **3 ay sonra** veya **katkıyla daha erken** açılır: 3 onaylı referansının her biri en az bir talebe yanıt vermişse. Hangisi önce gelirse. | S |
| FR-16 | Yönetici dondurma ve itiraz kuyruğunu görür, karar verir ve gerekçe yazar. | M |

## 5. Fonksiyonel olmayan gereksinimler

| ID | Kategori | Gereksinim |
|---|---|---|
| NFR-01 | KVKK | Kişisel veri yalnızca açık rıza ile işlenir. Aydınlatma metni ilk temasta gösterilir. Rıza kayıtları saklanır. |
| NFR-02 | KVKK | Kişisel veriler **Türkiye'deki** sunucuda barındırılır. Yurt dışına yalnızca e-posta gönderimi için zorunlu veri çıkar (standart sözleşme ile). |
| NFR-03 | KVKK | Kullanıcı verisini indirebilir ve hesabını silebilir. Silme talebi 30 gün içinde tamamlanır. |
| NFR-04 | KVKK | CV'ler talep kapandıktan **6 ay** sonra silinir. CV yükleme ekranı fotoğraf, TC kimlik no, sağlık ve din bilgisi koyulmaması için uyarır. |
| NFR-05 | Güvenlik | Tüm trafik HTTPS. Şifre tutulmaz (e-posta bağlantısı ile giriş). Oturumlar 30 gün sonra sona erer. |
| NFR-06 | Güvenlik | Davet, giriş ve talep uç noktalarında hız sınırı uygulanır. |
| NFR-07 | Gizlilik | İş arayan, referansların kimliğini kabulden önce göremez. Referans, adayın CV'sini kabulden önce göremez. |
| NFR-08 | Kullanılabilirlik | Arayüz Türkçedir, mobil öncelikli tasarlanır. |
| NFR-09 | Erişilebilirlik | WCAG 2.2 AA hedeflenir. |
| NFR-10 | Performans | Sayfalar 4G bağlantıda 2 saniye içinde açılır. Eşleştirme 50.000 kişilik ağda 1 saniyenin altında çalışır. |
| NFR-11 | Maliyet | Aylık işletme maliyeti 1.000 TL'nin altında kalır. |
| NFR-12 | Bakım | Kritik akış (davet → rıza → talep → kabul) uçtan uca testle korunur. Kod incelemesi olmadan birleştirme yapılmaz. |
| NFR-13 | Açıklık | Kaynak kod ve dokümanlar herkese açıktır (ekip anketi: 10 oy açık, 1 oy kapalı). |

## 6. Teknik kararlar (özet)

| Konu | Karar | Gerekçe |
|---|---|---|
| Veritabanı | PostgreSQL; referans ağı kenar tablosu + recursive CTE | Ayrı graf veritabanına gerek yok; 3 adım ve 50 bin kişi Postgres için küçük. |
| Uygulama | Next.js 16, TypeScript, Drizzle ORM, Better Auth, Zod, next-intl | Tek dil, uçtan uca tip güvenliği, AI araçlarıyla uyumlu. |
| Test | Vitest (birim), Playwright (uçtan uca) | Kritik akış otomatik test edilir. |
| Hosting | Türkiye'de VDS + Coolify, PostgreSQL Docker içinde | KVKK yurt dışı aktarım yükünden kaçınma; yaklaşık 400–600 TL/ay. |
| E-posta | Resend | Ücretsiz katman yeterli; newsletter v2'de aynı servisle. |

## 7. Varsayımlar ve kısıtlar

- Proje ticari değildir; reklam ve ücret yoktur. Vergi hesaplaması gerekmez.
- Hosting giderini hocamız karşılar.
- Ekip gönüllü öğrencilerden oluşur; deneyim düzeyleri farklıdır.
- Türkiye'de SMS başlığı için kurum veya şirket kaydı gerekir. Bu yüzden SMS doğrulama v1'de yoktur.

## 8. Hocalarımıza açık sorular

1. **Veri sorumlusu** kim olacak: hocamız, üniversite veya bir dernek? (Öğrenci grubunun tüzel kişiliği yok.)
2. **SMS hesabı** üniversite veya bir kurum üzerinden açılabilir mi?
3. Davet akışı (öğrenci yalnızca davet gönderir, referans kendi bilgisini girer) uygun mu?
