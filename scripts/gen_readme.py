#!/usr/bin/env python3
"""Generate README.md (English), README.zh-CN.md (Chinese) and README.ja.md (Japanese) from data/. Run: python3 scripts/gen_readme.py"""
import json, re
from pathlib import Path
from dataset_constants import BUDGET_TIER_BOUNDS_USD, DATA_ASOF
from scope_text import SCOPE, SEP
import hardware_index
R = Path(__file__).resolve().parent.parent
D = json.load(open(R/'data/recipes.json'))
REPOS = json.load(open(R/'data/repos.json'))
try: UPD = json.load(open(R/'data/repos.meta.json'))['updated_at']
except Exception: UPD = None
HWF_EN = {'NVIDIA 消费级':'NVIDIA consumer','二手数据中心卡':'Used datacenter GPU','其他':'Other'}
HWF_JA = {'NVIDIA 消费级':'NVIDIA コンシューマー','二手数据中心卡':'中古データセンター GPU','其他':'その他'}
PAGES = 'https://raytone-lab.github.io/awesome-local-inference-recipes/'
GUIDES = set(json.load(open(R/'data/guides.json'))) if (R/'data/guides.json').exists() else set()
LVI = {'官方':'🏛️','实测':'✅','转述':'🔁','宣称':'📣'}
CJK_CHAR = re.compile(r'[\u3000-\u303f\u3400-\u9fff\uff00-\uffef]')
CJK_OR_CURLY_QUOTE = re.compile(r'[\u3000-\u303f\u3400-\u9fff\uff00-\uffef“”]')
L = {
 'en': dict(file='README.md', tpl='readme_static.en.md',
   tiers=['Tier 1 · up to $2.5k','Tier 2 · $2.5k–7k','Tier 3 · $7k–14k','Tier 4 · $14k–30k'],
   tdesc=['Used 3090/4090, MI50/V100 cards, Strix Halo, R9700','One RTX 5090, one DGX Spark, Mac Studio Max','Two Sparks, Mac Studio Ultra','3–4 Spark clusters, multi-GPU workstations'],
   cats={'text':'📝 Text','image':'🖼️ Image','video-audio':'🎬 Video & Audio'},
   fam='Browse by Model Family', famdesc='Click a family to open the explorer pre-filtered. Tags: {tags}. The `gpu-unlock` tag shows a stock GPU with a firmware or driver unlock (no hardware change).', hwidx='Browse by Hardware', hwdesc='Recipe count and the fastest measured single-stream tok/s for each device (multi-GPU rigs: fastest measured on any rig). Links open the hardware page, or the explorer pre-filtered when a device has fewer than {m} recipes.', th4='| Family | Device (recipes · ⚡ fastest measured tok/s) |', engidx='Browse by Engine', engdesc='Engine names are normalized (`scripts/normalize_engines.py`); original strings are kept in `engine_note`.', th2='| Family | Recipes | Text | Image | Video & Audio |', th3='| Engine | Recipes |',
   hot='Popular on X', hotdesc='Most-engaged recipe posts on X (likes + 3×reposts; one entry per post, claimed-only results left out; counts as of {asof}).',
   unk='Cost Not Published', unkdesc='Multi-card builds priced per card, Macs whose memory (and so price) is not stated, and other rows without a single published price · {n} recipes. Top text recipes by tok/s:',
   guide='guide', gsuf='.md', more='…and {n} more in the [explorer](explore.html).', all='…browse all {n} in the [explorer](explore.html).', count='{n} recipes',
   src='source', see='see source', legend='Legend', eng='Engines & Tools', rel='Related Lists & Benchmarks', contrib='Contributing', lic='License',
   th='| Project | ⭐ Stars | Live | Last push | What |', site='*(site/blog)*', desc='desc',
   note='⭐ Snapshot updated {u} (UTC) by `scripts/update_stars.py` · *Live* badges are rendered by shields.io at view time.'),
 'zh': dict(file='README.zh-CN.md', tpl='readme_static.zh-CN.md',
   tiers=['第 1 档 · 2,500 美元以内','第 2 档 · 2,500–7,000 美元','第 3 档 · 7,000–14,000 美元','第 4 档 · 14,000–30,000 美元'],
   tdesc=['二手 3090/4090、MI50/V100、Strix Halo、R9700','单张 RTX 5090、单台 DGX Spark、Mac Studio Max','双 Spark、Mac Studio Ultra','3–4 台 Spark 集群、多卡工作站'],
   cats={'text':'📝 文字','image':'🖼️ 图像','video-audio':'🎬 影音'},
   fam='按模型系列浏览', famdesc='点击系列名即可打开已筛选的配方库。标签：{tags}。`gpu-unlock` 标签表示原厂显卡使用了固件或驱动解锁（无硬件改装）。', hwidx='按硬件浏览', hwdesc='每种设备的配方数，以及实测最快的单路 tok/s（多卡组合取任一组合的实测最快值）。点击打开该硬件页面；配方不足 {m} 条的设备会打开已筛选的配方库。', th4='| 类别 | 设备（配方数 · ⚡ 实测最快 tok/s） |', engidx='按引擎浏览', engdesc='引擎名已统一（`scripts/normalize_engines.py`），原始写法保留在 `engine_note` 字段。', th2='| 系列 | 配方数 | 文字 | 图像 | 影音 |', th3='| 引擎 | 配方数 |',
   hot='X 上的热门配方', hotdesc='X 上互动最多的配方帖（按 点赞 + 3×转发 排序；同一帖子只列一次，不含“宣称”条目；互动数截至 {asof}）。',
   unk='价格未公开', unkdesc='按张计价的多卡组合、未注明内存（因而无法定价）的 Mac 以及其他没有单一公开价格的配方 · 共 {n} 条。按 tok/s 排名靠前的文字配方：',
   guide='指南', gsuf='.zh-CN.md', more='……另有 {n} 条，见 [配方库](explore.html)。', all='……全部 {n} 条见 [配方库](explore.html)。', count='共 {n} 条',
   src='来源', see='见来源', legend='图例', eng='引擎与工具', rel='相关榜单与清单', contrib='参与贡献', lic='许可证',
   th='| 项目 | ⭐ Star | 实时 | 最后推送 | 简介 |', site='*（网站/博客）*', desc='desc_zh',
   note='⭐ 快照由 `scripts/update_stars.py` 更新于 {u}（UTC）· 「实时」徽章由 shields.io 在打开页面时实时渲染。'),
 'ja': dict(file='README.ja.md', tpl='readme_static.ja.md',
   tiers=['第 1 段階 · 2,500 ドルまで','第 2 段階 · 2,500〜7,000 ドル','第 3 段階 · 7,000〜14,000 ドル','第 4 段階 · 14,000〜30,000 ドル'],
   tdesc=['中古の 3090/4090、MI50/V100、Strix Halo、R9700','RTX 5090 1 枚、DGX Spark 1 台、Mac Studio Max','DGX Spark 2 台、Mac Studio Ultra','Spark 3〜4 台のクラスター、マルチ GPU ワークステーション'],
   cats={'text':'📝 テキスト','image':'🖼️ 画像','video-audio':'🎬 動画・音声'},
   fam='モデルファミリー別', famdesc='ファミリー名をクリックすると、絞り込み済みのエクスプローラーが開きます。タグ：{tags}。`gpu-unlock` タグは、市販の GPU にファームウェアまたはドライバーのロック解除を使った構成です（ハードウェア改造なし）。', hwidx='ハードウェア別', hwdesc='デバイスごとのレシピ数と、実測で最速の 1 ストリーム tok/s（マルチ GPU は全構成中の実測最速）。クリックでハードウェアページを開きます。レシピが {m} 件未満のデバイスは、絞り込み済みのエクスプローラーが開きます。', th4='| 分類 | デバイス（レシピ数 · ⚡ 実測最速 tok/s） |', engidx='エンジン別', engdesc='エンジン名は表記を統一しています（`scripts/normalize_engines.py`）。元の表記は `engine_note` に残しています。', th2='| ファミリー | レシピ数 | テキスト | 画像 | 動画・音声 |', th3='| エンジン | レシピ数 |',
   hot='X で話題のレシピ', hotdesc='X で反応が多かったレシピ投稿（いいね + リポスト×3 の順。1 投稿 1 件、「主張のみ」は除外。数値は {asof} 時点）。',
   unk='価格非公開', unkdesc='1 枚単位で価格が出ているマルチ GPU 構成、メモリ（＝価格）が不明な Mac など、単一の公開価格がないレシピ · {n} 件。tok/s 上位のテキストレシピ：',
   guide='手順', gsuf='.ja.md', more='…ほか {n} 件は[エクスプローラー](explore.html)で。', all='…全 {n} 件は[エクスプローラー](explore.html)で見られます。', count='{n} 件',
   src='出典', see='出典を参照', legend='凡例', eng='エンジンとツール', rel='関連リスト・ベンチマーク', contrib='コントリビュート', lic='ライセンス',
   th='| プロジェクト | ⭐ Star | ライブ | 最終 push | 概要 |', site='*（サイト・ブログ）*', desc='desc_ja',
   note='⭐ スナップショットは `scripts/update_stars.py` で {u}（UTC）に更新 · 「ライブ」バッジは表示時に shields.io が描画します。'),
}
SPEED={'en':('How fast is X tok/s?','Same answer, real Qwen3 tokens, streamed at 10 / 20 / 50 / 100 / 200 / 500 tok/s (log-spaced) vs. silent reading (≈5 tok/s, Brysbaert 2019), with cloud-API medians from Artificial Analysis for comparison.','Try it interactively →'),
       'zh':('X tok/s 到底有多快？','同一段回答、真实 Qwen3 token，以 10 / 20 / 50 / 100 / 200 / 500 tok/s（对数间隔）输出，对比默读速度（英文约 5 tok/s，Brysbaert 2019）和云端 API 中位速度（Artificial Analysis）。','在线互动体验 →'),
       'ja':('X tok/s ってどれくらい速い？','同じ回答を実際の Qwen3 トークンで 10 / 20 / 50 / 100 / 200 / 500 tok/s（対数間隔）で表示し、黙読の速さ（英語で約 5 tok/s、Brysbaert 2019）やクラウド API の中央値（Artificial Analysis）と比較。','インタラクティブ版を試す →')}
