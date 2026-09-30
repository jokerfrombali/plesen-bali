# -*- coding: utf-8 -*-
"""Сайт «Антиплесень · Бали»: удаление плесени (основное) + малярные работы. Выход: docs/ (GitHub Pages)."""
import json, os, re, shutil, html, urllib.parse
from districts import DISTRICTS
from mold_data import SERVICES, PAINT, MOLD_D, GRID, ARTICLES, district_article

ROOT = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(ROOT, "site_config.json"), encoding="utf-8"))
OUT = os.path.join(ROOT, "docs")
B = CFG["base_path"].rstrip("/")
E = html.escape
CSS = """:root{--bg:#FBF8F3;--surface:#fff;--ink:#1B2B27;--muted:#5B6B66;--line:#E8E2D8;--brand:#1F5E4F;--brand-2:#E9F2EE;--accent:#F2A65A;--accent-2:#FCEBD8;--wa:#25D366;--radius:20px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:600;line-height:1.15;letter-spacing:-.01em;margin:0 0 .5em}
h1{font-size:clamp(2rem,5vw,3.4rem)}h2{font-size:clamp(1.5rem,3vw,2.2rem)}h3{font-size:1.18rem}
a{color:var(--brand)}p{margin:0 0 1em}img{max-width:100%;display:block}
.wrap{max-width:1120px;margin:0 auto;padding-left:20px;padding-right:20px}
header{position:sticky;top:0;z-index:40;background:rgba(251,248,243,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
.nav{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.logo{font-family:Fraunces,serif;font-weight:600;font-size:1.3rem;color:var(--ink);text-decoration:none;white-space:nowrap}.logo span{color:var(--accent)}
.menu{display:flex;align-items:center;gap:22px}.menu>a,.dd>summary{color:var(--muted);text-decoration:none;font-size:.95rem;cursor:pointer;list-style:none}
.menu>a:hover,.dd>summary:hover{color:var(--ink)}.dd{position:relative}.dd>summary::-webkit-details-marker{display:none}.dd>summary::after{content:" ▾";font-size:.75em}
.dd-panel{position:absolute;top:34px;left:-16px;background:var(--surface);border:1px solid var(--line);border-radius:16px;box-shadow:0 16px 40px rgba(27,43,39,.12);padding:10px;display:grid;grid-template-columns:1fr 1fr;gap:2px;min-width:440px}
.dd-panel a{padding:8px 12px;border-radius:10px;text-decoration:none;color:var(--ink);font-size:.93rem}.dd-panel a:hover{background:var(--brand-2)}
.burger{display:none}
.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 22px;border-radius:999px;font-weight:600;text-decoration:none;font-size:1rem;transition:transform .15s,box-shadow .15s;white-space:nowrap}
.btn:hover{transform:translateY(-1px)}.btn-wa{background:var(--wa);color:#fff;box-shadow:0 6px 20px rgba(37,211,102,.3)}
.btn-ghost{background:transparent;color:var(--ink);border:1.5px solid var(--line)}.btn-sm{padding:9px 16px;font-size:.9rem}
.wa-ico{width:20px;height:20px;fill:currentColor;flex:none}
.hero{padding-top:56px;padding-bottom:48px;display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.eyebrow{display:inline-block;background:var(--brand-2);color:var(--brand);padding:6px 14px;border-radius:999px;font-size:.85rem;font-weight:600;margin-bottom:18px}
.lead{font-size:1.15rem;color:var(--muted);max-width:36em}
.cta-row{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0 18px}
.trust{display:flex;gap:10px 22px;flex-wrap:wrap;color:var(--muted);font-size:.92rem;list-style:none;padding:0;margin:0}
.trust li::before{content:"✓ ";color:var(--brand);font-weight:700}
.photo{position:relative;border-radius:28px;overflow:hidden;aspect-ratio:4/5;background:var(--accent-2)}.photo img{width:100%;height:100%;object-fit:cover}
.chip{position:absolute;left:18px;bottom:18px;background:#fff;border-radius:14px;padding:12px 16px;box-shadow:0 10px 30px rgba(0,0,0,.1);font-size:.9rem;max-width:80%}
.chip b{display:block;font-family:Fraunces,serif;font-size:1.05rem}
section{padding:56px 0}.alt-bg{background:var(--surface);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.sec-head{max-width:680px;margin-bottom:30px}.sec-head p{color:var(--muted)}
.grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit;display:flex;flex-direction:column;transition:border-color .15s,box-shadow .15s,transform .15s}
a.card:hover{border-color:#cfd9d4;box-shadow:0 12px 30px rgba(27,43,39,.08);transform:translateY(-2px)}
.card img{aspect-ratio:16/10;object-fit:cover;width:100%}.card .body{padding:18px 20px 22px}.card h3{margin-bottom:6px}.card p{color:var(--muted);font-size:.95rem;margin:0}
.pills{display:flex;flex-wrap:wrap;gap:10px;padding:0;list-style:none;margin:0}.pills a,.pills span{display:inline-block;background:var(--brand-2);color:var(--brand);border-radius:999px;padding:9px 16px;font-weight:600;font-size:.93rem;text-decoration:none}
.pills a:hover{background:#d8eae3}
.split{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}.split .photo{aspect-ratio:4/3}
.steps{counter-reset:s;display:grid;grid-template-columns:repeat(4,1fr);gap:18px;padding:0;list-style:none;margin:0}
.steps li{counter-increment:s;background:var(--surface);border-radius:var(--radius);padding:22px;border:1px solid var(--line)}
.steps li::before{content:counter(s);display:grid;place-items:center;width:36px;height:36px;border-radius:50%;background:var(--accent-2);color:#b0632a;font-weight:700;margin-bottom:12px}
.steps b{display:block;margin-bottom:4px}.steps.one{grid-template-columns:1fr}
.checks{list-style:none;padding:0;display:grid;gap:10px;margin:0}.checks li{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 18px}
.checks li::before{content:"✓";color:var(--brand);font-weight:700;margin-right:10px}
details.faq{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 18px;margin-bottom:10px}details.faq summary{cursor:pointer;font-weight:600}
details.faq p{margin:.6em 0 0;color:var(--muted)}
.crumbs{font-size:.88rem;color:var(--muted);padding-top:18px}.crumbs a{color:var(--muted)}
.band{background:var(--brand);color:#fff;border-radius:28px;padding:44px;display:grid;grid-template-columns:1.4fr 1fr;gap:24px;align-items:center}
.band h2{color:#fff}.band p{color:#d5e6df;margin:0}.band .cta-row{margin:0;justify-content:flex-end}
.page-hero{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center;padding-top:24px;padding-bottom:16px}.page-hero .photo{aspect-ratio:4/3}
.prose{max-width:760px}.prose h2{margin-top:1.6em}
.toc{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin:18px 0}.toc ol{margin:0;padding-left:20px}
.answer{background:var(--brand-2);border-radius:16px;padding:18px 22px;margin:14px 0 6px}
footer{border-top:1px solid var(--line);padding:40px 0 100px;color:var(--muted);font-size:.9rem}
.fcols{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-bottom:24px}.fcols a{display:block;color:var(--muted);text-decoration:none;padding:3px 0}.fcols b{color:var(--ink);display:block;margin-bottom:6px}
.ver{opacity:.6}.mbar{display:none}
.promises{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}.promise{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px}
.promise b{font-family:Fraunces,serif;font-size:1.15rem;display:block;margin-bottom:6px}.promise b::before{content:"✓ ";color:var(--brand)}.promise p{margin:0;color:var(--muted);font-size:.95rem}
.qf{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;background:var(--accent-2);border-radius:28px;padding:40px}
.qform{display:grid;gap:14px}.qform label{display:grid;gap:6px;font-weight:600;font-size:.92rem}
.qform select,.qform input{font:inherit;padding:13px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);width:100%}
.qform .btn{justify-content:center;border:0;cursor:pointer}
.prices{width:100%;border-collapse:collapse;background:var(--surface);border-radius:16px;overflow:hidden}.prices td{padding:14px 18px;border-bottom:1px solid var(--line)}
.dur{display:inline-block;background:var(--accent-2);color:#8a4b1c;border-radius:999px;padding:6px 14px;font-weight:600;font-size:.9rem;margin:0 0 14px}
@media (max-width:900px){
.menu{display:none}.burger{display:block}.burger>summary{list-style:none;cursor:pointer;width:44px;height:44px;display:grid;place-items:center;border:1.5px solid var(--line);border-radius:12px;font-size:1.3rem}
.burger>summary::-webkit-details-marker{display:none}
.burger[open]>summary{background:var(--brand-2)}
.mpanel{position:fixed;left:0;right:0;top:100%;height:calc(100vh - 68px);height:calc(100dvh - 68px);background:var(--bg);overflow:auto;padding:18px 20px 110px;border-top:1px solid var(--line)}
.mpanel b{display:block;margin:16px 0 6px;font-family:Fraunces,serif;font-size:1.1rem}.mpanel a{display:block;padding:9px 0;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line)}
.head-cta{display:none}body:has(.burger[open]){overflow:hidden}body:has(.burger[open]) .mbar{display:none}
.hero,.split,.page-hero,.band,.qf{grid-template-columns:1fr}.qf{padding:24px}.hero{padding-top:26px}.steps{grid-template-columns:1fr 1fr}.band{padding:28px}.band .cta-row{justify-content:flex-start}
.photo{aspect-ratio:4/3}.fcols{grid-template-columns:1fr 1fr}
.mbar{display:flex;position:fixed;left:12px;right:12px;bottom:12px;z-index:50}.mbar .btn{width:100%;justify-content:center}}
@media (max-width:520px){.steps{grid-template-columns:1fr}body{font-size:16px}.fcols{grid-template-columns:1fr}}"""
WA_SVG = '<svg class="wa-ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.4.6-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.4 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.8-.2 1.3z"/></svg>'
EXTRA_CSS = """
.promises{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}.promise{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);padding:22px}
.promise b{font-family:Fraunces,serif;font-size:1.15rem;display:block;margin-bottom:6px}.promise b::before{content:"✓ ";color:var(--brand)}.promise p{margin:0;color:var(--muted);font-size:.95rem}
.qf{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center;background:var(--accent-2);border-radius:28px;padding:40px}
.qform{display:grid;gap:14px}.qform label{display:grid;gap:6px;font-weight:600;font-size:.92rem}
.qform select,.qform input{font:inherit;padding:13px 14px;border:1.5px solid var(--line);border-radius:12px;background:#fff;color:var(--ink);width:100%}
.qform .btn{justify-content:center;border:0;cursor:pointer}
.prices{width:100%;border-collapse:collapse;background:var(--surface);border-radius:16px;overflow:hidden}.prices td{padding:14px 18px;border-bottom:1px solid var(--line)}
.dur{display:inline-block;background:var(--accent-2);color:#8a4b1c;border-radius:999px;padding:6px 14px;font-weight:600;font-size:.9rem;margin:0 0 14px}
.ver{opacity:.6}.dd-panel.one{grid-template-columns:1fr;min-width:260px}
@media (max-width:900px){.qf{grid-template-columns:1fr;padding:24px}}"""

