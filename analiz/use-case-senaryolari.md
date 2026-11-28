# Use Case Senaryoları (v1.0)

Diyagramlar: [`diyagramlar/svg/`](../diyagramlar/svg/). Gereksinim ID'leri: [`gereksinimler.md`](gereksinimler.md).

## 1. Tüm kullanım durumları

| ID | Ad | Birincil aktör | Gereksinimler | Diyagram |
|---|---|---|---|---|
| UC-01 | Kayıt ol / giriş yap | Ziyaretçi | FR-01 | UC-0 |
| UC-02 | Referans davet et | Üye | FR-02, FR-05 | UC-0, UC-1 |
| UC-03 | Daveti kabul et ve rıza ver | Referans | FR-03, FR-17, NFR-01 | UC-0, UC-2 |
| UC-04 | E-postayı doğrula | Referans | FR-04 | UC-2 |
| UC-05 | Referans kriterlerini belirle | Referans | FR-06 | UC-0, UC-2 |
| UC-06 | Sektör + pozisyon ile talep oluştur | İş arayan | FR-07, FR-14, FR-15, NFR-04 | UC-0, UC-1 |
| UC-07 | Talebi yanıtla | Referans | FR-09, FR-11 | UC-0, UC-2 |
| UC-08 | Platform içi mesajlaş | İş arayan, Referans | FR-10 | UC-0, UC-1, UC-2 |
| UC-09 | Taleplerimi izle | İş arayan | FR-11 | UC-0, UC-1 |
| UC-10 | Dondurma ve itirazı incele | Yönetici | FR-12, FR-16 | UC-0, UC-3 |
| UC-11 | İtiraz et | Üye, Referans | FR-12 | UC-0, UC-2 |
| UC-12 | Verimi indir / hesabımı sil | Üye | NFR-03 | UC-0, UC-1 |
| UC-13 | Eşleştir ve bildir | Sistem | FR-08 | UC-0, UC-1, UC-3 |
| UC-14 | Süresi dolan veriyi sil | Sistem | FR-05, NFR-04 | UC-0, UC-3 |
| UC-15 | Aktiflik değerini hesapla | Sistem | FR-13 | UC-3 |
| UC-16 | İş e-postasını doğrula (rozet) | Referans | FR-04 | UC-2 |
| UC-17 | Yanıtsız talep uyarısı gönder | Sistem | FR-12 | UC-3 |

## 2. Ayrıntılı senaryolar

### UC-02 · Referans davet et

| | |
|---|---|
| **Aktör** | Üye |
| **Amaç** | Tanıdığı bir çalışanı referans olarak ağa davet etmek. |
| **Ön koşul** | Üye giriş yapmış ve e-postasını doğrulamış. |
| **Son koşul** | Davet kaydı "Bekliyor" durumunda oluşur; davet edilen kişiye bağlantı gider. |

**Ana akış**
1. Üye "Referans davet et" ekranını açar.
2. Davet edilecek kişinin telefonunu **veya** e-postasını ve yakınlık türünü girer.
3. Sistem biçimi doğrular ve aynı kişiye açık bir davet olmadığını kontrol eder.
4. Sistem kısa aydınlatma metni içeren davet bağlantısını gönderir.
5. Davet, üyenin davet listesinde "Bekliyor — 14 gün içinde onaylanmazsa silinir" olarak görünür.

**Alternatif akışlar**
- 3a. Biçim hatalıysa sistem hatayı gösterir, davet gönderilmez.
- 3b. Aynı kişiye açık davet varsa sistem uyarır ve yeni davet oluşturmaz.
- 5a. 14 gün içinde onay gelmezse **UC-14** daveti ve iletişim bilgisini kalıcı olarak siler.

### UC-03 · Daveti kabul et ve rıza ver

| | |
|---|---|
| **Aktör** | Referans (davet edilen kişi) |
| **Amaç** | Ağa referans olarak katılmak. |
| **Ön koşul** | Geçerli ve süresi dolmamış bir davet bağlantısı var. |
| **Son koşul** | Referans "Aktif" olur; davet eden üyenin onaylı referans sayısı 1 artar. |

