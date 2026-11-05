#!/usr/bin/env python3
"""Write data/hw_index.json: one compact, machine-readable row per recipe for agents.
Schema: docs/hw_index.md. Generated file: never edit it by hand; run python3 scripts/gen_all.py --images."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataset_constants import DATA_ASOF
import url_safety as us

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'data/hw_index.json'
SITE = 'https://raytone-lab.github.io/awesome-local-inference-recipes/'
REPO_BLOB = 'https://github.com/raytone-lab/awesome-local-inference-recipes/blob/main/'
SCHEMA_VERSION = 1
# (chip, regex, VRAM GB per unit for discrete cards / None for unified memory, kind)
CHIPS = [
 ('RTX PRO 6000', r'RTX PRO 6000', 96, 'gpu'), ('RTX PRO 4500', r'RTX PRO 4500', 32, 'gpu'), ('RTX PRO 4000', r'RTX PRO 4000', 24, 'gpu'), ('RTX 5090', r'5090', 32, 'gpu'), ('RTX 5080', r'5080', 16, 'gpu'),
 ('RTX 5070 Ti', r'5070 ?Ti', 16, 'gpu'), ('RTX 5070', r'5070', 12, 'gpu'), ('RTX 5060 Ti', r'5060 ?Ti', 16, 'gpu'), ('RTX 5060', r'5060', 8, 'gpu'),
 ('RTX 4090', r'4090', 24, 'gpu'), ('RTX 4080', r'4080', 16, 'gpu'), ('RTX 4070 Ti SUPER', r'4070 ?Ti ?SUPER', 16, 'gpu'), ('RTX 4070 Ti', r'4070 ?Ti', 12, 'gpu'),
 ('RTX 4070', r'4070', 12, 'gpu'), ('RTX 4060 Ti', r'4060 ?Ti', 16, 'gpu'), ('RTX 4060', r'4060', 8, 'gpu'),
 ('RTX 3090', r'3090', 24, 'gpu'), ('RTX 3080 Ti', r'3080 ?Ti', 12, 'gpu'), ('RTX 3080', r'3080', 10, 'gpu'), ('RTX 3070', r'3070', 8, 'gpu'), ('RTX 3060', r'3060', 12, 'gpu'),
 ('RTX 5050', r'5050', 8, 'gpu'), ('RTX 4050', r'4050', 6, 'gpu'), ('GTX 1070 Ti', r'1070 ?Ti', 8, 'gpu'), ('GTX 1070', r'GTX 1070', 8, 'gpu'),
 ('RTX 2080 Ti', r'2080 ?Ti', 11, 'gpu'), ('RTX A6000', r'A6000', 48, 'gpu'), ('RTX A5000', r'A5000', 24, 'gpu'), ('RTX A4000', r'A4000', 16, 'gpu'),
 ('Tesla P40', r'P40\b', 24, 'gpu'), ('Tesla P100', r'P100', 16, 'gpu'), ('V100', r'V100', 32, 'gpu'), ('A100', r'A100', 80, 'gpu'),
 ('CMP 170HX', r'CMP ?170', 8, 'gpu'), ('MI50', r'MI50', 32, 'gpu'), ('MI60', r'MI60', 32, 'gpu'),
 ('RX 6800 XT', r'6800 ?XT', 16, 'gpu'), ('RX 6800', r'RX 6800', 16, 'gpu'), ('RX Vega 64', r'Vega 64', 8, 'gpu'),
 ('RX 7900 XTX', r'7900 ?XTX', 24, 'gpu'), ('RX 7900 XT', r'7900 ?XT', 20, 'gpu'), ('RX 5700 XT', r'5700 ?XT', 8, 'gpu'), ('RX 9070 XT', r'9070 ?XT', 16, 'gpu'), ('R9700', r'R9700', 32, 'gpu'),
 ('Arc B580', r'B580', 12, 'gpu'), ('Arc A770', r'A770', 16, 'gpu'),
 ('DGX Spark', r'DGX Spark|GB10|Spark', None, 'unified'), ('Strix Halo', r'Strix Halo|AI Max\+? ?3\d\d|Ryzen AI Max', None, 'unified'), ('Jetson Thor', r'Jetson (AGX )?Thor', None, 'unified'),
 ('M5 Ultra', r'M5 Ultra', None, 'unified'), ('M5 Max', r'M5 Max', None, 'unified'), ('M5 Pro', r'M5 Pro', None, 'unified'), ('M5', r'\bM5\b', None, 'unified'),
 ('M4 Max', r'M4 Max', None, 'unified'), ('M4 Pro', r'M4 Pro', None, 'unified'), ('M4', r'\bM4\b', None, 'unified'),
 ('M3 Ultra', r'M3 Ultra', None, 'unified'), ('M3 Max', r'M3 Max', None, 'unified'), ('M3 Pro', r'M3 Pro', None, 'unified'), ('M3', r'\bM3\b', None, 'unified'),
 ('M2 Ultra', r'M2 Ultra', None, 'unified'), ('M2 Max', r'M2 Max', None, 'unified'), ('M2 Pro', r'M2 Pro', None, 'unified'), ('M2', r'\bM2\b', None, 'unified'),
 ('M1 Ultra', r'M1 Ultra', None, 'unified'), ('M1 Max', r'M1 Max', None, 'unified'), ('M1', r'\bM1\b', None, 'unified'),
 ('Apple Silicon', r'Mac|Apple Silicon', None, 'unified'),
 ('Intel Arc iGPU', r'Arc B3\d\d|集成 ?Arc|integrated Arc|核显|Core Ultra \S+ ?\d{3}H', None, 'unified'),
 ('Intel Arc', r'Arc( Pro)? [AB]\d{2,3}', None, 'gpu'), ('RTX PRO', r'RTX PRO \d{4}', None, 'gpu'), ('RTX Ada', r'RTX \d000 Ada', None, 'gpu'),
 ('Quadro', r'Quadro', None, 'gpu'), ('GeForce', r'(RTX|GTX) ?\d{3,4}', None, 'gpu'), ('Radeon', r'RX ?\d{4}|Radeon', None, 'gpu'),
 ('iPhone', r'iPhone', None, 'phone'), ('Android phone', r'Snapdragon|iQOO|Samsung|RedMagic|红魔|手机|phone', None, 'phone'), ('PS5', r'PS5', None, 'console'),
 ('CPU', r'^(AMD )?(Ryzen|EPYC|Threadripper|Xeon|Core (i[3579]|Ultra))|仅 ?CPU|CPU only|CPU-only', None, 'cpu'),
]
UNIFIED_DEFAULT = {'DGX Spark': 128}
MAC_ONLY = re.compile(r'\bMLX|oMLX|MTPLX|mlx-|Metal|Splash|Strim|Osaurus|Kapitsa|MLX Swift', re.I)
LINUX_HINT = re.compile(r'Linux|Ubuntu|Gentoo|Fedora|Arch|Debian|WSL|vLLM|SGLang|TensorRT', re.I)
# Recipe engine name -> data/repos.json name, only where the two name the same project.
# Host apps: a repo in the source is a plugin, not the engine itself.
REPOS_JSON = set()
NO_DERIVE = {'Unspecified', 'ComfyUI', 'Ollama'}
ENGINE_ALIAS = {'DFlash': 'DFlash / DFlash 2', 'ds4': 'ds4 (DwarfStar)', 'halogen': 'halogen'}


def split_top(t):
    """Split on '+' outside brackets, so '(SXM2 + PCIe)' stays in one card's segment."""
    out, cur, d = [], '', 0
    for ch in t:
        if ch in '(（': d += 1
        elif ch in ')）': d = max(0, d - 1)
        if ch == '+' and d == 0: out.append(cur); cur = ''
        else: cur += ch
    return out + [cur]