SITE = CFG["site_url"].rstrip("/")
IMG_ALT = {"hero": "Мастер обрабатывает наружную стену дома", "facade": "Обработка и покраска белого фасада", "ladder": "Мастер на стремянке у фасада",
           "restore": "Мастер работает с деревом", "bali": "Мастер на объекте на Бали", "wood": "Балийский мастер работает с деревом",
           "roller": "Валик с краской на стене", "varnish": "Покрытие дерева кистью", "villa": "Вилла с бассейном на Бали", "deck": "Деревянная терраса после дождя"}
D_IMG = {"sanur": "facade", "changu": "villa", "pererenan": "deck", "seminyak": "ladder", "kuta": "hero",
         "dzhimbaran": "facade", "nusa-dua": "villa", "uluvatu": "roller", "ubud": "wood", "denpasar": "restore"}
SVC = {s["id"]: s for s in SERVICES}
ALL_SVC = SERVICES + PAINT

def art_url(a):
    return f"/stati/{a['slug']}/"

def svc_url(s):
    return f"/uslugi/{s['slug']}/"

def wa_href(text=""):
    n = re.sub(r"[^0-9]", "", CFG.get("whatsapp") or "")
    if n:
        return f"https://wa.me/{n}" + (f"?text={urllib.parse.quote(text)}" if text else "")
    if CFG.get("telegram"):
        return "https://t.me/" + CFG["telegram"].lstrip("@")
    return f"{B}/kontakty/"