GALT={'en':'Token streaming speed demo: 10, 20, 50, 100, 200 and 500 tokens per second compared with human silent reading pace','zh':'token 输出速度演示：10、20、50、100、200 和 500 tok/s，对比人的默读速度（动图内文字为英文）','ja':'トークン出力速度のデモ：10、20、50、100、200、500 tok/s と人の黙読速度の比較（アニメーション内の文字は英語）'}
IMGSUF={'en':'','zh':'.zh-CN','ja':'.ja'}
BALT={'en':'Bar chart: fastest measured and claimed text setup in each budget tier','zh':'条形图：各预算档最快的实测与宣称文字配置','ja':'棒グラフ：予算帯ごとの最速テキスト構成（実測と公称）'}
def scope_md(lang):
    S=SCOPE[lang]
    return '\n\n'.join([f"## {S['h']}", SEP[lang].join(S['intro']), S['lead'], '\n'.join('- '+i for i in S['items']), *S['outro']])
def clip(s,n=90): s=(s or '').replace('|','/').replace('\n',' '); return s if len(s)<=n else s[:n-1]+'…'
def en(s, cjk=CJK_OR_CURLY_QUOTE, strip=' ·+/,'):
    if not s: return s
    s=re.sub(r'（[^）]*）|\([^)]*[\u3400-\u9fff][^)]*\)','',str(s))
    s=' '.join(w for w in re.split(r'\s+',s) if not cjk.search(w))
    return re.sub(r'\s+',' ',s).strip(strip) or None
