<div class="kapak">
<div class="kapak-ust">Analiz ve Tasarım Raporu · v1.0</div>
<h1 class="kapak-baslik">Köprü</h1>
<div class="kapak-alt">Referansla iş bulmayı kolaylaştıran, gönüllülük esaslı bir dayanışma ağı</div>
<table class="kapak-tablo">
<tr><td>Tarih</td><td>28 Kasım 2026</td></tr>
<tr><td>Hazırlayan</td><td>Iliya Dindar</td></tr>
<tr><td>GitHub</td><td>github.com/iliyadindar</td></tr>
</table>
<div class="kapak-not">"Köprü" çalışma adıdır; kalıcı ad ekip oylamasıyla belirlenecektir.</div>
</div>

<div class="icindekiler">
<h2>İçindekiler</h2>
<ol>
<li>Gereksinim analizi</li>
<li>Use case şemaları ve senaryolar</li>
<li>Arayüz taslakları</li>
<li>Görev dağılımı</li>
<li>Use case / gereksinim zaman planlaması</li>
</ol>
</div>

!include ../analiz/gereksinimler.md

# Use Case Şemaları

Sistem dört diyagramla gösterilmiştir: genel bakış ve üç ayrıntılı görünüm. Diyagramlar `diyagramlar/uretici.py` betiğiyle koddan üretilir.

![UC-0 Genel bakış](../diyagramlar/svg/uc-0-genel-bakis.png)

![UC-1 İş arayan ve üye](../diyagramlar/svg/uc-1-is-arayan.png)

![UC-2 Referans](../diyagramlar/svg/uc-2-referans.png)

![UC-3 Yönetici ve sistem](../diyagramlar/svg/uc-3-yonetici-sistem.png)

!include ../analiz/use-case-senaryolari.md

# Arayüz Taslakları

Düşük çözünürlüklü, gri tonlu taslaklardır; renk ve görseller bilerek yer tutucu bırakılmıştır. Tüm kişi ve şirket adları uydurmadır. Mobil öncelikli tasarlanmış, ana ekranların masaüstü görünümü de çizilmiştir.

<div class="izgara">

![W-01 Karşılama (mobil) · FR-01, FR-14](../wireframe/png/w01-karsilama-mobil.png)

![W-02 Kayıt ve giriş (mobil) · FR-01](../wireframe/png/w02-kayit-giris-mobil.png)

![W-03 Referans davet et (mobil) · FR-02, FR-05](../wireframe/png/w03-davet-mobil.png)

![W-05 Referans profili ve kriterleri (mobil) · FR-04, FR-06](../wireframe/png/w05-referans-profili-mobil.png)

![W-06 Talep oluştur, kilitli (mobil) · FR-07, FR-14, FR-15](../wireframe/png/w06-talep-olustur-mobil.png)

![W-07 Gelen talep (mobil) · FR-08, FR-09](../wireframe/png/w07-gelen-talep-mobil.png)

![W-08 Taleplerim (mobil) · FR-10, FR-11](../wireframe/png/w08-taleplerim-mobil.png)

![W-09 Hesabım (mobil) · FR-12, NFR-03](../wireframe/png/w09-hesabim-mobil.png)

</div>

<div class="izgara tek">

![W-04 Davet kabul: aydınlatma, açık rıza, bilgiler, doğrulama, bağ soruları (mobil) · FR-03, FR-04, FR-17](../wireframe/png/w04-davet-kabul-mobil.png)

</div>

![W-01 Karşılama (masaüstü)](../wireframe/png/w01-karsilama-masaustu.png)

![W-06 Talep oluştur, açık durum (masaüstü) · FR-07, FR-08](../wireframe/png/w06-talep-olustur-masaustu.png)

![W-07 Gelen talepler, kabul sonrası CV ve platform içi mesajlaşma (masaüstü) · FR-08, FR-09, FR-10](../wireframe/png/w07-gelen-talep-masaustu.png)

![W-10 Yönetici: dondurma ve itiraz kuyruğu (masaüstü) · FR-12, FR-16](../wireframe/png/w10-yonetici-masaustu.png)

!include ../analiz/gorev-dagilimi.md

!include ../analiz/zaman-plani.md