def cta(cls="", label="Прислать фото плесени"):
    return f'<a class="btn btn-wa {cls}" href="{wa_href()}">{WA_SVG}{label}</a>'

def img(name, eager=False):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img src="{B}/img/{name}.webp" alt="{E(IMG_ALT[name])}" {load} decoding="async">'

def short(t, n=110):
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + "…"

def cards(items, url, title, text, pic):
    return '<div class="grid">' + "".join(
        f'<a class="card" href="{B}{url(x)}">{img(pic(x))}<div class="body"><h3>{E(title(x))}</h3><p>{E(short(text(x)))}</p></div></a>' for x in items) + "</div>"

def svc_cards(items=None):
    return cards(items or SERVICES, svc_url, lambda s: s["h1"].replace(" на Бали", ""), lambda s: s["intro"], lambda s: s["img"])

def district_cards():
    return cards(DISTRICTS, lambda d: f"/rayony/{d['slug']}/", lambda d: f"Плесень {d['loc']}", lambda d: MOLD_D[d["slug"]]["walls"], lambda d: D_IMG[d["slug"]])

def grid_url(d, sid):
    return f"/rayony/{d['slug']}/{SVC[sid]['slug']}/"

def nav_html():
    mold = "".join(f'<a href="{B}{svc_url(s)}">{E(s["h1"].replace(" на Бали", ""))}</a>' for s in SERVICES)
    paint = "".join(f'<a href="{B}{svc_url(s)}">{E(s["h1"])}</a>' for s in PAINT)
    dl = "".join(f'<a href="{B}/rayony/{d["slug"]}/">{E(d["ru"])}</a>' for d in DISTRICTS)
    desk = (f'<nav class="menu" aria-label="Главное меню"><details class="dd"><summary>Плесень</summary><div class="dd-panel">{mold}</div></details>'
            f'<details class="dd"><summary>Малярные работы</summary><div class="dd-panel one">{paint}</div></details>'
            f'<details class="dd"><summary>Районы</summary><div class="dd-panel">{dl}</div></details>'
            f'<a href="{B}/stati/">Статьи</a><a href="{B}/ceny/">Цены</a><a href="{B}/kontakty/">Контакты</a></nav>')
    mob = (f'<details class="burger"><summary aria-label="Открыть меню">☰</summary><div class="mpanel"><a href="{B}/">Главная</a>'
           f'<b>Удаление плесени</b>{mold}<b>Малярные работы</b>{paint}<b>Районы Бали</b>{dl}'
           f'<b>Ещё</b><a href="{B}/stati/">Статьи</a><a href="{B}/ceny/">Цены</a><a href="{B}/kontakty/">Контакты</a></div></details>')
    return desk, mob

def footer_html():
    col = lambda t, items: f'<div><b>{t}</b>' + "".join(f'<a href="{B}{u}">{E(n)}</a>' for n, u in items) + "</div>"
    return (f'<footer><div class="wrap"><div class="fcols">'
            + col("Удаление плесени", [(s["h1"], svc_url(s)) for s in SERVICES])
            + col("Районы", [(f"Плесень {d['loc']}", f"/rayony/{d['slug']}/") for d in DISTRICTS])
            + col("Ещё", [(s["h1"], svc_url(s)) for s in PAINT] + [("Статьи", "/stati/"), ("Цены", "/ceny/"), ("Контакты", "/kontakty/")])
            + f'</div>{E(CFG["name"])}: удаление плесени, антигрибковая обработка и малярные работы на Бали. '
              f'Советы по безопасности — по общедоступным рекомендациям EPA и CDC; при симптомах обращайтесь к врачу. '
              f'Фотографии — иллюстрации (Pexels, Unsplash). <span class="ver">Версия {E(CFG.get("version", ""))}</span></div></footer>')

