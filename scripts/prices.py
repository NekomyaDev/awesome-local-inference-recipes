#!/usr/bin/env python3
"""Read data/prices.json — the dated hardware-price snapshot used by the README banner,
approve_review.py, and the weekly link check. Refreshing the snapshot never changes a
recipe's hardware_cost_usd (see CONTRIBUTING)."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Hardware strings on new Hugging Face rows → (item name substring, multiplier).
# Multiplier is 2 for a 2× card of the same model. Order matters: more specific first.
HARDWARE_LOOKUP = [
    (re.compile(r'^2\s*[x×]\s*Tesla V100 32GB', re.I), 'Tesla V100 32GB', 2),
    (re.compile(r'^Tesla V100 32GB', re.I), 'Tesla V100 32GB', 1),
    (re.compile(r'^RTX 5090'), 'NVIDIA RTX 5090', 1),
    (re.compile(r'^RTX 4090'), 'RTX 4090', 1),
    (re.compile(r'^RTX 3090 24GB$'), 'RTX 3090 24GB', 1),
    (re.compile(r'^MacBook M4 Pro 48GB$'), 'MacBook Pro 14 M4 Pro 48GB', 1),
]
USD = re.compile(r'\$\s*([\d,]+(?:\.\d+)?)')
MONTH_EN = 'January February March April May June July August September October November December'.split()


def load(path=None):
    return json.loads((path or ROOT / 'data/prices.json').read_text(encoding='utf-8'))


def items(data=None):
    data = data if data is not None else load()
    return data.get('items', [])


def find_item(name_part, data=None):
    hits = [i for i in items(data) if name_part in i['item']]
    if not hits:
        return None
    # Prefer the shortest item name that contains the key, so "RTX 4090" does not
    # also match a longer "RTX 4090 D" entry if one is added later.
    return min(hits, key=lambda i: (len(i['item']), i['item']))


def dollars(text):
    """Dollar amounts in a price string, in order, as floats."""
    return [float(m.group(1).replace(',', '')) for m in USD.finditer(text or '')]


def first_usd(text):
    ds = dollars(text)
    return ds[0] if ds else None


def usd_int(n):
    """Whole dollars for hardware_cost_usd. Drops cents, so $6,499.99 stays 6499."""
    if n is None:
        return None
    return int(n)


def fmt_usd(n, about=False):
    n = float(n)
    if abs(n - round(n)) < 0.005:
        s = f"${int(round(n)):,}"
    else:
        s = f"${n:,.2f}".replace('.00', '')
    return ('about ' + s) if about else s


def month_parts(iso):
    """Calendar month of an ISO date: (year, month 1-12, day, early?). early is day <= 10."""
    y, m, d = (int(x) for x in iso[:10].split('-'))
    return y, m, d, d <= 10


def month_label(iso, lang):
    y, m, d, early = month_parts(iso)
    if lang == 'en':
        return (('early ' if early else '') + MONTH_EN[m - 1], str(y), MONTH_EN[m - 1])
    prefix = f'{m} 月' + ('初' if early and lang == 'zh' else ('初め' if early else ''))
    if lang == 'zh':
        return (f'{y} 年 {m} 月', prefix if early else f'{m} 月')
    return (f'{y} 年 {m} 月', prefix if early else f'{m} 月')


def cost_for_hardware(hw, data=None):
    """(hardware_cost_text, hardware_cost_usd) for a new row, or (None, None).

    The text is Chinese, like the rest of hardware_cost_text, and points at prices.json
    so a later snapshot refresh does not require a code change."""
    data = data if data is not None else load()
    asof = data.get('as_of') or ''
    for pat, key, n in HARDWARE_LOOKUP:
        if pat.search(hw or ''):
            item = find_item(key, data)
            if not item:
                return None, None
            unit = first_usd(item['price'])
            if unit is None:
                return None, None
            total = unit * n
            usd = usd_int(total)
            if n > 1:
                text = f"仅显卡 {n}×约 {fmt_usd(unit)} = 约 {fmt_usd(total)}（{asof}，见 prices.json）"
            else:
                text = f"{item['price']}（{asof}，见 prices.json）"
                # Keep the historical "仅显卡 …" prefix for GPU-only rows (not whole Macs).
                if not re.search(r'MacBook|Mac Studio|Mac mini', item['item']):
                    text = '仅显卡 ' + text
            return text, usd
    return None, None


def banner(data=None):
    """Figures the README price banner interpolates, all taken from the snapshot."""
    data = data if data is not None else load()
    asof = data['as_of']
    nxt = data['next_review']
    ddr5 = find_item('DDR5 台式机内存 64GB', data)
    rtx = find_item('RTX 4090', data)
    ddr = dollars(ddr5['price']) if ddr5 else []
    now = first_usd(rtx['price']) if rtx else None
    meta = data.get('banner') or {}
    # The October 4090 baseline is pinned on the banner object so a later snapshot
    # refresh (which rolls `previous`) does not rewrite the November-spike comparison.
    old = meta.get('rtx4090_baseline_usd')
    if old is None:
        old = first_usd((rtx.get('previous') or {}).get('price')) if rtx else None
    old_date = meta.get('rtx4090_baseline_date') or (rtx.get('previous') or {}).get('date') or ''
    # 899.99 / 1,339.99 → 900 / 1,340 for a short banner; keep whole dollars as-is.
    def short(n):
        if n is None:
            return ''
        if abs(n - round(n)) >= 0.005:
            return f"{int(round(n)):,}"
        return f"{int(round(n)):,}"
    spike = (data.get('banner') or {}).get('spike_month') or '2026-11'
    if len(spike) == 7:
        spike = spike + '-01'
    en_month, en_year, en_month_only = month_label(spike, 'en')
    zh_month, _ = month_label(spike, 'zh')
    ja_month, _ = month_label(spike, 'ja')
    # "November 2026" / "2026 年 11 月" for the historical spike, independent of as_of.
    spike_en = f'{en_month_only} {en_year}'
    if old_date:
        en_old = month_label(old_date, 'en')[0]
        zh_old = month_label(old_date, 'zh')[1]
        ja_old = month_label(old_date, 'ja')[1]
    else:
        en_old = zh_old = ja_old = ''
    return {
        'asof': asof, 'nxt': nxt,
        'ddr5_lo': short(ddr[0] if len(ddr) > 0 else None),
        'ddr5_hi': short(ddr[1] if len(ddr) > 1 else None),
        'rtx_now': short(now), 'rtx_old': short(old),
        'month_en': en_month, 'year': en_year, 'month_en_only': en_month_only,
        'month_zh': zh_month, 'month_ja': ja_month, 'month_num': str(month_parts(asof)[1]),
        'spike_en': spike_en, 'spike_zh': zh_month, 'spike_ja': ja_month,
        'spike_num': str(month_parts(spike)[1]),
        'old_month_en': en_old, 'old_month_zh': zh_old, 'old_month_ja': ja_old,
    }
