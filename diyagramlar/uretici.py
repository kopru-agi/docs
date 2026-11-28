"""Köprü use case diyagramı üreticisi.

Kullanım:  python diyagramlar/uretici.py
Çıktı:     diyagramlar/svg/*.svg

Her diyagram aşağıdaki DIYAGRAMLAR sözlüğünde tanımlıdır. Bir diyagramı
değiştirmek için ilgili tanımı düzenleyip betiği yeniden çalıştırın.
Koordinatlar piksel cinsindendir; (0, 0) sol üst köşedir.
"""

from __future__ import annotations

import math
from html import escape
from pathlib import Path

CIKTI = Path(__file__).parent / "svg"

RENK_CIZGI = "#1f2937"
RENK_KUTU = "#f8fafc"
RENK_ELIPS = "#eef2ff"
RENK_ELIPS_KENAR = "#4338ca"
RENK_DAHIL = "#f1f5f9"
RENK_YAZI = "#111827"
YAZI_TIPI = "Segoe UI, Arial, Helvetica, sans-serif"

RX, RY = 105, 34  # use case elipsi yarıçapları


def kenar_noktasi(cx: float, cy: float, rx: float, ry: float, px: float, py: float) -> tuple[float, float]:
    """Elipsin merkezinden (px, py) noktasına giden doğrunun elips kenarını kestiği nokta."""
    dx, dy = px - cx, py - cy
    if dx == 0 and dy == 0:
        return cx, cy
    t = 1 / math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx * t, cy + dy * t


def aktor(x: float, y: float, ad: str) -> str:
    """Çöp adam aktör. (x, y) başın merkezidir."""
    satirlar = ad.split("\n")
    yazi = "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else 15}">{escape(s)}</tspan>' for i, s in enumerate(satirlar)
    )
    return (
        f'<g stroke="{RENK_CIZGI}" stroke-width="2" fill="none">'
        f'<circle cx="{x}" cy="{y}" r="11" fill="#fff"/>'
        f'<line x1="{x}" y1="{y + 11}" x2="{x}" y2="{y + 44}"/>'
        f'<line x1="{x - 20}" y1="{y + 22}" x2="{x + 20}" y2="{y + 22}"/>'
        f'<line x1="{x}" y1="{y + 44}" x2="{x - 16}" y2="{y + 68}"/>'
        f'<line x1="{x}" y1="{y + 44}" x2="{x + 16}" y2="{y + 68}"/>'
        f"</g>"
        f'<text x="{x}" y="{y + 88}" text-anchor="middle" font-size="13" font-weight="600" '
        f'fill="{RENK_YAZI}">{yazi}</text>'
    )


def use_case(x: float, y: float, kod: str, ad: str, dahil: bool = False) -> str:
    satirlar = ad.split("\n")
    n = len(satirlar)
    bas = y - (n * 15) / 2 + 4
    yazi = f'<tspan x="{x}" y="{bas - 2}" font-size="10.5" font-weight="700" fill="{RENK_ELIPS_KENAR}">{escape(kod)}</tspan>'
    for i, s in enumerate(satirlar):
        yazi += f'<tspan x="{x}" y="{bas + 13 + i * 15}">{escape(s)}</tspan>'
    dolgu = RENK_DAHIL if dahil else RENK_ELIPS
    kesik = ' stroke-dasharray="5 3"' if dahil else ""
    return (
        f'<ellipse cx="{x}" cy="{y}" rx="{RX}" ry="{RY}" fill="{dolgu}" stroke="{RENK_ELIPS_KENAR}" '
        f'stroke-width="1.5"{kesik}/>'
        f'<text text-anchor="middle" font-size="12.5" fill="{RENK_YAZI}">{yazi}</text>'
    )


