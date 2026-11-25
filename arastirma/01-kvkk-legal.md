# 01 — KVKK / İYS legal findings: referral solidarity network

Researched 2026-11-25. Not legal advice. **[Inference]** = my reasoning, no direct source.

Statute (6698, as amended by 7499): https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf

## 1. Third-party contact data entered before consent

- **No Kurul kararı on this exact pattern was found.** The closest official text is the 21.07.2026 kamuoyu duyurusu on contact data obtained "referans, tavsiye veya müşteri önerisi yoluyla". Its points:
  - Getting data from a third party is not a legal basis by itself. An art. 5 condition is still needed.
  - Passive conduct is not açık rıza ("zımni davranış bunu karşılamıyor").
  - https://www.kvkk.gov.tr/Icerik/8830/ucuncu-kisilerden-elde-edilen-kisisel-verilerin-reklam-ve-pazarlama-amacli-kullanilmasina-iliskin-kamuoyu-duyurusu (mirror: https://www.alomaliye.com/2026/07/21/ucuncu-kisi-verileriyle-pazarlama-kvkkdan-aydinlatma-ve-acik-riza-hatirlatmasi/)
- **Aydınlatma timing.** When data does not come from the data subject, notice is due at the earliest of three points:
  - within "makul bir süre" of collection;
  - at the **first contact**, if the data is used to contact the person;
  - at the first transfer, at the latest.

  Aydınlatma and açık rıza are separate steps (Tebliğ art. 5). https://www.kvkk.gov.tr/Icerik/4132/aydinlatma-yukumlulugunun-yerine-getirilmesinde-uyulacak-usul-ve-esaslar-hakkinda-teblig
- **Açık rıza vs meşru menfaat.** Art. 5(2)(f) allows processing that is necessary for the controller's meşru menfaat when it does not harm the data subject's fundamental rights (statute above).
  - **[Inference]** Meşru menfaat covers only a minimal pre-consent step: one phone or email and the inviting student's name, used once to ask "join?", then deleted.
  - Storing company, sector or position, or matching the person before they confirm, needs the referrer's own açık rıza.
  - For an active referrer, use açık rıza for matching. Use art. 5(2)(c) for running the account.
- **Safest flow: invite link.**
  1. The student enters only a phone **or** an email, plus a relationship label.
  2. The system sends **one** invite. That invite is the "ilk iletişim", so it carries a short notice: the veri sorumlusu, the source ("X sizi davet etti"), the purpose, the retention period and a link to the full metin.
  3. The invitee enters their own company, sector and position. They tick a separate açık rıza box and pass email + SMS OTP.
  4. No confirmation within N days (7–14 suggested) means a hard delete. Keep at most a salted hash with a "do not re-invite" flag. **[Inference: art. 4(2) minimisation]**
  5. Send no reminders.

## 2. VERBİS and veri sorumlusu

- **Thresholds.** Kurul karar 2025/1572 (04.09.2025, RG 01.10.2025/33034) keeps the exception for controllers with **<50 employees and a balance sheet <100 million TL**.
  - A stricter test applies when the main activity is özel nitelikli veri: **<10 employees and <10 million TL**.
  - Karar 2025/2393 applies only the employee test to controllers that keep no balance-sheet books.
  - https://kvkk.gov.tr/Icerik/8388/KAMUOYU-DUYURUSU ; https://cottgroup.com/tr/blog/kvkk-gdpr/item/verbise-kayit-yukumlulugu-istisnasina-iliskin-uygulama-esaslari-netlestirildi
- **Result.** A group with no staff or turnover is exempt. VERBİS is **not required**.
- **Who is the veri sorumlusu.** The law defines it as the "gerçek veya tüzel kişi" who sets the purposes and means of processing (art. 3, statute above).
  - **[Inference]** An informal group has no legal personality, so it cannot be the controller. The options are:
    - named natural persons as joint controllers, such as the professor and/or the student leads;
    - the university, if the project is an official university activity. Universities already act as veri sorumlusu: https://www.kvkk.gov.tr/Icerik/7270/2021-1214 ; https://kvkk.metu.edu.tr/tr/system/files/kvkk_akademik_birimler.pdf;
    - a dernek, founded later.
  - Paying for hosting alone does not make the professor the controller. Art. 18 fines still apply without VERBİS.