def slug(s): return re.sub(r'[^\w \-]','',s.lower()).replace(' ','-')
def fmt(n): return f"{n/1000:.1f}k" if n>=1000 else str(n)
def js_length(s): return len(s.encode('utf-16-le'))//2
def _pad(s,w): return s+' '*(w-js_length(s))
def _cells(l):
    l=l.strip()[1:-1]; out=[];cur='';i=0
    while i<len(l):
        c=l[i]
        if c=='\\' and i+1<len(l): cur+=l[i:i+2]; i+=2; continue
        if c=='|': out.append(cur.strip()); cur=''
        else: cur+=c
        i+=1
    out.append(cur.strip()); return out
def align_tables(txt):
    lines=txt.split('\n'); res=[]; i=0
    while i<len(lines):
        if lines[i].startswith('|') and i+1<len(lines) and re.match(r'^\|[\s:|-]+\|$',lines[i+1].strip()):
            j=i
            while j<len(lines) and lines[j].startswith('|'): j+=1
            rows=[_cells(l) for l in lines[i:j]]; n=max(map(len,rows))
            rows=[r+['']*(n-len(r)) for r in rows]
            w=[max(3,max(js_length(r[k]) for k_,r in enumerate(rows) if k_!=1)) for k in range(n)]
            for k_,r in enumerate(rows):
                if k_==1: res.append('| '+' | '.join('-'*w[k] for k in range(n))+' |')
                else: res.append('| '+' | '.join(_pad(r[k],w[k]) for k in range(n))+' |')
            i=j
        else: res.append(lines[i]); i+=1
    return '\n'.join(res)

REPO = 'raytone-lab/awesome-local-inference-recipes'
SHOW = [
 ('text-092','mac'),('x-006','5090'),('x-009','amd'),('x-007','dc'),(hardware_index.fastest_on_page(D,'dgx-spark')['id'],'spark'),('text-021','cheap')]
