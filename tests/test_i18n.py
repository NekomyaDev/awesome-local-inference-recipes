import unittest
import json, re, subprocess, sys, unittest
from pathlib import Path
R = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(R / 'scripts'))
import hardware_index
CJK = re.compile(r'[\u3000-\u303f\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]+')
LANG_NAMES = {'中文', '简体中文', '日本語'}
DATA_ENUMS = {'官方', '实测', '转述', '宣称', 'NVIDIA 消费级', '消费级', '二手数据中心卡', '其他'}
SIMPLIFIED_ONLY = set('这们说时实为对务从无与样产发进过还经开关见让认请读选显传标单张门问间题须记设试详语论谁调质运连适钟错长阅难页顺预领风飞马验级络统维缓据')
EN_FIELDS = ['engine', 'model_family', 'quant', 'model', 'hardware', 'context', 'concurrency', 'engine_note', 'hardware_cost_text', 'source_note', 'launch_command', 'metric']

def visible(html):
    html = re.sub(r'<(script|style)\b.*?</\1>', '', html, flags=re.S)
    attrs = ' '.join(re.findall(r'(?:title|aria-label|placeholder|alt|content)="([^"]*)"', html))
    return re.sub(r'<[^>]+>', ' ', html) + ' ' + attrs

def node(js):
    return json.loads(subprocess.run(['node', '-e', "global.window=global;require('./cost.js');const D=require('./data/recipes.json');" + js], cwd=R, capture_output=True, text=True, check=True).stdout)

def dict_end(src, i):
    """Index just past the object literal opening at src[i] == '{' (skips quoted strings and template literals)."""
    depth, q, j = 0, None, i
    while j < len(src):
        c = src[j]
        if q:
            if c == '\\': j += 1
            elif c == q: q = None
        elif c in '\'"`': q = c
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if not depth: return j + 1
        j += 1
    return j

def lang_blocks(src):
    """{lang: text of its dictionary object} for every 'zh-CN':{ / en:{ / ja:{ literal (merged per language)."""
    out = {}
    for m in re.finditer(r"(?:^|[\s{,(])'?(zh-CN|en|ja)'?:(?=\{)", src):
        a = m.end(); out[m.group(1)] = out.get(m.group(1), '') + src[a:dict_end(src, a)]
    return out

def keys(block):
    block = re.sub(r"'(?:[^'\\]|\\.)*'|`(?:[^`\\]|\\.)*`", "''", block)
    return set(re.findall(r"[{,]\s*([A-Za-z_]\w*):(?=['`(\[{]|\w+=>|\()", block))

class EnglishHasNoCJK(unittest.TestCase):
    def test_every_rendered_field_in_english_mode(self):
        bad = node("const F=%s;const out=[];for(const r of D){const o=localizeRecipe(r,'en');for(const k of F)if(typeof o[k]=='string'&&/[\\u3000-\\u303f\\u3040-\\u30ff\\u3400-\\u9fff\\uff00-\\uffef]/.test(o[k]))out.push(r.id+' '+k)}process.stdout.write(JSON.stringify(out))" % json.dumps(EN_FIELDS))
        self.assertEqual(bad, [])

    def test_rows_with_chinese_text_carry_curated_english(self):
        for r in json.loads((R/'data/recipes.json').read_text(encoding='utf-8')):
            for k in EN_FIELDS:
                v = r.get(k)
                if isinstance(v, str) and CJK.search(v):
                    en = r.get('metric_en') if k == 'metric' else (r.get('en') or {}).get(k)
                    self.assertTrue(en and not CJK.search(en), f"{r['id']} {k}")

    def test_static_english_pages(self):
        pages = ['index.html', 'explore.html', 'speed.html', 'submit.html'] + [str(p.relative_to(R)) for p in (R/'hw').glob('*.html')] + [str(p.relative_to(R)) for p in (R/'model').glob('*.html')] + [str(p.relative_to(R)) for p in (R/'guides').glob('*.html')]
        for p in pages:
            allow = LANG_NAMES | (DATA_ENUMS if p == 'submit.html' else set())
            left = [h for h in CJK.findall(visible((R/p).read_text(encoding='utf-8'))) if h not in allow]
            self.assertEqual(left, [], p)

    def test_english_ui_dictionaries(self):
        for f in ['i18n.js', 'app.js', 'landing.js', 'site.js', 'submit.html', 'speed.html']:
            en = lang_blocks((R/f).read_text(encoding='utf-8')).get('en', '')
            left = [h for h in CJK.findall(en) if h not in LANG_NAMES | DATA_ENUMS]
            self.assertEqual(left, [], f)

