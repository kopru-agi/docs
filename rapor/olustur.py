"""Köprü analiz raporunu Markdown kaynaklarından üretir.

Kullanım:  python rapor/olustur.py
Çıktı:     rapor/cikti/kopru-analiz-raporu-v1.html  (görseller gömülü)
           rapor/cikti/kopru-analiz-raporu-v1.pdf   (Chrome ile)
           rapor/cikti/kopru-analiz-raporu-v1.docx  (LibreOffice ile)

Kaynak sıra rapor/rapor.md içindedir. `!include <yol>` satırı başka bir
Markdown dosyasını ekler. Desteklenen Markdown: başlıklar, tablolar,
listeler, alıntılar, kod blokları, kalın, eğik, satır içi kod, link, görsel.
"""

from __future__ import annotations

import base64
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

KOK = Path(__file__).resolve().parent
DEPO = KOK.parent
CIKTI = KOK / "cikti"
AD = "kopru-analiz-raporu-v1"
GITHUB = "https://github.com/kopru-agi/docs/blob/main/"

CHROME_ADAYLARI = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "google-chrome",
    "chromium",
]
SOFFICE_ADAYLARI = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    "soffice",
    "libreoffice",
]


# ---------------------------------------------------------------- Markdown ---

def satir_ici(metin: str, taban: Path, gomulu: bool) -> str:
    kodlar: list[str] = []

    def kod_sakla(m: re.Match) -> str:
        kodlar.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(kodlar) - 1}\x00"

    metin = re.sub(r"`([^`]+)`", kod_sakla, metin)
    metin = html.escape(metin, quote=False)

    def gorsel(m: re.Match) -> str:
        alt, yol = m.group(1), m.group(2)
        return gorsel_html(alt, taban, yol, gomulu)

    def link(m: re.Match) -> str:
        yazi, hedef = m.group(1), m.group(2)
        if not re.match(r"^(https?:|mailto:|#)", hedef):
            hedef = GITHUB + (taban / hedef).resolve().relative_to(DEPO).as_posix()
        return f'<a href="{html.escape(hedef)}">{yazi}</a>'

    metin = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", gorsel, metin)
    metin = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, metin)
    metin = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", metin)
    metin = re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])", r"<em>\1</em>", metin)
    metin = re.sub(r"\x00(\d+)\x00", lambda m: kodlar[int(m.group(1))], metin)
    return metin


def gorsel_html(alt: str, taban: Path, yol: str, gomulu: bool) -> str:
    dosya = (taban / yol).resolve()
    if gomulu:
        veri = base64.b64encode(dosya.read_bytes()).decode()
        src = f"data:image/png;base64,{veri}"
    else:
        src = dosya.as_uri()
    return (
        f'<figure><img src="{src}" alt="{html.escape(alt)}">'
        f"<figcaption>{html.escape(alt)}</figcaption></figure>"
    )


