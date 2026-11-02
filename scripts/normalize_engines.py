#!/usr/bin/env python3
"""Normalize `engine` to canonical names (idempotent, deterministic).
Original string is kept in `engine_raw`; flags/version details go to `engine_note`.
Run: python3 scripts/normalize_engines.py"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
UNSPEC = 'Unspecified'
ALREADY_CANONICAL_FORK = r'^.+? \([^)]+ fork\)$'
RULES = [
    (ALREADY_CANONICAL_FORK, None),
    (r'vahpetr|s1-fork', 'llama.cpp (vahpetr fork)'),
    (r'llama\.cpp-omni', 'llama.cpp (OpenBMB fork)'),
    (r'PrismML.*mlx-swift', 'MLX Swift (PrismML fork)'),
    (r'PrismML.*llama\.cpp', 'llama.cpp (PrismML fork)'),
    (r'^agentionai/llama\.cpp', 'llama.cpp (agentionai fork)'),
    (r'^llama\.cpp-mirai-s', 'llama.cpp (mirai-s fork)'),
    (r'^llama\.cpp', 'llama.cpp'),
    (r'^strata-mlx', 'strata-mlx'),
    (r'^Strata-DS', 'Strata (Strata-DS fork)'),
    (r'^Strata', 'Strata'),
    (r'^oMLX', 'oMLX'),
    (r'^TensorFold', 'TensorFold'),
    (r'^DFlash', 'DFlash'),
    (r'^MTPLX', 'MTPLX'),
    (r'^mlx-serve', 'mlx-serve'),
    (r'^MLX Swift', 'MLX Swift'),
    (r'^(mlx-lm|MLX)', 'MLX'),
    (r'^edge0', 'edge0'),
    (r'^SGLang', 'SGLang'),
    (r'^vLLM', 'vLLM'),
    (r'^Splash', 'Splash'),
    (r'^Project Maya', 'Project Maya'),
    (r'^halogen', 'Halogen'),
    (r'^Osaurus', 'Osaurus'),
    (r'^ExLlama', 'ExLlama'),
    (r'^Infernix', 'Infernix'),
    (r'^ds41\b', 'ds41'),
    (r'^TandemLLM', 'TandemLLM'),
    (r'^Geezuz', 'Geezuz'),
    (r'^MoEShift', 'MoEShift'),
    (r'^ik_llama\.cpp（Mcniiby', 'ik_llama.cpp (Mcniiby fork)'),
    (r'^Espetero', 'Espetero'),
    (r'^Paiton', 'Paiton'),
    (r'^Front_Eagle739 streaming stack', 'Front_Eagle739 streaming stack'),
    (r'^Halowin Bubo', 'Halowin Bubo'),
    (r'^Janas-LLM', 'Janas-LLM'),
    (r'^Strim', 'Strim'),
    (r'^Magnitude', 'Magnitude'),
    (r'^QEngine', 'QEngine'),
    (r'^PXA', 'PXA'),
    (r'^Betelgeuse', 'Betelgeuse'),
    (r'^Penny Royal', 'SGLang (Penny Royal fork)'),
    (r'^tandem\.cpp', 'llama.cpp (tandem.cpp fork)'),
    (r'^Speedy', 'Speedy'),
    (r'^未注明', 'Unspecified'),
]
INFER = [
    (r'Halogen', 'Halogen'), (r'\bSplash\b', 'Splash'), (r'sparkinfer', 'sparkinfer'),
    (r'FreeToken', 'FreeToken'), (r'tabbyAPI', 'TabbyAPI'), (r'Radiance fork', 'Radiance (fork)'),
    (r'project-maya|^Maya', 'Project Maya'), (r'DS41RT', 'DS41RT'), (r'^MTPLX', 'MTPLX'),
    (r'DwarfStar|ds4-metal|antirez ds4', 'ds4 (DwarfStar)'), (r'^mflux', 'mflux'),
    (r'NVIDIA Sol 引擎', 'NVIDIA Sol'),
]
def canon(raw):
    for p, c in RULES:
        if re.search(p, raw, re.I): return c if c is not None else raw
    return raw
def infer(r):
    for p, c in INFER:
        if re.search(p, r.get('quant') or '') : return c
    return UNSPEC
def normalize(recipes):
    prev = {}
    for r in recipes:
        raw = r.get('engine_raw', r['engine'])
        if raw == '同上': raw = prev.get(r['source_url'], raw)
        r['engine_raw'] = raw
        if raw.startswith('其他') or raw in ('同上', '', UNSPEC): eng = infer(r)
        else: eng = canon(raw)
        r['engine'] = eng
        note = raw if raw != eng and not raw.startswith('其他') else None
        if note: r['engine_note'] = note
        else: r.pop('engine_note', None)
        if r['engine_raw'] == eng: r.pop('engine_raw')
        prev[r['source_url']] = raw
    return recipes
if __name__ == '__main__':
    p = ROOT / 'data/recipes.json'; D = json.load(open(p))
    normalize(D); Path(p).write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    import collections; print(collections.Counter(r['engine'] for r in D).most_common())
