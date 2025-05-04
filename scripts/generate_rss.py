import os
import re
import datetime
from pathlib import Path
import frontmatter
import jinja2

def extract_description(content):
    # Extrahiere den ersten Absatz als Beschreibung
    paragraphs = content.split('\n\n')
    for p in paragraphs:
        if p.strip() and not p.startswith('#'):
            return p.strip()
    return ""

def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return datetime.datetime.now()

def generate_rss():
    # Verzeichnisse einrichten
    base_dir = Path(__file__).parent.parent
    blog_dir = base_dir / 'docs' / 'en' / 'blog'
    rss_dir = base_dir / 'docs' / 'assets' / 'rss'
    rss_dir.mkdir(parents=True, exist_ok=True)

    # Blog-Einträge sammeln
    posts = []
    for post_file in blog_dir.glob('*.md'):
        with open(post_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            
            # URL aus dem Dateinamen erstellen
            url = f"/en/blog/{post_file.stem}/"
            
            # Beschreibung extrahieren
            description = extract_description(post.content)
            
            # Datum parsen
            date = parse_date(post.get('date', ''))
            
            posts.append({
                'title': post.get('title', ''),
                'description': description,
                'url': url,
                'date': date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
                'author': post.get('author', 'XoL Team'),
                'tags': post.get('tags', [])
            })

    # Nach Datum sortieren (neueste zuerst)
    posts.sort(key=lambda x: x['date'], reverse=True)

    # RSS-Feed generieren
    template_dir = base_dir / 'docs' / 'assets' / 'rss'
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_dir)))
    template = env.get_template('blog.xml')

    now = datetime.datetime.now()
    rss_content = template.render(
        posts=posts,
        last_build_date=now.strftime('%a, %d %b %Y %H:%M:%S GMT'),
        pub_date=now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    )

    # RSS-Feed speichern
    with open(rss_dir / 'blog.xml', 'w', encoding='utf-8') as f:
        f.write(rss_content)

if __name__ == '__main__':
    generate_rss() 