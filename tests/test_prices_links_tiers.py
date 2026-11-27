import json, re, sys, unittest
from collections import Counter
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
import check_urls, gen_readme, linkcheck_urls, prices, ja_text, approve_review  # noqa: E402
from dataset_constants import BUDGET_TIER_BOUNDS_USD  # noqa: E402
README = {'en': 'README.md', 'zh': 'README.zh-CN.md', 'ja': 'README.ja.md'}


class GluedUrls(unittest.TestCase):
    def test_site_name_glued_to_a_url_is_caught(self):
        self.assertTrue(check_urls.glued_urls('页 https://llm-speed.com/can-run/sage-a1-5/rtx-4090llm-speed 页面只有汇总'))

    def test_ascii_glue_is_caught_against_the_other_language(self):
        zh = '见 https://example.com/blog/post/42measured 页面'
        en = 'See https://example.com/blog/post/42 for details'
        self.assertTrue(check_urls.glued_urls(zh, en))
        self.assertFalse(check_urls.glued_urls(en, zh))

    def test_cjk_glued_to_a_url_is_caught(self):
        self.assertTrue(check_urls.glued_urls('见 https://x.com/a/status/123页面'))

    def test_clean_urls_pass(self):
        for t in ['见 https://x.com/a/status/123 页面', '（https://github.com/a/b/issues/4）用', 'https://www.reddit.com/r/LocalLLaMA/comments/1x/，数字相同',
                  'https://reddit.com/r/subreddit/', 'https://github.com/foo/llm-speed']:
            self.assertFalse(check_urls.glued_urls(t), t)

    def test_ascii_glue_is_caught_against_another_url_of_the_row(self):
        row = {'id': 't-1', 'source_url': 'https://x.com/a/status/123', 'metric': '见 https://x.com/a/status/123details 页面'}
        self.assertTrue(check_urls.glue_violations([row], {'items': []}))
        row['metric'] = '见 https://x.com/a/status/123 页面'
        self.assertFalse(check_urls.glue_violations([row], {'items': []}))

    def test_prefix_glue_spares_real_pages_and_checks_price_items(self):
        row = {'id': 't-2', 'source_url': 'https://en.wikipedia.org/wiki/Java', 'metric': '另见 https://en.wikipedia.org/wiki/JavaScript 页面'}
        self.assertFalse(check_urls.glue_violations([row], {'items': []}))
        for a, b in (('https://example.com/', 'https://example.com/about'), ('https://en.wikipedia.org/wiki/Java', 'https://en.wikipedia.org/wiki/JavaScript')):
            row = {'id': 't-3', 'source_url': a, 'metric': f'见 {b} 页面', 'metric_en': f'See {a} here'}
            self.assertFalse(check_urls.glue_violations([row], {'items': []}), (a, b))
        item = {'item': 'x', 'source': 'https://gpusold.com/gpu/123', 'note': '见 https://gpusold.com/gpu/123details 页面'}
        self.assertTrue(check_urls.glue_violations([], {'items': [item]}))

    def test_data_has_no_glued_urls(self):
        R_ = json.loads((R / 'data/recipes.json').read_text(encoding='utf-8'))
        P = json.loads((R / 'data/prices.json').read_text(encoding='utf-8'))
        self.assertEqual(check_urls.glue_violations(R_, P), [])