## 3. Cross-border transfer (art. 9, in force 01.06.2024)

- **Order of transfer routes.**
  1. yeterlilik kararı;
  2. uygun güvenceler: standart sözleşme, BCR or taahhütname;
  3. arızi exceptions, including açık rıza, which are not usable for ongoing transfers.

  https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim (summary: https://bilalalyar.av.tr/?p=101222)
- **No yeterlilik kararı has been issued.** https://ey.com/content/dam/ey-unified-site/ey-com/tr-tr/services/law/documents/ey-tr-kisisel-verilerin-korunmasi.pdf
- **Standart sözleşme rules.**
  - The template comes from Kurul karar 2024/959. Only the seçimlik clauses can be edited.
  - Both parties must sign and date it.
  - Notice to the Kurum is due **within 5 iş günü** of signature, by KEP or through the Bildirim Modülü (open since 25.10.2024).
  - https://www.kvkk.gov.tr/Icerik/8170/Yurt-Disina-Kisisel-Veri-Aktariminda-Kullanilacak-Standart-Sozlesmelerde-Dikkat-Edilmesi-Gereken-Hususlara-Iliskin-Kamuoyu-Duyurusu ; https://www.kvkk.gov.tr/Icerik/8043/Standart-Sozlesme-Bildirim-Modulu-Hakkinda-Kamuoyu-Duyurusu
- **Foreign cloud hosting is a transfer**: "Veri yurt dışına çıkıyorsa m.9 uygulanır" (bilalalyar, above).
  - Vercel, Supabase, Resend and AWS EU are all abroad. An EU region does not help without an EU adequacy decision.
  - **[Inference]** Vendors' DPAs and EU SCCs are not the KVKK template, and a free-tier project will not get a US SaaS to sign it.
- **Recommendation.** Keep the DB, CVs and logs on a **Turkish host** (Turkish-DC VPS or university server). Use a Turkish SMS provider and a Turkish or self-hosted mail relay. A foreign CDN can serve a static frontend only if no personal data passes through it **[Inference]**. Otherwise, sign and notify a standart sözleşme per vendor.

## 4. İYS / ticari elektronik ileti

- **Scope.** Registration and consent apply only to messages sent "ticari amaçlarla". Yönetmelik art. 5(2): "Ticari elektronik ileti göndermek isteyen gerçek ve tüzel kişiler İYS'ye kaydolur".
- **Exemptions.** Art. 6(1)–(2) exempts messages about a service the recipient asked for, and membership notices, from consent and from İYS checks. These messages must promote nothing.
- https://www.lexpera.com.tr/mevzuat/yonetmelikler/ticari-iletisim-ve-ticari-elektronik-iletiler-hakkinda-yonetmelik ; https://ticaret.gov.tr/ic-ticaret/ticari-elektronik-iletiler/ileti-yonetim-sistemi-iys
- **[Inference]** OTPs and "a candidate wants your referral" messages to a confirmed referrer need **no İYS record or ticari onay**. They still need a KVKK basis.
- The first invite to an unconfirmed person must contain zero promotion. It is the riskiest message (see section 1).
- **Newsletter.**
  - **[Inference]** Pure network news for a free service is arguably outside 6563.
  - If it carries sponsors, paid events or partner job ads, it becomes ticari. It then needs İYS-recorded onay, an opt-out in every message (art. 9(4)) and a label (art. 8(6)), per the Yönetmelik above.
  - Either way, make it a separate, unticked opt-in.

## 5. CVs, özel nitelikli veri, retention

- **Art. 6 after 7499.** Özel nitelikli veri is prohibited unless a listed condition applies. The conditions include açık rıza and "alenileştirilmiş" data, but only within the person's intent. https://www.alomaliye.com/2025/03/03/ozel-nitelikli-kisisel-verilerin-islenmesine-iliskin-rehber/ ; https://www.kvkk.gov.tr/Icerik/8184/Ozel-Nitelikli-Kisisel-Verilerin-Islenmesine-Iliskin-Rehber
- **CV content.** Health or disability information on a CV is özel nitelikli. A photo is "görsel ve işitsel veri". https://www.kariyer.net/veri-politikamiz/aday-uyelik-aydinlatma-metni
  - Cinsiyet alone is not özel nitelikli. https://www.alomaliye.com/2025/03/26/kvkknin-dogru-bilinen-yanlislar-rehberi-ozeti/
  - Religion and union membership on older-style CVs are özel nitelikli (art. 6(1), statute above).
- **Mitigations [Inference].** Warn before upload: no photo, health, religion, T.C. kimlik no or marital status. Take a separate açık rıza for CV sharing. Share only after the referrer opts in, through an expiring link.
- **Retention.**
  - No statutory period applies. Keep data as long as the purpose needs; KVKK publishes no universal list (Doğru Bilinen Yanlışlar summary, above).
  - Under the Silme Yönetmeliği, a controller without a policy must delete within 3 months of the duty arising. Periodic imha intervals under a policy cannot exceed 6 months. https://www.resmigazete.gov.tr/eskiler/2017/10/20171028-10.htm
  - Suggested periods **[Inference]**:

    | Data | Retention |
    |---|---|
    | Unconfirmed invite | 7–14 days |
    | CV after the request closes | 90 days |
    | Inactive account | 12 months, then a warning, then deletion |
    | Logs | 12 months, then anonymise |
    | OTP records | 30 days |

## 6. Automated decisions

- Art. 11(1)(g) gives a right to object to an adverse result from analysis "münhasıran otomatik sistemler vasıtasıyla". It is an objection right, not a ban. https://www.kvkk.gov.tr/Icerik/5388/Madde-ve-Gerekcesi-ile-Kisisel-Verilerin-Korunmasi-Kanunu-Bilgi-Notu-ve-Kisisel-Verilerin-Korunmasina-Iliskin-Terimler-Sozlugu ; https://dergipark.org.tr/en/download/article-file/4097542
- **[Inference]** Auto-freezing and low activity scores are adverse results. Add human review and a warning before any freeze, plus an itiraz button. Explain the ranking factors in the aydınlatma metni. Rank on structured fields only, because sending CVs to a foreign LLM API is also an art. 9 transfer. Answer başvurular within 30 days (art. 13).

## 7. MVP checklist

| Item | Purpose |
|---|---|
| Aydınlatma metni (seeker / referrer / invitee) | Art. 10 notice: controller, purposes, basis, recipients, transfers, rights. |
| Invite notice (in SMS/email) | Meets "ilk iletişim" timing. |
| Açık rıza metni (separate, unticked) | Matching, CV sharing, any özel nitelikli veri. |
| Newsletter opt-in | Separate consent. Add İYS if the newsletter turns ticari. |
| Çerez politikası + banner | Necessary cookies only, unless the user opts in. https://kvkk.gov.tr/Icerik/7353/Cerez-Uygulamalari-Hakkinda-Rehber |
| İlgili kişi başvuru formu | Art. 11 rights; reply within 30 days. |
| Saklama-imha table + delete jobs | Enforces section 5. |
| Breach procedure | Notify the Kurul within 72 hours (art. 12(5), Kurul karar 2019/10). |
| Vendor/host register | Records the location and art. 9 basis per vendor. |

## Decisions the team must make

1. **Veri sorumlusu.** Choose the named professor/students, the university, or a dernek.
2. **Hosting.** Choose a Turkish host, or a standart sözleşme with notice per foreign vendor.
3. **Invite TTL (N) and what survives deletion.**
4. **"≥5 referrers" rule.** Count confirmed referrers only, or it rewards mass entry of third-party data.
5. **CV policy.** Choose upload or form, decide on a photo ban, and set retention.
6. **Freeze rules.** Set the human-review step, the warning and the itiraz channel.
7. **AI ranking.** Choose local or external, and the allowed fields.
8. **Newsletter.** Keep it strictly non-commercial, or register with İYS.
9. **Owner** of başvurular (30 days) and breach reports (72 hours).
