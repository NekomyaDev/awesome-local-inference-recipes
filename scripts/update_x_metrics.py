#!/usr/bin/env python3
"""Refresh X engagement (data/recipes.json x_post likes/reposts/as_of) and follower counts (data/sources.json, docs/internal/watchlist.md).

Live: X_BEARER_TOKEN=... python3 scripts/update_x_metrics.py
Offline: python3 scripts/update_x_metrics.py --posts posts.json --users users.json --as-of 2026-10-16
(--posts / --users take saved X API v2 responses with public_metrics.)
Then re-run gen_readme.py, gen_recipe_pages.py and gen_site.py."""
import argparse, datetime, json, os, re, urllib.parse, urllib.request
from pathlib import Path
import gen_watchlist
R = Path(__file__).resolve().parent.parent
RECIPES = R/'data/recipes.json'
SOURCES, WATCH = gen_watchlist.SOURCES, gen_watchlist.WATCH
API = 'https://api.x.com/2'

def post_id(url):
    m = re.search(r'/status/(\d+)', url or '')
    return m.group(1) if m else None

def x_handle(url):
    m = re.fullmatch(r'https://x\.com/([A-Za-z0-9_]+)/?', url or '')
    return m.group(1) if m else None

def _get(path, params, token):
    req = urllib.request.Request(f'{API}/{path}?{urllib.parse.urlencode(params)}', headers={'Authorization': f'Bearer {token}', 'User-Agent': 'awesome-local-inference-recipes'})
    return json.load(urllib.request.urlopen(req, timeout=30))

def _chunks(xs, n=100):
    for i in range(0, len(xs), n): yield xs[i:i+n]

def fetch_posts(ids, token):
    out = []
    for c in _chunks(ids): out += _get('tweets', {'ids': ','.join(c), 'tweet.fields': 'public_metrics'}, token).get('data', [])
    return out

def fetch_users(names, token):
    out = []
    for c in _chunks(names): out += _get('users/by', {'usernames': ','.join(c), 'user.fields': 'public_metrics'}, token).get('data', [])
    return out

def apply_posts(recipes, posts, as_of):
    m = {p['id']: p['public_metrics'] for p in posts}
    n = 0
    for r in recipes:
        pm = m.get(post_id(r.get('source_url'))) if r.get('x_post') else None
        if pm is None: continue
        r['x_post'].update(likes=pm['like_count'], reposts=pm['repost_count'], as_of=as_of); n += 1
    return n

def apply_users(sources, users, as_of):
    m = {u['username'].lower(): u['public_metrics']['followers_count'] for u in users}
    n = 0
    for s in sources['sources']:
        h = x_handle(s.get('url'))
        if h and h.lower() in m: s['followers'] = m[h.lower()]; n += 1
    sources['followers_as_of'] = sources['updated'] = as_of
    sources['note'] = re.sub(r'Follower counts from X API on \d{4}-\d{2}-\d{2}', 'Follower counts from X API on ' + as_of, sources['note'])
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--posts'); ap.add_argument('--users')
    ap.add_argument('--as-of', default=datetime.date.today().isoformat())
    a = ap.parse_args(); tok = os.environ.get('X_BEARER_TOKEN')
    recipes = json.loads(RECIPES.read_text(encoding='utf-8')); sources = json.loads(SOURCES.read_text(encoding='utf-8'))
    ids = sorted({post_id(r['source_url']) for r in recipes if r.get('x_post') and post_id(r['source_url'])})
    names = sorted({x_handle(s.get('url')) for s in sources['sources'] if x_handle(s.get('url'))})
    if a.posts: posts = json.loads(Path(a.posts).read_text(encoding='utf-8')).get('data', [])
    elif tok: posts = fetch_posts(ids, tok)
    else: raise SystemExit('Set X_BEARER_TOKEN or pass --posts/--users with saved X API responses')
    users = json.loads(Path(a.users).read_text(encoding='utf-8')).get('data', []) if a.users else (fetch_users(names, tok) if tok else [])
    np_ = apply_posts(recipes, posts, a.as_of)
    print(f'posts: {np_} recipes updated from {len(posts)}/{len(ids)} posts')
    RECIPES.write_text(json.dumps(recipes, ensure_ascii=False, indent=2), encoding='utf-8')
    if users:
        nu = apply_users(sources, users, a.as_of)
        print(f'followers: {nu} sources updated from {len(users)}/{len(names)} accounts')
        SOURCES.write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        WATCH.write_text(gen_watchlist.render(sources), encoding='utf-8')

if __name__ == '__main__': main()
