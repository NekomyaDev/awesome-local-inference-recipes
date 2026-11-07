#!/usr/bin/env python3
"""Derive `model_family` and `tags` from existing fields only (idempotent, deterministic).
Run: python3 scripts/tag_recipes.py"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
FAMILIES = [
    (r'Qwen-Image', 'Qwen-Image'), (r'Z-Image', 'Z-Image'), (r'Qwen', 'Qwen'),
    (r'DeepSeek', 'DeepSeek'), (r'GLM', 'GLM'), (r'Bonsai', 'Bonsai'),
    (r'MiniMax H3|FastH3', 'MiniMax H3'), (r'MiniMax', 'MiniMax'), (r'LTX', 'LTX'), (r'Wan\s?2', 'Wan'),
    (r'ACE-Step', 'ACE-Step'), (r'Edge0', 'Edge0'), (r'Llama', 'Llama'), (r'Gemma', 'Gemma'),
    (r'Mistral', 'Mistral'), (r'Kimi', 'Kimi'), (r'gpt-oss', 'gpt-oss'), (r'Flux', 'Flux'),
    (r'Hunyuan', 'Hunyuan'),
]
QUANT = [
    ('1bit', r'1-bit|\b1bit|\bI?Q1_'),
    ('ternary', r'ternary|\bTQ[12]_0'),
    ('2bit', r'\bI?Q2|2-bit|\b2bit|\b2\.\d+\s?bpw|\bW2\b|-W2'),
    ('3bit', r'\bW3(?=A\d|\b)|\bI?Q3|(?<![\w.])3-bit|\b3bit|(?<![\w.])3(\.\d+)?\s?bpw|q3_k'),
    ('4bit', r'\bI?Q4|(?<![\d.])4-bit|\b4bit|\bint4|MXFP4|NVFP4|\bFP4|\b4\.\d+\s?bpw|mixed-4|mixed 4/8|oQ4|\bAWQ\b'),
    ('5bit', r'\bQ5|5-bit|\b5bit'),
    ('6bit', r'\bQ6|6-bit|\b6bit|mix6|\bINT6'),
    ('8bit', r'\bQ8|q8_0|8-bit|\b8bit|\bINT8|\bFP8|int8'),
    ('bf16', r'\bBF16\b|\bFP16\b|bf16'),
]
# Models that are MoE by architecture, even when model/quant text does not say so.
MOE_MODELS = r'GLM-5\.3（\d+B 全量|Ornith-1\.5-122B|DeepSeek-V4(\.\d+)?-Flash|Qwen3\.8-Flash-Next|GLM-5\.3-Flash|MiniMax-M3\.1-Flash|Recursive Flint|Flint 40B|Ling-3\.[01]-flash|KAT-Coder|gpt-oss'
_DT = r'(?:[\w.]*\d[\w.\-]*|bf16|fp16)'
# A cache dtype is the dtype after 'KV' (or 'KV cache'); a dtype before 'KV' counts only when no dtype follows.
KV_OR_SOURCE = (r'\bKV(?:[\s-]*cache)?[\s:=]*' + _DT + r'|' + _DT + r'[\s-]*KV\b(?![\s-]*(?:cache)?[\s:=]*' + _DT + r')(?:[\s-]*cache)?'
                r'|自\s*BF16\s*量化|from BF16')
GPU_UNLOCK = r'gpu-unlock|解除\s*(?:LHR\s*)?(?:FP16|BF16|LHR)[^，；）]*限速'
SPEC = r'MTP|投机|DFlash|DSpark|草稿|draft|n-gram|\bEAGLE|speculative'
MULTI = r'(?<![\d.])(?:[2-9]|1\d)\s*[×x✕]\s|双|\bTP\s*=?\s*[2-9]|集群|cluster|[2-9]\s*张|[2-9]\s*台|\+\s*RTX'
def family(model):
    for p, f in FAMILIES:
        if re.search(p, model, re.I): return f
    return 'Other'
def ctx_k(s):
    if not s: return 0
    m = re.search(r'(\d[\d,]{4,})', s)
    best = int(m.group(1).replace(',', '')) // 1000 if m else 0
    for n, u in re.findall(r'(\d+(?:\.\d+)?)\s*([KkMm])\b', s):
        best = max(best, float(n) * (1000 if u in 'Mm' else 1))
    return best
def tags(r):
    mq = ' '.join(filter(None, [r['model'], r.get('quant')]))
    # Caveat notes about other builds/regressions must not drive speculative/MTP tags.
    metric = r.get('metric') or ''
    metric_for_spec = re.split(r'限定：|qualification\s*:', metric, maxsplit=1, flags=re.I)[0]
    allf = ' '.join(filter(None, [mq, r['engine'], r.get('engine_note'), metric_for_spec]))
    allf = re.sub(r'MTP\s*(关|off)|无投机|无草稿(模型)?|不开 MTP|无 ?(?:MTP|DFlash)(?:/(?:MTP|DFlash))*', '', allf, flags=re.I)
    # Quant tags describe the weights: ignore KV-cache dtypes and the source precision of a conversion.
    mq_w = re.sub(KV_OR_SOURCE, '', mq, flags=re.I)
    t = [k for k, p in QUANT if re.search(p, mq_w, re.I)]
    moe = bool(re.search(r'\bA\d+(\.\d+)?B\b|MoE|激活|REAP|专家', mq + ' ' + (r.get('quant') or ''))) or bool(re.search(MOE_MODELS, r['model'], re.I))
    if r['category'] == 'text':
        if moe: t.append('MoE')
        elif re.search(r'\b\d+B\b', r['model']): t.append('dense')
        if ctx_k(r.get('context')) >= 128: t.append('long-context')
    if re.search(SPEC, allf, re.I): t.append('speculative')
    if re.search(r'MTP', allf, re.I): t.append('MTP')
    if re.search(MULTI, (r.get('hardware') or '') + ' ' + (r.get('quant') or ''), re.I): t.append('multi-GPU')
    off = ' '.join(filter(None, [mq, r.get('hardware'), r.get('metric')]))
    if re.search(r'卸载|offload|NVMe|SSD(?! ?前缀)|闪存|流式读取|放内存|系统内存|RAM 卸载', off, re.I) or re.search(r'流式|stream', mq, re.I): t.append('offload')
    if r['category'] != 'text' and re.search(r'Turbo|蒸馏|distill|\b[1-8]\s*步', mq, re.I): t.append('few-step')
    if re.search(r'Abliterated|去拒答', r['model'], re.I): t.append('abliterated')
    # Firmware/driver unlock on a stock GPU (not a hardware mod, e.g. not a memory-changed CMP 170HX).
    unl = ' '.join(str(r.get(k) or '') for k in ('hardware', 'source_note', 'metric', 'quant'))
    if re.search(GPU_UNLOCK, unl, re.I): t.append('gpu-unlock')
    return t
def apply(recipes):
    for r in recipes:
        r['model_family'] = family(r['model']); r['tags'] = tags(r)
    return recipes
if __name__ == '__main__':
    p = ROOT / 'data/recipes.json'; D = json.load(open(p))
    apply(D); Path(p).write_text(json.dumps(D, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    import collections
    print(collections.Counter(r['model_family'] for r in D).most_common())
    print(collections.Counter(t for r in D for t in r['tags']).most_common())