def crumbs_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        dict({"@type": "ListItem", "position": i + 1, "name": n}, **({"item": SITE + u} if u else {})) for i, (n, u) in enumerate(items)]}

def faq_schema(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}

def faq_block(qa, title="Частые вопросы"):
    return (f'<section class="alt-bg"><div class="wrap"><div class="sec-head"><h2>{title}</h2></div>' +
            "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in qa) + "</div></section>")

def band(title="Пришлите фото плесени — оценю бесплатно", text="2–3 фото пятен, район и примерная площадь. Отвечу, что это, откуда сырость и что нужно сделать."):
    return f'<section><div class="wrap band"><div><h2>{E(title)}</h2><p>{E(text)}</p></div><div class="cta-row">{cta()}</div></div></section>'

def promises_block():
    items = list(CFG.get("promises") or [])
    if CFG.get("warranty"):
        items.append(["Гарантия", CFG["warranty"]])
    if CFG.get("response_time"):
        items.append(["Быстрый ответ", CFG["response_time"]])
    if not items:
        return ""
    c = "".join(f'<div class="promise"><b>{E(t)}</b><p>{E(x)}</p></div>' for t, x in items)
    return (f'<section><div class="wrap"><div class="sec-head"><h2>Как я работаю</h2><p>Плесень — не косметика. Поэтому сначала причина, потом обработка, '
            f'и всё — прозрачно для вас.</p></div><div class="promises">{c}</div></div></section>')

def master_block():
    if not (CFG.get("master_name") and CFG.get("master_story")):
        return ""
    pic = f'<div class="photo"><img src="{B}/img/{E(CFG["master_photo"])}" alt="{E(CFG["master_name"])}" loading="lazy"></div>' if CFG.get("master_photo") else ""
    return (f'<section class="alt-bg"><div class="wrap split">{pic}<div><span class="eyebrow">Кто приедет</span>'
            f'<h2>{E(CFG["master_name"])}</h2><p>{E(CFG["master_story"])}</p></div></div></section>')

def rating_badge():
    if CFG.get("google_rating") and CFG.get("google_reviews"):
        return f'<li>★ {E(str(CFG["google_rating"]))} в Google · {CFG["google_reviews"]} отзывов</li>'
    return ""

def prices_block():
    pr = CFG.get("prices") or []
    if not pr:
        return ""
    rows = "".join(f'<tr><td>{E(x["name"])}</td><td>от {E(x["from"])} {E(x.get("unit", ""))}</td></tr>' for x in pr)
    return (f'<section class="alt-bg"><div class="wrap"><div class="sec-head"><h2>Ориентиры цен</h2><p>Точная смета — по фото.</p></div>'
            f'<table class="prices">{rows}</table></div></section>')

WHERE = ["Стены и углы", "Потолок", "Ванная: швы, силикон", "Дерево и мебель", "Шкаф и одежда", "Фасад и забор", "Запах, пятен не видно"]

def quick_form():
    d_opts = "".join(f'<option>{E(d["ru"])}</option>' for d in DISTRICTS) + "<option>Другой район</option>"
    w_opts = "".join(f"<option>{E(w)}</option>" for w in WHERE)
    wa = re.sub(r"[^0-9]", "", CFG.get("whatsapp") or "")
    return f"""<section id="zayavka"><div class="wrap qf"><div><h2>Бесплатная оценка по фото</h2>
<p class="lead">Выберите район и где плесень — откроется WhatsApp с готовым сообщением. Приложите 2–3 фото.</p>
<ul class="trust"><li>Без выезда</li><li>Бесплатно</li><li>Скажу, откуда сырость</li></ul></div>
<form class="qform" onsubmit="return qsend(this)"><label>Район<select name="d">{d_opts}</select></label>
<label>Где плесень<select name="w">{w_opts}</select></label>
<label>Комментарий<input name="c" placeholder="например: пятна в спальне после дождей"></label>
<button class="btn btn-wa" type="submit">{WA_SVG}Отправить в WhatsApp</button></form></div></section>
<script>function qsend(f){{var t="Здравствуйте! Плесень. Район: "+f.d.value+". Где: "+f.w.value+". "+f.c.value+" Фото пришлю следом.";
var n="{wa}";location.href=n?"https://wa.me/"+n+"?text="+encodeURIComponent(t):"{B}/kontakty/";return false}}</script>"""

PAGES_META = []

def page(path, title, desc, body, crumbs=None, schema=None, og=None, kind="page"):
    canon = SITE + path
    cr = ""
    if crumbs:
        cr = '<nav class="wrap crumbs" aria-label="Хлебные крошки">' + " › ".join(f'<a href="{B}{u}">{E(t)}</a>' if u else E(t) for t, u in crumbs) + "</nav>"
        schema = (schema or []) + [crumbs_schema(crumbs)]
    sch = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (schema or []))
    desk, mob = nav_html()
    doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{SITE}/img/{og or 'bali'}.webp"><meta name="theme-color" content="#FBF8F3">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{B}/style.css">{sch}</head><body>
