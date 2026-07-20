#!/usr/bin/env python3
"""README görsellerini üretir. Metni değiştirip çalıştır: python3 build_cards.py

Tasarım dili: koyu dolgulu yüzeyler (Apple bento), beyaz tipografi,
tek imza rengi olarak gül→lila degrade. GitHub README'de CSS olmadığı
için her şey SVG; <img> içinde link/hover ÇALIŞMAZ, linki README'de
<a> ile ver.

Renkleri değiştirmek için sadece aşağıdaki sabitleri düzenle.
"""

SURFACE   = "#141416"   # kart zemini
PRIMARY   = "#F5F5F7"   # ana metin
SECONDARY = "#9A9AA0"   # ikincil metin
BODY      = "#B4B4BA"   # poster gövde metni
ACCENT    = "#C7A9DF"   # küçük vurgu metinleri (soft lila)
GRAD_A    = "#E8A0A6"   # degrade başı (gül)
GRAD_B    = "#B39DDB"   # degrade sonu (lila)
LINE      = "#2C2C2E"   # kart çerçevesi (koyu temada zeminden ayırır)

FONT = '"SF Pro Text",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Helvetica,Arial,sans-serif'

# README'de gösterildikleri genişlikle birebir aynı — kesirli ölçekleme
# metni bulanıklaştırıyor (Safari), o yüzden width değerleriyle eşit tut.
CARD_W, CARD_H = 405, 150


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(w, h):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '  <defs>',
        '    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0">',
        f'      <stop offset="0" stop-color="{GRAD_A}"/>',
        f'      <stop offset="1" stop-color="{GRAD_B}"/>',
        '    </linearGradient>',
        '  </defs>',
        '  <style>',
        f'    .t {{ font-family:{FONT}; }}',
        '  </style>',
        f'  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="26" fill="{SURFACE}" stroke="{LINE}"/>',
    ]


def poster(name="poster-hero.svg", w=830, h=360):
    """Tek parça tanıtım posteri: isim, kimlik, biyografi, dört alan."""
    cx = w / 2
    p = head(w, h)
    p += [
        f'  <text class="t" x="{cx}" y="96" text-anchor="middle" font-size="56" font-weight="700" '
        f'letter-spacing="-1.5" fill="url(#grad)">Sena Köse</text>',
        f'  <text class="t" x="{cx}" y="134" text-anchor="middle" font-size="16.5" '
        f'fill="{SECONDARY}">AI agents · thoughtful software</text>',
    ]
    bio = [
        "4th-year Software Engineering student.",
        "2nd place — Microsoft & UBITECH AI for Good Hackathon 2026.",
        "ABAP intern at NTT DATA — Center of Excellence, Istanbul.",
    ]
    for i, line in enumerate(bio):
        p.append(
            f'  <text class="t" x="{cx}" y="{178 + i*24}" text-anchor="middle" '
            f'font-size="13.5" fill="{BODY}">{esc(line)}</text>'
        )
    p.append(f'  <line x1="90" y1="262" x2="{w-90}" y2="262" stroke="url(#grad)" stroke-width="1" opacity="0.55"/>')
    domains = [
        ("AI agents", "that do real work"),
        ("Data & ML", "with Python"),
        ("Web apps", "React & TypeScript"),
        ("iOS apps", "native, SwiftUI"),
    ]
    for i, (title, sub) in enumerate(domains):
        x = w / 8 * (2 * i + 1)
        p += [
            f'  <text class="t" x="{x}" y="300" text-anchor="middle" font-size="15" '
            f'font-weight="600" fill="{PRIMARY}">{esc(title)}</text>',
            f'  <text class="t" x="{x}" y="321" text-anchor="middle" font-size="11.5" '
            f'fill="{SECONDARY}">{esc(sub)}</text>',
        ]
    p.append("</svg>\n")
    open(name, "w").write("\n".join(p))
    return name


