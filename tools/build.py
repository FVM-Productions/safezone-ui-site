"""Builds the safe-zone template PNGs, the per-platform pages, sitemap and llms.txt.

Run from the repo root:  python3 tools/build.py
Geometry mirrors lib/features/safezone/data/safe_zone_presets.dart in the app.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://fvm-productions.github.io/safezone-ui-site/"
APP_STORE = "https://apps.apple.com/app/id6814820004"
PLAY = "https://play.google.com/store/apps/details?id=com.freddyville.safezoneui"
UPDATED = "2026-10-12"

PLATFORMS = [
    dict(slug="tiktok", name="TikTok", w=1080, h=1920, top=220, bottom=360, right=150, left=60,
         covers="the username, caption and sound credit along the bottom, the like, comment, save and share column on the right, and the Following / For You tabs at the top"),
    dict(slug="instagram-reels", name="Instagram Reels", w=1080, h=1920, top=180, bottom=380, right=140, left=56,
         covers="the profile name, caption and audio credit along the bottom, the like, comment, share and more column on the right, and the Reels header and camera button at the top"),
    dict(slug="youtube-shorts", name="YouTube Shorts", w=1080, h=1920, top=160, bottom=340, right=160, left=56,
         covers="the channel name, subscribe button and title along the bottom, the like, dislike, comment, share and remix column on the right, and the search and menu icons at the top"),
    dict(slug="snapchat-spotlight", name="Snapchat Spotlight", w=1080, h=1920, top=200, bottom=400, right=140, left=56,
         covers="the creator name and caption along the bottom, the action column on the right, and the Spotlight header at the top"),
    dict(slug="facebook-reels", name="Facebook Reels", w=1080, h=1920, top=190, bottom=370, right=150, left=56,
         covers="the profile name, caption and audio credit along the bottom, the reaction, comment and share column on the right, and the Reels header at the top"),
    dict(slug="meta-ads-4x5", name="Meta 4:5 feed ads", w=1080, h=1350, top=240, bottom=240, right=120, left=60,
         covers="the sponsored label and profile row at the top, and the call-to-action bar and caption area at the bottom"),
]

RED = (229, 57, 53, 110)
GREEN = (46, 204, 113, 255)


def safe_box(p):
    return p["left"], p["top"], p["w"] - p["right"], p["h"] - p["bottom"]


def render_png(p):
    img = Image.new("RGBA", (p["w"], p["h"]), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = safe_box(p)
    for box in [(0, 0, p["w"], y0), (0, y1, p["w"], p["h"]), (0, y0, x0, y1), (x1, y0, p["w"], y1)]:
        d.rectangle(box, fill=RED)
    d.rectangle((x0, y0, x1 - 1, y1 - 1), outline=GREEN, width=6)
    out = ROOT / "templates" / f"{p['slug']}-safe-zone-{p['w']}x{p['h']}.png"
    out.parent.mkdir(exist_ok=True)
    img.save(out, optimize=True)
    return out.name


def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}{path}">
<link rel="icon" href="mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
{extra}</head>
<body>
<div class="wrap">
  <header>
    <a href="./"><img class="mark" src="mark.svg" alt=""><span class="brand">SafeZone UI</span></a>
    <nav aria-label="Site"><a href="safe-zones.html"{' aria-current="page"' if path.startswith('safe') or path.endswith('-safe-zone.html') else ''}>Safe zone templates</a><a href="./">Support</a><a href="privacy.html">Privacy</a></nav>
  </header>
"""


FOOT = f"""  <div class="card">
    <p><strong>Check your actual video, not just a template.</strong> SafeZone UI puts these zones over your own clip on your phone, so you can pinch and drag until nothing important is covered. It's free, with no account.</p>
    <p><a class="button" href="{APP_STORE}">Download on the App Store</a> <a class="button" href="{PLAY}">Get it on Google Play</a></p>
  </div>
  <footer>
    <p>Measurements are SafeZone UI's own, taken from the platforms' public apps and last reviewed {UPDATED}. Platforms change their layouts without notice, so treat them as a close guide, not an official spec. SafeZone UI is not affiliated with or endorsed by TikTok, Instagram, YouTube, Snapchat, Facebook or Meta.</p>
    <p>© 2026 Freddyville Media Productions LLC · <a href="privacy.html">Privacy Policy</a></p>
  </footer>
</div>
</body>
</html>
"""


