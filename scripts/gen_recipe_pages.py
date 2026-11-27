#!/usr/bin/env python3
"""Generate how-to guide pages (recipes/<id>.md, .zh-CN.md, .ja.md) for a curated batch.
Run: python3 scripts/gen_recipe_pages.py"""
import json, re
from pathlib import Path
import gen_readme, ja_text
R = Path(__file__).resolve().parent.parent
D = {r['id']: r for r in json.load(open(R/'data/recipes.json'))}
GUIDES = [
 'hf-ddalcu-qwen3-8-flash-next-mlx-serve-mixed-4-8bit-1','hf-youssofal-qwen3-6-27b-mtplx-optimized-speed-1',
 'hf-prism-ml-ternary-bonsai-2-27b-gguf-5','hf-prism-ml-ternary-bonsai-2-27b-gguf-1','hf-byteshape-qwen3-8-27b-gguf-1',
 'hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1','x-004','text-022','x-001','x-009','x-007','text-018',
 'image-001','video-audio-001','comm-056','comm-057']
ENGINE_URL = {
 'Strata (Strata-DS fork)':'https://github.com/Jackwwg83/Strata-DS',
 'llama.cpp':'https://github.com/ggml-org/llama.cpp','MLX':'https://github.com/ml-explore/mlx-lm','vLLM':'https://github.com/vllm-project/vllm',
 'SGLang':'https://github.com/sgl-project/sglang','ExLlama':'https://github.com/turboderp-org/exllamav3','Strata':'https://github.com/Niko1221/Strata',
 'oMLX':'https://github.com/jundot/omlx','TensorFold':'https://github.com/ashhart/TensorFold','LightX2V':'https://github.com/ModelTC/LightX2V',
 'Halogen':'https://github.com/peonist-ai/halogen-flash-server','ComfyUI':'https://github.com/comfyanonymous/ComfyUI'}
LV = {'官方':('🏛️ Official','🏛️ 官方','🏛️ 公式'),'实测':('✅ Measured','✅ 实测','✅ 実測'),'转述':('🔁 Relayed','🔁 转述','🔁 伝聞'),'宣称':('📣 Claimed','📣 宣称','📣 主張')}
HWF_JA = {'NVIDIA 消费级':'NVIDIA コンシューマー','二手数据中心卡':'中古データセンター GPU','其他':'その他'}
JA = {
 'Source level':'出典レベル','Date':'日付',
 'Numbers come from the source. This repo did not measure them again.':'数値は出典からの引用です。このリポジトリでは再計測していません。',
 'Hardware':'ハードウェア','Reference cost':'参考価格','Model':'モデル','Download':'ダウンロード','Engine':'エンジン',
 'install:':'インストール：','Note':'備考','Launch command':'起動コマンド',
 'Excerpt from the source (includes `...` or placeholders). See the source for full arguments.':'出典からの抜粋です（`...` またはプレースホルダーを含みます）。全引数は出典を参照してください。',
 'Command not published. See the source.':'コマンドは公開されていません。出典を参照してください。',
 'Key parameters':'主なパラメータ','Context':'コンテキスト','Concurrency':'同時実行','Tags':'タグ','Expected speed':'想定速度','Caveats':'注意点',
 'Not a first-hand measurement (claimed or relayed). Your results can differ.':'本人による実測ではありません（主張または伝聞）。実際の速度は異なる場合があります。',
 'Speed changes with drivers, engine version, context length, and prompt length.':'速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。',
 'Source & attribution':'出典とクレジット',
 'Credit to the original author. This page only summarizes and links. Data under CC BY 4.0.':'権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。'}

SUF = {'en':'.md','zh':'.zh-CN.md','ja':'.ja.md'}
def clip_note(s, n=200):
    """Shorten a note to about n characters. Never cut inside a URL; mark a cut with an ellipsis."""
    if len(s) <= n: return s
    for m in re.finditer(r'https?://\S+', s):
        if m.start() < n < m.end(): n = m.start(); break
    return s[:n].rstrip(' （(；;，,') + '…'
def switch(base, cur):
    names = [('en','English'),('zh','简体中文'),('ja','日本語')]
    return ' | '.join(f'**{n}**' if k==cur else f'[{n}]({base}{SUF[k]})' for k,n in names)