HL = {
 'en': dict(h1='Awesome Local Inference Recipes', tag='What speed will <b>your</b> hardware actually get? {n} source-backed local AI recipes, from a ${lo:,} GPU to a $30k rig.',
   lang='<b>English</b> · <a href="README.zh-CN.md">简体中文</a> · <a href="README.ja.md">日本語</a>',
   nav=[('Explore live','explore.html'),('Recipe guides','recipes/README.md'),('Getting started','docs/getting-started.md'),('Submit a recipe','submit.html')],
   stats='**{n} recipes** ({nt} text · {ni} image · {nv} video & audio) · **{hf} hardware families** · **{ne} engines** · **{mf} model families** · every number linked to its source · budget up to **$30k**',
   hd='### Headline numbers', th='| Record | Model · engine | Hardware | Result | Source |',
   lab={'mac':'Fastest on a Mac','5090':'Fastest on one RTX 5090','amd':'Fastest on AMD','dc':'Used datacenter GPUs','spark':'Fastest on one DGX Spark','cheap':'Cheapest rig in the list'},
   note='Single-stream generation speed, copied from each source; prices are the lowest published hardware price. ✅ = measured by the poster.',
   alt='Bar chart: top measured text setups per model-size group (dense ≥27B; big MoE ≥100B total; mid MoE <100B total, ≥5B active; small MoE <100B total, <5B active; with active parameters; only models with official parameter cards), ranked by tok/s per $1,000 of hardware, colored by hardware family', cost='≈ ${c:,}'),
 'zh': dict(h1='本地推理配方精选', tag='你的硬件到底能跑多快？{n} 条有出处的本地 AI 配方，从 {lo:,} 美元的显卡到 3 万美元的整机。',
   lang='<a href="README.md">English</a> · <b>简体中文</b> · <a href="README.ja.md">日本語</a>',
   nav=[('在线配方库','explore.html'),('配方指南','recipes/README.zh-CN.md'),('入门指南','docs/getting-started.zh-CN.md'),('提交配方','submit.html')],
   stats='**{n} 条配方**（文字 {nt} · 图像 {ni} · 影音 {nv}）· **{hf} 类硬件** · **{ne} 种引擎** · **{mf} 个模型系列** · 每个数字都有出处 · 预算 **3 万美元以内**',
   hd='### 亮点数据', th='| 记录 | 模型 · 引擎 | 硬件 | 结果 | 来源 |',
   lab={'mac':'Mac 最快','5090':'单张 RTX 5090 最快','amd':'AMD 最快','dc':'二手数据中心卡','spark':'单台 DGX Spark 最快','cheap':'最便宜的配置'},
   note='单路生成速度，均摘自来源；价格为公开的最低硬件价格。✅ = 发帖人实测。',
   alt='条形图：按模型规模分组（稠密 ≥27B；大 MoE 总参数 ≥100B；中 MoE 总参数 <100B、激活 ≥5B；小 MoE 激活 <5B；标注激活参数；仅含有官方参数卡的模型），按每 $1000 硬件对应 tok/s 排名的实测文字配置，按硬件类别着色', cost='约 ${c:,}'),
 'ja': dict(h1='ローカル推論レシピ集', tag='あなたのハードウェアで、実際どれくらいの速度が出る？出典付きのローカル AI レシピ {n} 件。{lo:,} ドルの GPU から 3 万ドルの構成まで。',
   lang='<a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <b>日本語</b>',
   nav=[('エクスプローラー','explore.html'),('レシピガイド','recipes/README.ja.md'),('はじめに','docs/getting-started.ja.md'),('レシピを投稿','submit.html')],
   stats='**レシピ {n} 件**（テキスト {nt} · 画像 {ni} · 動画・音声 {nv}）· **ハードウェア {hf} 分類** · **エンジン {ne} 種** · **モデルファミリー {mf} 系統** · すべての数字に出典リンク · 予算 **3 万ドルまで**',
   hd='### 注目の記録', th='| 記録 | モデル · エンジン | ハードウェア | 結果 | 出典 |',
   lab={'mac':'Mac で最速','5090':'RTX 5090 1 枚で最速','amd':'AMD で最速','dc':'中古データセンター GPU','spark':'DGX Spark 1 台で最速','cheap':'いちばん安い構成'},
   note='1 ストリームの生成速度で、いずれも出典からの引用です。価格は公開されている最安のハードウェア価格。✅ = 投稿者本人の実測。',
   alt='棒グラフ：モデル規模別（Dense ≥27B・大型 MoE 総 ≥100B・中型 MoE 総 <100B／アクティブ ≥5B・小型 MoE アクティブ <5B、アクティブパラメータ表示、公式パラメータカードのあるモデルのみ）に、ハードウェア $1,000 あたりの tok/s で並べた実測テキスト構成（ハードウェア分類で色分け）', cost='約 {c:,} ドル'),
}
PNOTE = {'x-006':{'en':'card only, excl. 256GB RAM; street price, MSRP $1,999','zh':'仅显卡，不含 256GB 内存；街价，MSRP $1,999','ja':'GPU のみ、256GB RAM 別。実売価格、MSRP $1,999'},
 'text-092':{'en':'peak figure; test machine memory not stated, so no single price; launch price $3,999–$9,499 depending on memory','zh':'峰值；原帖未注明测试机内存，无法给出单一价格；首发价按内存为 $3,999–$9,499','ja':'ピーク値。検証機のメモリが不明なため価格は 1 つに決まらない。発売時価格はメモリにより $3,999〜$9,499'}}
