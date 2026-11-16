"""Guards for single-language surfaces: EN recipe pages carry no CJK, the ZH metric has no bare
English decode/prefill/agent, and JA pages label the English data text they show."""
import json, re, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'scripts'))
import gen_readme, gen_recipe_pages, i18n_rules

CJK = re.compile(r'[\u3000-\u303f\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]')
D = json.load(open(R/'data/recipes.json', encoding='utf-8'))


def en_page(r):
    """EN recipe page minus the language-switcher labels (简体中文 / 日本語), which are meant to be native."""
    return gen_recipe_pages.page(r, 'en').replace('简体中文', '').replace('日本語', '')


class EnPagesHaveNoCjk(unittest.TestCase):
    def test_every_en_recipe_page(self):
        bad = [r['id'] for r in D if CJK.search(en_page(r))]
        self.assertEqual(bad, [])

    def test_hardware_fallback_never_uses_raw_chinese(self):
        r = dict(D[0], hardware='某国产加速卡（双卡）', en={}, hardware_family='其他')
        for lang in ('en', 'ja'):
            p = gen_recipe_pages.page(r, lang)
            self.assertNotIn('某国产加速卡', p)
        self.assertFalse(CJK.search(en_page(r)))
        self.assertIn('某国产加速卡', gen_recipe_pages.page(r, 'zh'))


class ZhMetricTerms(unittest.TestCase):
    def test_dataset_has_no_bare_terms(self):
        bad = [(r['id'], w) for r in D for _, w in i18n_rules.bare_en_terms(r.get('metric'))]
        self.assertEqual(bad, [], 'write 解码 / 预填充 / 智能体 in the ZH metric (see scripts/i18n_rules.py)')

    def test_flags_bare_words(self):
        self.assertEqual([w for _, w in i18n_rules.bare_en_terms('散文 decode 35；冷 prefill 500；agents 3')], ['decode', 'prefill', 'agents'])

    def test_allowed_exceptions(self):
        for s in ['agent-trace 168.5', '（--prefill-pipe 3072）', 'Hermes Agent 回合', 'oMLX Prefill Accelerator',
                  'scorecard「Decode (New C++20)」19.48', 'prompt/decode 配方', 'strata_bench chat/agent 68', 'ds4-agent 负载',
                  '`--decode 1`', 'https://example.com/decode', '“decode” 原话']:
            self.assertEqual(i18n_rules.bare_en_terms(s), [], s)
        self.assertEqual(len(i18n_rules.bare_en_terms('预填/decode 路径')), 1)


class JaEnglishMarker(unittest.TestCase):
    def test_mark(self):
        m = gen_readme.mark_ja_en
        self.assertEqual(m('12 tok/s decode, single stream'), '12 tok/s decode, single stream（英語）')
        self.assertEqual(m(m('single stream')), 'single stream（英語）')
        for s in (None, '', '262,144', '42 tok/s', 'MTP KV Q4_K_M', '単一ストリーム'):
            self.assertEqual(m(s), s)

    def test_ja_recipe_page_marks_english_metric(self):
        r = next(r for r in D if r.get('metric_en') and re.search(r'\b[a-z]{4,}\b', r['metric_en']))
        self.assertIn(r['metric_en'] + '（英語）', gen_recipe_pages.page(r, 'ja'))
        self.assertNotIn('（英語）', gen_recipe_pages.page(r, 'en'))


if __name__ == '__main__':
    unittest.main()
