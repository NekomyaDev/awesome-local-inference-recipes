"""Dataset-wide field rules from CONTRIBUTING rule 10: Chinese prose fields use 解码 / 预填充 / 智能体, avoid 并发
and never put 。 straight after a URL."""
import json, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R/'scripts'))
import i18n_rules

D = json.load(open(R/'data/recipes.json', encoding='utf-8'))


class ZhProseFields(unittest.TestCase):
    def test_dataset(self):
        bad = [(r['id'], f, p) for r in D for f, p in i18n_rules.zh_field_problems(r)]
        self.assertEqual(bad, [])

    def test_flags(self):
        r = {'source_note': '见 https://github.com/a/b/issues/1。另有 agent 跑法', 'quant': 'Q4（并发投机）',
             'metric': '短对话 30；见 github.com/a/b。'}
        self.assertEqual(sorted(i18n_rules.zh_field_problems(r)),
                         sorted([('source_note', 'URL followed by 。'), ('source_note', 'agent'), ('quant', '并发'), ('metric', 'URL followed by 。')]))

    def test_allowed(self):
        r = {'source_note': 'HF 模型卡; 预填充随上下文下降; 原文: | agent | prefill 4,883 |',
             'metric': '见 https://github.com/a/b/issues/1 。解码 30', 'engine_raw': 'decode kernels',
             'launch_command': 'llama-server --decode 1', 'context': '262K（v0.2.0。）'}
        self.assertEqual(i18n_rules.zh_field_problems(r), [])


if __name__ == '__main__':
    unittest.main()