class ChineseAndJapaneseUI(unittest.TestCase):
    def test_every_english_ui_key_has_a_chinese_string(self):
        for f in ['i18n.js', 'app.js', 'landing.js', 'submit.html', 'speed.html']:
            b = lang_blocks((R/f).read_text(encoding='utf-8'))
            self.assertEqual(keys(b['en']) - keys(b['zh-CN']), set(), f)
        b = lang_blocks((R/'speed.html').read_text(encoding='utf-8'))
        self.assertEqual(keys(b['en']) - keys(b['ja']), set(), 'speed.html ja')

    def test_every_english_ui_key_has_a_japanese_string(self):
        for f in ['i18n.js', 'app.js', 'landing.js', 'submit.html', 'speed.html']:
            b = lang_blocks((R/f).read_text(encoding='utf-8'))
            self.assertIn('ja', b, f)
            self.assertEqual(keys(b['en']) - keys(b['ja']), set(), f)

    def test_static_markup_keys_exist_in_chinese(self):
        zh = set()
        for f in ['i18n.js', 'app.js', 'landing.js', 'submit.html']: zh |= keys(lang_blocks((R/f).read_text(encoding='utf-8'))['zh-CN'])
        for p in ['index.html', 'explore.html', 'submit.html']:
            s = (R/p).read_text(encoding='utf-8')
            for k in re.findall(r'data-i18n(?:-ph|-al)?="([^"]+)"', s): self.assertIn(k, zh, f'{p}: {k}')
        sp = keys(lang_blocks((R/'speed.html').read_text(encoding='utf-8'))['zh-CN'])
        for k in re.findall(r'data-(?:t|i18n)="([^"]+)"', (R/'speed.html').read_text(encoding='utf-8')): self.assertIn(k, sp, f'speed.html: {k}')

    def test_static_zh_ja_landing_chrome(self):
        for lang, brand, nav in [('zh-CN', '本地推理配方', '指南'), ('ja', 'ローカル推論レシピ', 'ガイド')]:
            samples = list((R/'hw'/lang).glob('*.html'))[:2] + list((R/'model'/lang).glob('*.html'))[:2]
            self.assertTrue(samples, lang)
            for p in samples:
                s = p.read_text(encoding='utf-8')
                self.assertIn(brand, s, p.name)
                self.assertIn(f'guides/{lang}/index.html', s, p.name)
                self.assertNotIn('Local Inference Recipes</a>', s, p.name)

    def test_static_chinese_and_japanese_guide_chrome(self):
        for lang, brand in [('zh-CN', '本地推理配方'), ('ja', 'ローカル推論レシピ')]:
            for p in (R/'guides'/lang).glob('*.html'):
                s = (R/p).read_text(encoding='utf-8'); self.assertIn(brand, s, p.name); self.assertNotIn('Local Inference Recipes</a>', s, p.name)

    def test_japanese_pages_have_no_simplified_chinese(self):
        pages = [*(R/'guides'/'ja').rglob('*.html'), *(R/'recipes').glob('*.ja.md'), R/'README.ja.md',
                 *(R/'hw'/'ja').glob('*.html'), *(R/'model'/'ja').glob('*.html')]
        self.assertGreater(len(pages), 10)
        for p in pages:
            t = visible(p.read_text(encoding='utf-8')).replace('简体中文', '')
            self.assertEqual(sorted({c for c in t if c in SIMPLIFIED_ONLY}), [], p.name)
        ja = lang_blocks((R/'speed.html').read_text(encoding='utf-8'))['ja']
        self.assertEqual(sorted({c for c in ja if c in SIMPLIFIED_ONLY}), [], 'speed.html ja dictionary')

    def test_placeholder_sets_match_across_langs(self):
        def string_entries(block):
            out = {}
            for m in re.finditer(r"([{,]\s*)([A-Za-z_]\w*)\s*:\s*(['\"])((?:\\.|(?!\3).)*)\3", block):
                out[m.group(2)] = m.group(4)
            return out
        def placeholders(s):
            return sorted(set(re.findall(r'\{[A-Za-z_]+\}', s)))
        for f in ['i18n.js', 'app.js', 'landing.js', 'submit.html', 'speed.html']:
            blocks = {lang: string_entries(text) for lang, text in lang_blocks((R / f).read_text(encoding='utf-8')).items()}
            base = blocks.get('en') or blocks.get('zh-CN')
            self.assertTrue(base, f)
            bad = []
            for lang, d in blocks.items():
                if lang == 'en':
                    continue
                for k, v in base.items():
                    if k not in d:
                        continue
                    a, b = placeholders(v), placeholders(d[k])
                    if a != b:
                        bad.append(f'{lang}.{k}:en{a} vs{b}')
            self.assertEqual(bad, [], f)

    def test_japanese_localize_recipe_has_no_cjk(self):
        bad = node("const out=[];for(const r of D){const o=localizeRecipe(r,'ja');for(const k of %s)if(typeof o[k]=='string'&&/[\u3000-\u303f\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]/.test(o[k].replace(/（英語）$/,'')))out.push(r.id+' '+k)}process.stdout.write(JSON.stringify(out))" % json.dumps(EN_FIELDS))
        self.assertEqual(bad, [])

    def test_japanese_localize_recipe_marks_english_metric(self):
        # The only CJK allowed in JA data text is the trailing （英語） label on English source text.
        out = node("const r=D.find(r=>r.metric_en&&/\\b[a-z]{4,}\\b/.test(r.metric_en));process.stdout.write(JSON.stringify([localizeRecipe(r,'ja').metric,localizeRecipe(r,'en').metric,r.metric_en]))")
        self.assertEqual(out[0], out[2] + '（英語）')
        self.assertEqual(out[1], out[2])

