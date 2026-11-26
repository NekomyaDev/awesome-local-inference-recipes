"""Hardware landing pages (hw/<slug>.html) and the README "Browse by hardware" grid, shared by gen_site.py and gen_readme.py."""
import re
from typing import NamedTuple

MIN_ROWS = 5

class HardwarePage(NamedTuple):
    slug: str
    name: str
    pattern: str
    explorer_query: str

HW = [
 HardwarePage('rtx-5090','RTX 5090',r'RTX 5090','RTX 5090'),HardwarePage('rtx-4090','RTX 4090',r'RTX 4090','RTX 4090'),HardwarePage('rtx-3090','RTX 3090',r'RTX 3090','RTX 3090'),HardwarePage('rtx-5060-ti','RTX 5060 Ti',r'RTX 5060 Ti','RTX 5060 Ti'),
 HardwarePage('mac-studio-m3-ultra','Mac Studio M3 Ultra',r'M3 Ultra','M3 Ultra'),HardwarePage('mac-m4-max','Apple M4 Max',r'M4 Max','M4 Max'),HardwarePage('mac-m5','Apple M5 Pro / M5 Max',r'M5 (Pro|Max)','M5'),
 HardwarePage('dgx-spark','NVIDIA DGX Spark',r'DGX Spark','DGX Spark'),HardwarePage('strix-halo','AMD Strix Halo (Ryzen AI Max+ 395)',r'Strix Halo','Strix Halo'),
 HardwarePage('amd-radeon','AMD Radeon (RX 7900 / R9700)',r'RX 7900|R9700','R9700'),HardwarePage('tesla-p40','NVIDIA Tesla P40',r'P40','P40'),HardwarePage('rtx-pro-6000','RTX PRO 6000',r'RTX PRO 6000','RTX PRO 6000')]
BY_SLUG = {h.slug: h for h in HW}

# Text that says a row also reports several requests at once. Older rows wrote 并发; rows now write
# 同时处理 N 个请求 / 同时处理多个请求. Such rows stay out of the single-stream picks.
AGG_TEXT = r'并发|aggregate|总吞吐|同时处理 ?(?:[\d/]+ ?个|多)'

def selfrep(r): return '自称' in (r.get('metric') or '')
COMPARE = re.compile(r'\s/|/\s|\svs\.?\s', re.I)
def single_stream(r):
    return not r.get('superseded_by') and not re.search(AGG_TEXT, (r.get('metric') or '') + ' ' + str(r.get('concurrency') or ''), re.I)
def single(r):
    return ('multi-GPU' not in r['tags'] and not re.search(r'[2-9] ?[x×] ?|双|[2-9] ?台', r['hardware']) and not COMPARE.search(r['hardware'])
            and single_stream(r))
def meas_text(r): return r['source_level'] == '实测' and r['category'] == 'text' and r.get('tok_s') and not selfrep(r)

def explorer_text(r):
    """Same haystack as app.js match(): the explorer's ?q= search is a case-insensitive substring test over these fields."""
    return ' '.join(str(x) for x in [r['model'], r['quant'], r['engine'], r.get('engine_note'), r['hardware'], r['metric'], r.get('metric_en'), r['model_family'], *r['tags']] if x is not None).lower()

class Chip(NamedTuple):
    group: str
    label: str
    page: str | None = None
    query: str | None = None
    tag: str | None = None

GROUPS = {'nvidia': {'en': 'NVIDIA RTX', 'zh': 'NVIDIA RTX', 'ja': 'NVIDIA RTX'},
          'apple': {'en': 'Apple Silicon', 'zh': 'Apple 芯片', 'ja': 'Apple シリコン'},
          'spark': {'en': 'DGX Spark', 'zh': 'DGX Spark', 'ja': 'DGX Spark'},
          'amd': {'en': 'AMD', 'zh': 'AMD', 'ja': 'AMD'},
          'other': {'en': 'Multi-GPU & other', 'zh': '多卡及其他', 'ja': 'マルチ GPU・その他'}}
LABELS = {'Multi-GPU rigs': {'zh': '多卡组合', 'ja': 'マルチ GPU 構成'}}
CHIPS = [
 Chip('nvidia','RTX 5090','rtx-5090'), Chip('nvidia','RTX 4090','rtx-4090'), Chip('nvidia','RTX 3090','rtx-3090'), Chip('nvidia','RTX 5060 Ti','rtx-5060-ti'),
 Chip('nvidia','RTX 5070 / 5070 Ti',query='RTX 5070'), Chip('nvidia','RTX 3060',query='RTX 3060'),
 Chip('apple','M5 Pro / M5 Max','mac-m5'), Chip('apple','M4 Pro',query='M4 Pro'), Chip('apple','M3 Ultra','mac-studio-m3-ultra'), Chip('apple','M4 Max','mac-m4-max'),
 Chip('apple','M5 Ultra',query='M5 Ultra'), Chip('apple','M2 Ultra',query='M2 Ultra'),
 Chip('spark','DGX Spark','dgx-spark'),
 Chip('amd','Strix Halo','strix-halo'), Chip('amd','Radeon R9700 / RX 7900','amd-radeon'), Chip('amd','Instinct MI50',query='MI50'),
 Chip('other','Multi-GPU rigs',tag='multi-GPU'), Chip('other','Tesla V100',query='V100'), Chip('other','CMP 170HX',query='CMP'), Chip('other','iPhone',query='iPhone')]

def chip_rows(D, c):
    if c.page: return [r for r in D if re.search(BY_SLUG[c.page].pattern, r['hardware'])]
    if c.tag: return [r for r in D if c.tag in r['tags']]
    q = c.query.lower(); return [r for r in D if q in explorer_text(r)]

def fastest(rows, multi=False):
    ok = [r for r in rows if meas_text(r) and (single_stream(r) if multi else single(r))]
    return max(ok, key=lambda r: (r['tok_s'], r['id'])) if ok else None

def chip_link(c, D, base):
    from urllib.parse import quote
    if c.page and len(chip_rows(D, c)) >= MIN_ROWS: return f'{base}hw/{c.page}.html'
    if c.page: return f'{base}explore.html?q={quote(BY_SLUG[c.page].explorer_query)}'
    if c.tag: return f'{base}explore.html?tag={quote(c.tag)}'
    return f'{base}explore.html?q={quote(c.query)}'

def grid(D):
    """[(group, [(chip, n, best_row), ...])] with chips by count and groups by total count."""
    by = {}
    for c in CHIPS:
        rows = chip_rows(D, c)
        if rows: by.setdefault(c.group, []).append((c, len(rows), fastest(rows, multi=bool(c.tag))))
    for v in by.values(): v.sort(key=lambda x: (-x[1], x[0].label))
    return sorted(by.items(), key=lambda kv: (kv[0] == 'other', -sum(n for _, n, _ in kv[1])))

def fastest_on_page(D, slug):
    return fastest(chip_rows(D, next(c for c in CHIPS if c.page == slug)))
