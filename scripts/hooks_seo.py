"""MkDocs-Hook: hreflang-Angaben suchmaschinentauglich machen.

mkdocs-static-i18n erzeugt die Alternate-Links mit relativen Adressen
(`href="../glossary.html"`). Google verlangt fuer hreflang vollstaendig
qualifizierte URLs und ignoriert relative Angaben — die Verknuepfung zwischen
DE und EN kommt so nicht an. Der Hook loest sie gegen die kanonische URL der
Seite auf und haengt x-default an.

Dieselbe x-default-Angabe fehlt auch in der von MkDocs erzeugten sitemap.xml
und wird nach dem Build nachgetragen (siehe on_post_build).

Registriert in mkdocs.yml unter `hooks:`.
"""
import gzip
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


def on_post_build(config):
    """x-default in die Sitemap nachtragen und sitemap.xml.gz neu schreiben."""
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
