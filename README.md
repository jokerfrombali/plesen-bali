# Антиплесень · Бали

Сайт «Удаление плесени на Бали» (основное) + малярные работы (вторично). GitHub Pages из папки `docs/`.

- `site_config.json` — название, контакты, обещания, цены, данные мастера.
- `mold_data.py` — услуги, районы, статьи; `districts.py` — данные районов.
- `build_site.py` — генерирует `docs/`.
- `collect_mold.py` → `build_mold_core.py` — ядро по плесени из подсказок Google (книга Excel локально, в репозиторий не входит).
- `build_site_malyar.py`, `build_core.py`, `collect_suggest.py` — прошлая версия «Маляр на Бали».

Пересборка: `python build_site.py`.