<header><div class="wrap nav"><a class="logo" href="{B}/">Антиплесень<span>·</span>Бали</a>{desk}
<span class="head-cta">{cta("btn-sm", "Оценка по фото")}</span>{mob}</div></header>
<main>{cr}{body}</main>{footer_html()}
<div class="mbar">{cta()}</div></body></html>"""
    d = os.path.join(OUT, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(doc)
    PAGES_META.append((canon, title, desc, kind))

AREA_SERVED = [{"@type": "Place", "name": f"{d['en']}, Bali, Indonesia"} for d in DISTRICTS]
biz = {"@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": SITE + "/#business", "name": CFG["name"], "url": SITE + "/",
       "image": SITE + "/img/bali.webp", "description": "Удаление плесени на Бали: поиск причины сырости, очистка, антигрибковая обработка, защита и покраска.",
       "areaServed": AREA_SERVED, "knowsLanguage": ["ru", "en"], "knowsAbout": ["удаление плесени", "антигрибковая обработка", "сырость", "малярные работы"],
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Удаление плесени и малярные работы", "itemListElement": [
           {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["h1"], "url": SITE + svc_url(s)}} for s in ALL_SVC]}}
if CFG.get("phone"):
    biz["telephone"] = CFG["phone"]
if CFG.get("gbp_url"):
    biz["sameAs"] = [CFG["gbp_url"]]
website = {"@context": "https://schema.org", "@type": "WebSite", "name": CFG["name"], "url": SITE + "/", "inLanguage": "ru"}

def svc_schema(name, url, area=None):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": "Удаление плесени", "areaServed": area or AREA_SERVED,
            "provider": {"@id": SITE + "/#business"}, "url": SITE + url}

def article_schema(a, url):
    return {"@context": "https://schema.org", "@type": "Article", "headline": a["h1"], "description": a["desc"], "inLanguage": "ru",
            "author": {"@id": SITE + "/#business"}, "publisher": {"@id": SITE + "/#business"}, "image": f"{SITE}/img/{a['img']}.webp", "mainEntityOfPage": SITE + url}

# ---------------- генерация ----------------
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "img"))
for f in os.listdir(os.path.join(ROOT, "img_src")):
    if f.endswith(".webp"):
        shutil.copy(os.path.join(ROOT, "img_src", f), os.path.join(OUT, "img", f))
open(os.path.join(OUT, "style.css"), "w", encoding="utf-8").write(CSS + EXTRA_CSS)
open(os.path.join(OUT, ".nojekyll"), "w").write("")

for d in DISTRICTS:
    ARTICLES.append(dict(district_article(d, MOLD_D[d["slug"]]), img=D_IMG[d["slug"]], district=d["slug"]))
A_MAIN = [a for a in ARTICLES if not a.get("district")]
A_DIST = [a for a in ARTICLES if a.get("district")]

STEPS = [("Фото в WhatsApp", "Пришлите 2–3 фото пятен и район."), ("Причина", "Осмотр и замер влажности: откуда сырость."),
         ("Смета", "Что делаем, сколько стоит и сколько займёт."), ("Обработка и защита", "Очистка, фунгицид, просушка, покрытие.")]
HOME_FAQ = [("Как убрать плесень на Бали навсегда?", "Навсегда — только если убрать причину: протечку, конденсат или сырость от грунта, и наладить вентиляцию. Обработка без этого даёт эффект на недели."),
            ("Можно ли просто закрасить плесень?", "Нет: пятна проступят через краску. Нужны очистка, фунгицид, просушка, антигрибковый грунт и только потом краска."),
            ("Опасна ли плесень?", "По данным CDC, плесень может вызывать аллергические реакции, кашель и раздражение; сильнее реагируют люди с аллергией и астмой. При симптомах обращайтесь к врачу."),
            ("Когда можно убрать плесень самому?", "EPA ориентирует на небольшие участки — примерно до 1 м² на гладких поверхностях. Больше, на дереве, в потолках или после затопления — лучше специалист."),
            ("В каких районах вы работаете?", "Санур, Чангу, Перенан, Семиньяк, Кута, Джимбаран, Нуса Дуа, Улувату, Убуд и Денпасар."),
            ("Сколько стоит удаление плесени?", "Зависит от площади, материала и глубины поражения и нужна ли покраска. Предварительная оценка — бесплатно по фото.")]

page("/", "Удаление плесени на Бали — поиск причины, обработка, защита", "Удаление плесени на Бали: находим причину сырости, очищаем и обрабатываем стены, потолки, ванные, дерево и мебель. Бесплатная оценка по фото. Санур, Чангу, Убуд и другие районы.", f"""
<div class="wrap hero"><div>
<span class="eyebrow">Русскоязычный мастер · 10 районов Бали</span>
<h1>Удаление плесени на Бали</h1>
<p class="lead">Нахожу причину сырости, убираю плесень со стен, потолков, ванных, дерева и мебели и защищаю, чтобы она не вернулась после следующего дождя. Если нужно — крашу после обработки.</p>
<div class="cta-row">{cta()}<a class="btn btn-ghost" href="#zayavka">Оценка по фото</a></div>
<ul class="trust">{rating_badge()}<li>Сначала причина, потом обработка</li><li>Бесплатная оценка по фото</li><li>Фотоотчёт в WhatsApp</li></ul>
</div><div class="photo">{img("bali", eager=True)}<div class="chip"><b>Бали</b>Плесень · сырость · защита</div></div></div>