def parse_hw(h):
    t = h or ''
    chip = kind = per = None
    if re.search(r'CPU only|CPU-only|仅 ?CPU|纯 ?CPU|只用 ?CPU', t, re.I):
        chip, kind = ('Snapdragon X', 'cpu') if re.search(r'Snapdragon X', t) else ('CPU', 'cpu')
    for c, rx, v, k in ([] if chip else CHIPS):
        if re.search(rx, t, re.I):
            chip, per, kind = c, v, k; break
    m = re.search(r'(?:^|[\s(（+])([1-8])\s*[x×]\s?(?=[A-Za-z\u4e00-\u9fff])|([2-9])\s*台|([2-8])\s*(?:张|块|cards?\b)', t)
    n = int(next(g for g in m.groups() if g)) if m else (2 if re.search(r'双|dual', t, re.I) else 1)
    sys_ram = re.search(r'(\d{2,4})\s*Gi?B\s*(?:\S*\s*)?(?:DDR\S*|LPDDR\S*|RAM|内存|system|系统内存)', t)
    if not sys_ram and kind == 'gpu':  # '+ 128GB +' next to a CPU name
        sys_ram = next((re.search(r'(\d{2,4})\s*Gi?B', x) for x in re.split(r'\+', t)[1:] if re.fullmatch(r'\s*\d{2,4}\s*Gi?B\b.*', x.split('(')[0]) ), None)
    gbs = [int(g) for g in re.findall(r'(\d{1,4})\s*Gi?B(?!\s*(?:DDR|LPDDR|RAM|内存|system|系统内存|/s))', t)]
    vram = uni = None
    if kind == 'gpu':
        rx = next(x[1] for x in CHIPS if x[0] == chip)
        seg = next((x for x in re.split(r'\+|，|,', t) if re.search(rx, x, re.I)), '')
        own = re.search(r'(\d{1,3})\s*Gi?B(?!\s*(?:DDR|LPDDR|RAM|内存|system|系统内存|/s))', seg)
        v = int(own.group(1)) if own else per
        vram = v * n if v else None
        gsegs = [x for x in split_top(t) if any(k == 'gpu' and re.search(r, x, re.I) for _, r, _, k in CHIPS)]
        if len(gsegs) >= 2:  # mixed cards, e.g. 'RTX PRO 4500 32GB + RTX PRO 4000 24GB': count and sum each card
            n, tot = 0, 0
            for x in gsegs:
                c = next(c for c in CHIPS if c[3] == 'gpu' and re.search(c[1], x, re.I))
                xo = re.sub(r'[（(][^）)]*[）)]', '', x)  # a count or size inside brackets is commentary, unless it is the only size
                cm = re.search(r'([1-8])\s*[x×]', xo)
                k = int(cm.group(1)) if cm else 1
                gr = r'(\d{1,3})\s*Gi?B(?!\s*(?:DDR|LPDDR|RAM|内存|system|系统内存|/s))'
                g = re.search(gr, xo) or re.search(gr, x)
                gv = int(g.group(1)) if g else c[2]
                n += k; tot = None if tot is None or gv is None else tot + gv * k
            vram = tot
    elif kind == 'unified':
        u = gbs[0] if gbs else UNIFIED_DEFAULT.get(chip)
        uni = u * n if u else None
    return {'chip': chip, 'kind': kind, 'gpu_count': n if kind == 'gpu' else (n if kind == 'unified' else 0),
            'laptop': bool(re.search(r'Laptop|笔记本|移动版', t, re.I)) and kind == 'gpu',
            'vram_gb': vram, 'unified_mem_gb': uni,
            'sys_ram_gb': int(sys_ram.group(1)) if sys_ram else (uni if kind == 'unified' else (gbs[0] if kind == 'cpu' and gbs else None))}