def iliski(a: tuple[float, float], b: tuple[float, float]) -> str:
    """Aktör (a = baş merkezi) ile use case (b = elips merkezi) arasındaki düz çizgi."""
    ax, ay = a[0], a[1] + 30
    ex, ey = kenar_noktasi(b[0], b[1], RX, RY, ax, ay)
    return f'<line x1="{ax}" y1="{ay}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{RENK_CIZGI}" stroke-width="1.4"/>'


def bagimlilik(kaynak: tuple[float, float], hedef: tuple[float, float], tur: str) -> str:
    """<<include>> veya <<extend>> kesik oku. Ok hedefe doğru çizilir."""
    sx, sy = kenar_noktasi(kaynak[0], kaynak[1], RX, RY, hedef[0], hedef[1])
    tx, ty = kenar_noktasi(hedef[0], hedef[1], RX, RY, kaynak[0], kaynak[1])
    mx, my = (sx + tx) / 2, (sy + ty) / 2
    return (
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{RENK_CIZGI}" '
        f'stroke-width="1.3" stroke-dasharray="6 4" marker-end="url(#ok)"/>'
        f'<text x="{mx:.1f}" y="{my - 6:.1f}" text-anchor="middle" font-size="11" font-style="italic" '
        f'fill="#374151" paint-order="stroke" stroke="#fff" stroke-width="4">«{tur}»</text>'
    )


def genelleme(alt: tuple[float, float], ust: tuple[float, float]) -> str:
    """Aktörler arası genelleme (alt aktör üst aktörün özel hâlidir)."""
    x1, y1 = alt[0], alt[1] - 14
    x2, y2 = ust[0], ust[1] + 104
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RENK_CIZGI}" stroke-width="1.4" '
        f'marker-end="url(#ucgen)"/>'
    )


def ciz(tanim: dict) -> str:
    g, y = tanim["boyut"]
    sx, sy, sg, sy2 = tanim["sistem"]
    parca = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{g}" height="{y}" viewBox="0 0 {g} {y}" '
        f'font-family="{YAZI_TIPI}">',
        "<defs>"
        f'<marker id="ok" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10" fill="none" stroke="{RENK_CIZGI}" stroke-width="1.5"/></marker>'
        f'<marker id="ucgen" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="13" markerHeight="13" orient="auto-start-reverse">'
        f'<path d="M0,0 L12,6 L0,12 Z" fill="#fff" stroke="{RENK_CIZGI}" stroke-width="1.3"/></marker>'
        "</defs>",
        f'<rect width="{g}" height="{y}" fill="#fff"/>',
        f'<text x="24" y="34" font-size="18" font-weight="700" fill="{RENK_YAZI}">{escape(tanim["baslik"])}</text>',
        f'<text x="24" y="54" font-size="12" fill="#4b5563">{escape(tanim["alt_baslik"])}</text>',
        f'<rect x="{sx}" y="{sy}" width="{sg}" height="{sy2}" rx="10" fill="{RENK_KUTU}" stroke="{RENK_CIZGI}" stroke-width="1.5"/>',
        f'<text x="{sx + sg / 2}" y="{sy + 24}" text-anchor="middle" font-size="14" font-weight="700" '
        f'fill="{RENK_YAZI}">Köprü Sistemi</text>',
    ]
    aktorler = tanim["aktorler"]
    ucler = tanim["use_caseler"]
    for alt, ust in tanim.get("genellemeler", []):
        parca.append(genelleme(aktorler[alt][:2], aktorler[ust][:2]))
    for a, u in tanim["iliskiler"]:
        parca.append(iliski(aktorler[a][:2], ucler[u][:2]))
    for k, h, tur in tanim.get("bagimliliklar", []):
        parca.append(bagimlilik(ucler[k][:2], ucler[h][:2], tur))
    for kod, (x, yy, ad, *dahil) in ucler.items():
        parca.append(use_case(x, yy, kod, ad, bool(dahil and dahil[0])))
    for _, (x, yy, ad) in aktorler.items():
        parca.append(aktor(x, yy, ad))
    if not tanim.get("lejant_yok"):
        lx, ly = sx, sy + sy2 + 20
        parca.append(
            f'<text x="{lx}" y="{ly}" font-size="11" fill="#4b5563">Kesik kenarlı elips: «include»/«extend» ile gelen alt adım</text>'
        )
    parca.append("</svg>")
    return "\n".join(parca)