**Ana akış**
1. Kişi davet bağlantısını açar ve **aydınlatma metnini** okur.
2. **Açık rıza** kutusunu işaretler (kutu işaretli gelmez).
3. Şirket, sektör ve pozisyon bilgisini kendisi girer.
4. Davet edenle ilgili 3 **bağ gücü** sorusunu yanıtlar (UC-03a).
5. E-postasını doğrular (**UC-04**, include).
6. Sistem rıza kaydını zaman damgasıyla saklar ve referansı aktifleştirir.

**Alternatif akışlar**
- 1a. Bağlantının süresi dolmuşsa sistem "Davetin süresi doldu" mesajı gösterir.
- 2a. Kişi rıza vermezse süreç durur; davet silinir.
- 5a. İsterse iş e-postasını da doğrular ve rozet alır (**UC-16**, extend).

### UC-06 · Sektör + pozisyon ile talep oluştur

| | |
|---|---|
| **Aktör** | İş arayan |
| **Amaç** | Uygun bir referansa ulaşmak. |
| **Ön koşul** | Arama kilidi açık: en az 3 onaylı referans **ve** (3 ay geçmiş **veya** katkı şartı sağlanmış). |
| **Son koşul** | Talep "Gönderildi" durumunda oluşur; eşleştirme başlar. |

**Ana akış**
1. İş arayan "Talep oluştur" ekranını açar. Sistem kilit durumunu kontrol eder (UC-06b).
2. Sektör ve pozisyon seçer.
3. PDF CV yükler (UC-06a). Ekran fotoğraf, TC kimlik no, sağlık ve din bilgisi koyulmaması için uyarır.
4. Kısa bir not yazar ve gönderir.
5. Sistem **UC-13 Eşleştir ve bildir** adımını başlatır.

**Alternatif akışlar**
- 1a. Kilit kapalıysa sistem eksik koşulu gösterir ("2/3 onaylı referans") ve talep formunu açmaz.
- 3a. Dosya PDF değilse veya 5 MB'tan büyükse sistem reddeder.
- 5a. Uygun referans bulunamazsa talep "Bekliyor" kalır; yeni referans katıldıkça tekrar denenir.

### UC-07 · Talebi yanıtla

| | |
|---|---|
| **Aktör** | Referans |
| **Amaç** | Gelen talebe kabul veya ret yanıtı vermek. |
| **Ön koşul** | Referansa "Böyle bir aday var" bildirimi gelmiş. |
| **Son koşul** | Talep "Kabul edildi" veya "Reddedildi" olur; yanıt kaydedilir. |

**Ana akış**
1. Referans bildirimi açar. Sektör, pozisyon, not ve **adayla nasıl bağlantılı olduğunu** görür ("İş arkadaşınız Ayşe'nin sınıf arkadaşı"). CV görünmez.
2. "Kabul et" seçer.
3. Sistem CV'yi referansa açar ve platform içi mesaj kanalını başlatır (**UC-08**).
4. Aradaki tanıdıklara bilgi bildirimi gider.

**Alternatif akışlar**
- 2a. "Nazikçe reddet" seçerse talep "Reddedildi" olur. Ret bir yanıt sayılır; aktiflik değeri düşmez.
- 2b. "Daha sonra" seçerse talep açık kalır. 30 gün içinde 3 talep yanıtsız kalırsa **UC-17** uyarı gönderir.
- 4a. Süreç sonunda referans isterse geri bildirim verir (UC-07a, extend).

### UC-10 · Dondurma ve itirazı incele

| | |
|---|---|
| **Aktör** | Yönetici |
| **Amaç** | Kural ihlali veya şikâyet durumunda adil karar vermek. |
| **Ön koşul** | Kuyrukta bir dondurma önerisi veya itiraz var. |
| **Son koşul** | Hesap aktif kalır veya dondurulur; karar ve gerekçe kaydedilir; kullanıcı bilgilendirilir. |

**Ana akış**
1. Yönetici kuyruğu açar ve kaydı seçer.
2. Talep geçmişini, yanıt oranını ve geri bildirimleri inceler.
3. "Aktif bırak" veya "Dondur" kararı verir.
4. Karar gerekçesini yazar (UC-10a, include).
5. Sistem kullanıcıya kararı ve **itiraz hakkını** bildirir.

**Alternatif akışlar**
- 3a. Kullanıcı itiraz ederse (**UC-11**) kayıt kuyruğa tekrar düşer ve başka bir yönetici inceler.