def single_stream(r):
    return not r.get('superseded_by') and not re.search(r'并发|aggregate|总吞吐', (r.get('metric') or '') + ' ' + str(r.get('concurrency') or ''), re.I)


def model_size(r, params):
    for p in params:
        if re.search(p['match'], r['model']) and not (p.get('exclude') and re.search(p['exclude'], r['model'])):
            return p.get('total_b'), p.get('active_b'), p.get('source')
    tot = re.search(r'(\d+(?:\.\d+)?)B(?:-A(\d+(?:\.\d+)?)B)?\b', r['model'])
    return (float(tot.group(1)) if tot else None), (float(tot.group(2)) if tot and tot.group(2) else None), None


def engine_repo(r, repos):
    name = ENGINE_ALIAS.get(r['engine'], r['engine'])
    if name in repos and repos[name]: return repos[name], ('repos.json' if name in REPOS_JSON else 'source_url')
    if r['engine'] in NO_DERIVE or r.get('engine_fork'): return None, None
    k = us.repo_key(r['source_url'])  # the source itself is the engine's own repo
    if k and k.startswith(('github.com/', 'codeberg.org/')):
        slug = re.sub(r'[^a-z0-9]', '', r['engine'].lower())
        if slug and slug in re.sub(r'[^a-z0-9]', '', k.split('/')[2].lower()):
            return 'https://' + '/'.join(k.split('/')[:3]), 'source_url'
    return None, None


def weights_url(r, card, owners):
    text = ' '.join(str(x) for x in [r['source_url'], r.get('launch_command'), r.get('source_note'), r['quant'], r.get('engine_note')] if x)
    for u in us.URL_RE.findall(text):
        k = us.repo_key(u)
        if k and k.split('/')[0] in ('huggingface.co', 'hf.co', 'modelscope.cn') and k.split('/')[1].lower() in owners:
            return 'https://' + k, 'recipe'
    if card: return card, 'model-params.json'
    return None, None