<section class="alt-bg"><div class="wrap split"><div><h2>Почему плесень возвращается</h2>
<p>На Бали плесень почти никогда не бывает «просто пятном». Её кормит влага: протечки, конденсат от кондиционеров, сырость от грунта и закрытые помещения. Если только отмыть или закрасить — через несколько недель всё повторится.</p>
<ul class="checks"><li>Ищу источник влаги влагомером</li><li>Очищаю и обрабатываю фунгицидом</li><li>Просушиваю до покраски</li><li>Защищаю грунтом, краской или маслом</li></ul></div>
<div class="photo">{img("ladder")}</div></div></section>
{promises_block()}{master_block()}
<section id="uslugi"><div class="wrap"><div class="sec-head"><h2>Где убираем плесень</h2><p>Выберите, где у вас проблема.</p></div>{svc_cards()}</div></section>
<section class="alt-bg"><div class="wrap"><div class="sec-head"><h2>Как проходит работа</h2></div><ol class="steps">{"".join(f"<li><b>{E(a)}</b>{E(b)}</li>" for a, b in STEPS)}</ol></div></section>
<section id="rayony"><div class="wrap"><div class="sec-head"><h2>Плесень по районам Бали</h2><p>В Убуде сырее всего, у побережья добавляется соль, в новых виллах Чангу — непросохшие стены. Выберите район.</p></div>{district_cards()}</div></section>
{quick_form()}
<section class="alt-bg"><div class="wrap"><div class="sec-head"><h2>Полезно знать</h2></div>
{cards(A_MAIN[:6], art_url, lambda a: a["h1"], lambda a: a["short"], lambda a: a["img"])}
<p style="margin-top:18px"><a href="{B}/stati/">Все статьи о плесени →</a></p></div></section>
<section><div class="wrap"><div class="sec-head"><h2>Малярные работы</h2><p>После обработки или отдельно — покраска и защита дерева с учётом влажности.</p></div>
{cards(PAINT, svc_url, lambda s: s["h1"], lambda s: s["intro"], lambda s: s["img"])}</div></section>
{prices_block()}
{faq_block(HOME_FAQ)}
{band()}
""", schema=[biz, website, faq_schema(HOME_FAQ)], kind="home")

page("/uslugi/", "Удаление плесени на Бали — все услуги", "Все услуги: плесень на стенах, в ванной, на дереве, в шкафах, на фасаде, поиск причины сырости, обработка, покраска.",
     f'<section><div class="wrap"><div class="sec-head"><h1>Удаление плесени на Бали: услуги</h1><p class="lead">Выберите, где плесень.</p></div>{svc_cards()}'
     f'<div class="sec-head" style="margin-top:40px"><h2>Малярные работы</h2></div>{cards(PAINT, svc_url, lambda s: s["h1"], lambda s: s["intro"], lambda s: s["img"])}</div></section>',
     crumbs=[("Главная", "/"), ("Услуги", "")], kind="hub")

rel_art = {"M01": "pochemu-na-bali-plesen", "M02": "mozhno-li-zakrasit-plesen", "M03": "plesen-v-vannoy", "M04": "plesen-na-mebeli-iz-tika",
           "M05": "plesen-v-shkafu", "M06": "plesen-posle-sezona-dozhdey", "M07": "pochemu-na-bali-plesen", "M08": "plesen-posle-sezona-dozhdey",
           "M09": "zapah-syrosti-v-dome", "M10": "mozhno-li-zakrasit-plesen", "M11": "zapah-syrosti-v-dome", "M12": "plesen-v-arendovannoy-ville"}
AMAP = {a["slug"]: a for a in ARTICLES}
for s in ALL_SVC:
    is_mold = s["id"].startswith("M")
    grid = dict(GRID).get(s["id"])
    d_links = "".join(f'<li><a href="{B}{grid_url(d, s["id"]) if grid else "/rayony/" + d["slug"] + "/"}">{E(d["ru"])}</a></li>' for d in DISTRICTS)
    art = AMAP.get(rel_art.get(s["id"], ""))
    others = [o for o in SERVICES if o["id"] != s["id"]][:3]
    faq = s.get("faq", [])
    page(svc_url(s), f"{s['h1']}{'' if 'Бали' in s['h1'] else ' на Бали'} — мастер, оценка по фото", short(s["intro"], 155), f"""
