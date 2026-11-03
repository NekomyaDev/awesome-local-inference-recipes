import copy, json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import normalize_engines as N, tag_recipes as T
R = os.path.join(os.path.dirname(__file__), '..')
def rec(**k):
    b = dict(id='t-1', category='text', model='X', quant=None, engine='其他/未注明', hardware='RTX 4090',
             context=None, metric=None, source_url='u1')
    b.update(k); return b
class TestNormalize(unittest.TestCase):
    def test_canon(self):
        for raw, c in [('llama.cpp（-np 1 -fa on）', 'llama.cpp'), ('llama.cpp b10434', 'llama.cpp'),
                       ('PrismML llama.cpp fork（Metal）', 'llama.cpp (PrismML fork)'),
                       ('PrismML mlx-swift fork', 'MLX Swift (PrismML fork)'),
                       ('agentionai/llama.cpp fork（Vulkan）', 'llama.cpp (agentionai fork)'),
                       ('MTPLX 2.11.3 serve', 'MTPLX'), ('mlx-lm 0.30.7', 'MLX'), ('Strata v0.1.42', 'Strata'),
                       ('ComfyUI', 'ComfyUI')]:
            self.assertEqual(N.canon(raw), c, raw)
    def test_note_kept_and_idempotent(self):
        d = [rec(engine='llama.cpp（-np 1 -fa on）')]
        N.normalize(d); once = copy.deepcopy(d); N.normalize(d)
        self.assertEqual(d, once)
        self.assertEqual(d[0]['engine'], 'llama.cpp'); self.assertEqual(d[0]['engine_note'], 'llama.cpp（-np 1 -fa on）')
    def test_infer_and_unspecified(self):
        d = [rec(quant='Splash · 4-bit'), rec(quant='Q6'), rec(quant='Halogen Flash server')]
        N.normalize(d)
        self.assertEqual([r['engine'] for r in d], ['Splash', 'Unspecified', 'Halogen'])
        self.assertNotIn('engine_note', d[1])
    def test_same_as_above(self):
        d = [rec(engine='mlx-serve 26.8.11', source_url='a'), rec(engine='同上', source_url='a')]
        N.normalize(d); self.assertEqual(d[1]['engine'], 'mlx-serve')
class TestTags(unittest.TestCase):
    def test_family(self):
        for m, f in [('Qwen-Image 2.1', 'Qwen-Image'), ('Qwen3.8-27B', 'Qwen'), ('FastH3 V2', 'MiniMax H3'),
                     ('RED-SNOW-5.3-FLASH（GLM-5.3-Flash 去拒答版）', 'GLM'), ('Wan2.2', 'Wan'), ('AREX-2', 'Other')]:
            self.assertEqual(T.family(m), f, m)
    def test_tags(self):
        t = T.tags(rec(model='Qwen3.6-35B-A3B', quant='Q4_K_M + MTP', engine='llama.cpp', context='262K', hardware='2× RTX 3090'))
        for x in ('4bit', 'MoE', 'long-context', 'speculative', 'MTP', 'multi-GPU'): self.assertIn(x, t)
        self.assertNotIn('dense', t)
        t = T.tags(rec(model='Qwen3.8-27B', quant='oQ4e（MTP 关）', engine='oMLX', hardware='1× DGX Spark'))
        self.assertEqual(t, ['4bit', 'dense'])
        t = T.tags(rec(category='image', model='Z-Image Turbo', quant='int8 · 25 步', engine='ComfyUI'))
        self.assertEqual(t, ['8bit', 'few-step'])
    def test_gpu_unlock(self):
        t = T.tags(rec(model='Qwen3.8-27B', quant='Q4', engine='vLLM', hardware='4× RTX 3090 24GB（gpu-unlock 解锁 fp32 累加）'))
        self.assertIn('gpu-unlock', t)
        t = T.tags(rec(model='Qwen3.8-27B', quant='Q4', engine='vLLM', hardware='2× RTX 3080（解除 LHR FP16 限速）'))
        self.assertIn('gpu-unlock', t)
        t = T.tags(rec(model='Qwen3.8-27B', quant='Q4', engine='vLLM', hardware='CMP 170HX（解锁 64GB 矿卡）'))
        self.assertNotIn('gpu-unlock', t)
    def test_bpw_and_bit_suffixes(self):
        t = T.tags(rec(model='DeepSeek-V4.1-Flash', quant='EXL3 3bpw', engine='vLLM'))
        self.assertIn('3bit', t)
        t = T.tags(rec(model='DeepSeek-V4.1-Flash', quant='GPTQ 1.75/2.25/3.44-bit tiers', engine='ds41'))
        self.assertNotIn('4bit', t)
        self.assertNotIn('3bit', T.tags(rec(model='GLM-5.3-Flash', quant='EXL3 2.3bpw', engine='vLLM')))
        self.assertNotIn('3bit', T.tags(rec(model='GLM-5.3-Flash', quant='2.3-bit mix', engine='vLLM')))
        self.assertNotIn('3bit', T.tags(rec(model='GLM-5.3-Flash', quant='EXL3 bpw 2.9', engine='vLLM')))
    def test_mtp_not_multi_gpu(self):
        t = T.tags(rec(model='Qwen3.8-Flash-Next', quant='NVFP4 + MTP2', engine='vLLM', hardware='RTX PRO 6000 Blackwell 96GB'))
        self.assertNotIn('multi-GPU', t)
        self.assertIn('MTP', t)
        t = T.tags(rec(model='Qwen3.8-Flash-Next', quant='官方 NVFP4 · TP=2', engine='capy-flash', hardware='2× RTX 5070 Ti 16GB'))
        self.assertIn('multi-GPU', t)
    def test_no_dense_on_image(self):
        self.assertNotIn('dense', T.tags(rec(category='image', model='Qwen-Image 2.1（7B）', engine='ComfyUI')))
    def test_data_is_up_to_date(self):
        d = json.load(open(os.path.join(R, 'data/recipes.json')))
        x = copy.deepcopy(d); T.apply(N.normalize(x)); self.assertEqual(x, d)
if __name__ == '__main__': unittest.main()
