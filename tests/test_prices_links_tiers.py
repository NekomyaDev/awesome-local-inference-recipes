import json, re, sys, unittest
from collections import Counter
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
import check_urls, gen_readme, linkcheck_urls  # noqa: E402
from dataset_constants import BUDGET_TIER_BOUNDS_USD  # noqa: E402
README = {'en': 'README.md', 'zh': 'README.zh-CN.md', 'ja': 'README.ja.md'}


class GluedUrls(unittest.TestCase):
    def test_site_name_glued_to_a_url_is_caught(self):
        self.assertTrue(check_urls.glued_urls('页 https://llm-speed.com/can-run/sage-a1-5/rtx-4090llm-speed 页面只有汇总'))

    def test_ascii_glue_is_caught_against_the_other_language(self):
        zh = '见 https://example.com/blog/post-measuredfoo 页面'
        en = 'See https://example.com/blog/post-measured for details'
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
            self.assertIn('(data/prices.json)', s, lang); self.assertIn(self.P['as_of'], s, lang); self.assertIn(self.P['next_review'], s, lang)


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


if __name__ == '__main__': unittest.main()