def hero(lang, E):
    H=HL[lang]; T=L[lang]; byid={r['id']:r for r in D}
    n={c:sum(r['category']==c for r in D) for c in ('text','image','video-audio')}
    lo=min(r['hardware_cost_usd'] for r in D if r['hardware_cost_usd'])
    from urllib.parse import quote as q
    def b(l,r,c): return f"https://img.shields.io/badge/{q(l)}-{q(r)}-{c}?style=flat-square"
    upd=DATA_ASOF
    badges=' '.join([
      f'<a href="{PAGES}explore.html"><img src="{b("recipes",str(len(D)),"0891B2")}" alt="{len(D)} recipes"></a>',
      f'<img src="{b("data as of",upd.replace("-","--"),"4B5563")}" alt="data as of {upd}">',
      f'<a href="https://github.com/{REPO}/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/{REPO}/validate.yml?branch=main&style=flat-square&label=validate" alt="validate"></a>',
      f'<a href="LICENSE"><img src="{b("code","MIT","22C55E")}" alt="MIT"></a>',
      f'<a href="LICENSE-DATA"><img src="{b("data","CC BY 4.0","22C55E")}" alt="CC BY 4.0"></a>',
      f'<a href="https://github.com/{REPO}/stargazers"><img src="https://img.shields.io/github/stars/{REPO}?style=flat-square" alt="GitHub stars"></a>',
      '<a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-7C3AED?style=flat-square" alt="PRs welcome"></a>'])
    nav=' · '.join(f'<a href="{u}"><b>{t}</b></a>' for t,u in H['nav'])
    out=[f'<h1 align="center">{H["h1"]} <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a></h1>','',
         f'<p align="center">{H["tag"].format(n=len(D),lo=lo)}</p>','',f'<p align="center">{H["lang"]}</p>','',
         f'<p align="center">{badges}</p>','',f'<p align="center">{nav}</p>','',
         f'<p align="center"><img src="docs/hero{IMGSUF[lang]}.png" width="860" alt="{H["alt"]}"></p>','',
         f'### {SPEED[lang][0]}','',f'<p align="center"><a href="{PAGES}speed.html"><img src="docs/speed-feel.gif" width="860" alt="{GALT[lang]}"></a></p>','',
         f'<p align="center">{SPEED[lang][1]} <a href="{PAGES}speed.html"><b>{SPEED[lang][2]}</b></a></p>','',
         H['stats'].format(n=len(D),nt=n['text'],ni=n['image'],nv=n['video-audio'],hf=len({r["hardware_family"] for r in D}),ne=len({r["engine"] for r in D if r["engine"]!="Unspecified"}),mf=len({r["model_family"] for r in D if r["model_family"]!="Other"})),'',
         H['hd'],'',H['th'],'|---|---|---|---|---|']
    for i,k in SHOW:
        r=byid[i]; eg=E(r['engine']) if r['engine']!='Unspecified' else ''
        hw=clip(E(r['hardware']) or r['hardware'],44)
        c=f" · {H['cost'].format(c=r['hardware_cost_usd'])}" if r.get('hardware_cost_usd') else ''
        if i in PNOTE: c+=(f"（{PNOTE[i][lang]}）" if lang!='en' else f" ({PNOTE[i][lang]})")
        who=(r.get('x_post') or {}).get('author'); src=f'@{who}' if who else T['src']
        out.append(f"| {H['lab'][k]} | {E(r['model'])}{' · '+eg if eg else ''} | {hw}{c} | **{r['tok_s']:g} tok/s** {LVI[r['source_level']]} | [{src}]({r['source_url']}) |")
    out+=['',f"<sub>{H['note']}</sub>"]
    return '\n'.join(out)
MULTI_OR_LAPTOP_HW = re.compile(r'[2-9] ?[x×] ?(RTX|DGX|NVIDIA)|双|[2-9] ?台|\s/|/\s|\svs\.?\s|笔记本|[Ll]aptop')
QA_HARDWARE = [
 ('5090', r'^(单 ?)?(NVIDIA )?(GeForce )?RTX 5090( 32GB)?\b'), ('4090', r'^(单 ?)?(NVIDIA )?(GeForce )?RTX 4090( 24GB)?\b'),
 ('3090', r'^(单 ?)?(NVIDIA )?(GeForce )?RTX 3090( 24GB)?\b'), ('m3u', r'Mac Studio M3 Ultra'), ('spark', r'^(1 ?[x×] ?|单台 ?)?DGX Spark\b'),
 ('strix', r'Strix Halo|Ryzen AI Max\+? ?395')]
