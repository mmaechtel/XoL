"""MkDocs-Hook: hreflang-Angaben suchmaschinentauglich machen.

mkdocs-static-i18n erzeugt die Alternate-Links mit relativen Adressen
(`href="../glossary.html"`). Google verlangt fuer hreflang vollstaendig
qualifizierte URLs und ignoriert relative Angaben — die Verknuepfung zwischen
DE und EN kommt so nicht an. Der Hook loest sie gegen die kanonische URL der
Seite auf und haengt x-default an.

Dieselbe x-default-Angabe fehlt auch in der von MkDocs erzeugten sitemap.xml
und wird nach dem Build nachgetragen (siehe on_post_build). Ebenfalls dort
entsteht video-sitemap.xml aus scripts/video_meta.json — Google nimmt selbst
gehostete MP4s nur ueber eine Video-Sitemap in den Videoindex auf, das
VideoObject-Markup allein reicht nicht (Search Console: "ohne indexierte Videos").

Registriert in mkdocs.yml unter `hooks:`.
"""
import gzip
import json
import os
import re
from urllib.parse import urljoin

# <link rel="alternate" href="..." hreflang="..."> — Attributreihenfolge wie vom
# Material-Theme erzeugt. x-default wird ausgelassen, damit ein zweiter Lauf
# (mkdocs serve baut Seiten mehrfach) nichts doppelt.
ALTERNATE = re.compile(
    r'<link rel="alternate" href="(?P<href>[^"]+)" hreflang="(?P<lang>(?!x-default)[^"]+)">'
)

# Sprache, die Besucher ohne passende Fassung bekommen sollen.
X_DEFAULT_LANG = "en"

# VideoObject-Metadaten fuer die Videos-Seiten (erzeugt von
# scripts/generate_video_meta.py); main.html liest sie aus config.extra.
VIDEO_META = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_meta.json")


def on_config(config):
    if os.path.exists(VIDEO_META):
        with open(VIDEO_META, encoding="utf-8") as datei:
            config["extra"]["video_meta"] = json.load(datei)
    return config


def on_post_page(output, page, config):
    canonical = getattr(page, "canonical_url", None)
    if not canonical:
        return output

    absolut = {}

    def ersetzen(treffer):
        lang = treffer.group("lang")
        url = urljoin(canonical, treffer.group("href"))
        absolut[lang] = url
        return '<link rel="alternate" href="%s" hreflang="%s">' % (url, lang)

    output, anzahl = ALTERNATE.subn(ersetzen, output)
    if not anzahl:
        return output

    ziel = absolut.get(X_DEFAULT_LANG)
    if ziel and 'hreflang="x-default"' not in output:
        marke = '<link rel="alternate" href="%s" hreflang="%s">' % (ziel, X_DEFAULT_LANG)
        output = output.replace(
            marke,
            marke + '\n    <link rel="alternate" href="%s" hreflang="x-default">' % ziel,
            1,
        )

    return output


# <xhtml:link rel="alternate" hreflang="en" href="..."/> in der Sitemap. Der
# von MkDocs erzeugte Eintrag kennt nur die konfigurierten Sprachen — x-default
# fehlt und wird hier je URL-Block nachgetragen.
SITEMAP_ALTERNATE = re.compile(
    r'(?P<einzug>[ \t]*)<xhtml:link rel="alternate" hreflang="%s" href="(?P<href>[^"]+)"/>'
    % X_DEFAULT_LANG
)


# Seite, auf der die Videos je Sprache eingebettet sind (Standardsprache DE
# liegt an der Wurzel, EN unter /en/).
VIDEO_SEITEN = {"de": "videos.html", "en": "en/videos.html"}


def _xml(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def video_sitemap_schreiben(config):
    meta = config["extra"].get("video_meta") or {}
    site_url = config["site_url"]
    zeilen = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">',
    ]
    for lang, seite in VIDEO_SEITEN.items():
        videos = meta.get(lang)
        if not videos:
            continue
        zeilen.append("  <url>")
        zeilen.append("    <loc>%s%s</loc>" % (site_url, seite))
        for v in videos:
            zeilen += [
                "    <video:video>",
                "      <video:thumbnail_loc>%s%s</video:thumbnail_loc>" % (site_url, v["thumbnailUrl"]),
                "      <video:title>%s</video:title>" % _xml(v["name"]),
                "      <video:description>%s</video:description>" % _xml(v["description"]),
                "      <video:content_loc>%s%s</video:content_loc>" % (site_url, v["contentUrl"]),
                "      <video:duration>%d</video:duration>" % _iso_sekunden(v["duration"]),
                "      <video:publication_date>%s</video:publication_date>" % v["uploadDate"],
                "      <video:family_friendly>yes</video:family_friendly>",
                "    </video:video>",
            ]
        zeilen.append("  </url>")
    zeilen.append("</urlset>")
    if len(zeilen) <= 4:
        return
    pfad = os.path.join(config["site_dir"], "video-sitemap.xml")
    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write("\n".join(zeilen) + "\n")


ISO_DAUER = re.compile(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?")


def _iso_sekunden(dauer):
    h, m, s = (int(x or 0) for x in ISO_DAUER.fullmatch(dauer).groups())
    return h * 3600 + m * 60 + s


def on_post_build(config):
    """x-default in die Sitemap nachtragen, sitemap.xml.gz neu schreiben,
    Video-Sitemap erzeugen."""
    video_sitemap_schreiben(config)
    pfad = os.path.join(config["site_dir"], "sitemap.xml")
    if not os.path.exists(pfad):
        return

    with open(pfad, encoding="utf-8") as datei:
        inhalt = datei.read()

    if 'hreflang="x-default"' in inhalt:
        return

    def ergaenzen(treffer):
        return '%s\n%s<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % (
            treffer.group(0),
            treffer.group("einzug"),
            treffer.group("href"),
        )

    inhalt, anzahl = SITEMAP_ALTERNATE.subn(ergaenzen, inhalt)
    if not anzahl:
        return

    with open(pfad, "w", encoding="utf-8") as datei:
        datei.write(inhalt)

    # MkDocs liefert beide Fassungen aus — die gepackte muss mitziehen.
    gz_pfad = pfad + ".gz"
    if os.path.exists(gz_pfad):
        with gzip.GzipFile(gz_pfad, "wb", mtime=0) as datei:
            datei.write(inhalt.encode("utf-8"))
