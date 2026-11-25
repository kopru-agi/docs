# 02 — Messaging and identity (SMS OTP, email, anti-fake-referrer)

Researched 2026-11-25. TL prices include 20% KDV and 10% ÖİV unless noted. "Calc" means price divided by package size.

## 1. SMS OTP providers for Turkey

| Provider | Price to TR | Smallest buy | Sender ID / company need | API |
|---|---|---|---|---|
| **Netgsm** | 500 SMS = 198 TL (calc 0.40 TL); 5,000 = 1,089 TL; new-subscriber 10,000 = 899 TL; pay-as-you-go 0.42 TL [netgsm](https://www.netgsm.com.tr/fiyatlar/) | 500 SMS, prepaid | Page is silent on individuals [netgsm](https://www.netgsm.com.tr/fiyatlar/); a 2019 forum post says only vergi levhası holders were served [r10](https://www.r10.net/freelancer/1990522-whatsapp-business-telefon-numarasi-9-tl-post1074454187.html) | REST/XML; official PHP package [packagist](https://packagist.org/packages/netgsm/sms) |
| **İleti Merkezi** | 500 = 189 TL (calc 0.38); 5,000 = 1,049 TL; new-subscriber 10,000 = 879 TL [iletimerkezi](https://www.iletimerkezi.com/toplu-sms-fiyatlari) | 500 SMS, no fixed fee; undelivered TR SMS refunded [iletimerkezi](https://www.iletimerkezi.com/) | Business-oriented ("Firmanızın adı ile") [iletimerkezi](https://www.iletimerkezi.com/); approved sender ID needed [netmera](https://user.netmera.com/netmera-developer-guide/integrations/sms-providers/ileti-merkezi) | Good docs; API also covers BTK/İYS/KVKK layer [docs](https://www.iletimerkezi.com/en/docs/api/overview) |
| **Verimor** | OTP packs: 500/month = 159 TL (calc 0.32); 5,000/month = 899 TL; **new subscriber: 2,000 OTP free (annual, one-time)** [verimor](https://www.verimor.com.tr/otp-sms-paketleri/) | 500; charged on delivery only | OTP must go out with a başlık [verimor](https://www.verimor.com.tr/otp-sms-paketleri/). Başlıks are "yalnızca İYS'ye kayıtlı işletmelere" and need BTK + İYS approval, 1–3 business days [verimor](https://www.verimor.com.tr/sms-basligi/), [verimor](https://www.verimor.com.tr/toplu-sms). Şahıs işletmesi is OK [verimor](https://www.verimor.com.tr/toplu-sms) | REST, panel |
| **Mutlucell** | No public price found (site TLS error, no search hits) [search](https://www.mutlucell.com.tr/) | Unknown | Same BTK regime | Unverified |
| **Twilio Verify** | $0.05 per successful verification + channel fee [twilio](https://www.twilio.com/en-us/verify/pricing); TR SMS $0.0305/segment [twilio](https://www.twilio.com/en-us/sms/pricing/tr) → about $0.08 per OTP | None | Alphanumeric sender pre-registration (~2 weeks); unregistered senders blocked from **18 Nov 2026**; since 1 Apr 2026 no URLs for non-local entities [twilio](https://www.twilio.com/en-us/guidelines/tr/sms) | Excellent |
| **Vonage** | No TR rate published; US from $0.00809 [apidog](https://apidog.com/blog/vonage-sms-api-cost) | None | Same TR operator rules | Good |
| **Bird** | Contact sales [bird](https://bird.com/products/sms/destinations/turkey) | — | Registration required, 15 business days [bird](https://bird.com/products/sms/destinations/turkey) | Good |

TR rules apply to all foreign routes: numeric senders are replaced, unregistered alphanumeric senders are not delivered, and links are blocked for clients without a local presence [plivo](https://www.plivo.com/sms/coverage/tr/).

**What a student group can sign up for.** No provider says it serves private individuals with no business. Verimor ties a başlık to an İYS-registered business [verimor](https://www.verimor.com.tr/sms-basligi/). Foreign CPaaS need a registered sender too, and they cannot send links [twilio](https://www.twilio.com/en-us/guidelines/tr/sms). Realistic paths: (a) the university or a registered student club/dernek is the subscriber; (b) a volunteer with a şahıs işletmesi signs up. *Inference: confirm with Verimor and İleti Merkezi sales which documents they accept from a dernek or university unit.*

## 2. Firebase / Supabase phone auth

- **Firebase (Identity Platform):** Turkey is $0.03 per SMS. The first 10 SMS per day are free [google](https://cloud.google.com/identity-platform/pricing) (via [search](https://goo.gle/3CVD0vz)). It needs the Blaze plan; Spark has no phone auth [firebase](https://firebase.google.com/pricing). You must allow TR in the SMS region policy [firebase](https://firebase.google.com/docs/auth/web/phone-auth). Google does not document the sender ID used or any custom-provider option [firebase](https://firebase.google.com/docs/auth/web/phone-auth). Deliverability in TR after the 18 Nov 2026 cut-off is **unverified**. It does not solve your başlık problem; it hides it.
- **Supabase:** It does not send SMS itself. Built-in providers are Twilio, MessageBird, Vonage and TextLocal [supabase](https://supabase.com/docs/guides/auth/phone-login). The **Send SMS Hook** lets you plug in any provider, for example Verimor or Netgsm [supabase](https://supabase.com/docs/guides/auth/auth-hooks/send-sms-hook). The sender-ID problem stays with the provider.

## 3. Detecting virtual numbers

- **Supply exists.** onlinesim lists "Turkey +90" [onlinesim](https://onlinesim.io/). Cyberyozh sells Turkish numbers "for one purpose: getting you past SMS verification" [cyberyozh](https://app.cyberyozh.com/reception-sms/virtual/turkey/). Prices were not shown.
- **Twilio Lookup Line Type Intelligence:** $0.008 per lookup [twilio](https://www.twilio.com/en-us/user-authentication-identity/pricing/lookup). It returns `mobile`, `fixedVoip`, `nonFixedVoip` and more, "available for phone numbers worldwide", with no published accuracy [twilio docs](https://www.twilio.com/docs/lookup/v2-api/line-type-intelligence).
- **Numverify:** free tier 100 req/month, non-commercial only; $14.99 for 5,000. It documents only mobile/landline, not VoIP [numverify](https://numverify.com/product).
- **Limit (inference):** activation services in TR mostly resell real SIM-backed `+90 5xx` lines. Line-type checks will report them as `mobile`. Use Lookup as one weak signal. Add velocity limits, one phone per account, and manual review of referrers.

## 4. Cheaper than SMS

**WhatsApp OTP (Meta Cloud API).** Billing is per delivered message since 1 Jul 2025. TR utility and authentication rates dropped on 1 Apr 2026 [meta](https://developers.facebook.com/docs/whatsapp/pricing). Third-party rate cards show TR authentication at about **$0.00104** per message [sleekflow](https://help.sleekflow.io/en_US/pricing), [gallabox](https://docs.gallabox.com/pricing-and-billing/whatsapp-pricing/rate-card.md). Verify this against Meta's CSV rate card.
- Pros: about 30× cheaper than SMS, and no BTK başlık.
- Cons: you need a Meta business portfolio and number. Some users lack WhatsApp. WhatsApp accounts can also sit on virtual numbers, so it proves even less.

**Email-only plus trust signals.** Cost is zero. Strong free signals: a verified `.edu.tr` alumni address, a verified **work email on the employer's domain** (a referrer must prove they work there), a LinkedIn URL, vouching by an existing referrer, and admin approval. *Inference: work-email proof stops more fake referrers than any phone check.*

## 5. Email

- **Resend:** free = 3,000 emails/month, **100/day**, 3 domains. Pro = $20 for 50k. Marketing (Broadcasts) free = 1,000 contacts; $40 for 5k contacts [resend](https://resend.com/pricing).
- **DNS setup:** an SPF `TXT` plus an `MX` on `send.<domain>` (newer domains use `CNAME`s), and DKIM `TXT` at `resend._domainkey` [resend](https://resend.com/docs/knowledge-base/what-if-my-domain-is-not-verifying). Send from a subdomain. Resend recommends DMARC [resend](https://resend.com/docs/dashboard/domains/introduction). Start with `p=none`, then move to `quarantine`.
- **React Email:** open source, and works with Resend, SES, SendGrid and others [react.email](https://react.email/).
- **Broadcasts covers the newsletter:** segments, topics/unsubscribe, scheduling, metrics, and an API [resend](https://resend.com/docs/dashboard/broadcasts/introduction).
- **Brevo:** free = 300 emails/day, 100k contacts, Brevo branding [sender.net](https://www.sender.net/reviews/brevo/pricing/free-plan), [emailtooltester](https://www.emailtooltester.com/en/reviews/sendinblue/pricing/). Starter is about $9 [sendx](https://www.sendx.io/blog/brevo-pricing-plans-costs-alternatives-2026).
- **AWS SES:** $0.10 per 1,000. New accounts get up to $200 in credits [aws](https://aws.amazon.com/ses/pricing/). It is the cheapest at scale, but you build list and unsubscribe handling yourself.

## 6. Turkish identity (later)

- **e-Devlet login:** 129 private institutions use it, but no public onboarding, attribute list or fee exists [didit](https://didit.me/blog/e-devlet-turkey-identity-verification). **Not feasible** for a volunteer project today.
- **NFC ID chip:** Didit sells NFC verification at $0.15 and full KYC at $0.33 per check [didit](https://didit.me/blog/e-devlet-turkey-identity-verification). Feasible later, on a per-referrer basis.
- **TCKN checksum:** the 10th digit is `((d1+d3+d5+d7+d9)*7 − (d2+d4+d6+d8)) mod 10` and the 11th is `sum(d1..d10) mod 10` [python-stdnum](https://sources.debian.org/src/python-stdnum/2.1-3/stdnum/tr/tckimlik.py). It is free, but proves format only. The free NVI KPSPublic name match was reportedly closed on 30 Sep 2025 (unverified forum claim) [r10](https://www.r10.net/sorum-var/4844778-sitede-tc-dogrulamasi.html). Collecting TCKNs also adds KVKK burden. Skip it.

## Recommended MVP stack

1. **Email-first auth** with magic links via Resend + React Email. Newsletter on Resend Broadcasts.
2. **Referrers must verify a work email** on the employer's domain, plus admin approval.
3. **Phone OTP for referrers only**, `+90 5\d{9}` regex, through Supabase Send SMS Hook → **Verimor** (2,000 free OTP for a new subscriber). The account holder is the university or a dernek.
4. Optionally add Twilio Lookup ($0.008) on referrer phones as a weak flag. WhatsApp OTP is a fallback if no entity can own a başlık.

**Monthly cost estimate.** Assumptions: 1.2 OTP per new referrer; referrers are 20% of users; growth is 20% of users per month; one newsletter per month.

| Item | 500 users | 5,000 users |
|---|---|---|
| SMS OTP (Verimor) | ~24 OTP → covered by 2,000 free | ~240 OTP → 500/month pack = 159 TL [verimor](https://www.verimor.com.tr/otp-sms-paketleri/) |
| Transactional email | Resend free $0 | Resend Pro $20 (100/day cap is too low) |
| Newsletter | Resend marketing free (≤1,000 contacts) | Resend marketing $40 (5k contacts) [resend](https://resend.com/pricing) |
| Lookup (optional) | ~$0.20 | ~$2 |
| **Total** | **~$0** | **~159 TL + ~$62** (or ~$25 with SES for the newsletter) |

Worst case at 5,000 users, if every user does an OTP each month: 5,000 OTP = 899 TL with Verimor monthly [verimor](https://www.verimor.com.tr/otp-sms-paketleri/). The same volume costs about $400 on Twilio Verify, or about $5 on WhatsApp.
