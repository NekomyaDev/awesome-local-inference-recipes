#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
from dataset_constants import BUDGET_TIER_BOUNDS_USD
ROOT = Path(__file__).resolve().parent.parent
MAX_DEVICES = 4
MAX_COST_USD = BUDGET_TIER_BOUNDS_USD[-1][1]
OVER_BUDGET_MARK = f'⚠️超${MAX_COST_USD // 1000}k'
MANUAL_CHECKS = ('at most 4 machines', 'total power about 2 kW from at most two ordinary outlets on separate circuits, with no special wiring', 'at most one desktop-class network switch')
DEVICE = re.compile(
    r'RTX|GTX|Radeon|\bRX ?\d|R9700|Instinct|\bMI\d{2,3}|Tesla|\b[VPAHLB](?:\d{2}|[1-9]00)S?s?(?![A-Za-z0-9])|\bA\d{4}s?(?![A-Za-z0-9])|\b(?:A(?:310|380|580|750|770)|B5[78]0|P10[246])s?(?![A-Za-z0-9])|CMP|DGX|Spark|GB10|Ascent|AI TOP'
    r'|Strix Halo|Ryzen AI Max|Framework Desktop|\bMac\b|MacBook|\bM\d (?:Pro|Max|Ultra)\b|\bArc\b|(?<![A-Za-z])GPU'
    r'|(?<![\d-])[1-9]0[5-9]0(?:S|Ti|D)?s?(?![A-Za-z0-9])|\b7900(?:XTX|XT|GRE)?s?(?![A-Za-z0-9])|\b9070(?:XT|GRE)?s?(?![A-Za-z0-9])')
SERVER_ONLY = re.compile(r'SXM|HGX|(?<!ASRock )(?<!ASRock-)\brack|\b[124]U\b|机架|机柜', re.I)
SXM2_BOARD = re.compile(r'server[- ]?(?:mother)?board|服务器主板|サーバー用?(?:マザー)?ボード', re.I)
BASEBOARD = re.compile(r'baseboard(?![\s-]*to)', re.I)
LIQUID = re.compile(r'液冷|水冷|liquid[- ]?cool|water[- ]?cool', re.I)
CUSTOM_LOOP = re.compile(r'custom[- ]?(?:water|liquid)?[- ]?(?:cool(?:ing|ed)?[- ]?)?loop|hardline|water[- ]?block|分体式?水冷|非一[体體][式型]?(?:水冷|液冷)|自定义水冷|カスタムループ|本格水冷', re.I)
SXM2_ADAPTER = re.compile(r'SXM2\s*(?:-?to-?|→|转)\s*PCIe|SXM2[\s-]*(?:PCIe[\s-]*)?(?:adapter|转接|変換)', re.I)
SXM2 = re.compile(r'SXM2(?!\d)', re.I)
FACTORY_AIO = re.compile(r'(?<![A-Za-z])AIO(?![A-Za-z])|all[- ]in[- ]one|(?<!非)一[体體][式型]?(?:水冷|液冷)|簡易水冷', re.I)
CONSUMER_GPU = re.compile(r'RTX|GTX|Radeon|\bRX ?\d|\bArc\b|(?<![\d-])[1-9]0[5-9]0(?:S|Ti|D)?(?![\dA-Za-z])|\b7900|\b9070', re.I)
NON_CONSUMER_GPU = re.compile(r'Instinct|\bMI\d|Tesla|Quadro|\bW\d{4}|\bRTX (?:PRO )?A?\d[05]00s?\b|\bA\d[05]00s?\b|R9700|Radeon (?:AI )?Pro|Server Edition|(?<!home )server(?![- ]?(?:mother)?board)|(?<!家用)服务器(?!主板)|サーバー(?!用?(?:マザー)?ボード)|\b[VPAHL](?:\d{2}|[1-9]00)S?\b|\bB[12]00\b', re.I)
PARTS = re.compile(r'[+＋;&]')
PARENS = re.compile(r'（([^）]*)）|\(([^)]*)\)')
ALTERNATIVES = re.compile(r'/|\bvs\.?\b')
PCIE_LANES = re.compile(r'(?:PCIe|Gen\s?\d|@)[\s\d.]*[xX]\d+')
MULTIPLIERS = (re.compile(r'(?<![\w.])(\d{1,2})\s*(?:×|[xX](?=[\sA-Z0-9]))'),
               re.compile(r'(?:×|(?<=\s)[xX])\s*(\d{1,2})(?![\w.])'),
               re.compile(r'(?<![\w.])(\d{1,2})\s*(?:张|卡|台)'),
               re.compile(r'(?<![\w.])(\d{1,2})\s+(?:GPUs?|cards?)\b'))

def part_count(part):
    part = PCIE_LANES.sub('', part)
    if not DEVICE.search(part): return 0
    for m in (p.search(part) for p in MULTIPLIERS):
        if m: return int(m.group(1))
    return 1

def flat_count(text):
    return max(sum(part_count(p) for p in alt.split('+')) for alt in ALTERNATIVES.split(text))

def device_count(hardware):
    inner = [a or b for a, b in PARENS.findall(hardware)]
    return max([flat_count(PARENS.sub('', hardware))] + [flat_count(t) for t in inner])

def aio_part(p):
    return bool(FACTORY_AIO.search(p)) and not NON_CONSUMER_GPU.search(p) and (bool(CONSUMER_GPU.search(p)) or not DEVICE.search(p))

def server_only(hardware):
    adapter = SXM2_ADAPTER.search(hardware)
    hw = SXM2.sub('', hardware) if adapter else hardware
    sxm2_board = any(SXM2.search(p) and SXM2_BOARD.search(p) for p in PARTS.split(hardware))
    board = adapter and (BASEBOARD.search(hardware) or sxm2_board)
    liquid = any(LIQUID.search(p) and not aio_part(p) for p in PARTS.split(hw))
    return bool(SERVER_ONLY.search(hw) or board or liquid or CUSTOM_LOOP.search(hw))

def violations(r):
    out = []
    usd = r.get('hardware_cost_usd')
    if (usd is not None and usd > MAX_COST_USD) or OVER_BUDGET_MARK in (r.get('hardware_cost_text') or ''):
        out.append(f'cost over ${MAX_COST_USD:,}')
    # Budget is the main limit. Machine count (at most 4) is checked by hand; GPU count has no hard cap.
    if server_only(r['hardware']):
        out.append('out-of-scope hardware type (rack, server board, SXM/HGX, custom-loop or server liquid cooling)')
    return out

if __name__ == '__main__':
    with open(ROOT/'data/recipes.json', encoding='utf-8') as f: D = json.load(f)
    bad = [(r, violations(r)) for r in D]
    bad = [(r, v) for r, v in bad if v]
    for r, v in bad: print(r['id'], '|', r['hardware'], '|', '; '.join(v))
    print(f'{len(bad)} of {len(D)} recipes fail a mechanical check. Check by hand: ' + '; '.join(MANUAL_CHECKS) + '.')
    sys.exit(1 if bad else 0)