<div class="wrap page-hero"><div><span class="eyebrow">Бали · оценка по фото</span><h1>{E(s["h1"])}</h1><span class="dur">Срок: {E(s["dur"])}</span>
<p class="lead">{E(s["intro"])}</p><div class="cta-row">{cta()}</div></div><div class="photo">{img(s["img"], eager=True)}</div></div>
<section><div class="wrap split"><div><h2>Этапы работы</h2><ol class="steps one">{"".join(f"<li>{E(x)}</li>" for x in s["steps"])}</ol></div>
<div><h2>Стоимость</h2><p>Зависит от площади, материала и глубины поражения, нужна ли покраска и есть ли доступ. Предварительная оценка — бесплатно по фото.</p>
{f'<p><a href="{B}/stati/{art["slug"]}/">Читать: {E(art["h1"])}</a></p>' if art else ""}
<h2 style="margin-top:28px">По районам</h2><ul class="pills">{d_links}</ul></div></div></section>
{faq_block(faq) if faq else ""}
{quick_form() if is_mold else band("Нужна оценка?", "Пришлите фото и район.")}
<section><div class="wrap"><div class="sec-head"><h2>Другие работы с плесенью</h2></div>{svc_cards(others)}</div></section>
""", crumbs=[("Главная", "/"), ("Услуги", "/uslugi/"), (s["h1"], "")], schema=[svc_schema(s["h1"], svc_url(s))] + ([faq_schema(faq)] if faq else []), og=s["img"], kind="service")

page("/rayony/", "Удаление плесени по районам Бали", "Плесень в Сануре, Чангу, Перенане, Семиньяке, Куте, Джимбаране, Нуса Дуа, Улувату, Убуде и Денпасаре: особенности и услуги.",
     f'<section><div class="wrap"><div class="sec-head"><h1>Плесень по районам Бали</h1><p class="lead">Климат и дома разные — разные и причины сырости.</p></div>{district_cards()}</div></section>',
     crumbs=[("Главная", "/"), ("Районы", "")], kind="hub")

for i, d in enumerate(DISTRICTS):
    n = MOLD_D[d["slug"]]
    near = [DISTRICTS[(i + k) % len(DISTRICTS)] for k in (1, 2, 3)]
    area = {"@type": "Place", "name": f"{d['en']}, Bali, Indonesia"}
    art = next(a for a in A_DIST if a["district"] == d["slug"])
    qa = [(f"Убираете плесень {d['loc']}?", f"Да, {d['ru']} — один из районов выезда. Пришлите фото и адрес для бесплатной оценки."),
          (f"Почему {d['loc']} появляется плесень?", d["notes"]["mold"])] + d["faq"][1:]
    gcards = '<div class="grid">' + "".join(
        f'<a class="card" href="{B}{grid_url(d, sid)}">{img(SVC[sid]["img"])}<div class="body"><h3>{E(SVC[sid]["h1"].split(":")[0])} {E(d["loc"])}</h3><p>{E(short(n[k], 105))}</p></div></a>'
        for sid, k in GRID) + "</div>"
    page(f"/rayony/{d['slug']}/", f"Удаление плесени {d['loc']} — причина, обработка, защита", f"Удаление плесени {d['loc']}: {short(d['notes']['mold'], 120)} Бесплатная оценка по фото.", f"""
<div class="wrap page-hero"><div><span class="eyebrow">{E(d["ru"])} · Бали</span><h1>Удаление плесени {E(d["loc"])}</h1>
<div class="answer">{E(d["notes"]["mold"])}</div><p class="lead">{E(d["intro"])}</p><div class="cta-row">{cta()}</div></div><div class="photo">{img(D_IMG[d["slug"]], eager=True)}</div></div>
<section class="alt-bg"><div class="wrap"><div class="sec-head"><h2>Где чаще всего плесень {E(d["loc"])}</h2></div>{gcards}</div></section>
<section><div class="wrap split"><div><h2>Что усиливает сырость {E(d["loc"])}</h2><ul class="checks">{"".join(f"<li>{E(r[0].upper() + r[1:])}</li>" for r in d["risks"])}</ul>
<p style="margin-top:18px"><a href="{B}/stati/{art["slug"]}/">Подробно: {E(art["h1"])}</a></p></div>
<div><h2>Другие услуги</h2><ul class="pills">{"".join(f'<li><a href="{B}{svc_url(s)}">{E(s["h1"].replace(" на Бали", ""))}</a></li>' for s in SERVICES if s["id"] not in dict(GRID))}</ul></div></div></section>
{faq_block(qa)}
<section><div class="wrap"><div class="sec-head"><h2>Соседние районы</h2></div><ul class="pills">{"".join(f'<li><a href="{B}/rayony/{x["slug"]}/">Плесень {E(x["loc"])}</a></li>' for x in near)}<li><a href="{B}/rayony/">Все районы</a></li></ul></div></section>
{quick_form()}
""", crumbs=[("Главная", "/"), ("Районы", "/rayony/"), (d["ru"], "")], schema=[svc_schema(f"Удаление плесени {d['loc']}", f"/rayony/{d['slug']}/", area), faq_schema(qa)], og=D_IMG[d["slug"]], kind="district")

    for sid, k in GRID:
        s = SVC[sid]
        name = s["h1"].split(":")[0]
        h1 = f"{name} {d['loc']}"
        qa2 = [(f"Убираете {name.lower()} {d['loc']}?", f"Да. Пришлите фото — оценю бесплатно и скажу, что нужно сделать."), (f"Что важно {d['loc']}?", n[k])] + s["faq"][:1]
        page(grid_url(d, sid), f"{h1} — удаление и защита", f"{h1}: {short(n[k], 120)}", f"""
