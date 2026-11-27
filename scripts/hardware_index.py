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
 HardwarePage('dgx-spark','NVIDIA DGX Spark',r'DGX Spark','DGX Spark'),HardwarePage('strix-halo','AMD Strix Halo (Ryzen AI Max+ 395)',r'Strix Halo|Ryzen AI Max\+? ?(?:PRO )?3[89]5|Radeon 8060S','Strix Halo'),
 HardwarePage('amd-radeon','AMD Radeon (RX 7900 / R9700)',r'RX 7900|R9700','R9700'),HardwarePage('tesla-p40','NVIDIA Tesla P40',r'P40','Tesla P40'),HardwarePage('rtx-pro-6000','RTX PRO 6000',r'RTX PRO 6000','RTX PRO 6000')]
BY_SLUG = {h.slug: h for h in HW}

# Text that says a row also reports several requests at once. Older rows wrote 并发; rows now write
# 同时处理 N 个请求 / 同时处理多个请求. Such rows stay out of the single-stream picks.
AGG_TEXT = r'并发|aggregate|总吞吐|同时处理 ?(?:[\d/]+ ?个|多)'

def selfrep(r): return '自称' in (r.get('metric') or '')
COMPARE = re.compile(r'\s/|/\s|\svs\.?\s', re.I)
def single_stream(r):
    return not r.get('superseded_by') and not re.search(AGG_TEXT, (r.get('metric') or '') + ' ' + str(r.get('concurrency') or ''), re.I)
# Laptops, tablets, phones and handhelds. The README picks (quick answers, the hardware grid's fastest value and the
# headline numbers) compare single desktop devices only, so a mobile part never answers "how fast is one RTX 5090".
MOBILE = re.compile(r'笔记本|移动工作站|平板|ノート|[Ll]aptop|[Nn]otebook|MacBook|[Tt]ablet|iPhone|iPad|ROG Flow|Zenbook|ZBook|ThinkPad|XPS 1\d|ProArt PX\d|'
                    r'Steam Deck|ROG Ally|Legion Go|\b[3-5]0[5-9]0 ?M\b|[Mm]obile GPU')
# Discrete devices joined with '+' at the top level (outside brackets): a mixed rig such as "Strix Halo + R9700" or
# "RTX 5060 Ti + MacBook Pro M1 Max". Each top-level part is matched with its bracketed details, so
# "MS-S1 MAX（Ryzen AI Max+ 395）+ R9700" counts two devices. Only the '+' of the SoC name "Ryzen AI Max+" is not a separator;
# "Mac Studio M4 Max+RTX 5090" is two devices.
_DEVICE = re.compile(r'RTX|GTX|Radeon|\bRX ?\d|R9700|Instinct|\bMI\d{2,3}|Tesla|\b[VPAHL]\d{2,3}\b|\bArc\b|DGX|Spark|GB10|Strix Halo|Ryzen AI Max|\bMac\b|MacBook|\bM\d (?:Pro|Max|Ultra)\b|CMP', re.I)
def top_level_parts(hw):
    parts, cur, depth = [], '', 0
    for i, ch in enumerate(hw):
        if ch in '(（[': depth += 1
        elif ch in ')）]': depth = max(0, depth - 1)
        if ch in '+＋' and depth == 0 and not re.search(r'AI Max$', hw[:i], re.I):
            parts.append(cur); cur = ''
        else: cur += ch
    return parts + [cur]
def mixed_devices(hw):
    return sum(bool(_DEVICE.search(p)) for p in top_level_parts(hw)) > 1
# A Mac with an M Pro or M Max chip whose machine is not stated: the same chip ships in MacBooks, so it is not counted as a desktop.
UNKNOWN_MAC = re.compile(r'\bM\d+ (?:Pro|Max)\b.*机型未注明')
def single_device(hw, tags=()):
    """One desktop device: no multi-GPU tag, no 2-9× / 双 / N 台, no '/' or 'vs' comparison, no mixed '+' rig, no laptop or tablet."""
    return ('multi-GPU' not in tags and not re.search(r'[2-9] ?[x×] ?|双|[2-9] ?台', hw) and not COMPARE.search(hw)
            and not mixed_devices(hw) and not MOBILE.search(hw) and not UNKNOWN_MAC.search(hw))
def single(r):
    """The shared single-desktop, single-stream predicate behind the quick answers, the grid's ⚡ value, the headline numbers and the hw pages."""
    return single_device(r['hardware'], r['tags']) and single_stream(r)
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
 Chip('nvidia','RTX PRO 6000','rtx-pro-6000'),
 Chip('other','Multi-GPU rigs',tag='multi-GPU'), Chip('other','Tesla V100',query='V100'), Chip('other','Tesla P40','tesla-p40'), Chip('other','CMP 170HX',query='CMP'), Chip('other','iPhone',query='iPhone')]

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
        if rows: by.setdefault(c.group, []).append((c, len(rows), fastest(speed_rows(rows, c), multi=bool(c.tag))))
    for v in by.values(): v.sort(key=lambda x: (-x[1], x[0].label))
    return sorted(by.items(), key=lambda kv: (kv[0] == 'other', -sum(n for _, n, _ in kv[1])))

def fastest_on_page(D, slug):
    return fastest(chip_rows(D, next(c for c in CHIPS if c.page == slug)))

def speed_rows(rows, c):
    """Rows that may give a chip its fastest value. An explorer-query chip counts every row whose text mentions the
    query (so the count matches the explorer), but only a row whose hardware names the device can be its fastest."""
    if c.query: return [r for r in rows if c.query.lower() in r['hardware'].lower()]
    return rows

def group_best(D, group):
    """Fastest measured single-desktop, single-stream text row across the chips of one grid group (same rule as each chip's ⚡)."""
    best = [b for g, chips in grid(D) if g == group for _, _, b in chips if b]
    return max(best, key=lambda r: (r['tok_s'], r['id'])) if best else None

USED_DC_FAMILY = '二手数据中心卡'
def headline_rows(D):
    """[(key, row)] for the README headline table, computed from the data. Device rows use the grid's ⚡ rule
    (fastest measured single-stream text result on one desktop device). Used datacenter GPUs use the multi-GPU chip's
    rule (any rig size), because these cards are mostly run in pairs or more. The cheapest rig is the lowest published
    hardware price among measured single-stream text rows, fastest first on a tie."""
    dc = fastest([r for r in D if r['hardware_family'] == USED_DC_FAMILY], multi=True)
    priced = [r for r in D if meas_text(r) and single_stream(r) and r.get('hardware_cost_usd')]
    cheap = min(priced, key=lambda r: (r['hardware_cost_usd'], -r['tok_s'], r['id'])) if priced else None
    out = [('mac', group_best(D, 'apple')), ('5090', fastest_on_page(D, 'rtx-5090')), ('amd', group_best(D, 'amd')),
           ('dc', dc), ('spark', fastest_on_page(D, 'dgx-spark')), ('cheap', cheap)]
    return [(k, r) for k, r in out if r]
