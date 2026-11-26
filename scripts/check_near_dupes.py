#!/usr/bin/env python3
"""Near-duplicate check for data/recipes.json. CI runs it after check_dupes.mjs.

Fails (exit 1) when two ids hold the same data: the same source (an X post id, a GitHub or Codeberg
issue/PR number, a Reddit post or comment, a Hugging Face repo, otherwise the URL), model, hardware,
engine, quant and tok_s. URL spelling (x.com vs twitter.com, handle, query string, case, issues vs
pull) does not hide such a pair.

Warns (exit 0) about possible CONTRIBUTING rule 8 updates: rows from different sources with the same
tester, hardware, model, engine and quant, and posts of one tester that repeat the same tok_s for the
same model and quant. A pair is not reported when either row names the other by id or source link."""
import json, re, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def source_key(u):
    u = u.strip().split('#')[0]
    u = re.sub(r'^http://', 'https://', u)
    u = re.sub(r'^https://(?:www\.|old\.|np\.|mobile\.)', 'https://', u)
    m = re.match(r'https://(?:x|twitter)\.com/(?:[^/]+|i/web)/status/(\d+)', u, re.I)
    if m: return 'x:' + m[1]
    m = re.match(r'https://(github\.com|codeberg\.org)/([^/]+)/([^/]+)/(?:issues|pull|pulls)/(\d+)', u, re.I)
    if m: return f'{m[1].lower()}:{m[2].lower()}/{m[3].lower()}#{m[4]}'
    m = re.search(r'reddit\.com/r/[^/]+/comments/([a-z0-9]+)(?:/[^/]*/([a-z0-9]+))?', u, re.I)
    if m: return 'reddit:' + m[1].lower() + ('/' + m[2].lower() if m[2] else '')
    m = re.match(r'https://(?:huggingface\.co|hf\.co)/([^/?]+/[^/?]+)', u, re.I)
    if m and m[1].split('/')[0] not in ('datasets', 'spaces', 'blog', 'papers', 'docs'): return 'hf:' + m[1].lower()
    return u.split('?')[0].rstrip('/').lower()


PAREN = re.compile(r'（[^）]*）|\([^)]*\)')


def hw_key(h):
    h = PAREN.sub('', (h or '').lower())
    h = re.sub(r'(?<![\d.])1\s*[×x]\s*|单\s*', '', h)
    return re.sub(r'[\s·,，/+]+', ' ', h).strip()


def model_key(m):
    return re.sub(r'[^0-9a-z]', '', PAREN.sub('', (m or '').lower()))


def quant_key(q):
    return re.sub(r'[\s,，;；]+', ' ', PAREN.sub('', (q or '').lower())).strip()


def person(r):
    p = r.get('measured_by')
    if p: return PAREN.sub('', p).strip().lstrip('@').lower() or None
    m = re.match(r'https?://(?:www\.)?(?:x|twitter)\.com/([^/]+)/status/', r['source_url'], re.I)
    return m[1].lower() if m else None


def mentions(a, b):
    """True when row a names row b by id or by its source link."""
    t = json.dumps({k: v for k, v in a.items() if k not in ('id', 'source_url', 'source_id')}, ensure_ascii=False)
    if re.search(r'(?<![\w-])' + re.escape(b['id']) + r'(?![\w-])', t): return True
    k = source_key(b['source_url'])
    if k.startswith(('x:', 'reddit:')):
        post = k.split(':', 1)[1].split('/')[-1]
        if len(post) >= 6 and re.search(r'(?<![\w])' + re.escape(post) + r'(?![\w])', t): return True
    m = re.match(r'(github\.com|codeberg\.org):(.+)#(\d+)$', k)
    if m and re.search(re.escape(m[2].split('/')[1]) + r'[^\s]{0,12}?(?:#|/issues/|/pulls?/)' + m[3] + r'(?!\d)', t, re.I): return True
    return b['source_url'].split('://')[-1].rstrip('/') in t


def linked(a, b): return mentions(a, b) or mentions(b, a)


def check(D):
    errors, warnings = [], []
    same = defaultdict(list)
    for r in D:
        if r.get('tok_s') is not None:
            same[(source_key(r['source_url']), model_key(r['model']), hw_key(r['hardware']), r['engine'].lower(), quant_key(r.get('quant')), r['tok_s'])].append(r['id'])
    for ids in same.values():
        if len(ids) > 1: errors.append(f'same data under different ids: {", ".join(ids)}')
    rule8 = defaultdict(list)
    repeat = defaultdict(list)
    for r in D:
        p = person(r)
        if not p: continue
        rule8[(p, hw_key(r['hardware']), model_key(r['model']), r['engine'].lower(), quant_key(r.get('quant')))].append(r)
        if r.get('tok_s') is not None: repeat[(p, model_key(r['model']), quant_key(r.get('quant')), r['tok_s'])].append(r)
    seen = set()
    for kind, groups in (('possible rule-8 update (same tester, machine, model, engine and quant)', rule8), ('same tester repeats the same tok_s for this model and quant', repeat)):
        for rows in groups.values():
            for a, b in combinations(rows, 2):
                pair = tuple(sorted((a['id'], b['id'])))
                if pair in seen or source_key(a['source_url']) == source_key(b['source_url']) or linked(a, b): continue
                seen.add(pair); warnings.append(f'{kind}: {pair[0]} / {pair[1]}')
    return errors, warnings


def main():
    with open(ROOT / 'data/recipes.json', encoding='utf-8') as f: D = json.load(f)
    errors, warnings = check(D)
    for w in warnings: print('warn:', w)
    for e in errors: print('NEAR-DUPE:', e)
    print(f'check_near_dupes: {len(errors)} error(s), {len(warnings)} warning(s)')
    sys.exit(1 if errors else 0)


if __name__ == '__main__': main()
