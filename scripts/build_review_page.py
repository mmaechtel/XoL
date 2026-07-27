#!/usr/bin/env python3
"""Baut aus Faktencheck-Rohdaten eine HTML-Review-Seite mit Vorher/Nachher-Diff.

Aufruf:
    python3 scripts/build_review_page.py <findings.json> <decisions.json> <out.html> [Titel]

findings.json   Liste: [{"page","upstream","findings":[{line,severity,category,claim,
                evidence,source_url,correction}]}]
decisions.json  Liste: [{"page","titel","frage","empfehlung","begruendung","tragweite","zeilen"}]

Die Seite ist self-contained (CSP-tauglich): kein externes CSS, JS oder Font.
"""
import json
import sys
import html
import shutil
import subprocess
import tempfile
import re
import collections

SEV = {
    "FAIL": ("fail", "falsch"),
    "HALLUZINIERT": ("hall", "erfunden"),
    "WARN": ("warn", "ungenau"),
    "VERSION_ENTFERNEN": ("vers", "Version raus"),
    "NV": ("nv", "unbelegt"),
}
ORDER = {"hoch": 0, "mittel": 1, "niedrig": 2}


def esc(s):
    return html.escape(str(s or ""))


def strip_prefix(p, pref):
    return p.replace(pref, "")


def diffblock(diff, page, line):
    f = diff.get(page, {}).get(line)
    if not f:
        return f'<p class="miss">Zeile {line}: kein Datensatz</p>'
    cls, lab = SEV.get(f["severity"], ("warn", f["severity"]))
    corr = (f.get("correction") or "").strip()
    entf = corr.upper().rstrip(".") == "ENTFERNEN"
    neu = '<span class="gone">ersatzlos streichen</span>' if entf else f"<code>{esc(corr)}</code>"
    src = f.get("source_url", "") or ""
    srch = f'<a href="{esc(src)}" target="_blank" rel="noopener">Quelle</a>' if src.startswith("http") else ""
    return f"""<div class="dif">
<div class="difhead"><span class="ln">Zeile {line}</span><span class="sev {cls}">{esc(lab)}</span><span class="cat">{esc(f.get('category'))}</span>{srch}</div>
<div class="cols">
<div class="col ist"><span class="lbl">Ist</span><code>{esc((f.get('claim') or '').strip())}</code></div>
<div class="col neu"><span class="lbl">Neu</span>{neu}</div>
</div>
<details class="ev"><summary>Beleg</summary><p>{esc(f.get('evidence'))}</p></details>
</div>"""