class LinkcheckLists(unittest.TestCase):
    def test_free_text_and_prices_urls_are_listed_and_split(self):
        urls = linkcheck_urls.all_urls()
        self.assertIn('https://llm-speed.com/can-run/sage-a1-5/rtx-4090', urls)  # free text (metric) of comm-382
        self.assertIn('https://gpusold.com/gpu/a100-40', urls)  # data/prices.json
        walled, strict = linkcheck_urls.split(urls)
        self.assertTrue(walled and strict)
        self.assertTrue(all(re.search(r'(^|\.)(x|twitter|reddit)\.com$', linkcheck_urls.us.host_of(u)) for u in walled))
        self.assertFalse(any(re.search(r'(^|\.)(x|twitter|reddit)\.com$', linkcheck_urls.us.host_of(u)) for u in strict))

    def test_workflow_accepts_403_429_only_for_walled_hosts(self):
        wf = (R / '.github/workflows/linkcheck.yml').read_text(encoding='utf-8')
        args = re.findall(r'args: (.*)', wf)
        strict = next(a for a in args if 'urls-strict.txt' in a); walled = next(a for a in args if 'urls-walled.txt' in a)
        self.assertNotIn('403', strict); self.assertNotIn('429', strict)
        self.assertIn('403', walled); self.assertIn('429', walled)
        # The strict run also reads the Markdown files, so it must exclude X and Reddit; those go to the walled list.
        ex = re.search(r"--exclude '([^']+)'", strict).group(1)
        for u in ('https://x.com/a/status/1', 'https://www.reddit.com/r/LocalLLaMA/', 'https://twitter.com/a'): self.assertRegex(u, ex)
        for u in ('https://github.com/x/y', 'https://example.com/x.com'): self.assertNotRegex(u, ex)
        md_walled = {u for g in linkcheck_urls.MARKDOWN for f in R.glob(g) for u in linkcheck_urls.MD_URL.findall(f.read_text(encoding='utf-8'))
                     if re.search(ex, u)}
        walled_list = set(linkcheck_urls.split(linkcheck_urls.all_urls())[0])
        self.assertTrue(md_walled); self.assertTrue({u.rstrip('.,;:。') for u in md_walled} <= walled_list)

    def test_replaced_price_sources_are_not_checked(self):
        self.assertFalse(any('clustermelt' in u for u in linkcheck_urls.all_urls()))


class Prices(unittest.TestCase):
    def setUp(self):
        self.P = json.loads((R / 'data/prices.json').read_text(encoding='utf-8'))

    def test_snapshot_has_dates_and_status(self):
        self.assertRegex(self.P['as_of'], r'^\d{4}-\d{2}-\d{2}$'); self.assertRegex(self.P['next_review'], r'^\d{4}-\d{2}-\d{2}$')
        self.assertGreater(self.P['next_review'], self.P['as_of'])
        for i in self.P['items']:
            self.assertTrue({'item', 'price', 'date', 'source', 'status'} <= set(i), i['item'])
            self.assertIn(i['status'], ('verified', 'verified-secondary', 'unverified'), i['item'])
            if i['status'] != 'verified': self.assertTrue(i.get('note'), i['item'])
        self.assertFalse(any('clustermelt' in i['source'] for i in self.P['items']))
        a100 = next(i for i in self.P['items'] if 'A100' in i['item'])
        self.assertIn('clustermelt', json.dumps(a100.get('previous'), ensure_ascii=False))

    def test_readme_banner_in_every_language(self):
        for lang, f in README.items():
            s = (R / f).read_text(encoding='utf-8')
            banner = [l for l in s.splitlines() if l.startswith('> ') and '(data/prices.json)' in l]
            self.assertEqual(len(banner), 1, lang)
            self.assertIn(self.P['as_of'], banner[0], lang); self.assertIn(self.P['next_review'], banner[0], lang)


class TierOrder(unittest.TestCase):
    def test_tier_lists_put_measured_first(self):
        D = gen_readme.D
        for lo, hi in BUDGET_TIER_BOUNDS_USD:
            rs = sorted([r for r in D if r['hardware_cost_usd'] is not None and lo < r['hardware_cost_usd'] <= hi and r['category'] == 'text'], key=gen_readme.tier_key)
            ranks = [gen_readme.LEVEL_ORDER[r['source_level']] for r in rs]
            self.assertEqual(ranks, sorted(ranks))
        self.assertLess(gen_readme.LEVEL_ORDER['实测'], gen_readme.LEVEL_ORDER['官方']); self.assertLess(gen_readme.LEVEL_ORDER['官方'], gen_readme.LEVEL_ORDER['宣称'])

    def test_readme_tier_top_is_measured_when_the_tier_has_a_measured_row(self):
        s = (R / 'README.md').read_text(encoding='utf-8')
        for t in gen_readme.L['en']['tiers']:
            sec = s.split('## ' + t, 1)[1].split('\n## ', 1)[0]
            first = re.search(r'\*\*📝 Text\*\*\n\n- .*', sec)
            if first: self.assertIn('✅', first.group(0), t)


