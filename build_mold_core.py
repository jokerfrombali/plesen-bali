# -*- coding: utf-8 -*-
"""Семантическое ядро «Удаление плесени на Бали» из Google Autocomplete (gl=id) + экспертные фразы.
Выход: SEO-плесень-Бали-<дата>.xlsx. Частотность и выдача не измерены — поля пустые со статусом."""
import json, re, time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from districts import DISTRICTS
from mold_data import SERVICES, PAINT, ARTICLES, GRID, district_article, MOLD_D

DATE = time.strftime("%Y-%m-%d")
OUT = rf"D:\Маляр\SEO-плесень-Бали-{DATE}.xlsx"
SUG = json.load(open(r"D:\Маляр\suggest_cache.json", encoding="utf-8"))

ROOT_RE = re.compile(r"плесен|грибок|грибк|сырост|влажн|осушит|антиплес|mold|mould|damp|humid|dehumid|jamur|lembab")
STOP = ["хлеб", "сыр ", "сыре", "сыра", "варен", "еда", "продукт", "ногт", "кож", "легк", "лёгк", "стиральн", "холодильник", "растени", "почв",
        "цвет", "аквариум", "машин", "авто", "телефон", " ухе", "ушах", "организм", "лечени", "симптом", "таблет", "мазь", "врач", "стоп", "ног",
        "огурц", "томат", "клубник", "рассад", "орхиде", "фикус", "варенье", "джем", "фрукт", "ягод", "кофе", "чай", "вино", "пиво", "колбас", "мяс",
        "рыб", "сон", "сонник", "английск", "перевод", "майнкрафт", "игр", "кот", "собак", "попугай", "черепах", "бассейн вода", "мед", "сухофрукт",
        "bread", "cheese", "food", "skin", "lung", "car ", "plant", "soil", "fruit", "coffee", "aquarium", "game", "minecraft", "meaning", "strawberr",
        " jam ", "sourdough", "weed", "cannabis", "pet ", "dog", "cat ", "cake", "cup", "jewelry", "silicone mold", "resin", "candle", "soap", "chocolate",
        "ice", "cookie", "concrete mold", "injection", "casting", "3d", "mold maker", "mold making", "baking", "tray", "pan", "makanan", "roti", "kue",
        "cetakan", "kulit", "tanaman", "mobil", "kucing", "anjing", "mulut", "lidah", "kaki", "kuku", "bayi", "vagina", "ketiak", "kepala",
        "pineapple", "zucchini", "potato", "apple", "vegetable", "tomato", "berry", "lemon", "orange", "onion", "garlic", "rice", "cucumber", "avocado", "peach", "grape", "banana", "melon", "squash", "pumpkin",
        "dishwasher", "washer", "washing machine", "evaporator", "coil", "fridge", "refrigerator", "freezer", "hvac", "air condition", "ac unit", "humidifier ", "cpap", "water bottle", "straw",
        "football", "boot", "hair", "5e", "dnd", "jelent", "hindi", "tamil", "telugu", "bangla", "urdu", "basement", "attic", "crawl", "grow tent", "terrarium", "tent",
        "теплиц", "голов", "гемотест", "анализ", "яблок", "картош", "картофел", "огород", "земле", "эпицентр", "подвал", "погреб", "лаборатор", "стиралк", "посудомо",
        "кондиционер", "холодил", "автомобил", "в машине", "в рту", "во рту", "ребенк", "у детей", "у кошки", "у собаки", "беремен", "аллерги", "легки", "печен"]
GEO = ("москв спб питер киев минск казан новосиб екатеринб краснодар сочи ростов самар алмат ташкент тайланд таиланд пхукет вьетнам турци "
       "дубай кипр грузи израил австрали лимассол казакш казахск india uk london usa florida texas australia sydney melbourne jakarta surabaya bandung jogja malang "
       "milwaukee montreal toronto vancouver calgary ottawa ontario chicago houston dallas austin atlanta seattle portland denver phoenix boston nyc brooklyn "
       "philadelphia miami orlando tampa california san los vegas utah ohio michigan jersey york virginia carolina charlotte nc georgia arizona colorado oregon "
       "ann arbor washington manchester birmingham glasgow dublin auckland perth brisbane adelaide singapore malaysia kuala manila kottayam kerala").split()