QAT = {
 'en': dict(h='Quick answers', d='Data as of {d}. Each answer is the fastest single-stream text result in the dataset with its trust level; ✅ = measured by the poster. Models differ between answers.',
   q={'5090':'How fast is a single RTX 5090 for local LLMs?','4090':'How fast is a single RTX 4090 for local LLMs?','3090':'How fast is a single RTX 3090 for local LLMs?',
      'm3u':'How fast is a Mac Studio M3 Ultra for local LLMs?','spark':'How fast is one NVIDIA DGX Spark for local LLMs?','strix':'How fast is an AMD Strix Halo (Ryzen AI Max+ 395) for local LLMs?',
      'b25':'What is the fastest measured setup under $2,500?'},
   a='Fastest measured: **{tok:g} tok/s** — {m}{e} on {hw} ({lv} {lvn}, {dt}, [source]({u})). {n} recipe(s) {scope}, {nm} measured.',
   none='No measured result yet; {n} recipe(s) are claimed/relayed — see the explorer.', lvn='measured', nodate='date not stated', s_hw='for this hardware', s_b='in this budget'),
 'zh': dict(h='快速问答', d='数据截至 {d}。每条回答取数据集中最快的单路文字生成结果，并标注来源等级；✅ = 发帖人实测。不同回答的模型不同。',
   q={'5090':'单张 RTX 5090 跑本地大模型有多快？','4090':'单张 RTX 4090 跑本地大模型有多快？','3090':'单张 RTX 3090 跑本地大模型有多快？',
      'm3u':'Mac Studio M3 Ultra 跑本地大模型有多快？','spark':'一台 NVIDIA DGX Spark 跑本地大模型有多快？','strix':'AMD Strix Halo（Ryzen AI Max+ 395）跑本地大模型有多快？',
      'b25':'2500 美元以内实测最快的配置是什么？'},
   a='实测最快：**{tok:g} tok/s**，{m}{e}，硬件 {hw}（{lv} {lvn}，{dt}，[来源]({u})）。{scope}共 {n} 条配方，其中实测 {nm} 条。',
   none='暂无实测结果；共 {n} 条宣称/转述数据，见配方库。', lvn='实测', nodate='日期未注明', s_hw='该硬件', s_b='该预算内'),
 'ja': dict(h='よくある質問', d='データ時点 {d}。各回答はデータセット中で最速の 1 ストリーム テキスト生成結果で、出典レベルを併記しています。✅ = 投稿者本人の実測。回答ごとにモデルは異なります。',
   q={'5090':'RTX 5090 1 枚でローカル LLM はどれくらい速い？','4090':'RTX 4090 1 枚でローカル LLM はどれくらい速い？','3090':'RTX 3090 1 枚でローカル LLM はどれくらい速い？',
      'm3u':'Mac Studio M3 Ultra でローカル LLM はどれくらい速い？','spark':'NVIDIA DGX Spark 1 台でローカル LLM はどれくらい速い？','strix':'AMD Strix Halo（Ryzen AI Max+ 395）でローカル LLM はどれくらい速い？',
      'b25':'2,500 ドル以下で実測最速の構成は？'},
   a='実測最速：**{tok:g} tok/s** — {m}{e}、{hw}（{lv} {lvn}、{dt}、[出典]({u})）。{scope}のレシピ {n} 件、うち実測 {nm} 件。',
   none='実測結果はまだありません。主張・伝聞 {n} 件はエクスプローラーで。', lvn='実測', nodate='日付不明', s_hw='このハードウェア', s_b='この予算内')}
def is_single_desktop_device(r): return 'multi-GPU' not in r['tags'] and not MULTI_OR_LAPTOP_HW.search(r['hardware'])
def is_measured_text(r): return r['source_level']=='实测' and r['category']=='text' and r.get('tok_s') and '自称' not in (r.get('metric') or '') and not r.get('superseded_by')
def qa(lang, E):
    Q=QAT[lang]; out=[Q['d'].format(d=DATA_ASOF),'']
    def ans(rows,scope):
        m=[r for r in rows if is_measured_text(r)]
        if not m: return Q['none'].format(n=len(rows))
        r=max(m,key=lambda r:(r['tok_s'],r['id'])); eg=E(r['engine']) if r['engine']!='Unspecified' else ''
        return Q['a'].format(tok=r['tok_s'],m=E(r['model']),e=(' · '+eg) if eg else '',hw=clip(E(r['hardware']) or r['hardware'],60),lv=LVI['实测'],lvn=Q['lvn'],
                             dt=r.get('date') or Q['nodate'],u=r['source_url'],n=len(rows),nm=len(m),scope=Q[scope])
    for k,rx in QA_HARDWARE:
        rows=[r for r in D if r['category']=='text' and re.search(rx,r['hardware']) and is_single_desktop_device(r)]
        if rows: out.append(f"**{Q['q'][k]}**  \n{ans(rows,'s_hw')}\n")
    b=[r for r in D if r['category']=='text' and r.get('hardware_cost_usd') and r['hardware_cost_usd']<=BUDGET_TIER_BOUNDS_USD[0][1]]
    out.append(f"**{Q['q']['b25']}**  \n{ans(b,'s_b')}\n")
    return '\n'.join(out)
