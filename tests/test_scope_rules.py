import json, os, re, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import scope_rules as S
from scope_text import SCOPE
R = os.path.join(os.path.dirname(__file__), '..')

def row(hardware, usd=None, cost_text=None):
    return {'hardware': hardware, 'hardware_cost_usd': usd, 'hardware_cost_text': cost_text}


def read(path):
    with open(os.path.join(R, path), encoding='utf-8') as f: return f.read()


class DeviceCount(unittest.TestCase):
    def test_counts(self):
        for hw, n in [('RTX 5090 32GB', 1), ('2× RTX 3090 + 64GB DDR5', 2), ('4× DGX Spark + RTX 5090', 5),
                      ('Threadripper PRO 9955WX + 128GB + 4× Radeon AI PRO R9700', 4), ('6× RTX 3090 + 7950X', 6),
                      ('RTX 5090 vs 1× DGX Spark', 1), ('1× / 2× DGX Spark', 2), ('8x H100', 8),
                      ('4× DGX Spark（有/无交换机均可）', 4), ('M4 Mac mini 16GB + RTX 3090 + iGPU', 2),
                      ('5× Strix Halo', 5), ('5× ASUS Ascent GX10', 5), ('8× P40', 8), ('M3 Ultra 512GB', 1)]:
            self.assertEqual(S.device_count(hw), n, hw)

    def test_multiplier_forms(self):
        for hw, n in [('RTX 3090 ×5', 5), ('RTX 3090 x5', 5), ('4x4090', 4), ('4xRTX 3090', 4), ('8 卡 4090', 8),
                      ('HP Z8（6× RTX A6000）', 6), ('1× DGX Spark（对照 4090）', 1), ('5× 4090显卡', 5), ('6×3090卡', 6),
                      ('4 GPUs', 4), ('4× B580', 4), ('P102-100 ×6', 6), ('2× 7900XTX', 2),
                      ('3× 9070XT', 3), ('2× 4090D', 2), ('6× 3090s', 6), ('2× 4060Tis', 2), ('2× 7900XTXs', 2), ('4× P40s', 4), ('2× A6000s', 2),
                      ('2× B570s', 2)]:
            self.assertEqual(S.device_count(hw), n, hw)

    def test_model_numbers_and_lanes_are_not_multipliers(self):
        for hw in ('AMD RX 7900 XTX 24GB', 'AMD RX 9070 XT 16GB', 'RX 7900 XTX + Ryzen 9 9950X（PCIe 4.0 x16）',
                   'RTX 3090 PCIe 4.0 x16', 'i9-10900K + RTX 3090', 'RTX 5080 16GB（外置 M.2×2 RAID0 SSD）',
                   'RTX 5090 卡', 'RTX 3090 Gen4 x16', 'RTX 3090 @ x8', '7800X3D + B650 + RTX 4070', 'H610 + A620 + RTX 4060',
                   'ASUS Dual RTX 4060 Ti', 'Dual-slot RTX 4090', 'Dual Xeon workstation with RTX A6000',
                   'A520 + RTX 3060', 'A320 + RTX 3060', 'Dual 2690 v4 workstation with RTX 3090'):
            self.assertEqual(S.device_count(hw), 1, hw)