class Families(unittest.TestCase):
    def test_no_model_prefix_with_ten_rows_left_in_other(self):
        D = json.loads((R / 'data/recipes.json').read_text(encoding='utf-8'))
        c = Counter(re.split(r'[ \-（(.]', r['model'])[0] for r in D if r['model_family'] == 'Other')
        self.assertFalse([k for k, n in c.items() if n >= 10], c.most_common(3))



class PriceSnapshotCadence(unittest.TestCase):
    def test_next_review_is_two_weeks_after_as_of(self):
        from datetime import date
        P = json.loads((R / 'data/prices.json').read_text(encoding='utf-8'))
        self.assertEqual((date.fromisoformat(P['next_review']) - date.fromisoformat(P['as_of'])).days, 14)

    def test_contributing_says_every_two_weeks(self):
        t = (R / 'CONTRIBUTING.md').read_text(encoding='utf-8')
        self.assertIn('every two weeks', t)
        self.assertIn('每两周核对一次', t)
        self.assertIn('2 週間ごとに見直します', t)
        self.assertNotIn('2026-12-27', t)

    def test_banner_figures_come_from_the_snapshot(self):
        P = json.loads((R / 'data/prices.json').read_text(encoding='utf-8'))
        b = prices.banner(P)
        for lang, f in README.items():
            line = next(l for l in (R / f).read_text(encoding='utf-8').splitlines() if l.startswith('> ') and '(data/prices.json)' in l)
            self.assertIn(b['asof'], line); self.assertIn(b['nxt'], line)
            self.assertIn(b['ddr5_lo'], line); self.assertIn(b['ddr5_hi'], line)
            self.assertIn(b['rtx_now'], line); self.assertIn(b['rtx_old'], line)
            self.assertNotIn('2026-12-27', line)

    def test_apple_studio_rows_are_no_longer_unverified(self):
        P = json.loads((R / 'data/prices.json').read_text(encoding='utf-8'))
        keys = ('M5 Ultra 256GB', 'M4 Max', 'M3 Ultra', 'M2 Ultra')
        rows = [i for i in P['items'] if any(k in i['item'] for k in keys)]
        self.assertGreaterEqual(len(rows), 4)
        for i in rows:
            self.assertNotEqual(i['status'], 'unverified', i['item'])
            self.assertTrue(i['source'].startswith('http'), i['item'])