HWF = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter GPU','其他':'Other'}
def en(s): return gen_readme.en(s, cjk=gen_readme.CJK_CHAR, strip=' ;,·') if s else None
def hf_repo(r):
    m = re.match(r'https://huggingface\.co/([^/]+/[^/?#]+)', r['source_url'])
    return m.group(1) if m else None
def engine_url(e):
    if not e: return None
    if e in ENGINE_URL: return ENGINE_URL[e]
    for k, u in ENGINE_URL.items():
        if e == k or e.startswith(k+' '): return u
def page(r, lang):
    Z = lang == 'zh'; T = (lambda s: s) if Z else en
    F = lambda k: r.get(k) if Z else ((r.get('en') or {}).get(k) or en(r.get(k)))
    J = gen_readme.mark_ja_en if lang == 'ja' else (lambda s: s)  # JA pages show English data text: label it
    fam = r['hardware_family'] if Z else (HWF_JA if lang=='ja' else HWF).get(r['hardware_family'], r['hardware_family'])
    hw = F('hardware') or (r['hardware'] if Z else fam)  # never fall back to the raw (Chinese) hardware value on EN/JA pages
    lvl = LV.get(r['source_level'], ('','',''))[{'en':0,'zh':1,'ja':2}[lang]]
    na = '未公开。见来源' if Z else ('未公開。出典を参照' if lang=='ja' else 'Not published. See the source.')
    repo = hf_repo(r); eu = engine_url(r.get('engine'))
    if Z: metric = r.get('metric')
    elif lang=='ja':
        metric = ja_text.metric(r) or (f"{r['tok_s']} tok/s（生成）" if r.get('tok_s') else None)
        if ja_text.needs_en_mark(metric): metric = J(metric)
    else: metric = r.get('metric_en') or (f"{r['tok_s']} tok/s (generation)" if r.get('tok_s') else None)
    cmd = r.get('launch_command') if Z else F('launch_command')
    if cmd and cmd.startswith('见'): cmd = None
    other = 'README'+SUF[lang]
    L = []
    L.append(f"# {F('model') or r['model']} · {F('engine') or '—'} · {hw}")
    L.append('')
    L.append(f"{switch(r['id'], lang)} · [← {({'zh':'返回列表','ja':'一覧に戻る'}).get(lang,'All recipes')}](../{other})")
    L.append('')
    h = (lambda zh, e: zh if Z else (JA[e] if lang=='ja' else e))
    L.append(f"> {h('来源等级','Source level')}: **{lvl}** · {h('日期','Date')}: {r.get('date') or '—'} · {h('数字来自来源。本仓库未复测。','Numbers come from the source. This repo did not measure them again.')}")
    L.append('')
    L.append(f"## {h('硬件','Hardware')}\n")
    L.append(f"- {hw} ({fam})")
    cost = r.get('hardware_cost_text') if Z else (f"≈ ${r['hardware_cost_usd']:,}" if r.get('hardware_cost_usd') else None)
    L.append(f"- {h('参考价格','Reference cost')}: {cost or na}\n")
    L.append(f"## {h('模型','Model')}\n")
    L.append(f"- {F('model') or r['model']}" + (f" · `{F('quant')}`" if F('quant') else ''))
    links = list(r.get('downloads') or []) or ([f"https://huggingface.co/{repo}"] if repo else [])
    L.append(f"- {h('下载','Download')}: " + (' · '.join(f"[{u.split('://', 1)[1]}]({u})" for u in links) if links else na) + '\n')
    L.append(f"## {h('引擎','Engine')}\n")
    L.append(f"- {F('engine') or na}" + (f" — {h('安装见','install:')} {eu}" if eu else ''))
    if F('engine_note'): L.append(f"- {h('备注','Note')}: {J(F('engine_note'))}")
    L.append('')
    L.append(f"## {h('启动命令','Launch command')}\n")
    if cmd and T(cmd):
        L.append(f"```bash\n{cmd if Z else T(cmd)}\n```")
        if '...' in cmd or '<' in cmd: L.append(f"\n{h('命令为来源节选（含 `...` 或占位符）。完整参数见来源。','Excerpt from the source (includes `...` or placeholders). See the source for full arguments.')}")
    else: L.append(f"{h('命令未公开。见来源。','Command not published. See the source.')}")
    L.append('')
    L.append(f"## {h('关键参数','Key parameters')}\n")
    L.append(f"- {h('上下文','Context')}: {J(F('context')) or '—'}")
    L.append(f"- {h('并发','Concurrency')}: {J(F('concurrency')) or '—'}")
    if r.get('tags'): L.append(f"- {h('标签','Tags')}: " + ', '.join(f'`{t}`' for t in r['tags']))
    L.append('')
    L.append(f"## {h('预期速度','Expected speed')}\n")
    L.append(f"- {metric or na} ({lvl})\n")
    L.append(f"## {h('注意事项','Caveats')}\n")
    cav = []
    if r['source_level'] in ('宣称','转述'): cav.append(h('非一手实测（宣称或转述）。实际速度可能不同。','Not a first-hand measurement (claimed or relayed). Your results can differ.'))
    if Z and r.get('source_note'): cav.append(clip_note(r['source_note'].split('; 原文')[0]))
    cav.append(h('速度随驱动、引擎版本、上下文长度和提示长度变化。','Speed changes with drivers, engine version, context length, and prompt length.'))
    L += [f'- {c}' for c in cav]; L.append('')
    L.append(f"## {h('来源与致谢','Source & attribution')}\n")
    who = (r.get('x_post') or {}).get('author')
    L.append(f"- [{r['source_url']}]({r['source_url']})" + (f" — @{who}" if who else ''))
    L.append(f"- {h('版权归原作者。本页仅摘要并链接。数据以 CC BY 4.0 发布。','Credit to the original author. This page only summarizes and links. Data under CC BY 4.0.')}")
    return '\n'.join(L) + '\n'