STOP += ["тыкв", "инвитро", "сериал", "бров", "триходерм", "лобков", "que es", "lowes", "home depot", "education", "mushroom", "laundry", "ламинат", "компот", " еде", "еды", "долл", "испанск", "украинск", "корень", "okc", "jamaica", "delaware", "wajah", "malassezia", "emping", "melinjo", "spa", "mold kit", "mold zero", "x15", "sickness", "для человека", "фото"]

def relevant(s):
    s = s.lower()
    if not ROOT_RE.search(s):
        return False
    toks = s.split()
    if any((t.startswith(g) if len(g) >= 5 else t == g) for t in toks for g in GEO):
        return False
    return not any(w in f" {s} " for w in STOP)

RULES = [  # (regex, page_id, page_type)
    (r"цен|стоим|сколько стоит|price|cost|harga|biaya", "P090"),
    (r"аренд|снима|rent|landlord|tenant", "A:plesen-v-arendovannoy-ville"),
    (r"ванн|душ|шв|плитк|силикон|герметик|затирк|туалет|bathroom|shower|grout|silicone|caulk|tile|toilet|kamar mandi", "M03"),
    (r"шкаф|одежд|вещ|ткан|обув|жалюз|штор|closet|cloth|wardrobe|shoe|curtain|lemari|baju|pakaian|sepatu", "M05"),
    (r"фасад|забор|налет|налёт|водорос|мох|exterior|facade|outside wall|fence|luar", "M06"),
    (r"(дерев|балк).*потол|потол.*дерев|wood.*ceiling|ceiling.*wood|beam", "M07"),
    (r"дерев|мебел|тик|ротанг|бамбук|двер|окн|рам|wood|furniture|teak|rattan|bamboo|door|window|kayu", "M04"),
    (r"запах|пахн|smell|odor|odour|bau", "A:zapah-syrosti-v-dome"),
    (r"осушит|dehumid|humidit|влажност|kelembaban", "A:osushitel-vozduha-na-bali"),
    (r"краск|покрас|paint|cat ", "M10"),
    (r"уксус|хлор|белизн|перекис|сод|спрей|средств|чем убрать|чем обработ|bleach|vinegar|peroxide|spray|product|kill|cairan|obat", "A:chem-ubrat-plesen"),
    (r"черн|black|hitam", "A:chernaya-plesen-v-dome"),
    (r"потол|стен|угл|обо|бетон|гипсокарт|ceiling|wall|corner|drywall|plafon|dinding|tembok|gypsum", "M02"),
    (r"причин|почему|откуда|why|cause|penyebab", "M09"),
    (r"профилакт|предотвр|prevent|mencegah|anti", "M08"),
    (r"сезон|дожд|rain|hujan", "A:plesen-posle-sezona-dozhdey"),
    (r"вилл|villa", "M12"),
    (r"удален|удалит|убрать|избав|обработ|removal|remov|remediat|treat|inspection|jasa|menghilangkan|bali", "M01"),
]
def assign(s):
    for rx, pid in RULES:
        if re.search(rx, s):
            return pid
    return "A:pochemu-na-bali-plesen"

def intent(s):
    return "коммерческий" if re.search(r"цен|стоим|заказ|услуг|мастер|удаление плесени|removal|remediation|service|company|jasa|harga|near me|bali", s) else "информационный"

rows, seen = [], set()
def add(phrase, lang, src, basis, status=None, page=None, region="Бали"):
    n = re.sub(r"\s+", " ", phrase.lower().replace("ё", "е")).strip()
    if not n or n in seen:
        return
    seen.add(n)
    ok = relevant(n)
    rows.append(dict(id=f"Q{len(rows)+1:05d}", raw=phrase, norm=n, lang=lang, intent=intent(n), page=page or (assign(n) if ok else ""),
                     status=status or ("принято условно" if ok else "исключено"), basis=basis if ok else "вне ниши или гео вне Бали / омоним", src=src, region=region))

