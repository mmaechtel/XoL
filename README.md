# XoL — X-Plane on Linux

Bilingual documentation site (German/English) for running [X-Plane 12](https://www.x-plane.com/) on Linux. Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), hosted at [emvisio.com](https://emvisio.com/).

## Prerequisites

- **pyenv** — Python version management. The `.python-version` in the repo root enforces the correct Python version automatically.
- **pip** — Python package manager (comes with pyenv-installed Python).

## Setup

```bash
# 1. Install pyenv (if not already installed)
# See https://github.com/pyenv/pyenv#installation

# 2. Install the Python version specified in .python-version
pyenv install

# 3. Install dependencies
pip install mkdocs \
            mkdocs-material \
            mkdocs-material-extensions \
            mkdocs-static-i18n \
            mkdocs-git-revision-date-localized-plugin \
            mkdocs-publisher \
            pymdown-extensions \
            pillow
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

Content is provided as-is for the X-Plane on Linux community.