<div class="wrap page-hero"><div><span class="eyebrow">{E(d["ru"])} · {E(name)}</span><h1>{E(h1)}</h1>
<div class="answer">{E(n[k])}</div><p class="lead">{E(s["intro"])}</p><div class="cta-row">{cta()}</div></div><div class="photo">{img(s["img"], eager=True)}</div></div>
<section><div class="wrap split"><div><h2>Этапы</h2><ol class="steps one">{"".join(f"<li>{E(x)}</li>" for x in s["steps"])}</ol></div>
<div><h2>Особенности района</h2><p>{E(d["notes"]["mold"])}</p><ul class="checks">{"".join(f"<li>{E(r[0].upper() + r[1:])}</li>" for r in d["risks"][:3])}</ul></div></div></section>
{faq_block(qa2)}
<section><div class="wrap split"><div><h2>Ещё {E(d["loc"])}</h2><ul class="pills">{"".join(f'<li><a href="{B}{grid_url(d, s2)}">{E(SVC[s2]["h1"].split(":")[0])}</a></li>' for s2, _ in GRID if s2 != sid)}<li><a href="{B}/rayony/{d["slug"]}/">Плесень {E(d["loc"])}</a></li></ul></div>
<div><h2>{E(name)} в других районах</h2><ul class="pills">{"".join(f'<li><a href="{B}{grid_url(x, sid)}">{E(x["ru"])}</a></li>' for x in near)}<li><a href="{B}{svc_url(s)}">Об услуге</a></li></ul></div></div></section>
{band()}
""", crumbs=[("Главная", "/"), ("Районы", "/rayony/"), (d["ru"], f"/rayony/{d['slug']}/"), (name, "")], schema=[svc_schema(h1, grid_url(d, sid), area), faq_schema(qa2)], og=s["img"], kind="grid")

for a in ARTICLES:
    url = f"/stati/{a['slug']}/"
    toc = "".join(f'<li><a href="#s{j}">{E(t)}</a></li>' for j, (t, _) in enumerate(a["sections"]))
    body = "".join(f'<h2 id="s{j}">{E(t)}</h2><p>{E(x)}</p>' for j, (t, x) in enumerate(a["sections"]))
    more = [x for x in A_MAIN if x["slug"] != a["slug"]][:4]
    page(url, a["h1"] + " — Антиплесень Бали", a["desc"], f"""
<article class="wrap prose"><h1>{E(a["h1"])}</h1><div class="answer"><b>Коротко:</b> {E(a["short"])}</div>
<div class="toc"><b>Содержание</b><ol>{toc}</ol></div>{body}
<h2>Читайте также</h2><ul class="pills">{"".join(f'<li><a href="{B}/stati/{x["slug"]}/">{E(x["h1"])}</a></li>' for x in more)}</ul>
</article>{quick_form()}
""", crumbs=[("Главная", "/"), ("Статьи", "/stati/"), (short(a["h1"], 40), "")], schema=[article_schema(a, url)], og=a["img"], kind="article")

page("/stati/", "Статьи о плесени на Бали", "Почему на Бали плесень, чем её убрать, что делать с ванной, мебелью, шкафом и запахом сырости. Гайды по районам.",
     f'<section><div class="wrap"><div class="sec-head"><h1>Статьи о плесени на Бали</h1></div>'
     f'{cards(A_MAIN, art_url, lambda a: a["h1"], lambda a: a["short"], lambda a: a["img"])}'
     f'<div class="sec-head" style="margin-top:40px"><h2>Плесень по районам</h2></div>'
     f'{cards(A_DIST, art_url, lambda a: a["h1"], lambda a: a["desc"], lambda a: a["img"])}</div></section>',
     crumbs=[("Главная", "/"), ("Статьи", "")], kind="hub")

for path, h1, title, desc, text, pic in [
        ("/ceny/", "Цены на удаление плесени на Бали", "Цены на удаление плесени и антигрибковую обработку — Бали", "Из чего складывается цена удаления плесени. Бесплатная оценка по фото.",
         "Цена зависит от площади, материала (стена, плитка, дерево), глубины поражения, нужна ли покраска и доступа. Пришлите фото и район — пришлю оценку.", "roller"),
        ("/kontakty/", "Контакты", "Контакты — удаление плесени на Бали", "Связаться: WhatsApp, Telegram. 10 районов Бали.",
         "Пришлите 2–3 фото плесени и район — отвечу, что это, откуда сырость и что делать.", "bali")]:
    page(path, title, desc, f'<div class="wrap page-hero"><div><h1>{E(h1)}</h1><p class="lead">{E(text)}</p><div class="cta-row">{cta()}</div></div><div class="photo">{img(pic, eager=True)}</div></div>'
         + (prices_block() if path == "/ceny/" else quick_form()), crumbs=[("Главная", "/"), (h1, "")], og=pic)

open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
    "".join(f"<url><loc>{m[0]}</loc></url>" for m in PAGES_META) + "</urlset>")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(f'<!doctype html><meta charset="utf-8"><title>Страница не найдена</title><p>Страница не найдена. <a href="{B}/">На главную</a></p>')
L = [f"# {CFG['name']}", "", "> Удаление плесени на Бали: поиск причины сырости, очистка, антигрибковая обработка, защита и покраска. "
     "Районы: " + ", ".join(d["ru"] for d in DISTRICTS) + ". Русский и английский. Бесплатная оценка по фото.", ""]
for kind, head in [("home", "Главная"), ("service", "Услуги"), ("district", "Районы"), ("grid", "Плесень по районам и типам"), ("article", "Статьи"), ("hub", "Разделы"), ("page", "Прочее")]:
    items = [m for m in PAGES_META if m[3] == kind]
    if items:
        L += [f"## {head}", ""] + [f"- [{t}]({u}): {d_}" for u, t, d_, _ in items] + [""]
open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write("\n".join(L))
print("pages:", len(PAGES_META))