# 1) экспертные коммерческие фразы
MODS = ["", "бали", "на бали", "цена", "стоимость", "мастер", "заказать", "услуги", "срочно"]
for s in SERVICES:
    base = s["h1"].split(":")[0].lower().replace(" на бали", "")
    for m in MODS:
        add(f"{base} {m}".strip(), "ru", "SRC01", "экспертная коммерческая фраза", page=s["id"])
    for d in DISTRICTS:
        add(f"{base} {d['ru'].lower()}", "ru", "SRC01", "гео-коммерческая", page=s["id"] if s["id"] not in dict(GRID) else f"G:{d['slug']}:{s['id']}", region=d["ru"])
for d in DISTRICTS:
    for f in ["удаление плесени", "плесень", "обработка от плесени", "mold removal", "mold"]:
        add(f"{f} {d['ru'].lower() if not f.startswith('mold') else d['en'].lower()}", "en" if f.startswith("mold") else "ru", "SRC01", "гео район", page=f"D:{d['slug']}", region=d["ru"])
for e in ["mold removal bali", "mould removal bali", "mold remediation bali", "mold treatment bali", "anti mold bali", "mold inspection bali", "villa mold bali"]:
    add(e, "en", "SRC01", "EN экспаты", page="M01")
# 2) темы статей
for a in ARTICLES:
    add(a["h1"].lower(), "ru", "SRC02", "тема статьи (экспертно)", page=f"A:{a['slug']}")
# 3) Google Autocomplete
MARK = ("плесен", "грибок", "грибк", "сырост", "влажност", "осушит", "антиплес", "запах плесени", "запах сырости", "краска от плесени",
        "mold", "mould", "dehumid", "jamur")
n_seed = 0
for key, v in SUG.items():
    hl, seed = key.split("|", 1)
    if not any(m in seed for m in MARK) or not v.get("s"):
        continue
    n_seed += 1
    for s in v["s"]:
        add(s, hl, "SRC03", f"Google Autocomplete gl=id hl={hl}, сид «{seed.strip()}», {v['ts']}")

acc = [r for r in rows if r["status"] == "принято условно"]
exc = [r for r in rows if r["status"] == "исключено"]

# Страницы сайта
PAGES = [("P000", "/", "главная", "Удаление плесени на Бали")]
PAGES += [(s["id"], f"/uslugi/{s['slug']}/", "услуга", s["h1"]) for s in SERVICES + PAINT]
PAGES += [(f"D:{d['slug']}", f"/rayony/{d['slug']}/", "район", f"Удаление плесени {d['loc']}") for d in DISTRICTS]
PAGES += [(f"G:{d['slug']}:{sid}", f"/rayony/{d['slug']}/{[s for s in SERVICES if s['id']==sid][0]['slug']}/", "район×услуга",
           f"{[s for s in SERVICES if s['id']==sid][0]['h1'].split(':')[0]} {d['loc']}") for d in DISTRICTS for sid, _ in GRID]
PAGES += [(f"A:{a['slug']}", f"/stati/{a['slug']}/", "статья", a["h1"]) for a in ARTICLES]
PAGES += [(f"A:plesen-{d['slug']}", f"/stati/plesen-{d['slug']}/", "статья", district_article(d, MOLD_D[d['slug']])["h1"]) for d in DISTRICTS]
PAGES += [("P090", "/ceny/", "служебная", "Цены на удаление плесени"), ("P092", "/kontakty/", "служебная", "Контакты")]
cnt = {}
for r in acc:
    cnt[r["page"]] = cnt.get(r["page"], 0) + 1

wb = Workbook(); wb.remove(wb.active)
HF = Font(bold=True, color="FFFFFF"); HFILL = PatternFill("solid", fgColor="1F5E4F")
def sheet(name, header, data, widths):
    ws = wb.create_sheet(name); ws.append(header)
    for c in ws[1]:
        c.font = HF; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in data:
        ws.append(list(r))
    ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
    for i, w in enumerate(widths):
        ws.column_dimensions[ws.cell(1, i + 1).column_letter].width = w

