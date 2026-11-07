import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import normalize_engines as N, tag_recipes as T
def rec(**k):
    b = dict(id='t-1', category='text', model='X', quant=None, engine='llama.cpp', hardware='RTX 4090',
             context=None, metric=None, source_url='u1')
    b.update(k); return b
class TestForkAndTags(unittest.TestCase):
    def test_fork_names_kept(self):
        for raw, c in [('llama.cpp (vahpetr fork)', 'llama.cpp (vahpetr fork)'),
                       ('llama.cpp s1-fork + MTP', 'llama.cpp (vahpetr fork)'),
                       ('llama.cpp-omni + LES', 'llama.cpp (OpenBMB fork)'),
                       ('llama.cpp (PrismML fork)', 'llama.cpp (PrismML fork)')]:
            self.assertEqual(N.canon(raw), c, raw)
    def test_no_draft_is_not_speculative(self):
        self.assertNotIn('speculative', T.tags(rec(metric='68 tok/s（无草稿模型）')))
        self.assertNotIn('speculative', T.tags(rec(quant='oMLX（无 MTP/DFlash）')))
        self.assertIn('speculative', T.tags(rec(metric='MTP 头 50 tok/s（无草稿 39）')))
    def test_offload_from_hardware_and_metric(self):
        self.assertIn('offload', T.tags(rec(hardware='RTX 5090 32GB + 系统内存（部分卸载）')))
        self.assertIn('offload', T.tags(rec(metric='超过一半模型从 NVMe 流式读取')))
        self.assertNotIn('offload', T.tags(rec(metric='29 tok/s（SSD 前缀缓存 ~85%）')))
    def test_qualification_note_does_not_add_speculative(self):
        # Regression caveats that mention DFlash2/MTP about other builds must not tag this row.
        metric = (
            'engine 0.1.55 hip-rdna2：短提示 decode 49.0；'
            '限定：Strata 0.2.10 起 Auto 默认改用 DFlash2；双卡 decode 可能弱于 MTP'
        )
        self.assertNotIn('speculative', T.tags(rec(metric=metric, quant='IQ3_XXS')))
        self.assertNotIn('MTP', T.tags(rec(metric=metric, quant='IQ3_XXS')))
    def test_own_mtp_before_qualification_still_tags(self):
        metric = (
            'Strata 0.1.48.1，--spec 4 --mtp rt：短对话 117.5；'
            '限定：Strata 0.2.10 起 Auto 默认改用 DFlash2；双卡 decode 可能弱于 MTP'
        )
        self.assertIn('speculative', T.tags(rec(metric=metric, quant='unsloth UD-IQ4_XS')))
        self.assertIn('MTP', T.tags(rec(metric=metric, quant='unsloth UD-IQ4_XS')))
if __name__ == '__main__': unittest.main()