def platform_page(p, png):
    x0, y0, x1, y1 = safe_box(p)
    sw, sh = x1 - x0, y1 - y0
    pct = round(100 * sw * sh / (p["w"] * p["h"]))
    ratio = "4:5" if p["h"] == 1350 else "9:16"
    path = f"{p['slug']}-safe-zone.html"
    title = f"{p['name']} safe zone: dimensions and free template ({p['w']}×{p['h']})"
    desc = f"The {p['name']} safe zone on a {p['w']}×{p['h']} canvas: keep text and faces inside {sw}×{sh} px, {y0} px from the top and {p['bottom']} px from the bottom. Free transparent PNG template."
    faq = [
        (f"What is the {p['name']} safe zone?",
         f"It's the part of a {ratio} video that stays visible once {p['name']} draws its interface on top. On a {p['w']}×{p['h']} canvas, it's a {sw}×{sh} px box starting {x0} px from the left and {y0} px from the top."),
        (f"How much of a {p['name']} video gets covered?",
         f"About {100 - pct}% of the frame sits under {p['covers']}. Roughly {pct}% stays clear."),
        (f"Where should captions go on {p['name']}?",
         f"Keep burned-in captions above {y1} px from the top (at least {p['bottom']} px off the bottom edge) and left of {x1} px, so the right-hand buttons don't cover them."),
    ]
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>\n'
    rows = "".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in [
        ("Canvas", f"{p['w']} × {p['h']} px ({ratio})"),
        ("Safe area", f"{sw} × {sh} px"),
        ("Top margin", f"{y0} px"), ("Bottom margin", f"{p['bottom']} px"),
        ("Left margin", f"{x0} px"), ("Right margin", f"{p['right']} px"),
        ("Visible share of frame", f"about {pct}%"),
    ])
    faqs = "".join(f"<h3>{q}</h3>\n<p>{a}</p>\n" for q, a in faq)
    body = f"""  <main>
    <h1>{p['name']} safe zone</h1>
    <p class="lede">On a {p['w']}×{p['h']} {ratio} video, keep text, faces and logos inside a <strong>{sw}×{sh} px</strong> box: {y0} px down from the top, {p['bottom']} px up from the bottom, {x0} px in from the left and {p['right']} px in from the right. Everything outside it can end up under {p['covers']}.</p>
    <table class="spec">{rows}</table>
    <h2>Free {p['name']} safe zone template</h2>
    <p>Transparent PNG, {p['w']}×{p['h']}. Drop it on a track above your footage in CapCut, Premiere Pro, Final Cut, DaVinci Resolve or Canva, and turn it off before you export. Red is covered, the green box is safe.</p>
    <figure class="template"><img src="templates/{png}" width="{p['w']}" height="{p['h']}" alt="{p['name']} safe zone overlay: red covered areas around a green safe box" loading="lazy"></figure>
    <p><a class="button" href="templates/{png}" download>Download the PNG</a></p>
    <h2>Common questions</h2>
{faqs}  </main>
"""
    (ROOT / path).write_text(head(title, desc, path, extra) + body + FOOT)
    return path, title, sw, sh


def hub(entries):
    path = "safe-zones.html"
    title = "Safe zone templates for TikTok, Reels, Shorts and more (free PNG)"
    desc = "Free transparent safe zone templates and exact pixel dimensions for TikTok, Instagram Reels, YouTube Shorts, Snapchat Spotlight, Facebook Reels and Meta 4:5 ads."
    rows = "".join(
        f"<tr><th scope=\"row\"><a href=\"{e[0]}\">{p['name']}</a></th><td>{p['w']}×{p['h']}</td><td>{e[2]}×{e[3]} px</td><td>{p['top']} / {p['bottom']} px</td></tr>"
        for p, e in zip(PLATFORMS, entries))
    body = f"""  <main>
    <h1>Safe zone templates</h1>
    <p class="lede">Every short-video app draws buttons, captions and headers over your video. These free transparent PNGs show exactly where, so you can keep text and faces clear before you post.</p>
    <table class="spec"><thead><tr><th>Platform</th><th>Canvas</th><th>Safe area</th><th>Top / bottom</th></tr></thead><tbody>{rows}</tbody></table>
    <h2>How to use a template</h2>
    <p>Open the platform's page, download the PNG and place it on the top track of your editor at full frame. Line up your text and subject inside the green box, then hide the overlay before exporting.</p>
  </main>
"""
    (ROOT / path).write_text(head(title, desc, path) + body + FOOT)
    return path


def sitemap(paths):
    urls = "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{UPDATED}</lastmod></url>" for p in ["", *paths, "privacy.html"])
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")


def llms(entries):
    lines = "\n".join(f"- [{p['name']} safe zone]({BASE}{e[0]}): {e[2]}×{e[3]} px safe area on {p['w']}×{p['h']}, top {p['top']} px, bottom {p['bottom']} px, left {p['left']} px, right {p['right']} px."
                      for p, e in zip(PLATFORMS, entries))
    (ROOT / "llms.txt").write_text(f"""# SafeZone UI

> SafeZone UI is a free iOS and Android app that overlays a to-scale reconstruction of TikTok, Instagram Reels, YouTube Shorts, Snapchat Spotlight, Facebook Reels and Meta ad interfaces on your own vertical video, so you can see what will be covered before you post. No account; videos never leave the phone. Made by Freddyville Media Productions LLC. Not affiliated with any of these platforms.

- App Store: {APP_STORE}
- Google Play: {PLAY}

## Safe zone dimensions (free PNG templates on each page)

{lines}

## Other

- [All templates]({BASE}safe-zones.html)
- [Support and FAQ]({BASE})
- [Privacy policy]({BASE}privacy.html)
""")


if __name__ == "__main__":
    entries = [platform_page(p, render_png(p)) for p in PLATFORMS]
    paths = [hub(entries)] + [e[0] for e in entries]
    sitemap(paths)
    llms(entries)
    print("\n".join(paths))
