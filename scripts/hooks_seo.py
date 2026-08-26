"""MkDocs-Hook: hreflang-Angaben suchmaschinentauglich machen.

mkdocs-static-i18n erzeugt die Alternate-Links mit relativen Adressen
(`href="../glossary.html"`). Google verlangt fuer hreflang vollstaendig
qualifizierte URLs und ignoriert relative Angaben — die Verknuepfung zwischen
DE und EN kommt so nicht an. Der Hook loest sie gegen die kanonische URL der
Seite auf und haengt x-default an.

Registriert in mkdocs.yml unter `hooks:`.
"""
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