def card(name, title, desc_lines, tech, badge=None):
    y = 42 if badge is None else 68
    p = head(CARD_W, CARD_H)
    if badge:
        bw = 16 + len(badge) * 7
        p += [
            f'  <rect x="28" y="24" width="{bw}" height="22" rx="11" fill="none" stroke="url(#grad)"/>',
            f'  <text class="t" x="{28 + bw/2}" y="39" text-anchor="middle" font-size="10.5" '
            f'font-weight="600" letter-spacing="0.9" fill="{ACCENT}">{esc(badge)}</text>',
        ]
    p.append(f'  <text class="t" x="28" y="{y}" font-size="17" font-weight="600" fill="{PRIMARY}">{esc(title)}</text>')
    for i, line in enumerate(desc_lines):
        p.append(f'  <text class="t" x="28" y="{y + 26 + i*19}" font-size="12.5" fill="{SECONDARY}">{esc(line)}</text>')
    p.append(f'  <text class="t" x="28" y="{CARD_H-22}" font-size="11.5" fill="{ACCENT}">{esc(tech)}</text>')
    p.append("</svg>\n")
    open(name, "w").write("\n".join(p))
    return name


HIGHLIGHTS = [
    ("highlight-echoward.svg", "EchoWard",
     ["2nd place at the Microsoft & UBITECH AI for Good",
      "Hackathon — voice-first agent shielding shoppers."],
     "Copilot Studio · Azure Speech · GPT-4o Vision", "2ND PLACE"),

    ("highlight-ntt.svg", "NTT DATA",
     ["ABAP Intern at the Center of Excellence,",
      "Istanbul — since July 2026."],
     "SAP · ABAP", "NOW"),
]

PROJECTS = [
    ("card-echoward.svg", "EchoWard",
     ["Voice-first AI agent that warns vulnerable shoppers",
      "about scam listings while they browse."],
     "Copilot Studio · Azure Speech · GPT-4o Vision", None),

    ("card-omr.svg", "OMR Scanner",
     ["Reads exam sheets from a phone camera — optical marks,",
      "handwriting recognition, automatic grading. Built in 2 days."],
     "React 19 · FastAPI · OpenCV", None),

    ("card-playlist.svg", "Playlist Platform",
     ["Playlist sharing on a microservice architecture —",
      "independent services behind an API gateway."],
     "Node.js · Express · Docker · AWS", None),

    ("card-notation.svg", "Notation Visualizer",
     ["Teaching tool that animates the stack step by step",
      "through infix, postfix and prefix conversions."],
     "React · Vite", None),

    ("card-collatz.svg", "Collatz Cipher",
     ["Stream cipher and pseudo-random generator built",
      "on the Collatz conjecture."],
     "Python · Cryptography", None),

    ("card-datamining.svg", "Data Mining",
     ["CART (Gini & Twoing), KNN and classification studies",
      "on real datasets — churn, loans, student performance."],
     "Python · scikit-learn · pandas", None),
]

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def to_png(svg_name):
    """SVG'yi 2x çözünürlükte PNG'ye çevirir (retina'da keskin).

    README PNG kullanıyor: Safari, <img> içindeki SVG metnini rasterleştirirken
    bulanıklaştırıyor; 2x PNG her tarayıcıda aynı ve keskin görünüyor.
    """
    import re
    import subprocess
    svg = open(svg_name).read()
    w, h = map(int, re.search(r'viewBox="0 0 (\d+) (\d+)"', svg).groups())
    png_name = svg_name.replace(".svg", ".png")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu",
         "--force-device-scale-factor=2", f"--window-size={w},{h}",
         "--default-background-color=00000000",
         f"--screenshot={png_name}", f"file://{__import__('os').path.abspath(svg_name)}"],
        check=True, capture_output=True)
    return png_name


if __name__ == "__main__":
    for name in [poster()] + [card(*args) for args in HIGHLIGHTS + PROJECTS]:
        print("yazıldı:", name, "→", to_png(name))