by_lang = {l: sum(1 for r in acc if r["lang"] == l) for l in ("ru", "en", "id")}
sheet("01 Резюме", ["Показатель", "Значение", "Комментарий"], [
    ("Ниша", "Удаление плесени на Бали (основное) + малярные работы (вторично)", ""),
    ("Поисковая система", "Google, гео Индонезия, языки ru / en / id", ""),
    ("Кандидатов всего", len(rows), ""),
    ("Принято условно", len(acc), f"ru {by_lang['ru']}, en {by_lang['en']}, id {by_lang['id']}"),
    ("Исключено", len(exc), "омонимы (плесень на хлебе, коже, формы для литья), гео вне Бали"),
    ("Сидов автодополнения по плесени", n_seed, "маркеры × алфавит, ru/en/id"),
    ("Фраз из Google Autocomplete (принято)", sum(1 for r in acc if r["src"] == "SRC03"), "реально вводимые формулировки; объём спроса не даёт"),
    ("Страниц в структуре", len(PAGES), ""),
    ("Страниц с назначенными фразами", len(cnt), ""),
    ("Частотность (Keyword Planner)", "0 измерено", "нужен доступ к Google Ads"),
    ("Выдача Google", "0 снято", "нужен SERP-сервис"),
    ("Качество автофильтра", "~80% релевантных по выборке", "перед написанием статей просмотреть SRC03 вручную (лист 02, фильтр по source_id)"),
    ("Статус", "ЧАСТИЧНЫЙ РЕЗУЛЬТАТ", "ядро и структура готовы; объёмы спроса не измерены"),
], [36, 40, 70])
sheet("02 Семантика", ["query_id", "Фраза", "Нормализованная", "Язык", "Интент", "Регион", "page_id", "Статус", "Основание", "source_id"],
      [(r["id"], r["raw"], r["norm"], r["lang"], r["intent"], r["region"], r["page"], r["status"], r["basis"], r["src"]) for r in rows],
      [9, 45, 45, 6, 14, 12, 26, 16, 60, 8])
sheet("03 Структура", ["page_id", "URL", "Тип", "H1", "Фраз назначено"], [(p[0], p[1], p[2], p[3], cnt.get(p[0], 0)) for p in PAGES], [30, 50, 14, 60, 12])
sheet("04 Без страницы", ["page_id", "Фраз", "Решение"], [(k, v, "страница отсутствует — создать или переназначить") for k, v in cnt.items() if k not in {p[0] for p in PAGES}], [30, 10, 60])
top = {}
for r in acc:
    if r["src"] == "SRC03":
        top.setdefault(r["page"], []).append(r["norm"])
sheet("05 Вопросы по страницам", ["page_id", "Вопросы из подсказок (до 15)"],
      [(k, " | ".join([q for q in v if re.match(r"(как|чем|почему|что|можно ли|сколько|откуда|нужно ли|how|why|what|can|is|does|cara|apa)\b", q)][:15])) for k, v in top.items()], [30, 150])
sheet("06 Исключения", ["Фраза", "Причина"], [(r["norm"], r["basis"]) for r in exc], [60, 60])
sheet("07 Источники", ["source_id", "Источник", "Ограничения"], [
    ("SRC01", "Экспертная матрица: услуги × модификаторы × районы", "не подтверждает спрос"),
    ("SRC02", "Темы статей сайта", "экспертно"),
    ("SRC03", f"Google Autocomplete, gl=id, hl=ru/en/id, {n_seed} сидов", "подсказка ≠ объём; выдача персонализирована"),
    ("—", "Google Keyword Planner", "не выполнено: нет доступа"), ("—", "Выдача Google топ-10", "не выполнено")], [10, 70, 60])
sheet("08 Методика", ["Пункт", "Описание"], [
    ("Фильтр ниши", "фраза должна содержать корень плесен/грибок/сырост/влажн/осушит/mold/mould/damp/humid/jamur/lembab"),
    ("Стоп-лист", "еда, кожа/медицина, растения, авто, формы для литья (mold making), гео вне Бали"),
    ("Назначение страниц", "правила по ключевым словам: ванная → M03, дерево → M04, шкаф → M05, фасад → M06, запах → статья и т.д."),
    ("Обновление", "python collect_mold.py → python build_mold_core.py → python build_site.py")], [20, 110])
wb.save(OUT)
print(OUT, "rows", len(rows), "acc", len(acc), "exc", len(exc), "seeds", n_seed, "pages", len(PAGES))