def build(lang):
    T=L[lang]; E=(lambda s:en(s)) if lang in ('en','ja') else (lambda s:s)
    def key(r):
        if r['tok_s'] is not None: return f"**{r['tok_s']:g} tok/s**"
        m=(r.get('metric_en') or r['metric']) if lang in ('en','ja') else r['metric']
        if lang in ('en','ja') and m and CJK_OR_CURLY_QUOTE.search(m): m=None
        return clip(m,70) if m else T['see']
    def ln(r):
        q=E(r['quant']); q=f" `{clip(q,28)}`" if q else ''
        eg=E(r['engine']); eg='' if (not eg or r['engine']=='Unspecified') else f" · {eg}"
        return f"- **{E(r['model'])}**{eg}{q} — {clip(E(r['hardware']) or ({'en':HWF_EN,'ja':HWF_JA}.get(lang,{}).get(r['hardware_family'],r['hardware_family'])),60)} → {key(r)} {LVI.get(r['source_level'],'')} [{T['src']}]({r['source_url']})"+(f" · [{T['guide']}](recipes/{r['id']}{T['gsuf']})" if r['id'] in GUIDES else '')
    out=[];toc=[]
    def sec(t): out.append(f"\n## {t}\n"); toc.append(f"- [{t}](#{slug(t)})")
    seen=set();hot=[r for r in sorted([r for r in D if r.get('x_post') and r['source_level']!='宣称'],key=lambda r:-(r['x_post']['likes']+3*r['x_post']['reposts'])) if not (r['source_url'] in seen or seen.add(r['source_url']))][:8]
    sec(QAT[lang]['h']); out.append(qa(lang,E))
    sec(T['hot']); asof=max((r['x_post'].get('as_of') or '' for r in hot),default=''); out.append(T['hotdesc'].format(asof=asof)+'\n')
    for r in hot:
        eg=E(r['engine']); eg=f" · {eg}" if eg and r['engine']!='Unspecified' else ''
        out.append(f"- **{E(r['model'])}**{eg} — {clip(E(r['hardware']),50)} → {key(r)} {LVI[r['source_level']]} [@{r['x_post']['author']}]({r['source_url']}) ♥{r['x_post']['likes']}")
    from collections import Counter
    from urllib.parse import quote
    sec(T['hwidx']); out.append(T['hwdesc'].format(m=hardware_index.MIN_ROWS)+'\n'); out.append(T['th4']); out.append('|---|---|')
    for g,chips in hardware_index.grid(D):
        cells=[f"[{hardware_index.LABELS.get(c.label,{}).get(lang,c.label)}]({hardware_index.chip_link(c,D,PAGES)}) ({n}"+(f" · ⚡**{b['tok_s']:g}**" if b else '')+')' for c,n,b in chips]
        out.append(f"| {hardware_index.GROUPS[g][lang].replace(' ','&nbsp;')} | "+' &nbsp;·&nbsp; '.join(cells)+' |')
    sec(T['fam']); fc=Counter(r['model_family'] for r in D); tc=Counter(t for r in D for t in r['tags'])
    tl=', '.join(f"[`{t}`](explore.html?tag={quote(t)}) {n}" for t,n in tc.most_common())
    out.append(T['famdesc'].format(tags=tl)+'\n'); out.append(T['th2']); out.append('|---|--:|--:|--:|--:|')
    for f,n in sorted(fc.items(),key=lambda x:(x[0]=='Other',-x[1],x[0])):
        cc=[sum(1 for r in D if r['model_family']==f and r['category']==c) or '' for c in ('text','image','video-audio')]
        out.append(f"| [{f}](explore.html?family={quote(f)}) | {n} | "+' | '.join(map(str,cc))+' |')
    sec(T['engidx']); out.append(T['engdesc']+'\n'); out.append(T['th3']); out.append('|---|--:|')
    for e,n in sorted(Counter(r['engine'] for r in D).items(),key=lambda x:(x[0]=='Unspecified',-x[1],x[0])):
        out.append(f"| [{e}](explore.html?engine={quote(e)}) | {n} |")
    out.append(f'\n<p align="center"><img src="docs/budget-tiers{IMGSUF[lang]}.png" width="860" alt="{BALT[lang]}"></p>\n')
    for t,d,(lo,hi) in zip(T['tiers'],T['tdesc'],BUDGET_TIER_BOUNDS_USD,strict=True):
        sec(t); rs=[r for r in D if r['hardware_cost_usd'] is not None and lo<r['hardware_cost_usd']<=hi]
        out.append(f"*{d}* · {T['count'].format(n=len(rs))}\n")
        for c,ct in T['cats'].items():
            cr=sorted([r for r in rs if r['category']==c],key=lambda r:-(r['tok_s'] or 0))
            if not cr: continue
            out.append(f"\n**{ct}**\n"); sh=cr[:10] if c=='text' else cr
            out+= [ln(r) for r in sh]
            if len(cr)>len(sh): out.append('- *'+T['more'].format(n=len(cr)-len(sh))+'*')
    unk=[r for r in D if r['hardware_cost_usd'] is None]
    sec(T['unk']); out.append(T['unkdesc'].format(n=len(unk))+'\n')
    out+= [ln(r) for r in sorted([r for r in unk if r['tok_s']],key=lambda r:-r['tok_s'])[:12]]
    out.append('- *'+T['all'].format(n=len(unk))+'*')
    def rtable(s):
        rows=[T['th'],"|---|--:|---|---|---|"]
        for r in sorted([r for r in REPOS if r['section']==s],key=lambda r:-(r.get('stars') or -1)):
            url=r.get('url') or f"https://github.com/{r['repo']}"
            if r.get('repo'): st=fmt(r['stars']) if r.get('stars') is not None else '—'; lv=f"![stars](https://img.shields.io/github/stars/{r['repo']}?style=flat&label=)"; pu=(r.get('pushed_at') or '')[:10] or '—'
            else: st,lv,pu='—',T['site'],'—'
            rows.append(f"| [{r['name']}]({url}) | {st} | {lv} | {pu} | {r[T['desc']]} |")
        return '\n'.join(rows)+(f"\n\n<sub>{T['note'].format(u=UPD)}</sub>" if UPD else '')
    tpl=open(R/'scripts'/T['tpl']).read(); head,tail=tpl.split('<!--RECIPES-->')
    n={c:sum(r['category']==c for r in D) for c in T['cats']}
    toc=[f"- [{x}](#{slug(x)})" for x in (T['legend'],SCOPE[lang]['h'])]+toc+[f"- [{x}](#{slug(x)})" for x in (T['eng'],T['rel'],T['lic'])]
    head=head.replace('{{HERO}}',hero(lang,E)).replace('{{SCOPE}}',scope_md(lang)).replace('{{TOC}}','\n'.join(toc)).replace('{{N}}',str(len(D))).replace('{{NT}}',str(n['text'])).replace('{{NI}}',str(n['image'])).replace('{{NV}}',str(n['video-audio']))
    tail=tail.replace('<!--ENGINES-->',rtable('engines')).replace('<!--RELATED-->',rtable('related'))
    txt=head+'\n'.join(out)+'\n'+tail
    for pg in ('explore.html','submit.html'):
        txt=txt.replace(f'](%s'%pg,f']({PAGES}{pg}').replace(f'href="{pg}','href="'+PAGES+pg)
    txt=localize_site_links(txt,lang)
    txt=align_tables(txt)
    open(R/T['file'],'w').write(txt)
    return T['file']
