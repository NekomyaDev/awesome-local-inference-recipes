"""scripts/check_near_dupes.py: URL spellings of one source map to one key, re-ingested rows fail,
rule-8 candidates only warn, and rows that name each other are not reported."""
import json, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'scripts'))
import check_near_dupes as nd


def row(id, url, **kw):
    r = dict(id=id, source_url=url, model='Qwen3.8-Flash-Next', hardware='1× RTX 5090 32GB', engine='Strata',
             quant='IQ4_XS', tok_s=100, measured_by='@someone')
    r.update(kw); return r


class SourceKey(unittest.TestCase):
    def test_same_source_spellings(self):
        for a, b in [('https://x.com/a/status/123?s=20', 'https://twitter.com/B/status/123'),
                     ('https://github.com/Org/Repo/issues/5', 'https://github.com/org/repo/pull/5#issuecomment-1'),
                     ('https://codeberg.org/o/r/issues/248', 'https://codeberg.org/o/r/pulls/248'),
                     ('https://www.reddit.com/r/LocalLLaMA/comments/abc12/title/', 'https://old.reddit.com/r/LocalLLaMA/comments/abc12/'),
                     ('https://huggingface.co/Org/Model-GGUF', 'https://hf.co/org/model-gguf/tree/main')]:
            self.assertEqual(nd.source_key(a), nd.source_key(b), (a, b))

    def test_different_sources(self):
        self.assertNotEqual(nd.source_key('https://x.com/a/status/1'), nd.source_key('https://x.com/a/status/2'))
        self.assertNotEqual(nd.source_key('https://www.reddit.com/r/x/comments/abc/t/def/'), nd.source_key('https://www.reddit.com/r/x/comments/abc/t/'))


class Check(unittest.TestCase):
    def test_reingest_fails(self):
        errors, _ = nd.check([row('a', 'https://x.com/someone/status/1'), row('b', 'https://twitter.com/someone/status/1?s=46')])
        self.assertEqual(len(errors), 1)

    def test_rule8_candidate_warns(self):
        errors, warnings = nd.check([row('a', 'https://x.com/someone/status/1'), row('b', 'https://x.com/someone/status/2', tok_s=110)])
        self.assertEqual(errors, []); self.assertEqual(len(warnings), 1)

    def test_cross_reference_silences(self):
        rows = [row('a', 'https://x.com/someone/status/1'), row('b', 'https://x.com/someone/status/2', tok_s=110, metric='旧数字见 a')]
        self.assertEqual(nd.check(rows), ([], []))

    def test_different_quant_is_separate(self):
        self.assertEqual(nd.check([row('a', 'https://x.com/s/status/1'), row('b', 'https://x.com/s/status/2', quant='Q8_0')]), ([], []))

    def test_dataset_has_no_near_dupes(self):
        with open(R/'data/recipes.json', encoding='utf-8') as f: errors, _ = nd.check(json.load(f))
        self.assertEqual(errors, [])


if __name__ == '__main__':
    unittest.main()
