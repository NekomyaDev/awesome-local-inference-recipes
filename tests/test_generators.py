import re, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
import gen_readme, gen_site, gen_recipe_pages, hardware_index
from dataset_constants import BUDGET_TIER_BOUNDS_USD


class EnglishFilter(unittest.TestCase):
    def test_readme_treats_curly_quotes_as_cjk(self):
        self.assertEqual(gen_readme.en('Mac Studio “M4 128G”（帖文原话）'), 'Mac Studio')

    def test_site_keeps_curly_quoted_latin_words(self):
        self.assertEqual(gen_site.en('Mac Studio “M4 128G”（帖文原话）'), 'Mac Studio “M4 128G”')

    def test_site_splits_full_width_separators_before_filtering(self):
        self.assertEqual(gen_site.normalize_punct('a；b，c'), 'a; b, c')
        self.assertEqual(gen_site.en('RTX 4090；单卡'), 'RTX 4090')

    def test_site_falls_back_to_original_when_nothing_is_left(self):
        self.assertEqual(gen_site.en('二手显卡'), '二手显卡')

    def test_recipe_pages_returns_none_when_nothing_is_left(self):
        self.assertIsNone(gen_recipe_pages.en('二手显卡'))
        self.assertIsNone(gen_recipe_pages.en(''))


class BudgetTiers(unittest.TestCase):
    def test_every_language_has_one_label_per_bound(self):
        for lang, t in gen_readme.L.items():
            self.assertEqual(len(t['tiers']), len(BUDGET_TIER_BOUNDS_USD), lang)
            self.assertEqual(len(t['tdesc']), len(BUDGET_TIER_BOUNDS_USD), lang)

    def test_cjk_labels_name_their_bounds(self):
        for lang in ('zh', 'ja'):
            for label, (lo, hi) in zip(gen_readme.L[lang]['tiers'], BUDGET_TIER_BOUNDS_USD):
                self.assertIn(f'{hi:,}', label, lang)
                if lo: self.assertIn(f'{lo:,}', label, lang)

    def test_budget_question_names_the_first_bound(self):
        cap = BUDGET_TIER_BOUNDS_USD[0][1]
        for lang, t in gen_readme.QAT.items():
            self.assertIn(str(cap), t['q']['b25'].replace(',', ''), lang)

    def test_english_labels_name_their_bounds(self):
        for label, (lo, hi) in zip(gen_readme.L['en']['tiers'], BUDGET_TIER_BOUNDS_USD):
            self.assertIn(f'{hi/1000:g}k', label)
            if lo: self.assertIn(f'${lo/1000:g}k', label)


MULTI_DEVICE_SAMPLES = {'5090': '2× RTX 5090 32GB', '4090': '双 RTX 4090', '3090': '4x RTX 3090', 'm3u': '2 台 Mac Studio M3 Ultra',
                        'spark': '2× DGX Spark', 'strix': 'Strix Halo / RTX 4090'}
SINGLE_DEVICE_SAMPLES = {'5090': '1× RTX 5090 32GB', '4090': '单 RTX 4090', '3090': 'RTX 3090 24GB', 'm3u': 'Mac Studio M3 Ultra 512GB',
                         'spark': '1× DGX Spark（GB10）', 'strix': 'AMD Ryzen AI Max+ 395'}
MOBILE_SAMPLES = ['RTX 5090 Laptop', 'Apple M5 Max 128GB（机型未注明）', 'RTX 5090 Laptop GPU（5090M）', '笔记本 RTX 5070 Ti 12GB', 'MacBook Pro M5 Max 128GB', 'iPad Pro 11 英寸 M4 16GB',
                  'Radeon 8060S（Ryzen AI Max+ 395，ASUS ROG Flow Z13 @80W，64GB UMA）', 'Strix Halo laptop (gfx1151, 128GB)', 'iPhone 17 Pro Max (A19 Pro)']
MIXED_SAMPLES = ['Strix Halo + R9700', 'Mac Studio M4 Max+RTX 5090', 'Minisforum MS-S1 MAX（Ryzen AI Max+ 395，128GB）+ Radeon AI PRO R9700 32GB', 'RTX 5060 Ti 16GB（Thunderbolt 外接）+ MacBook Pro M1 Max（Linux）', '1× RTX 7900 XTX 24GB + Ryzen AI Max+ 395 + 128GB RAM']
SINGLE_WITH_HOST_SAMPLES = ['RTX 5090 32GB + Core Ultra 9 285K + 247GB DDR5', 'Radeon 8060S（Ryzen AI Max+ 395，Vulkan）', '1× DGX Spark（GB10）',
                            'Geekom A9 Mega（Ryzen AI Max+ 395，128GB LPDDR5X）', '1× Radeon AI PRO R9700 32GB + Ryzen 7 7800X3D + 128GB DDR5']


def qa_row(hw): return dict(hardware=hw, tags=[], metric='', concurrency=None)