class ApproveReviewPrices(unittest.TestCase):
    def test_approve_review_reads_prices_json_not_october_constants(self):
        src = (R / 'scripts/approve_review.py').read_text(encoding='utf-8')
        self.assertNotIn('SOURCED_PRICES_BY_HARDWARE', src)
        self.assertNotIn('2026-10-11', src)
        self.assertNotIn('$5,400', src)
        self.assertIn('sourced_prices.cost_for_hardware', src)

    def test_approve_review_writes_snapshot_costs_into_a_new_row(self):
        import tempfile, shutil
        P = prices.load()
        want_text, want_usd = prices.cost_for_hardware('RTX 4090 24GB', P)
        self.assertTrue(want_text and want_usd)
        scratch = Path(tempfile.mkdtemp())
        try:
            (scratch / 'data').mkdir(); (scratch / 'data' / 'candidates').mkdir()
            shutil.copy(R / 'data/prices.json', scratch / 'data/prices.json')
            # A tiny empty recipe list so the new row is the only one added.
            (scratch / 'data' / 'recipes.json').write_text('[]\n', encoding='utf-8')
            cid = 'hf-test--Tiny-7B-gguf'
            cand = {'candidates': [{'id': cid, 'status': 'pending'}]}
            review = {'reviews': [{'id': cid, 'decision': '收录', 'url': 'https://example.com/model',
                'recipes': [{'hardware': 'RTX 4090 24GB', 'quant': 'Q4', 'engine': 'llama.cpp',
                             'gen_tok_s': 10, 'prefill_tok_s': None, 'level': '宣称', 'quote': '10 tok/s'}]}]}
            rp = scratch / 'data/candidates/hf-2099-01-01.review.json'
            rp.write_text(json.dumps(review), encoding='utf-8')
            (scratch / 'data/candidates/hf-2099-01-01.json').write_text(json.dumps(cand), encoding='utf-8')
            old_root, old_argv = approve_review.ROOT, sys.argv[:]
            try:
                approve_review.ROOT = str(scratch)
                sys.argv = ['approve_review.py', str(rp)]
                approve_review.main()
            finally:
                approve_review.ROOT = old_root
                sys.argv = old_argv
            rows = json.loads((scratch / 'data/recipes.json').read_text(encoding='utf-8'))
        finally:
            shutil.rmtree(scratch, ignore_errors=True)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['hardware_cost_usd'], want_usd)
        self.assertEqual(rows[0]['hardware_cost_text'], want_text)
        self.assertIn('prices.json', rows[0]['hardware_cost_text'])


class JapaneseMetrics(unittest.TestCase):
    def test_short_tier_labels_are_japanese(self):
        D = {r['id']: r for r in json.loads((R / 'data/recipes.json').read_text(encoding='utf-8'))}
        self.assertIn('公開の領収', ja_text.metric(D['image-002']))
        self.assertNotIn('public receipt', ja_text.metric(D['image-002']))
        self.assertIn('宣伝投稿', ja_text.metric(D['video-audio-019']))
        self.assertNotIn('promo post', ja_text.metric(D['video-audio-019']))
        self.assertIn('曲全体', ja_text.metric(D['video-audio-019']))
        self.assertNotIn('快約', ja_text.metric(D['image-016']))
        self.assertIn('約', ja_text.metric(D['image-016']))
        # Long English cookbook blurbs stay English (and get the JA marker), not a mixed sentence.
        self.assertTrue(ja_text.english_fallback(D['comm-430']) or ja_text.needs_en_mark(ja_text.metric(D['comm-430'])))

    def test_ja_readme_and_site_do_not_leave_those_labels_in_english(self):
        ja = (R / 'README.ja.md').read_text(encoding='utf-8')
        for s in ('public receipt', 'promo post', 'Whole song'):
            self.assertNotIn(s, ja, s)
        self.assertIn('公開の領収', ja)
        self.assertIn('宣伝投稿', ja)
        self.assertNotIn('快約', ja)
        # A leftover English cookbook sentence must be marked, not mixed mid-sentence.
        if 'One DGX Spark' in ja:
            self.assertIn('One DGX Spark', ja)
            self.assertIn('（英語）', ja)
        # Banner states lowest and median separately, and keeps the spike in November even if as_of moves.
        banner = next(l for l in ja.splitlines() if l.startswith('> ') and 'prices.json' in l)
        self.assertIn('最低約', banner); self.assertIn('中央値約', banner)
        self.assertIn('11 月', banner)
        page = (R / 'recipes/image-001.ja.md').read_text(encoding='utf-8') if (R / 'recipes/image-001.ja.md').exists() else ''
        # The JA image guide should use ステップ, not the English "steps" label from metric_en.
        if page:
            self.assertNotIn('(40 steps)', page)


if __name__ == '__main__': unittest.main()
