#!/usr/bin/env python3
"""Write the URL lists for the weekly link check (.github/workflows/linkcheck.yml).
Every URL in data/recipes.json (structured fields and free text such as metric and source_note), data/prices.json and
data/sources.json goes into one of two files:
- urls-walled.txt: x.com, twitter.com and reddit.com. These sites block anonymous fetches, so lychee accepts 403 and 429.
- urls-strict.txt: every other host. Only 2xx is accepted, so a 403, 429 or 404 there is reported.
Run: python3 scripts/linkcheck_urls.py [OUT_DIR]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import url_safety as us

ROOT = Path(__file__).resolve().parent.parent
WALLED = ('x.com', 'twitter.com', 'reddit.com')
FILES = ('data/recipes.json', 'data/prices.json', 'data/sources.json')


def strings(o):
    if isinstance(o, str): yield o
    elif isinstance(o, dict):
        for v in o.values(): yield from strings(v)
    elif isinstance(o, list):
        for v in o: yield from strings(v)


def all_urls():
    out = set()
    for f in FILES:
        for t in strings(json.loads((ROOT / f).read_text(encoding='utf-8'))):
            for u in us.URL_RE.findall(t):
                u = u.rstrip('.。:：')
                if us.host_of(u): out.add(u)
    return sorted(out)


def split(urls):
    walled = [u for u in urls if any(us.under(us.host_of(u), d) for d in WALLED)]
    return walled, [u for u in urls if u not in set(walled)]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    walled, strict = split(all_urls())
    (out / 'urls-walled.txt').write_text('\n'.join(walled) + '\n', encoding='utf-8')
    (out / 'urls-strict.txt').write_text('\n'.join(strict) + '\n', encoding='utf-8')
    print(f'linkcheck_urls: {len(strict)} strict, {len(walled)} walled (403/429 accepted)')


if __name__ == '__main__': main()