class Violations(unittest.TestCase):
    def test_each_condition(self):
        self.assertEqual(S.violations(row('RTX 5090', 5400)), [])
        self.assertEqual(S.violations(row('4× DGX Spark', 27800)), [])
        self.assertEqual(S.violations(row('5× RTX 3090')), [])  # GPU count has no hard cap; budget is the main limit
        self.assertEqual(S.violations(row('2 台各 4× RTX 3060')), [])
        self.assertIn('cost over $30,000', S.violations(row('2× RTX PRO 6000', 32000)))
        self.assertIn('cost over $30,000', S.violations(row('2× RTX PRO 6000', None, '≈$33,000 ⚠️超$30k')))
        self.assertTrue(S.violations(row('4× V100 SXM2')))
        self.assertTrue(S.violations(row('RTX 5090（液冷）')))
        self.assertTrue(S.violations(row('4U server + 2× RTX 3090')))
        self.assertEqual(S.OVER_BUDGET_MARK, '⚠️超$30k')

    def test_every_recipe_is_in_scope(self):
        D = json.loads(read('data/recipes.json'))
        self.assertEqual({r['id']: v for r in D if (v := S.violations(r))}, {})

    def test_sxm2_to_pcie_adapter_builds_are_allowed(self):
        for hw in ('2× Tesla V100 SXM2 + SXM2-to-PCIe adapter', '2× V100 SXM2 转 PCIe 转接卡 + 64GB RAM', 'V100 SXM2 adapter in a desktop', '2× V100 SXM2-PCIe adapter', '4× V100 SXM2-to-PCIe adapter + EPYC 7543 server motherboard'):
            self.assertEqual(S.violations(row(hw)), [], hw)
        for hw in ('4× V100 SXM2 server board', '4× V100 SXM2 server board + SXM2-to-PCIe adapter', '2× A100 SXM4 转 PCIe 转接卡', '4× H100 SXM5 to PCIe', '4× V100 SXM2 server motherboard + SXM2 adapter', '4× V100 SXM2 baseboard + SXM2 adapter', '4× V100 SXM2 サーバー用マザーボード + SXM2 変換', '4× V100 SXM2 + SXM2 adapter + NVLink baseboard'):
            self.assertTrue(S.violations(row(hw)), hw)

    def test_server_motherboard_in_a_tower_is_allowed(self):
        for hw in ('4× RTX 3090 + EPYC 7543 server motherboard', '4× RTX 3090 + Xeon W serverboard', '2× RTX 3090 + ASRock Rack ROMED8-2T', '2× RTX 3090 + ASRock-Rack ROMED8-2T'):
            self.assertEqual(S.violations(row(hw)), [], hw)

    def test_factory_aio_consumer_cards_are_allowed(self):
        for hw in ('RTX 5090 Suprim Liquid（AIO liquid cooled）', 'RTX 4090（出厂一体式水冷）', 'RTX 5090 factory AIO', 'RTX 4090（簡易水冷）', 'RTX 4090（一体水冷）', 'RTX 5090（一体式液冷）', 'RTX 4090 liquid-cooled (AIO)', 'RTX 4090（AIO 水冷）', 'RTX 4090 AIO水冷', 'RTX 5090 水冷（AIO）', 'RTX 5090 AIO 360mm liquid cooled', 'RTX 4090 all in one liquid cooler', 'RTX 4090 + AIO CPU cooler', 'RTX 4090 + 360mm AIO liquid cooler', 'RTX 4090 + Corsair H150i (AIO liquid cooler)', '4090 AIO liquid cooled', 'RTX 4090 一體式水冷', 'RTX 4090 + ASUS H770-PLUS (360mm AIO liquid cooler)', 'Arc A770 AIO liquid cooled', '4× A100 + AIO water cooling', 'RTX 4090 AIO liquid-cooled home server', 'RTX 4090 家用服务器 一体式水冷', 'RTX 4090 + EPYC server motherboard with 360mm AIO liquid cooler', 'RTX 4090 + A620 board, 240mm AIO liquid cooler'):
            self.assertEqual(S.violations(row(hw)), [], hw)
        for hw in ('2× RTX 3090 custom loop', 'RTX 4090（分体式水冷）', '4× A100 liquid cooled', '4× A100 liquid cooled + AIO CPU cooler', 'H100 NVL liquid-cooled all-in-one server', '2× RTX 3090 water block', '2× RTX 3090 hardline loop', '4× A100 AIO liquid-cooled', 'H100 all-in-one liquid cooled server', '2× Radeon Instinct MI50 AIO liquid cooled', 'RTX A6000 AIO liquid cooled', 'RTX PRO 6000 Server Edition AIO liquid cooled', 'RTX 6000 Ada AIO liquid cooled', 'RTX A4500 AIO liquid cooled', '2× RTX A6000s AIO liquid cooled', 'RTX PRO 4500 AIO liquid cooled', 'RTX 4090 服务器 一体式水冷', 'RTX 4090 サーバー 簡易水冷', 'Radeon AI PRO R9700 AIO liquid cooled', 'Radeon Pro W7900 AIO liquid cooled', '4× A100 + all-in-one liquid cooled server', '4× A100 watercooled', '2× RTX 3090 custom watercooling loop', '2× RTX 3090 非一体式水冷'):
            self.assertTrue(S.violations(row(hw)), hw)


class RuleText(unittest.TestCase):
    def test_contributing_and_submit_page_carry_the_readme_rule(self):
        contributing = read('CONTRIBUTING.md')
        page, script = read('submit.html').split('<script src="i18n.js">')
        blocks = dict(zip(('zh', 'en', 'ja'), re.split(r"\n(?:'zh-CN'|en|ja):\{", script)[1:]))
        for lang, s in SCOPE.items():
            for sentence in s['intro'] + [s['lead']] + s['items'] + s['outro']:
                html = re.sub(r'`([^`]*)`', r'<code>\1</code>', sentence)
                self.assertIn(sentence, contributing, lang)
                self.assertIn(html, blocks[lang], lang)
                if lang == 'en': self.assertIn(html, page)


if __name__ == '__main__': unittest.main()
