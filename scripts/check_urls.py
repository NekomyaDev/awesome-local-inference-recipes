#!/usr/bin/env python3
"""URL and launch-command hygiene check. CI runs this. Exit 1 on any violation.
Rules: scripts/url_safety.py and docs/hw_index.md (Security).
Also checks that no URL in free text is glued to the text after it (see glued_urls), in data/recipes.json and data/prices.json."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import url_safety as us

ROOT = Path(__file__).resolve().parent.parent
# Launch commands that a test already knows about. The index does not emit them (launch_cmd is null, launch_cmd_warning says why).
KNOWN_UNSAFE_CMDS = {'comm-053', 'comm-057', 'x-108'}


def load(p): return json.loads((ROOT / p).read_text(encoding='utf-8'))


def known_owners():
    """HF/ModelScope owners named by the data itself: model cards in model-params.json and recipe sources on the hubs."""
    out = {k for k in us.CFG.get('verified_hub_owners', {}) if not k.startswith('_')}
    for u in [m['source'] for m in load('data/model-params.json')['models']] + [r['source_url'] for r in load('data/recipes.json')]:
        k = us.repo_key(u)
        if k and k.split('/')[0] in ('huggingface.co', 'hf.co', 'modelscope.cn'): out.add(k.split('/')[1])
    return out


# A URL must end at whitespace or at punctuation that URL_RE stops at. Text glued straight after a URL becomes part of
# the link: CJK text makes the URL non-ASCII; ASCII text is caught when the same field's other-language copy has the
# URL without the tail, or when a site name is stuck to the end of the path (".../rtx-4090llm-speed").
CJK = re.compile(r'[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\uff01-\uff60]')
SITE_TAIL = re.compile(r'(?<=[a-z0-9])(?<!sub)(?:llm-speed|llmspeed|reddit|github|huggingface|modelscope)$', re.I)
# (Chinese field, English copy) pairs. The English copy lives at the top level (metric_en) or under "en".
PAIRS = (('metric', 'metric_en'), ('source_note', 'en.source_note'), ('engine_note', 'en.engine_note'), ('quant', 'en.quant'),
         ('hardware', 'en.hardware'), ('context', 'en.context'), ('concurrency', 'en.concurrency'), ('hardware_cost_text', 'en.hardware_cost_text'))


def _get(r, path):
    for k in path.split('.'):
        r = r.get(k) if isinstance(r, dict) else None
    return r if isinstance(r, str) else ''


def _strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from _strings(v)
    elif isinstance(o, list):
        for v in o: yield from _strings(v)


def glued_urls(text, other=''):
    """URLs in text that run straight into the next word. other: the same field in another language, if any."""
    out = []
    others = us.URL_RE.findall(other or '')
    for u in us.URL_RE.findall(text or ''):
        m = CJK.search(u)
        if m: out.append((u, f'glued to the text after it ({u[m.start():m.start() + 6]!r}); put a space after the URL')); continue
        if SITE_TAIL.search(u.rstrip('/')): out.append((u, 'a site name is glued to the end of the URL; put a space after the URL')); continue
        for v in others:
            v = v.rstrip('.。')
            if len(v) < len(u) and u.startswith(v) and u[len(v)].isalnum() and v not in us.URL_RE.findall(text):
                out.append((u, f'the other-language copy has {v}; the rest ({u[len(v):]!r}) is glued text')); break
    return out


def glue_violations(R, prices):
    bad = []
    for r in R:
        seen = set()
        for zh, en in PAIRS:
            for u, why in glued_urls(_get(r, zh), _get(r, en)) + glued_urls(_get(r, en), _get(r, zh)):
                if u not in seen: seen.add(u); bad.append(f"{r['id']}: {u}: {why}")
        for t in _strings(r):
            for u, why in glued_urls(t):
                if u not in seen: seen.add(u); bad.append(f"{r['id']}: {u}: {why}")
        # A URL that is another URL of the same row plus a run of letters (".../123" and ".../123details") is glued text.
        # A glued ASCII word with no second copy of the URL anywhere cannot be told apart from a real path.
        urls = {u for t in _strings(r) for u in us.URL_RE.findall(t)}
        for u in sorted(urls):
            for v in urls:
                if len(v) < len(u) and u.startswith(v) and re.fullmatch(r'[A-Za-z]+', u[len(v):]) and u not in seen:
                    seen.add(u); bad.append(f"{r['id']}: {u}: the row also has {v}; the rest ({u[len(v):]!r}) is glued text"); break
    for p in (prices.get('items', []) if isinstance(prices, dict) else prices):
        for t in _strings(p):
            for u, why in glued_urls(t): bad.append(f"prices.json {p.get('item')}: {u}: {why}")
    return bad


def violations():
    bad = []
    R = load('data/recipes.json')
    texts = [(r['id'], json.dumps(r, ensure_ascii=False)) for r in R]
    texts += [('repos.json', json.dumps(load('data/repos.json'), ensure_ascii=False)), ('sources.json', json.dumps(load('data/sources.json'), ensure_ascii=False))]
    prices = load('data/prices.json')
    texts += [('prices.json', json.dumps(prices, ensure_ascii=False))]
    for where, t in texts:
        for u in us.URL_RE.findall(t):
            for p in us.problems(u): bad.append(f'{where}: {u}: {p}')
    bad += glue_violations(R, prices)
    for r in R:
        cp = us.cmd_problems(r.get('launch_command'))
        if cp and r['id'] not in KNOWN_UNSAFE_CMDS: bad.append(f"{r['id']}: launch_command: {', '.join(cp)}")
    idx = ROOT / 'data/hw_index.json'
    if idx.exists():
        owners = {o.lower() for o in known_owners()}
        for x in load('data/hw_index.json')['recipes']:
            w = x.get('weights_url')
            if w:
                k = us.repo_key(w['url'])
                if not k: bad.append(f"{x['id']}: weights_url is not a hub owner/repo URL: {w['url']}")
                elif k.split('/')[1].lower() not in owners: bad.append(f"{x['id']}: weights_url owner {k.split('/')[1]} is not a known owner")
            for f in ('engine_repo', 'weights_url'):
                if x.get(f) and x[f]['trust'] != 'allowlisted': bad.append(f"{x['id']}: {f} is not on an allowlisted host: {x[f]['url']}")
            if x.get('launch_cmd') and us.cmd_problems(x['launch_cmd']): bad.append(f"{x['id']}: unsafe launch_cmd in index")
    return bad


def main():
    bad = violations()
    for b in bad: print('URL CHECK:', b)
    print(f'check_urls: {len(bad)} violation(s)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__': main()