class QuickAnswerHardware(unittest.TestCase):
    def test_every_key_has_samples_and_a_page(self):
        keys = sorted(k for k, _ in gen_readme.QA_HARDWARE)
        self.assertEqual(keys, sorted(MULTI_DEVICE_SAMPLES)); self.assertEqual(keys, sorted(SINGLE_DEVICE_SAMPLES))
        for _, slug in gen_readme.QA_HARDWARE: self.assertIn(slug, hardware_index.BY_SLUG)

    def test_single_device_rows_are_answered(self):
        for key, slug in gen_readme.QA_HARDWARE:
            hw = SINGLE_DEVICE_SAMPLES[key]
            self.assertTrue(re.search(hardware_index.BY_SLUG[slug].pattern, hw) and hardware_index.single(qa_row(hw)), key)

    def test_multi_device_rows_are_excluded(self):
        for key, slug in gen_readme.QA_HARDWARE:
            self.assertFalse(hardware_index.single(qa_row(MULTI_DEVICE_SAMPLES[key])), key)

    def test_multi_gpu_tag_excludes_the_row(self):
        self.assertFalse(hardware_index.single(dict(qa_row('RTX 5090'), tags=['multi-GPU'])))

    def test_laptops_tablets_and_phones_are_excluded(self):
        for hw in MOBILE_SAMPLES: self.assertFalse(hardware_index.single(qa_row(hw)), hw)

    def test_mixed_rigs_are_excluded_but_a_host_cpu_is_not(self):
        for hw in MIXED_SAMPLES: self.assertFalse(hardware_index.single(qa_row(hw)), hw)
        for hw in SINGLE_WITH_HOST_SAMPLES: self.assertTrue(hardware_index.single(qa_row(hw)), hw)

    def test_quick_answer_equals_the_chip_fastest(self):
        for key, slug in gen_readme.QA_HARDWARE:
            rows = gen_readme.qa_rows(slug)
            best = max([r for r in rows if hardware_index.meas_text(r)], key=lambda r: (r['tok_s'], r['id']), default=None)
            chip = hardware_index.fastest_on_page(gen_readme.D, slug)
            self.assertEqual(best and best['id'], chip and chip['id'], key)

    def test_readme_quick_answers_show_the_chip_fastest(self):
        for key, slug in gen_readme.QA_HARDWARE:
            b = hardware_index.fastest_on_page(gen_readme.D, slug)
            if not b: continue
            for f in ('README.md', 'README.zh-CN.md', 'README.ja.md'):
                s = (R / f).read_text(encoding='utf-8')
                self.assertIn(f"**{b['tok_s']:g} tok/s**", s.split(gen_readme.QAT[{'README.md': 'en', 'README.zh-CN.md': 'zh', 'README.ja.md': 'ja'}[f]]['q'][key], 1)[1].split('\n\n', 1)[0], (f, key))


class HardwarePages(unittest.TestCase):
    # The explorer's ?q= is one substring. Strix Halo rows name the chip three ways (Strix Halo / Ryzen AI Max+ 395 /
    # Radeon 8060S) and no single substring covers them, so the page lists more rows than its explorer link finds.
    KNOWN_PARTIAL_EXPLORER_QUERY = {'amd-radeon', 'strix-halo'}

    def test_explorer_query_finds_every_row_the_page_lists(self):
        for page in gen_site.HW:
            missed = [r['id'] for r in gen_site.D if re.search(page.pattern, r['hardware']) and page.explorer_query not in r['hardware']]
            if page.slug in self.KNOWN_PARTIAL_EXPLORER_QUERY:
                self.assertTrue(missed, f'{page.slug} is fixed; drop it from KNOWN_PARTIAL_EXPLORER_QUERY')
            else:
                self.assertEqual(missed, [], page.slug)


class RecipePageDownloads(unittest.TestCase):
    ROW = {'id': 'x', 'category': 'text', 'model': 'M', 'engine': 'Strata (Strata-DS fork)', 'hardware': 'H',
           'hardware_family': 'DGX Spark', 'source_url': 'https://github.com/a/b/blob/main/docs/R.md', 'source_level': '实测',
           'model_family': 'DeepSeek', 'tags': []}

    def test_downloads_are_listed_in_every_language(self):
        row = dict(self.ROW, downloads=['https://huggingface.co/org/quant', 'https://huggingface.co/org/base'])
        for lang in ('en', 'zh', 'ja'):
            page = gen_recipe_pages.page(row, lang)
            self.assertIn('[huggingface.co/org/quant](https://huggingface.co/org/quant)', page, lang)
            self.assertIn('[huggingface.co/org/base](https://huggingface.co/org/base)', page, lang)

    def test_a_fork_links_its_own_repository(self):
        page = gen_recipe_pages.page(dict(self.ROW), 'en')
        self.assertIn('https://github.com/Jackwwg83/Strata-DS', page)
        self.assertNotIn('Niko1221/Strata', page)

    def test_without_downloads_a_hugging_face_source_is_linked(self):
        row = dict(self.ROW, source_url='https://huggingface.co/org/model')
        self.assertIn('[huggingface.co/org/model](https://huggingface.co/org/model)', gen_recipe_pages.page(row, 'en'))

    def test_download_pattern_rejects_unsafe_links(self):
        import json
        pat = re.compile(json.loads((R / 'schema/recipe.schema.json').read_text())['properties']['downloads']['items']['pattern'])
        self.assertTrue(pat.match('https://huggingface.co/org/quant'))
        for bad in ('http://huggingface.co/org/quant', 'javascript:alert(1)', 'https://x](javascript:alert(1))', 'https://a b'):
            self.assertIsNone(pat.match(bad), bad)


if __name__ == '__main__': unittest.main()