class SpeedPage(unittest.TestCase):
    def setUp(self): self.s = (R/'speed.html').read_text(encoding='utf-8')

    def test_lanes_are_sorted_ascending_after_every_relabel(self):
        label = re.search(r'function label\(\)\{.*?\n  sortLanes\(\)\}', self.s, re.S)
        self.assertIsNotNone(label, 'label() must re-sort the lanes after updating rates')
        page = ''.join(re.search(p, self.s, re.S).group(0) for p in (r'const SMIN=.*?;\n', r'const rateOf=.*?;\n', r'const laneOrder=.*?;\n'))
        for custom in (3, 35, 50, 800):
            js = "const _cr={value:String(%d)};const $=()=>_cr;" % 0 + page + "_cr.value=String(r2sl(%d));" % custom + "process.stdout.write(JSON.stringify(laneOrder([5,10,20,50,100,200,500,'c'].map(r=>({r}))).map(L=>[rateOf(L),L.r==='c'])))"
            order = json.loads(subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout)
            rates = [x for x, _ in order]
            self.assertEqual(rates, sorted(rates), custom)
            cus = [x for x, c in order if c]
            self.assertEqual(len(cus), 1); self.assertLess(abs(cus[0] / custom - 1), 0.01, custom)
            ties = [i for i, (x, c) in enumerate(order) if x == cus[0]]
            self.assertTrue(order[ties[-1]][1], 'custom lane goes after a fixed lane of the same rate')

    def test_embed_tiers_are_the_fixed_ascending_set(self):
        self.assertIn("const RATES=EMBED?[10,20,50,100,200,500]:[5,10,20,50,100,200,500]", self.s)
        self.assertIn("for(const r of EMBED?RATES:[...RATES,'c'])", self.s)

    def test_local_picks_use_the_python_aggregate_pattern(self):
        js = re.search(r"!/(.*?)/i\.test\(\(r\.metric", self.s).group(1)
        self.assertEqual(js.replace('\\/', '/'), hardware_index.AGG_TEXT)

    def test_local_picks_are_measured_single_stream_and_localized(self):
        fn = re.search(r'function localPicks\(rc,lang\)\{.*?\n', self.s).group(0)
        for lang in ('en', 'ja'):
            picks = node(fn + f"process.stdout.write(JSON.stringify(localPicks(D,'{lang}').map(r=>[r.id,r.source_level,r.hardware,r.model,r.metric,r.concurrency||''])))")
            src = {r['id']: r for r in json.loads((R/'data/recipes.json').read_text(encoding='utf-8'))}
            for i, lv, hw, model, met, conc in picks:
                self.assertEqual(src[i]['source_level'], '实测', i)
                self.assertFalse(src[i].get('superseded_by'), i)
                self.assertNotRegex((src[i].get('metric') or '') + ' ' + str(src[i].get('concurrency') or ''), hardware_index.AGG_TEXT + '|自称', i)
                self.assertIsNone(CJK.search(hw + ' ' + model), f'{lang} {i}')


class ExploreGuideLink(unittest.TestCase):
    def test_guide_href_uses_active_lang(self):
        src = (R / 'app.js').read_text(encoding='utf-8')
        self.assertIn("${LANG=='en'?'':'.'+LANG}.md", src)
        self.assertNotIn("${LANG=='zh-CN'?'.zh-CN':''}.md", src)


class GuideLocales(unittest.TestCase):
    def test_every_guide_has_three_langs(self):
        import json
        ids = json.loads((R / 'data/guides.json').read_text(encoding='utf-8'))
        for gid in ids:
            for suf in ('', '.zh-CN', '.ja'):
                self.assertTrue((R / 'recipes' / f'{gid}{suf}.md').is_file(), f'missing recipes/{gid}{suf}.md')

if __name__ == '__main__': unittest.main()