# ---------------------------------------------------------------------------
# Diyagram tanımları
# ---------------------------------------------------------------------------

DIYAGRAMLAR: dict[str, dict] = {
    "uc-0-genel-bakis": {
        "baslik": "UC-0 · Genel bakış",
        "alt_baslik": "Köprü v1 — tüm aktörler ve ana kullanım durumları",
        "boyut": (1300, 900),
        "sistem": (230, 80, 840, 800),
        "aktorler": {
            "ziyaretci": (110, 120, "Ziyaretçi"),
            "uye": (110, 320, "Üye"),
            "arayan": (110, 600, "İş arayan"),
            "referans": (1190, 300, "Referans"),
            "yonetici": (1190, 560, "Yönetici"),
            "sistem": (1190, 720, "Sistem\n(zamanlayıcı)"),
        },
        "genellemeler": [("arayan", "uye")],
        "use_caseler": {
            "UC-01": (380, 150, "Kayıt ol /\ngiriş yap"),
            "UC-02": (380, 260, "Referans\ndavet et"),
            "UC-12": (380, 370, "Verimi indir /\nhesabımı sil"),
            "UC-11": (380, 470, "İtiraz et"),
            "UC-06": (380, 600, "Sektör + pozisyon\nile talep oluştur"),
            "UC-09": (380, 720, "Taleplerimi izle"),
            "UC-08": (620, 480, "Platform içi\nmesajlaş"),
            "UC-03": (860, 150, "Daveti kabul et\nve rıza ver"),
            "UC-05": (860, 260, "Referans\nkriterlerini belirle"),
            "UC-07": (860, 370, "Talebi yanıtla"),
            "UC-10": (860, 590, "Dondurma ve\nitirazı incele"),
            "UC-13": (860, 700, "Eşleştir ve\nbildir"),
            "UC-14": (860, 810, "Süresi dolan\nveriyi sil"),
        },
        "iliskiler": [
            ("ziyaretci", "UC-01"),
            ("uye", "UC-02"), ("uye", "UC-12"), ("uye", "UC-11"),
            ("arayan", "UC-06"), ("arayan", "UC-09"), ("arayan", "UC-08"),
            ("referans", "UC-03"), ("referans", "UC-05"), ("referans", "UC-07"), ("referans", "UC-08"),
            ("yonetici", "UC-10"),
            ("sistem", "UC-13"), ("sistem", "UC-14"),
        ],
        "lejant_yok": True,
    },
    "uc-1-is-arayan": {
        "baslik": "UC-1 · İş arayan ve üye",
        "alt_baslik": "Davet, talep oluşturma ve takip",
        "boyut": (1180, 760),
        "sistem": (230, 80, 760, 650),
        "aktorler": {
            "uye": (110, 170, "Üye"),
            "arayan": (110, 470, "İş arayan"),
            "sistem": (1090, 400, "Sistem"),
        },
        "genellemeler": [("arayan", "uye")],
        "use_caseler": {
            "UC-02": (410, 150, "Referans\ndavet et"),
            "UC-12": (410, 260, "Verimi indir /\nhesabımı sil"),
            "UC-06": (410, 400, "Sektör + pozisyon\nile talep oluştur"),
            "UC-09": (410, 530, "Taleplerimi izle"),
            "UC-08": (410, 640, "Platform içi\nmesajlaş"),
            "UC-06a": (790, 330, "CV yükle\n(uyarılı)", True),
            "UC-06b": (790, 460, "Arama kilidini\nkontrol et", True),
            "UC-13": (790, 590, "Eşleştir ve\nbildir"),
            "UC-02a": (790, 170, "14 gün sonra\ndaveti sil", True),
        },
        "iliskiler": [
            ("uye", "UC-02"), ("uye", "UC-12"),
            ("arayan", "UC-06"), ("arayan", "UC-09"), ("arayan", "UC-08"),
            ("sistem", "UC-13"), ("sistem", "UC-02a"),
        ],
        "bagimliliklar": [
            ("UC-06", "UC-06a", "include"),
            ("UC-06", "UC-06b", "include"),
            ("UC-06", "UC-13", "include"),
            ("UC-02a", "UC-02", "extend"),
        ],
    },
    "uc-2-referans": {
        "baslik": "UC-2 · Referans",
        "alt_baslik": "Davet kabulü, rıza, kriterler ve talep yanıtı",
        "boyut": (1180, 760),
        "sistem": (230, 80, 760, 650),
        "aktorler": {
            "referans": (110, 360, "Referans"),
            "arayan": (1090, 560, "İş arayan"),
        },
        "use_caseler": {
            "UC-03": (410, 160, "Daveti kabul et\nve rıza ver"),
            "UC-05": (410, 290, "Referans\nkriterlerini belirle"),
            "UC-07": (410, 420, "Talebi yanıtla\n(kabul / nazik ret)"),
            "UC-08": (410, 550, "Platform içi\nmesajlaş"),
            "UC-11": (410, 660, "İtiraz et"),
            "UC-03a": (790, 130, "Bağ gücü\nsorularını yanıtla", True),
            "UC-04": (790, 250, "E-postayı\ndoğrula", True),
            "UC-16": (790, 380, "İş e-postasını\ndoğrula (rozet)", True),
            "UC-07a": (790, 510, "Geri bildirim\nver", True),
        },
        "iliskiler": [
            ("referans", "UC-03"), ("referans", "UC-05"), ("referans", "UC-07"),
            ("referans", "UC-08"), ("referans", "UC-11"),
            ("arayan", "UC-08"),
        ],
        "bagimliliklar": [
            ("UC-03", "UC-04", "include"),
            ("UC-03", "UC-03a", "include"),
            ("UC-16", "UC-04", "extend"),
            ("UC-07a", "UC-07", "extend"),
        ],
    },
    "uc-3-yonetici-sistem": {
        "baslik": "UC-3 · Yönetici ve sistem",
        "alt_baslik": "Dondurma, itiraz, eşleştirme ve otomatik veri imhası",
        "boyut": (1180, 700),
        "sistem": (230, 80, 760, 590),
        "aktorler": {
            "yonetici": (110, 200, "Yönetici"),
            "sistem": (1090, 360, "Sistem\n(zamanlayıcı)"),
        },
        "use_caseler": {
            "UC-10": (410, 200, "Dondurma ve\nitirazı incele"),
            "UC-10a": (410, 340, "Karar gerekçesi\nyaz", True),
            "UC-15": (790, 150, "Aktiflik değerini\nhesapla"),
            "UC-17": (790, 260, "Yanıtsız talep\nuyarısı gönder"),
            "UC-13": (790, 370, "Eşleştir ve\nbildir"),
            "UC-14": (790, 480, "Süresi dolan veriyi\nsil (davet, CV)"),
            "UC-13a": (410, 520, "Bağlantı yolunu\nhesapla (≤ 3 adım)", True),
        },
        "iliskiler": [
            ("yonetici", "UC-10"),
            ("sistem", "UC-15"), ("sistem", "UC-17"), ("sistem", "UC-13"), ("sistem", "UC-14"),
        ],
        "bagimliliklar": [
            ("UC-10", "UC-10a", "include"),
            ("UC-13", "UC-13a", "include"),
        ],
    },
}


def main() -> None:
    CIKTI.mkdir(exist_ok=True)
    for ad, tanim in DIYAGRAMLAR.items():
        (CIKTI / f"{ad}.svg").write_text(ciz(tanim), encoding="utf-8")
        print(f"ok: svg/{ad}.svg")


if __name__ == "__main__":
    main()
