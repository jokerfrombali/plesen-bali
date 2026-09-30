# -*- coding: utf-8 -*-
"""Google Autocomplete (gl=id) по нише «плесень на Бали»: ru, en, id. Кеш общий: suggest_cache.json."""
import json, os, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

CACHE = r"D:\Маляр\suggest_cache.json"
cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}

def fetch(q, hl):
    key = f"{hl}|{q}"
    if key in cache:
        return
    url = "https://suggestqueries.google.com/complete/search?client=firefox&gl=id&hl=%s&q=%s" % (hl, urllib.parse.quote(q))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=15) as r:
                cache[key] = {"ts": time.strftime("%Y-%m-%d %H:%M"), "s": json.loads(r.read().decode("utf-8", "replace"))[1]}
                return
        except Exception:
            time.sleep(3 * (attempt + 1))
    cache[key] = {"ts": time.strftime("%Y-%m-%d %H:%M"), "s": None, "err": "fail"}

RU = ["плесень", "плесень на", "плесень в", "черная плесень", "грибок на стене", "грибок на потолке", "грибок в ванной",
      "как убрать плесень", "как избавиться от плесени", "чем убрать плесень", "чем обработать от плесени", "средство от плесени",
      "удаление плесени", "обработка от плесени", "запах плесени", "запах сырости", "сырость в доме", "влажность в доме",
      "осушитель воздуха", "антиплесень", "краска от плесени", "плесень бали", "плесень на бали", "плесень на дереве", "плесень в шкафу"]
EN = ["mold", "mould", "black mold", "mold removal", "mold in", "mold on", "how to remove mold", "mold smell", "dehumidifier",
      "anti mold", "mold bali", "mould bali", "mold villa", "mold inspection", "mold remediation"]
ID = ["jamur dinding", "jasa anti jamur", "cara menghilangkan jamur", "jamur di plafon"]
seeds = []
for lst, hl, alph in [(RU, "ru", "абвгдежзиклмнопрстуфхцчшэя"), (EN, "en", "abcdefghijklmnopqrstuvwxyz"), (ID, "id", "abcdefghijklmnopqrstuvwxyz")]:
    for m in lst:
        seeds.append((m + " ", hl))
        seeds += [(f"{m} {c}", hl) for c in alph]
todo = [s for s in dict.fromkeys(seeds) if f"{s[1]}|{s[0]}" not in cache]
print("seeds", len(seeds), "todo", len(todo), flush=True)
def job(a):
    fetch(*a); time.sleep(0.3)
with ThreadPoolExecutor(6) as ex:
    for i, _ in enumerate(ex.map(job, todo), 1):
        if i % 100 == 0:
            json.dump(dict(cache), open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
            print(i, flush=True)
json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False)
print("done", len(cache), sum(1 for v in cache.values() if v.get("s") is None), flush=True)