def os_hints(r, hw):
    t = ' '.join(str(x) for x in [r['hardware'], r.get('source_note'), r.get('engine_note'), r['engine']] if x)
    eng = r['engine'] + ' ' + (r.get('engine_note') or '')
    if r['hardware_family'] == 'Mac' or (hw['chip'] or '').startswith(('M1', 'M2', 'M3', 'M4', 'M5')): return ['macos']
    if hw['chip'] == 'iPhone': return ['ios']
    out = []
    if re.search(r'Windows|Win ?1[01]', t, re.I): out.append('windows')
    if LINUX_HINT.search(t) or hw['chip'] == 'DGX Spark': out.append('linux')
    return out or ['linux', 'windows']


def recipe_pages():
    d = ROOT / 'recipes'
    return {p.stem for p in d.glob('*.md') if '.' not in p.stem and p.stem != 'README'}


def build(R=None):
    R = R if R is not None else json.loads((ROOT / 'data/recipes.json').read_text(encoding='utf-8'))
    repos = {p['name']: p.get('url') for p in json.loads((ROOT / 'data/repos.json').read_text(encoding='utf-8'))}
    REPOS_JSON.clear(); REPOS_JSON.update(repos)
    params = json.loads((ROOT / 'data/model-params.json').read_text(encoding='utf-8'))['models']
    from check_urls import known_owners
    owners = {o.lower() for o in known_owners()}
    pages = recipe_pages(); rows = []
    for r in R:  # an engine repo found in one recipe's own source applies to every recipe of that engine
        u, src = engine_repo(r, repos)
        if src == 'source_url': repos.setdefault(r['engine'], u)
    for r in sorted(R, key=lambda x: x['id']):
        hw = parse_hw(r['hardware']); tot, act, card = model_size(r, params)
        er, er_src = engine_repo(r, repos); wu, wu_src = weights_url(r, card, owners)
        cmd = r.get('launch_command'); bad = us.cmd_problems(cmd) if cmd else []
        def link(u):
            return None if not u else {'url': u, 'trust': 'allowlisted' if us.trusted(u) and not us.problems(u) else 'unverified'}
        rows.append({
            'id': r['id'], 'category': r['category'], 'model': r['model'], 'model_family': r['model_family'],
            'total_params_b': tot, 'active_params_b': act, 'quant': (r.get('en') or {}).get('quant', r['quant']),
            'engine': r['engine'], 'engine_fork': r.get('engine_fork'), 'engine_repo': link(er), 'engine_repo_from': er_src,
            'weights_url': link(wu), 'weights_url_from': wu_src,
            'launch_cmd': None if bad else cmd, 'launch_cmd_warning': bad or None,
            **{k: hw[k] for k in ('chip', 'kind', 'gpu_count', 'laptop', 'vram_gb', 'unified_mem_gb', 'sys_ram_gb')},
            'hardware': (r.get('en') or {}).get('hardware', r['hardware']), 'os_hints': os_hints(r, hw),
            'mac_only_engine': bool(MAC_ONLY.search(r['engine'] + ' ' + (r.get('engine_note') or ''))),
            'tok_s': r.get('tok_s'), 'single_stream': single_stream(r), 'context': r.get('context'),
            'source_level': r['source_level'], 'source_url': link(r['source_url']), 'date': r.get('date'),
            'tags': r.get('tags', []), 'superseded_by': r.get('superseded_by'),
            'recipe_page': SITE + 'explore.html?id=' + r['id'], 'recipe_md': REPO_BLOB + f"recipes/{r['id']}.md" if r['id'] in pages else None})
    pats = [{'chip': c, 'regex': rx, 'kind': k, 'generic': k == 'gpu' and v is None} for c, rx, v, k in CHIPS if k in ('gpu', 'unified')]
    return {'schema_version': SCHEMA_VERSION, 'data_asof': DATA_ASOF, 'schema_doc': REPO_BLOB + 'docs/hw_index.md', 'chip_patterns': pats,
            'source': 'data/recipes.json', 'count': len(rows), 'recipes': rows}


def render(idx):
    return json.dumps(idx, ensure_ascii=False, separators=(',', ':')).replace('},{"id"', '},\n{"id"') + '\n'


def main():
    idx = build(); OUT.write_text(render(idx), encoding='utf-8')
    rows = idx['recipes']; n = len(rows)
    unk = [x for x in rows if not x['chip']]
    print(f'hw_index.json: {n} rows; engine_repo {sum(bool(x["engine_repo"]) for x in rows)/n:.0%}, weights_url {sum(bool(x["weights_url"]) for x in rows)/n:.0%}, unparsed hardware {len(unk)}')
    for x in unk: print(f'  UNPARSED {x["id"]}: {x["hardware"]}')


if __name__ == '__main__': main()
