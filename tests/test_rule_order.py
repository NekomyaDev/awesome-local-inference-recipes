import os, re, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
import normalize_engines as N, tag_recipes as T


RAW_ENGINE_SAMPLES = {
    'llama.cpp (vahpetr fork)': 'vahpetr llama.cpp s1-fork',
    'llama.cpp (OpenBMB fork)': 'llama.cpp-omni b123',
    'MLX Swift (PrismML fork)': 'PrismML mlx-swift fork',
    'llama.cpp (PrismML fork)': 'PrismML llama.cpp fork（Metal）',
    'llama.cpp (agentionai fork)': 'agentionai/llama.cpp fork',
    'llama.cpp (mirai-s fork)': 'llama.cpp-mirai-s build 7',
    'llama.cpp': 'llama.cpp b10434',
    'strata-mlx': 'strata-mlx 0.4.1',
    'Strata (Strata-DS fork)': 'Strata-DS（Strata 分支，自带 DeepSeek 引擎 ds41_serve）',
    'Strata (Strata-rdna3 fork)': 'Strata-rdna3（7900 XTX fork）',
    'Strata': 'Strata v0.1.42',
    'Foundry Local': 'Foundry Local ≥0.13.0',
    'WHIRL': 'WHIRL 0.2.5.1 balance',
    'oMLX': 'oMLX 0.3', 'TensorFold': 'TensorFold beta', 'DFlash': 'DFlash spec', 'MTPLX': 'MTPLX 2.11.3 serve',
    'mlx-serve': 'mlx-serve 26.8.11', 'MLX Swift': 'MLX Swift 0.21', 'MLX': 'mlx-lm 0.30.7', 'edge0': 'edge0 runtime',
    'SGLang': 'SGLang 0.5', 'vLLM': 'vLLM 0.11', 'Splash': 'Splash 1.2', 'Project Maya': 'Project Maya alpha',
    'Halogen': 'halogen flash server', 'Osaurus': 'Osaurus 1.0', 'ExLlama': 'ExLlamaV3',
    'Infernix': 'Infernix windows-2026.10.11', 'ds41': 'ds41 Rust + CUDA',
    'TandemLLM': 'TandemLLM 0.13.0 MTP', 'Geezuz': 'Geezuz kernel TP2',
    'MoEShift': 'MoEShift（未开源）', 'ik_llama.cpp (Mcniiby fork)': 'ik_llama.cpp（Mcniiby/ik_llama.cpp-raon 分支）',
    'Espetero': 'Espetero 0.1.2', 'Paiton': 'Paiton（vLLM 插件）',
    'Halowin Bubo': 'Halowin Bubo（Gufo 分支）', 'Janas-LLM': 'Janas-LLM（纯 C）', 'Strim': 'Strim（Swift + MLX）', 'Magnitude': 'Magnitude',
    'QEngine': 'QEngine 1.3.1（自编 sm_120）', 'PXA': 'PXA 4.0（llama.cpp 分支）', 'Betelgeuse': 'Betelgeuse（llama.cpp 分支）',
    'SGLang (Penny Royal fork)': 'Penny Royal 3.1.4（SGLang 分支）', 'llama.cpp (tandem.cpp fork)': 'tandem.cpp（llama.cpp 补丁集）', 'Speedy': 'Speedy（Strata 衍生）',
    'RustingStrata': 'RustingStrata（纯 Rust）', 'libosmos': 'libosmos 0.1', 'JITEngine': 'JITEngine SSD offload',
    'Front_Eagle739 streaming stack': 'Front_Eagle739 streaming stack（作者自研）', 'Unspecified': '未注明（EXL3 权重）',
}


class EngineRuleOrder(unittest.TestCase):
    def test_every_rule_has_a_raw_sample(self):
        self.assertEqual(sorted(c for _, c in N.RULES if c is not None), sorted(RAW_ENGINE_SAMPLES))

    def test_each_raw_sample_reaches_its_own_rule(self):
        for canonical, raw in RAW_ENGINE_SAMPLES.items():
            self.assertEqual(N.canon(raw), canonical, f'an earlier rule shadows {canonical!r} for {raw!r}')

    def test_no_earlier_rule_matches_a_later_rules_sample(self):
        index = {c: i for i, (_, c) in enumerate(N.RULES)}
        for canonical, raw in RAW_ENGINE_SAMPLES.items():
            earlier = [c for p, c in N.RULES[:index[canonical]] if re.search(p, raw, re.I)]
            self.assertEqual(earlier, [], f'{raw!r} is captured before reaching {canonical!r}')

    def test_strata_mlx_is_not_swallowed_by_strata(self):
        self.assertEqual(N.canon('STRATA-MLX'), 'strata-mlx')

    def test_ds41_rule_leaves_ds41rt_alone(self):
        self.assertEqual(N.canon('DS41RT'), 'DS41RT')

    def test_ds41rt_row_is_inferred_from_quant(self):
        row = {'engine': '其他/未注明', 'quant': 'DS41RT 2-bit', 'source_url': 'https://example.com/ds41rt'}
        self.assertEqual(N.normalize([row])[0]['engine'], 'DS41RT')

    def test_canonical_fork_names_are_kept_verbatim(self):
        self.assertEqual(N.canon('llama.cpp (Radiance fork)'), 'llama.cpp (Radiance fork)')


class FamilyRuleOrder(unittest.TestCase):
    def test_specific_families_win_over_generic_ones(self):
        for model, family in [('Qwen-Image 2.1', 'Qwen-Image'), ('Qwen-Image-Edit', 'Qwen-Image'), ('Qwen3.8-27B', 'Qwen'),
                              ('FastH3 V2', 'MiniMax H3'), ('MiniMax H3', 'MiniMax H3'), ('Z-Image Turbo', 'Z-Image')]:
            self.assertEqual(T.family(model), family, model)

    def test_every_family_name_maps_to_itself(self):
        for pattern, family in T.FAMILIES:
            if not re.search(pattern, family, re.I):
                continue
            self.assertEqual(T.family(family), family, f'an earlier rule shadows {family!r}')

    def test_wan_requires_version(self):
        self.assertEqual(T.family('Wan2.2'), 'Wan')
        self.assertEqual(T.family('Wan'), 'Other')


if __name__ == '__main__': unittest.main()