def tablo(satirlar: list[str], taban: Path, gomulu: bool) -> str:
    def hucreler(s: str) -> list[str]:
        s = s.strip().strip("|")
        return [h.strip() for h in s.split("|")]

    bas = hucreler(satirlar[0])
    govde = [hucreler(s) for s in satirlar[2:]]
    out = ["<table><thead><tr>"]
    out += [f"<th>{satir_ici(h, taban, gomulu)}</th>" for h in bas]
    out.append("</tr></thead><tbody>")
    for r in govde:
        out.append("<tr>" + "".join(f"<td>{satir_ici(h, taban, gomulu)}</td>" for h in r) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def markdown(metin: str, taban: Path, gomulu: bool) -> str:
    satirlar = metin.splitlines()
    out: list[str] = []
    i = 0
    while i < len(satirlar):
        s = satirlar[i]
        if not s.strip():
            i += 1
            continue
        if s.startswith("!include "):
            hedef = (taban / s[len("!include "):].strip()).resolve()
            out.append(markdown(hedef.read_text(encoding="utf-8"), hedef.parent, gomulu))
            i += 1
            continue
        if s.lstrip().startswith("<"):
            out.append(s)
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            while j < len(satirlar) and not satirlar[j].startswith("```"):
                j += 1
            out.append("<pre>" + html.escape("\n".join(satirlar[i + 1:j])) + "</pre>")
            i = j + 1
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            n = len(m.group(1))
            out.append(f"<h{n}>{satir_ici(m.group(2), taban, gomulu)}</h{n}>")
            i += 1
            continue
        if s.startswith("|"):
            j = i
            while j < len(satirlar) and satirlar[j].startswith("|"):
                j += 1
            out.append(tablo(satirlar[i:j], taban, gomulu))
            i = j
            continue
        if s.startswith(">"):
            j = i
            parca = []
            while j < len(satirlar) and satirlar[j].startswith(">"):
                parca.append(satirlar[j].lstrip("> ").rstrip())
                j += 1
            out.append("<blockquote>" + "<br>".join(satir_ici(p, taban, gomulu) for p in parca) + "</blockquote>")
            i = j
            continue
        if re.match(r"^\s*(- |\d+\. )", s):
            sirali = bool(re.match(r"^\s*\d+\. ", s))
            etiket = "ol" if sirali else "ul"
            j = i
            ogeler = []
            while j < len(satirlar) and re.match(r"^\s*(- |\d+\. )", satirlar[j]):
                ogeler.append(re.sub(r"^\s*(- |\d+\. )", "", satirlar[j]))
                j += 1
            out.append(f"<{etiket}>" + "".join(f"<li>{satir_ici(o, taban, gomulu)}</li>" for o in ogeler) + f"</{etiket}>")
            i = j
            continue
        if re.match(r"^!\[", s):
            out.append(satir_ici(s, taban, gomulu))
            i += 1
            continue
        j = i
        parca = []
        while j < len(satirlar) and satirlar[j].strip() and not re.match(r"^(#|\||>|- |\d+\. |```|<|!)", satirlar[j]):
            parca.append(satirlar[j].strip())
            j += 1
        if not parca:
            parca, j = [s.strip()], i + 1
        out.append("<p>" + satir_ici(" ".join(parca), taban, gomulu) + "</p>")
        i = j
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: "Segoe UI", Arial, Helvetica, sans-serif; font-size: 10.5pt; color: #111827; line-height: 1.45; }
h1 { font-size: 20pt; color: #312e81; border-bottom: 2px solid #c7d2fe; padding-bottom: 6px; page-break-before: always; margin-top: 0; }
h2 { font-size: 14pt; color: #312e81; margin-top: 22px; }
h3 { font-size: 12pt; color: #1f2937; margin-top: 18px; }
h4 { font-size: 11pt; }
h2, h3, h4 { page-break-after: avoid; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px; font-size: 9.5pt; page-break-inside: auto; }
th { background: #eef2ff; text-align: left; }
th, td { border: 1px solid #d1d5db; padding: 5px 7px; vertical-align: top; }
tr { page-break-inside: avoid; }
td:first-child { white-space: nowrap; }
blockquote { margin: 8px 0; padding: 8px 12px; background: #f8fafc; border-left: 4px solid #a5b4fc; color: #374151; font-size: 9.5pt; }
code { font-family: Consolas, monospace; font-size: 9pt; background: #f1f5f9; padding: 0 3px; }
pre { background: #f1f5f9; padding: 8px; font-size: 8.5pt; white-space: pre-wrap; }
a { color: #3730a3; text-decoration: none; }
figure { margin: 14px 0; text-align: center; page-break-inside: avoid; }
figure img { max-width: 100%; max-height: 235mm; border: 1px solid #e5e7eb; }
figcaption { font-size: 9pt; color: #4b5563; margin-top: 4px; }
.izgara { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 18px; }
.izgara figure img { max-height: 100mm; }
.izgara.tek { grid-template-columns: 1fr; }
.izgara.tek figure img { max-height: 240mm; }
.kapak { height: 250mm; display: flex; flex-direction: column; justify-content: center; }
.kapak-ust { color: #4338ca; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 10pt; }
.kapak-baslik { font-size: 54pt; border: none; page-break-before: avoid; margin: 8px 0 4px; color: #1e1b4b; }
.kapak-alt { font-size: 15pt; color: #374151; margin-bottom: 36px; }
.kapak-tablo { width: 60%; font-size: 11pt; }
.kapak-tablo td:first-child { width: 35%; color: #4b5563; background: #f8fafc; }
.kapak-not { margin-top: 28px; font-size: 9.5pt; color: #6b7280; }
.icindekiler { page-break-before: always; }
.icindekiler li { font-size: 13pt; margin: 8px 0; }
"""


def sayfa(govde: str) -> str:
    return (
        '<!doctype html><html lang="tr"><head><meta charset="utf-8">'
        "<title>Köprü — Analiz ve Tasarım Raporu v1.0</title>"
        f"<style>{CSS}</style></head><body>{govde}</body></html>"
    )


# ------------------------------------------------------------------ Çıktı ---

def bul(adaylar: list[str]) -> str | None:
    for a in adaylar:
        if os.path.isfile(a):
            return a
        w = shutil.which(a)
        if w:
            return w
    return None


def main() -> int:
    CIKTI.mkdir(exist_ok=True)
    kaynak = (KOK / "rapor.md").read_text(encoding="utf-8")

    html_yolu = CIKTI / f"{AD}.html"
    html_yolu.write_text(sayfa(markdown(kaynak, KOK, gomulu=True)), encoding="utf-8")
    print(f"ok: {html_yolu.relative_to(DEPO)}")

    chrome = bul(CHROME_ADAYLARI)
    if chrome:
        pdf = CIKTI / f"{AD}.pdf"
        with tempfile.TemporaryDirectory() as profil:
            subprocess.run(
                [chrome, "--headless=new", "--disable-gpu", f"--user-data-dir={profil}",
                 "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html_yolu.as_uri()],
                check=True, capture_output=True,
            )
        print(f"ok: {pdf.relative_to(DEPO)}")
    else:
        print("uyari: Chrome bulunamadi, PDF uretilmedi")

    soffice = bul(SOFFICE_ADAYLARI)
    if soffice:
        # Gorseller data: URI olarak gomulu gider; LibreOffice bunlari DOCX'e gomer.
        gecici = CIKTI / f"{AD}.docx-kaynak.html"
        gecici.write_text(sayfa(markdown(kaynak, KOK, gomulu=True)), encoding="utf-8")
        with tempfile.TemporaryDirectory() as profil:
            subprocess.run(
                [soffice, f"-env:UserInstallation={Path(profil).as_uri()}", "--headless",
                 "--infilter=HTML (StarWriter)", "--convert-to", "docx:MS Word 2007 XML",
                 "--outdir", str(CIKTI), str(gecici)],
                check=True, capture_output=True,
            )
        uretilen = CIKTI / f"{AD}.docx-kaynak.docx"
        hedef = CIKTI / f"{AD}.docx"
        uretilen.replace(hedef)
        gecici.unlink()
        print(f"ok: {hedef.relative_to(DEPO)}")
    else:
        print("uyari: LibreOffice bulunamadi, DOCX uretilmedi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