SITE_LANG={'en':'en','zh':'zh-CN','zh-CN':'zh-CN','ja':'ja'}
def localize_site_links(txt,lang):
    """Point every site link at the README's language. The site picks its language from ?lang=, then localStorage, then the browser,
    so a link without ?lang= can open in another language. Static hw pages have one file per language (hw/, hw/zh-CN/, hw/ja/)."""
    import re
    code=SITE_LANG.get(lang,lang); pre={'en':'','zh-CN':'zh-CN/','ja':'ja/'}[code]
    def fix(m):
        url=m.group(0); path,_,frag=url.partition('#')
        if path.startswith(PAGES+'hw/'):
            rest=path[len(PAGES)+3:]
            if not rest.startswith(('zh-CN/','ja/')): path=PAGES+'hw/'+pre+rest
            return path+('#'+frag if frag else '')
        if re.search(r'[?&]lang=',path): return url
        path+=('&' if '?' in path else '?')+'lang='+code
        return path+('#'+frag if frag else '')
    return re.sub(re.escape(PAGES)+r'[A-Za-z0-9_./-]*\.html(?:\?[^\s)"\'<>#]*)?(?:#[^\s)"\'<>]*)?',fix,txt)

if __name__ == '__main__':
    for lang in L: print('written', build(lang))
