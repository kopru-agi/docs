"""Köprü zaman planı (Gantt) üreticisi.

Kullanım:  python diyagramlar/zaman_plani.py
Çıktı:     diyagramlar/svg/zaman-plani.svg
Satırları değiştirmek için ISLER listesini düzenleyin. Haftalar 1'den başlar.
"""

from __future__ import annotations

from html import escape
from pathlib import Path

HAFTALAR = [
    "30 Kas", "7 Ara", "14 Ara", "21 Ara", "28 Ara", "4 Oca",
    "11 Oca", "18 Oca", "25 Oca", "1 Şub", "8 Şub", "15 Şub",
]

# (grup, iş paketi, başlangıç haftası, bitiş haftası, renk)
ISLER = [
    ("Hazırlık", "İP-04–06 Analiz onayı", 1, 1, "#4338ca"),
    ("Hazırlık", "İP-07 İK görüşmeleri", 1, 2, "#6366f1"),
    ("Hazırlık", "İP-08 Kalıcı ad oylaması", 1, 1, "#6366f1"),
    ("Hazırlık", "İP-09 KVKK metinleri", 2, 3, "#6366f1"),
    ("Hazırlık", "İP-10 Yüksek çözünürlüklü tasarım", 2, 3, "#6366f1"),
    ("Hazırlık", "İP-11 Veri modeli (ER)", 2, 3, "#6366f1"),
    ("Hazırlık", "İP-12 Altyapı kurulumu", 3, 3, "#6366f1"),
    ("Geliştirme", "İP-13 Sprint 1 · UC-01–05, UC-16", 4, 5, "#0f766e"),
    ("Geliştirme", "İP-14 Sprint 2 · UC-06, 08, 09, 13", 6, 7, "#0f766e"),
    ("Geliştirme", "İP-15 Sprint 3 · UC-07, 10–12, 14, 15, 17", 8, 9, "#0f766e"),
    ("Yayın", "İP-16 Test ve pilot", 10, 10, "#b45309"),
    ("Yayın", "İP-17 Düzeltme ve yayına alma", 11, 12, "#b45309"),
    ("Yayın", "İP-18 Tanıtım ve referans kazanımı", 10, 12, "#b45309"),
]

KILOMETRE = [(1, "K1"), (3, "K2"), (5, "K3"), (7, "K4"), (9, "K5"), (10, "K6"), (12, "K7")]
FINAL = (6, 7)  # tahmini final dönemi

SOL, UST, HG, SY = 330, 110, 66, 34  # sol boşluk, üst boşluk, hafta genişliği, satır yüksekliği
YAZI = "Segoe UI, Arial, Helvetica, sans-serif"


def main() -> None:
    g = SOL + HG * len(HAFTALAR) + 30
    y = UST + SY * len(ISLER) + 90
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{g}" height="{y}" viewBox="0 0 {g} {y}" font-family="{YAZI}">',
        f'<rect width="{g}" height="{y}" fill="#fff"/>',
        '<text x="24" y="34" font-size="18" font-weight="700" fill="#111827">Köprü · Zaman planı (H1–H12)</text>',
        '<text x="24" y="54" font-size="12" fill="#4b5563">30 Kasım 2026 – 21 Şubat 2027 · çubuklar iş paketlerini, ◆ kilometre taşlarını gösterir</text>',
    ]
    fx = SOL + (FINAL[0] - 1) * HG
    p.append(
        f'<rect x="{fx}" y="{UST - 34}" width="{HG * (FINAL[1] - FINAL[0] + 1)}" height="{SY * len(ISLER) + 34}" fill="#fef3c7"/>'
        f'<text x="{fx + HG}" y="{UST + SY * len(ISLER) + 18}" text-anchor="middle" font-size="11" fill="#92400e">Final dönemi (tahmini)</text>'
    )
    for i, h in enumerate(HAFTALAR):
        x = SOL + i * HG
        p.append(f'<line x1="{x}" y1="{UST - 34}" x2="{x}" y2="{UST + SY * len(ISLER)}" stroke="#e5e7eb"/>')
        p.append(f'<text x="{x + HG / 2}" y="{UST - 18}" text-anchor="middle" font-size="11" font-weight="700" fill="#111827">H{i + 1}</text>')
        p.append(f'<text x="{x + HG / 2}" y="{UST - 5}" text-anchor="middle" font-size="10" fill="#6b7280">{escape(h)}</text>')
    onceki = None
    for r, (grup, ad, b, s, renk) in enumerate(ISLER):
        yy = UST + r * SY
        if grup != onceki:
            p.append(f'<line x1="24" y1="{yy}" x2="{g - 30}" y2="{yy}" stroke="#9ca3af"/>')
            p.append(f'<text x="24" y="{yy + 22}" font-size="11" font-weight="700" fill="#6b7280">{escape(grup.replace("i", "İ").replace("ı", "I").upper())}</text>')
            onceki = grup
        p.append(f'<text x="{SOL - 10}" y="{yy + 22}" text-anchor="end" font-size="12" fill="#111827">{escape(ad)}</text>')
        p.append(f'<rect x="{SOL + (b - 1) * HG + 4}" y="{yy + 8}" width="{(s - b + 1) * HG - 8}" height="{SY - 16}" rx="5" fill="{renk}"/>')
    ky = UST + SY * len(ISLER) + 44
    p.append(f'<text x="24" y="{ky + 4}" font-size="11" font-weight="700" fill="#6b7280">KİLOMETRE TAŞLARI</text>')
    for h, ad in KILOMETRE:
        x = SOL + h * HG - 6
        p.append(f'<path d="M{x},{ky - 8} l8,8 l-8,8 l-8,-8 z" fill="#111827"/>')
        p.append(f'<text x="{x}" y="{ky + 26}" text-anchor="middle" font-size="11" fill="#111827">{ad}</text>')
    p.append("</svg>")
    out = Path(__file__).parent / "svg" / "zaman-plani.svg"
    out.write_text("\n".join(p), encoding="utf-8")
    print("ok: svg/zaman-plani.svg")


if __name__ == "__main__":
    main()