def main():
    out = R/'recipes'; out.mkdir(exist_ok=True)
    for f in out.glob('*.md'): f.unlink()
    idx_en = ['# Recipe guides', '', switch('README','en'), '', 'Step-by-step pages for a first set of well-sourced recipes. New here? Read [Getting started](../docs/getting-started.md).', '', '| Recipe | Hardware | Level |', '|---|---|---|']
    idx_zh = ['# 配方指南', '', switch('README','zh'), '', '首批来源可靠配方的分步页面。第一次来？先看 [入门指南](../docs/getting-started.zh-CN.md)。', '', '| 配方 | 硬件 | 来源等级 |', '|---|---|---|']
    idx_ja = ['# レシピガイド', '', switch('README','ja'), '', '出典のしっかりしたレシピを手順付きでまとめた最初のページです。初めての方は[はじめに](../docs/getting-started.ja.md)をどうぞ。', '', '| レシピ | ハードウェア | 出典レベル |', '|---|---|---|']
    for i in GUIDES:
        r = D[i]
        (out/f'{i}.md').write_text(page(r, 'en')); (out/f'{i}.zh-CN.md').write_text(page(r, 'zh')); (out/f'{i}.ja.md').write_text(page(r, 'ja'))
        idx_en.append(f"| [{en(r['model'])} · {en(r.get('engine')) or '—'}]({i}.md) | {en(r['hardware']) or r['hardware']} | {LV[r['source_level']][0]} |")
        idx_zh.append(f"| [{r['model']} · {r.get('engine') or '—'}]({i}.zh-CN.md) | {r['hardware']} | {LV[r['source_level']][1]} |")
        idx_ja.append(f"| [{en(r['model'])} · {en(r.get('engine')) or '—'}]({i}.ja.md) | {en(r['hardware']) or r['hardware']} | {LV[r['source_level']][2]} |")
    (out/'README.ja.md').write_text('\n'.join(idx_ja)+'\n'); (out/'README.md').write_text('\n'.join(idx_en)+'\n'); (out/'README.zh-CN.md').write_text('\n'.join(idx_zh)+'\n')
    json.dump(GUIDES, open(R/'data/guides.json','w'))
    print(len(GUIDES), 'guides written')
if __name__ == '__main__': main()
