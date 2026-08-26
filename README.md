# XoL — X-Plane on Linux

Bilingual documentation site (German/English) for running [X-Plane 12](https://www.x-plane.com/) on Linux. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), hosted at [xol.emvisio.de](https://xol.emvisio.de/).

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Start local dev server (http://127.0.0.1:8000)
mkdocs serve

# Build static site (output in site/)
mkdocs build

# Deploy to server (dry run)
./update_emvisio.sh <hostname> --dry

# Deploy to server
./update_emvisio.sh <hostname>
```

## Content Structure

```
docs/
  de/          German (default language)
  en/          English
```

Every page exists in both languages with identical filenames. Navigation is defined in `mkdocs.yml` per locale.

## License

Content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [LICENSE](LICENSE) for the full text.