def build(findings_path, decisions_path, out_path, titel="Faktencheck — Freigabe"):
    diff = {p["page"]: {f["line"]: f for f in p["findings"]} for p in json.load(open(findings_path))}
    dec = json.load(open(decisions_path))
    dec.sort(key=lambda c: (ORDER.get(c["tragweite"], 9), c["page"], c["titel"]))

    prefix = "docs/en/"
    cards = []
    for i, c in enumerate(dec):
        rec = c["empfehlung"]
        lines = "".join(diffblock(diff, c["page"], l) for l in c["zeilen"])
        n = len(c["zeilen"])
        zh = f'<span class="nz">{n} Stellen</span>' if n > 1 else ""
        uns = (f'<span class="uns" title="{esc(c["unsicher"])}">unsicher</span>'
               if c.get("unsicher") else "")
        cards.append(f"""<article class="card" data-tw="{c['tragweite']}" data-uns="{1 if c.get('unsicher') else 0}" data-k="{esc(c['page'])}|{esc(c['titel'])}" id="d{i}">
<header class="chead">
<div class="ctop"><span class="tw {c['tragweite']}">{c['tragweite']}</span><span class="pg">{esc(strip_prefix(c['page'], prefix))}</span>{zh}{uns}<span class="st"></span></div>
<h3>{esc(c['titel'])}</h3>
<p class="q">{esc(c['frage'])}</p>
</header>
<p class="rec"><span class="recb {rec}">Empfehlung: {rec}</span> {esc(c['begruendung'])}</p>
<details class="difs"><summary>{n} Textstelle{'n' if n > 1 else ''} zeigen</summary>{lines}</details>
<div class="act">
<button class="b ja" data-a="ja">übernehmen</button>
<button class="b nein" data-a="nein">ablehnen</button>
<button class="b mrk" data-a="mark">markieren</button>
</div>
</article>""")

    tw = collections.Counter(c["tragweite"] for c in dec)
    nuns = sum(1 for c in dec if c.get("unsicher"))
    nfind = sum(len(c["zeilen"]) for c in dec)
    npages = len({c["page"] for c in dec})

    css = """
:root{--bg:#F2F4F5;--surf:#FFF;--surf2:#E9ECEE;--ink:#15191C;--ink2:#525C63;--ink3:#7C868D;
--line:#D3D9DC;--acc:#2D6E7E;--acc2:#EAF2F3;--fail:#B3261E;--hall:#6B3FA0;--warn:#8A5A00;
--vers:#3F5566;--nv:#6B7076;--ist:#FDF3F2;--istb:#E8C4C0;--neu:#F0F7F2;--neub:#B8D6C2;
--r:5px;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
--sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@media (prefers-color-scheme:dark){:root{--bg:#131719;--surf:#1B2023;--surf2:#242A2E;
--ink:#E3E8EA;--ink2:#A3ADB3;--ink3:#7A848A;--line:#333B40;--acc:#5FA8B8;--acc2:#1D2E33;
--fail:#F2837B;--hall:#B99AE0;--warn:#D9A441;--vers:#8FA6B5;--nv:#98A0A6;--ist:#2B1E1E;
--istb:#5C3A38;--neu:#1B2A21;--neub:#375943}}
:root[data-theme="dark"]{--bg:#131719;--surf:#1B2023;--surf2:#242A2E;--ink:#E3E8EA;
--ink2:#A3ADB3;--ink3:#7A848A;--line:#333B40;--acc:#5FA8B8;--acc2:#1D2E33;--fail:#F2837B;
--hall:#B99AE0;--warn:#D9A441;--vers:#8FA6B5;--nv:#98A0A6;--ist:#2B1E1E;--istb:#5C3A38;
--neu:#1B2A21;--neub:#375943}
:root[data-theme="light"]{--bg:#F2F4F5;--surf:#FFF;--surf2:#E9ECEE;--ink:#15191C;
--ink2:#525C63;--ink3:#7C868D;--line:#D3D9DC;--acc:#2D6E7E;--acc2:#EAF2F3;--fail:#B3261E;
--hall:#6B3FA0;--warn:#8A5A00;--vers:#3F5566;--nv:#6B7076;--ist:#FDF3F2;--istb:#E8C4C0;
--neu:#F0F7F2;--neub:#B8D6C2}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 var(--sans);
-webkit-font-smoothing:antialiased}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px 80px}
header.top{border-bottom:1px solid var(--line);background:var(--surf);position:sticky;top:0;z-index:10}
.tin{max-width:1120px;margin:0 auto;padding:14px 20px;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
h1{font-size:16px;margin:0;letter-spacing:-.01em;font-weight:650}
.sub{color:var(--ink3);font-size:12.5px;margin:0}
.sp{flex:1}
.fil{display:flex;gap:5px}
.fb{font:inherit;font-size:12.5px;padding:4px 11px;border:1px solid var(--line);
background:var(--surf);color:var(--ink2);border-radius:99px;cursor:pointer}
.fb[aria-pressed="true"]{background:var(--acc);border-color:var(--acc);color:#fff}
.fb:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
.cnt{font-variant-numeric:tabular-nums;font-size:12.5px;color:var(--ink3)}
.intro{padding:26px 0 16px;max-width:66ch}
.intro h2{font-size:22px;margin:0 0 8px;letter-spacing:-.015em;text-wrap:balance}
.intro p{margin:0 0 8px;color:var(--ink2);font-size:14px}
.card{background:var(--surf);border:1px solid var(--line);border-radius:var(--r);margin:0 0 14px;overflow:hidden}
.card.hide{display:none}
.card.done{opacity:.5}
.chead{padding:14px 16px 0}
.ctop{display:flex;gap:8px;align-items:center;margin-bottom:7px;flex-wrap:wrap}
.tw{font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;font-weight:700;padding:2px 8px;border-radius:3px}
.tw.hoch{background:var(--fail);color:var(--surf)}
.tw.mittel{background:var(--warn);color:var(--surf)}
.tw.niedrig{background:var(--surf2);color:var(--ink2)}
.pg{font:12px var(--mono);color:var(--ink3)}
.nz{font-size:11px;color:var(--ink3);border:1px solid var(--line);padding:1px 7px;border-radius:99px}
.chead h3{font-size:16.5px;margin:0 0 5px;letter-spacing:-.01em;text-wrap:balance}
.q{margin:0;color:var(--ink2);font-size:14px}
.rec{margin:12px 16px;padding:11px 13px;background:var(--acc2);border-left:2px solid var(--acc);
border-radius:0 3px 3px 0;font-size:13.5px;color:var(--ink2)}
.recb{font-weight:700;color:var(--ink);margin-right:4px}
.recb.ja::before{content:"✓ "}
.recb.nein::before{content:"✕ "}
.difs{padding:0 16px}
.dif{border-top:1px solid var(--line);padding:12px 0}
.difhead{display:flex;gap:8px;align-items:center;margin-bottom:8px;flex-wrap:wrap}
.ln{font:11.5px var(--mono);color:var(--ink3)}
.sev{font-size:10.5px;text-transform:uppercase;letter-spacing:.05em;font-weight:700}
.sev.fail{color:var(--fail)}.sev.hall{color:var(--hall)}.sev.warn{color:var(--warn)}
.sev.vers{color:var(--vers)}.sev.nv{color:var(--nv)}
.cat{font-size:11px;color:var(--ink3)}
.difhead a{font-size:11.5px;color:var(--acc);margin-left:auto}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:9px}
@media(max-width:720px){.cols{grid-template-columns:1fr}}
.col{padding:9px 11px;border-radius:3px;overflow-x:auto}
.col.ist{background:var(--ist);border:1px solid var(--istb)}
.col.neu{background:var(--neu);border:1px solid var(--neub)}
.lbl{display:block;font-size:10px;text-transform:uppercase;letter-spacing:.08em;
color:var(--ink3);margin-bottom:4px;font-weight:700}
.col code{font:12.5px/1.5 var(--mono);white-space:pre-wrap;word-break:break-word;display:block}
.gone{font:12.5px var(--mono);color:var(--ink3);font-style:italic}
.ev{margin-top:8px}
.ev summary{font-size:12px;color:var(--ink3);cursor:pointer}
.ev p{margin:6px 0 0;font-size:12.5px;color:var(--ink2);padding-left:11px;border-left:1px solid var(--line)}
.act{display:flex;gap:16px;padding:11px 16px;border-top:1px solid var(--line);background:var(--surf2)}
.ch{font-size:12.5px;color:var(--ink2);display:flex;gap:6px;align-items:center;cursor:pointer}
.bar{position:fixed;bottom:0;left:0;right:0;background:var(--surf);border-top:1px solid var(--line);
padding:10px 20px;display:flex;gap:14px;align-items:center;justify-content:center;font-size:13px}
button.exp{font:inherit;font-size:13px;padding:6px 15px;background:var(--acc);color:#fff;
border:0;border-radius:4px;cursor:pointer}
.miss{font-size:12.5px;color:var(--nv)}
.uns{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;
color:var(--hall);border:1px solid var(--hall);padding:1px 7px;border-radius:99px;cursor:help}
.st{margin-left:auto;font-size:11px;font-weight:700;letter-spacing:.04em;
padding:2px 9px;border-radius:99px;text-transform:uppercase}
.card[data-s="ja"] .st{background:var(--acc);color:#fff}
.card[data-s="nein"] .st{background:var(--fail);color:#fff}
.card[data-s="mark"] .st{background:var(--warn);color:#fff}
.card[data-s="ja"] .st::after{content:"übernehmen"}
.card[data-s="nein"] .st::after{content:"abgelehnt"}
.card[data-s="mark"] .st::after{content:"markiert"}
.card{border-left:3px solid transparent}
.card[data-s="ja"]{border-left-color:var(--acc);background:var(--acc2)}
.card[data-s="nein"]{border-left-color:var(--fail)}
.card[data-s="mark"]{border-left-color:var(--warn)}
.card[data-s] .chead h3,.card[data-s] .q{opacity:.65}
.card.cur{border-color:var(--acc);box-shadow:0 0 0 2px var(--acc2)}
.difs{padding:0 16px;border-top:1px solid var(--line);margin-top:12px}
.difs>summary{padding:10px 0;font-size:12.5px;color:var(--acc);cursor:pointer}
.difs[open]>summary{color:var(--ink3)}
.b{font:inherit;font-size:12.5px;padding:5px 13px;border:1px solid var(--line);
background:var(--surf);color:var(--ink2);border-radius:4px;cursor:pointer}
.b:hover{border-color:var(--acc);color:var(--ink)}
.card[data-s="ja"] .b.ja{background:var(--acc);border-color:var(--acc);color:#fff}
.card[data-s="nein"] .b.nein{background:var(--fail);border-color:var(--fail);color:#fff}
.card[data-s="mark"] .b.mrk{background:var(--warn);border-color:var(--warn);color:#fff}
.prog{height:3px;background:var(--surf2);position:absolute;bottom:-1px;left:0;right:0}
.prog>i{display:block;height:100%;background:var(--acc);width:0;transition:width .2s}
kbd{font:11px var(--mono);background:var(--surf2);border:1px solid var(--line);
border-radius:3px;padding:1px 5px;color:var(--ink2)}
.hint{font-size:12.5px;color:var(--ink3);margin:0}
.out{position:fixed;inset:0;background:rgba(0,0,0,.45);display:none;
place-items:center;z-index:20;padding:20px}
.out[open]{display:grid}
.outb{background:var(--surf);border:1px solid var(--line);border-radius:var(--r);
padding:18px;max-width:640px;width:100%;display:flex;flex-direction:column;gap:11px}
.outb h4{margin:0;font-size:15px}
.outb textarea{width:100%;height:220px;font:12.5px/1.5 var(--mono);padding:10px;
background:var(--bg);color:var(--ink);border:1px solid var(--line);border-radius:4px;resize:vertical}
.outr{display:flex;gap:9px;justify-content:flex-end}
.okmsg{font-size:12.5px;color:var(--acc);margin:0}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
"""

    js = r"""
const KEY='faktencheck-v1';
const cards=[...document.querySelectorAll('.card')];
const cnt=document.getElementById('cnt'),stat=document.getElementById('stat'),
      pro=document.getElementById('pro');
let st=JSON.parse(localStorage.getItem(KEY)||'{}');
let cur=0,filt='hoch';

function save(){localStorage.setItem(KEY,JSON.stringify(st));}
function apply(){
  cards.forEach(c=>{
    const v=st[c.dataset.k];
    if(v)c.dataset.s=v; else c.removeAttribute('data-s');
    const off=(filt==='offen'&&v)||(filt==='unsicher'&&c.dataset.uns!=='1')
             ||(['hoch','mittel','niedrig'].includes(filt)&&c.dataset.tw!==filt);
    c.classList.toggle('hide',off);
  });
  upd();
}
function upd(){
  const vis=cards.filter(c=>!c.classList.contains('hide'));
  const done=cards.filter(c=>st[c.dataset.k]).length;
  cnt.textContent=vis.length+' sichtbar';
  stat.textContent=done+' von '+cards.length+' entschieden';
  pro.style.width=(done/cards.length*100)+'%';
}
function set(c,a){st[c.dataset.k]=a;save();apply();}
function vis(){return cards.filter(c=>!c.classList.contains('hide'));}
function focus(n){
  const v=vis(); if(!v.length)return;
  cur=Math.max(0,Math.min(n,v.length-1));
  cards.forEach(c=>c.classList.remove('cur'));
  v[cur].classList.add('cur');
  v[cur].scrollIntoView({block:'center',behavior:'smooth'});
}
document.querySelectorAll('.fb').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.fb').forEach(x=>x.setAttribute('aria-pressed','false'));
  b.setAttribute('aria-pressed','true');filt=b.dataset.f;apply();focus(0);
}));
document.addEventListener('click',e=>{
  const b=e.target.closest('.act .b'); if(!b)return;
  const c=b.closest('.card'); if(!c)return;
  set(c,b.dataset.a);
});
document.addEventListener('keydown',e=>{
  if(e.target.matches('input,textarea')||e.metaKey||e.ctrlKey)return;
  const v=vis(); const c=v[cur];
  if(e.key==='j'){focus(cur+1);e.preventDefault();}
  else if(e.key==='k'){focus(cur-1);e.preventDefault();}
  else if(c&&'ynm'.includes(e.key)){
    set(c,{y:'ja',n:'nein',m:'mark'}[e.key]);
    const nv=vis(); if(cur<nv.length)focus(cur); else focus(nv.length-1);
    e.preventDefault();
  }
  else if(c&&e.key==='Enter'){c.querySelector('.difs').open=!c.querySelector('.difs').open;e.preventDefault();}
});
function report(){
  const out=[];
  cards.forEach(c=>{
    const v=st[c.dataset.k];
    if(!v||v==='ja')return;
    out.push((v==='mark'?'MARKIERT ':'ABGELEHNT')+'  '+c.querySelector('.pg').textContent
      +' — '+c.querySelector('h3').textContent);
  });
  const off=cards.filter(c=>!st[c.dataset.k]).length;
  let t=out.length?out.join('\n'):'keine Abweichungen — alles wie empfohlen';
  if(off)t+='\n\n('+off+' noch nicht entschieden)';
  return t;
}
document.getElementById('exp').addEventListener('click',()=>{
  const t=report(), ta=document.getElementById('outt'), msg=document.getElementById('okmsg');
  ta.value=t; document.getElementById('out').setAttribute('open','');
  ta.focus(); ta.select();
  msg.textContent='';
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(t)
      .then(()=>{msg.textContent='In die Zwischenablage kopiert.';})
      .catch(()=>{msg.textContent='Zwischenablage nicht erlaubt — Text ist markiert, mit Strg+C kopieren.';});
  } else {
    msg.textContent='Zwischenablage nicht verfügbar — Text ist markiert, mit Strg+C kopieren.';
  }
});
document.getElementById('outx').addEventListener('click',()=>
  document.getElementById('out').removeAttribute('open'));
document.getElementById('out').addEventListener('click',e=>{
  if(e.target.id==='out')e.target.removeAttribute('open');
});
document.getElementById('rst').addEventListener('click',()=>{st={};save();apply();focus(0);});
apply();focus(0);
"""

    page = f"""<title>{esc(titel)}</title>
<style>{css}</style>
<header class="top"><div class="tin">
<div><h1>{esc(titel)}</h1><p class="sub">{npages} Seiten · {nfind} Befunde · {len(dec)} Entscheidungen</p></div>
<div class="sp"></div>
<div class="fil">
<button class="fb" data-f="hoch" aria-pressed="true">hoch {tw['hoch']}</button>
<button class="fb" data-f="mittel" aria-pressed="false">mittel {tw['mittel']}</button>
<button class="fb" data-f="niedrig" aria-pressed="false">niedrig {tw['niedrig']}</button>
<button class="fb" data-f="unsicher" aria-pressed="false">unsicher {nuns}</button>
<button class="fb" data-f="offen" aria-pressed="false">offen</button>
<button class="fb" data-f="alle" aria-pressed="false">alle</button>
</div>
<span class="cnt" id="cnt"></span>
<div class="prog"><i id="pro"></i></div>
</div></header>
<div class="wrap">
<section class="intro">
<h2>Was geändert werden soll</h2>
<p>Eine Karte ist eine Entscheidung, kein Einzelfund — wo mehrere Textstellen an derselben Frage hängen, sind sie zusammengefasst. Die Textstellen sind eingeklappt; du brauchst sie nur, wenn dir Frage und Begründung nicht reichen.</p>
<p>Die Seite startet auf <strong>hoch</strong> ({tw['hoch']} Stück) — dort ändert sich Empfehlung, Linux-Tauglichkeit oder Deprecation. Karten mit <span class="uns">unsicher</span> stützen sich auf einen schwachen Beleg; die lohnen einen zweiten Blick.</p>
<p class="hint">Tastatur: <kbd>j</kbd>/<kbd>k</kbd> weiter/zurück · <kbd>y</kbd> übernehmen · <kbd>n</kbd> ablehnen · <kbd>m</kbd> markieren · <kbd>Enter</kbd> Textstellen auf/zu. Dein Stand wird im Browser gespeichert und überlebt einen Reload.</p>
</section>
{''.join(cards)}
</div>
<div class="bar">
<span class="cnt" id="stat"></span>
<button class="exp" id="exp">Abweichungen kopieren</button>
<button class="b" id="rst">zurücksetzen</button>
</div>
<div class="out" id="out"><div class="outb">
<h4>Deine Abweichungen</h4>
<p class="hint">Alles, was hier nicht steht, wird wie empfohlen umgesetzt. Text in den Chat einfügen.</p>
<textarea id="outt" readonly></textarea>
<p class="okmsg" id="okmsg"></p>
<div class="outr"><button class="b" id="outx">schließen</button></div>
</div></div>
<script>{js}</script>"""

    open(out_path, "w").write(page)
    validate(out_path)
    return len(dec), nfind


def validate(path):
    """Prueft das erzeugte HTML. Ein Syntaxfehler im Script-Block legt die ganze
    Seite lahm, ohne dass man es ihr ansieht — deshalb hart pruefen, nicht warnen.

    Hintergrund: Escape-Sequenzen durchlaufen zwei Ebenen (Python-Quelltext ->
    emittiertes JS). Ein \\n, das zu einem echten Zeilenumbruch kollabiert,
    zerreisst den String und damit jedes Event-Handling auf der Seite.
    """
    src = open(path).read()
    problems = []

    m = re.search(r"<script>(.*?)</script>", src, re.S)
    if not m:
        problems.append("kein <script>-Block gefunden")
    elif shutil.which("node"):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
            fh.write(m.group(1))
            tmp = fh.name
        r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
        if r.returncode:
            problems.append("JS-Syntaxfehler:\n" + r.stderr.strip())
    else:
        # Ersatzpruefung ohne node: unterminierte Stringliterale finden
        for i, ln in enumerate(m.group(1).split("\n"), 1):
            if ln.count("'") % 2 or ln.count('"') % 2:
                problems.append(f"JS Zeile {i}: unterminierter String — {ln.strip()[:60]}")

    # Elemente, die das Script per getElementById erwartet
    for eid in ("cnt", "stat", "pro", "exp", "rst"):
        if f'id="{eid}"' not in src:
            problems.append(f'Element id="{eid}" fehlt — Script bricht beim Laden ab')

    if '<article class="card"' not in src:
        problems.append("keine Karten gerendert — f-String-Klammern doppelt escaped?")

    for bad in ("\\2713", "\\2715", "\\25CF"):
        if bad in src:
            problems.append(f"CSS-Escape {bad} nicht aufgeloest — Unicode-Zeichen direkt einsetzen")

    if problems:
        print("VALIDIERUNG FEHLGESCHLAGEN:", file=sys.stderr)
        for p in problems:
            print("  - " + p, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    t = sys.argv[4] if len(sys.argv) > 4 else "Faktencheck — Freigabe"
    n, f = build(sys.argv[1], sys.argv[2], sys.argv[3], t)
    print(f"{sys.argv[3]}: {n} Entscheidungen aus {f} Befunden")
