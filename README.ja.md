<h1 align="center">ローカル推論レシピ集 <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a></h1>

<p align="center">あなたのハードウェアで、実際どれくらいの速度が出る？出典付きのローカル AI レシピ 795 件。405 ドルの GPU から 3 万ドルの構成まで。</p>

<p align="center"><a href="README.md">English</a> · <a href="README.zh-CN.md">简体中文</a> · <b>日本語</b></p>

<p align="center"><a href="https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja"><img src="https://img.shields.io/badge/recipes-795-0891B2?style=flat-square" alt="795 recipes"></a> <img src="https://img.shields.io/badge/data%20as%20of-2026--11--05-4B5563?style=flat-square" alt="data as of 2026-11-05"> <a href="https://github.com/raytone-lab/awesome-local-inference-recipes/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/raytone-lab/awesome-local-inference-recipes/validate.yml?branch=main&style=flat-square&label=validate" alt="validate"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-22C55E?style=flat-square" alt="MIT"></a> <a href="LICENSE-DATA"><img src="https://img.shields.io/badge/data-CC%20BY%204.0-22C55E?style=flat-square" alt="CC BY 4.0"></a> <a href="https://github.com/raytone-lab/awesome-local-inference-recipes/stargazers"><img src="https://img.shields.io/github/stars/raytone-lab/awesome-local-inference-recipes?style=flat-square" alt="GitHub stars"></a> <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-7C3AED?style=flat-square" alt="PRs welcome"></a></p>

<p align="center"><a href="https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja"><b>エクスプローラー</b></a> · <a href="recipes/README.ja.md"><b>レシピガイド</b></a> · <a href="docs/getting-started.ja.md"><b>はじめに</b></a> · <a href="https://raytone-lab.github.io/awesome-local-inference-recipes/submit.html?lang=ja"><b>レシピを投稿</b></a></p>

<p align="center"><img src="docs/hero.ja.png" width="860" alt="棒グラフ：モデル規模別（Dense ≥27B・大型 MoE 総 ≥100B・中型 MoE 総 <100B／アクティブ ≥5B・小型 MoE アクティブ <5B、アクティブパラメータ表示、公式パラメータカードのあるモデルのみ）に、ハードウェア $1,000 あたりの tok/s で並べた実測テキスト構成（ハードウェア分類で色分け）"></p>

### X tok/s ってどれくらい速い？

<p align="center"><a href="https://raytone-lab.github.io/awesome-local-inference-recipes/speed.html?lang=ja"><img src="docs/speed-feel.gif" width="860" alt="トークン出力速度のデモ：10、20、50、100、200、500 tok/s と人の黙読速度の比較（アニメーション内の文字は英語）"></a></p>

<p align="center">同じ回答を実際の Qwen3 トークンで 10 / 20 / 50 / 100 / 200 / 500 tok/s（対数間隔）で表示し、黙読の速さ（英語で約 5 tok/s、Brysbaert 2019）やクラウド API の中央値（Artificial Analysis）と比較。 <a href="https://raytone-lab.github.io/awesome-local-inference-recipes/speed.html?lang=ja"><b>インタラクティブ版を試す →</b></a></p>

**レシピ 795 件**（テキスト 754 · 画像 15 · 動画・音声 26）· **ハードウェア 6 分類** · **エンジン 105 種** · **モデルファミリー 17 系統** · すべての数字に出典リンク · 予算 **3 万ドルまで**

### 注目の記録

| 記録               | モデル · エンジン                      | ハードウェア                                                                          | 結果                | 出典                                                                       |
| ---------------- | ------------------------------- | ------------------------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------ |
| Mac で最速          | Qwen3.8-Flash-Next · TensorFold | Mac Studio M3 Ultra（ピーク値。検証機のメモリが不明なため価格は 1 つに決まらない。発売時価格はメモリにより $3,999〜$9,499） | **130 tok/s** ✅   | [出典](https://x.com/ivanfioravanti/status/2104183112611614780)            |
| RTX 5090 1 枚で最速  | Qwen3.8-Flash-Next · Strata     | RTX 5090 + 256GB RAM · 約 5,400 ドル（GPU のみ、256GB RAM 別。実売価格、MSRP $1,999）          | **176 tok/s** ✅   | [@TechPractice1](https://x.com/TechPractice1/status/2105087037363884483) |
| AMD で最速          | Qwen3.8-Flash-Next · Strata     | AMD Radeon AI PRO R9700 · 約 1,600 ドル                                            | **100 tok/s** ✅   | [@TechPractice1](https://x.com/TechPractice1/status/2105338176055509376) |
| 中古データセンター GPU    | Qwen3.8-Flash-Next · Strata     | 2× Tesla V100 32GB PCIe                                                         | **120 tok/s** ✅   | [@rewin123](https://x.com/rewin123/status/2108669905616736529)           |
| DGX Spark 1 台で最速 | Qwen3.8-Flash-Next · TensorFold | 1× DGX Spark · 約 6,950 ドル                                                       | **130.1 tok/s** ✅ | [出典](https://x.com/Leoskie_L/status/2115262189506535697)                 |
| いちばん安い構成         | Qwen3.8-Flash-Next · Strata     | Tesla P40 24GB · 約 405 ドル                                                       | **30 tok/s** ✅    | [出典](https://github.com/Niko1221/Strata/blob/main/docs/OLDER_GPUS.md)    |

<sub>1 ストリームの生成速度で、いずれも出典からの引用です。価格は公開されている最安のハードウェア価格。✅ = 投稿者本人の実測。</sub>

## 目次

- [凡例](#凡例)
- [収録範囲](#収録範囲)
- [よくある質問](#よくある質問)
- [X で話題のレシピ](#x-で話題のレシピ)
- [ハードウェア別](#ハードウェア別)
- [モデルファミリー別](#モデルファミリー別)
- [エンジン別](#エンジン別)
- [第 1 段階 · 2,500 ドルまで](#第-1-段階--2500-ドルまで)
- [第 2 段階 · 2,500〜7,000 ドル](#第-2-段階--25007000-ドル)
- [第 3 段階 · 7,000〜14,000 ドル](#第-3-段階--700014000-ドル)
- [第 4 段階 · 14,000〜30,000 ドル](#第-4-段階--1400030000-ドル)
- [価格非公開](#価格非公開)
- [エンジンとツール](#エンジンとツール)
- [関連リスト・ベンチマーク](#関連リストベンチマーク)
- [ライセンス](#ライセンス)

## 凡例

| 出典レベル      | 意味                                                    | 表記                                                   |
| ---------- | ----------------------------------------------------- | ---------------------------------------------------- |
| 🏛️ **公式** | 開発元やベンダーが公表した数字                                       | **モデル** · エンジン `量子化` — ハードウェア → **主要な数字** レベル \[出典\] |
| ✅ **実測**   | 投稿者本人が計測（ログやスクリーンショットあり）。エンジンまたはレシピの作者は生データと再現手順も公開する | **tok/s** は 1 ストリームの生成速度（プリフィルや合計値は含まない）             |
| 🔁 **伝聞**  | 他人の結果の引用。元の投稿で確認を                                     | 価格帯は公開されている最安のハードウェア価格（米ドル）で区分                       |
| 📣 **主張**  | 見込み値で、再現条件なし                                          | 不明な値は推定しません                                          |

## 収録範囲

このリストは、個人、家庭やオフィスのデスクトップ利用者、小規模スタジオが組める構成だけを収録します。データセンター構成は対象外です。デスクトップ PC に載せた中古データセンター GPU は対象です。

次の条件をすべて満たす構成だけを収録します：

- ハードウェアの合計価格が 3 万ドル以下。
- GPU 4 枚またはマシン 4 台まで。GPU は 1 枚ずつ、独立 GPU のないマシンは 1 台ずつ数えます。例：PC 1 台に GPU 4 枚は 4、DGX Spark 4 台は 4、DGX Spark 4 台と RTX 5090 搭載 PC 1 台は 5。
- 一般的な家庭用・オフィス用の電源で動く：合計約 2 kW 以内で、ふつうのコンセント 2 口までに分けてよく、専用の配線工事は不要。2 口を使うときは、別々の回路のコンセントにする。米国の 120 V / 15 A 回路 1 本は連続で約 1.44 kW、日本の 100 V / 15 A コンセント 1 口は定格で約 1.5 kW。
- ラック、SXM / HGX サーバーボード、カスタムループ水冷、サーバー用液冷を使わない。デスクトップに収まる DIY の SXM2→PCIe 変換構成は対象。メーカー出荷時から簡易水冷（AIO）付きのコンシューマー GPU も対象。
- ネットワークスイッチはデスクトップ型 1 台まで。
- 改造 GPU は当面対象外。ハードウェアを変更した GPU（例：メモリを変更した GPU）のことです。例：48GB メモリの RTX 4090D、メモリを変更した CMP 170HX。リストにすでにある改造 GPU のレシピは、後の見直しまで残します。市販の GPU にファームウェアまたはドライバーのロック解除だけを使った構成は対象です。例：Ampere カードの FP16 制限を外す gpu-unlock カーネルモジュール。このレシピには `gpu-unlock` タグを付けます。

1 つでも満たさない構成は、3 万ドル未満でも対象外です。

価格は収録日の価格を記録します。後で値上がりしても、価格メモ（`hardware_cost_text`）だけを更新し、レシピは削除しません。

`python3 scripts/scope_rules.py` は、価格・台数・ハードウェア種別のチェックに通らないレシピを一覧表示します。

## よくある質問

データ時点 2026-11-05。各回答はデータセット中で最速の 1 ストリーム テキスト生成結果で、出典レベルを併記しています。✅ = 投稿者本人の実測。回答ごとにモデルは異なります。

**RTX 5090 1 枚でローカル LLM はどれくらい速い？**  
実測最速：**351.5 tok/s** — LFM2.5-24B-A2B · llama.cpp、RTX 5090 32GB（✅ 実測、2026-10-15、[出典](https://x.com/niklaslenz_ai/status/2110469931011612895)）。このハードウェアのレシピ 50 件、うち実測 28 件。

**RTX 4090 1 枚でローカル LLM はどれくらい速い？**  
実測最速：**179.4 tok/s** — Recursive Flint 40B-A2.5B · llama.cpp、RTX 4090 24GB（✅ 実測、2026-10-22、[出典](https://llm-speed.com/m/flint-40b-a2-5b)）。このハードウェアのレシピ 14 件、うち実測 5 件。

**RTX 3090 1 枚でローカル LLM はどれくらい速い？**  
実測最速：**384 tok/s** — LFM3-1.7B · llama.cpp、RTX 3090 24GB（✅ 実測、2026-10-28、[出典](https://x.com/Layton_Gott/status/2115244678056464384)）。このハードウェアのレシピ 21 件、うち実測 11 件。

**Mac Studio M3 Ultra でローカル LLM はどれくらい速い？**  
実測最速：**130 tok/s** — Qwen3.8-Flash-Next · TensorFold、Mac Studio M3 Ultra（✅ 実測、日付不明、[出典](https://x.com/ivanfioravanti/status/2104183112611614780)）。このハードウェアのレシピ 24 件、うち実測 7 件。

**NVIDIA DGX Spark 1 台でローカル LLM はどれくらい速い？**  
実測最速：**130.1 tok/s** — Qwen3.8-Flash-Next · TensorFold、1× DGX Spark（✅ 実測、2026-10-28、[出典](https://x.com/Leoskie_L/status/2115262189506535697)）。このハードウェアのレシピ 66 件、うち実測 41 件。

**AMD Strix Halo（Ryzen AI Max+ 395）でローカル LLM はどれくらい速い？**  
実測最速：**98 tok/s** — Recursive Flint 40B-A2.5B · Halogen、AMD Ryzen AI Max+ 395 128GB（✅ 実測、2026-10-23、[出典](https://www.reddit.com/r/StrixHalo/comments/1xcxjpv/)）。このハードウェアのレシピ 25 件、うち実測 12 件。

**2,500 ドル以下で実測最速の構成は？**  
実測最速：**190 tok/s** — Qwen3.8-27B · Geezuz、2× RTX 3090（✅ 実測、2026-10-20、[出典](https://github.com/ohgeebtw/geezuz-qwen3.8-27b-dual-gpu)）。この予算内のレシピ 61 件、うち実測 32 件。


## X で話題のレシピ

X で反応が多かったレシピ投稿（いいね + リポスト×3 の順。1 投稿 1 件、「主張のみ」は除外。数値は 2026-10-30 時点）。

- **DeepSeek-V4.1-Flash** — 2× DGX Spark → **29 tok/s** ✅ [@0xSero](https://x.com/0xSero/status/2106373861818224907) ♥2459
- **Ternary Bonsai 2 27B** — RTX 3060 12GB → **50 tok/s** ✅ [@sudoingX](https://x.com/sudoingX/status/2110451458302943383) ♥811
- **Qwen3.8-Flash-Next** · vLLM — 1× DGX Spark → **48.7 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2101339268203380857) ♥800
- **GLM-5.3-Flash** · TensorFold — 2× DGX Spark → **38.7 tok/s** ✅ [@MiaAI_lab](https://x.com/niklaslenz_ai/status/2118066082204242326) ♥683
- **Qwen3.8-Flash-Next** · Strata — RTX 5090 32GB → **204 tok/s** ✅ [@niklaslenz_ai](https://x.com/niklaslenz_ai/status/2110132306061013386) ♥503
- **Qwen3.8-Flash-Next** · TensorFold — 1× DGX Spark → **64.4 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2108203605685596490) ♥386
- **DeepSeek-V4-Flash (0731 GA)** — 2× DGX Spark → **82 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2083326111144906836) ♥365
- **Qwen3.8-27B** · vLLM — RTX 5090 32GB → **147 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2088734058842878037) ♥377

## ハードウェア別

デバイスごとのレシピ数と、実測で最速の 1 ストリーム tok/s（マルチ GPU は全構成中の実測最速）。クリックでハードウェアページを開きます。レシピが 5 件未満のデバイスは、絞り込み済みのエクスプローラーが開きます。

| 分類               | デバイス（レシピ数 · ⚡ 実測最速 tok/s）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| NVIDIA&nbsp;RTX  | [RTX 5090](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/rtx-5090.html) (99 · ⚡**538.1**) &nbsp;·&nbsp; [RTX 3090](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/rtx-3090.html) (51 · ⚡**384**) &nbsp;·&nbsp; [RTX 4090](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/rtx-4090.html) (27 · ⚡**179.4**) &nbsp;·&nbsp; [RTX 5060 Ti](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/rtx-5060-ti.html) (23 · ⚡**162**) &nbsp;·&nbsp; [RTX 5070 / 5070 Ti](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=RTX%205070&lang=ja) (20 · ⚡**141.3**) &nbsp;·&nbsp; [RTX 3060](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=RTX%203060&lang=ja) (18 · ⚡**244**)        |
| Apple&nbsp;シリコン  | [M5 Pro / M5 Max](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/mac-m5.html) (59 · ⚡**157**) &nbsp;·&nbsp; [M3 Ultra](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/mac-studio-m3-ultra.html) (33 · ⚡**130**) &nbsp;·&nbsp; [M5 Ultra](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=M5%20Ultra&lang=ja) (33 · ⚡**141**) &nbsp;·&nbsp; [M4 Pro](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=M4%20Pro&lang=ja) (31 · ⚡**127.9**) &nbsp;·&nbsp; [M4 Max](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/mac-m4-max.html) (20 · ⚡**78.7**) &nbsp;·&nbsp; [M2 Ultra](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=M2%20Ultra&lang=ja) (2 · ⚡**59.9**) |
| DGX&nbsp;Spark   | [DGX Spark](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/dgx-spark.html) (148 · ⚡**130.1**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| AMD              | [Radeon R9700 / RX 7900](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/amd-radeon.html) (47 · ⚡**109.9**) &nbsp;·&nbsp; [Strix Halo](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/ja/strix-halo.html) (25 · ⚡**78**) &nbsp;·&nbsp; [Instinct MI50](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=MI50&lang=ja) (6 · ⚡**36.8**)                                                                                                                                                                                                                                                                                                                                                                                                            |
| マルチ&nbsp;GPU・その他 | [マルチ GPU 構成](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=multi-GPU&lang=ja) (202 · ⚡**370**) &nbsp;·&nbsp; [Tesla V100](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=V100&lang=ja) (23 · ⚡**74.7**) &nbsp;·&nbsp; [CMP 170HX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=CMP&lang=ja) (6) &nbsp;·&nbsp; [iPhone](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=iPhone&lang=ja) (4)                                                                                                                                                                                                                                                                                             |

## モデルファミリー別

ファミリー名をクリックすると、絞り込み済みのエクスプローラーが開きます。タグ：[`MoE`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=MoE&lang=ja) 538, [`long-context`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=long-context&lang=ja) 298, [`speculative`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=speculative&lang=ja) 294, [`4bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=4bit&lang=ja) 269, [`dense`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=dense&lang=ja) 205, [`multi-GPU`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=multi-GPU&lang=ja) 202, [`MTP`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=MTP&lang=ja) 153, [`3bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=3bit&lang=ja) 121, [`2bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=2bit&lang=ja) 110, [`offload`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=offload&lang=ja) 85, [`8bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=8bit&lang=ja) 53, [`1bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=1bit&lang=ja) 29, [`ternary`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=ternary&lang=ja) 26, [`abliterated`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=abliterated&lang=ja) 14, [`bf16`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=bf16&lang=ja) 12, [`few-step`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=few-step&lang=ja) 12, [`6bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=6bit&lang=ja) 9, [`gpu-unlock`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=gpu-unlock&lang=ja) 4, [`5bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=5bit&lang=ja) 2。`gpu-unlock` タグは、市販の GPU にファームウェアまたはドライバーのロック解除を使った構成です（ハードウェア改造なし）。

| ファミリー                                                                                                                | レシピ数 | テキスト | 画像  | 動画・音声 |
| -------------------------------------------------------------------------------------------------------------------- | ---- | ---- | --- | ----- |
| [Qwen](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Qwen&lang=ja)               | 423  | 423  |     |       |
| [DeepSeek](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=DeepSeek&lang=ja)       | 125  | 125  |     |       |
| [GLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=GLM&lang=ja)                 | 41   | 41   |     |       |
| [Bonsai](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Bonsai&lang=ja)           | 33   | 33   |     |       |
| [MiniMax H3](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=MiniMax%20H3&lang=ja) | 18   |      |     | 18    |
| [Qwen-Image](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Qwen-Image&lang=ja)   | 13   |      | 13  |       |
| [MiniMax](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=MiniMax&lang=ja)         | 9    | 9    |     |       |
| [Gemma](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Gemma&lang=ja)             | 8    | 8    |     |       |
| [Mistral](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Mistral&lang=ja)         | 5    | 5    |     |       |
| [LTX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=LTX&lang=ja)                 | 4    |      |     | 4     |
| [gpt-oss](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=gpt-oss&lang=ja)         | 3    | 3    |     |       |
| [ACE-Step](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=ACE-Step&lang=ja)       | 2    |      |     | 2     |
| [Edge0](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Edge0&lang=ja)             | 2    | 2    |     |       |
| [Wan](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Wan&lang=ja)                 | 2    |      |     | 2     |
| [Z-Image](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Z-Image&lang=ja)         | 2    |      | 2   |       |
| [Kimi](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Kimi&lang=ja)               | 1    | 1    |     |       |
| [Llama](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Llama&lang=ja)             | 1    | 1    |     |       |
| [Other](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Other&lang=ja)             | 103  | 103  |     |       |

## エンジン別

エンジン名は表記を統一しています（`scripts/normalize_engines.py`）。元の表記は `engine_note` に残しています。

| エンジン                                                                                                                                                                                                     | レシピ数 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| [Strata](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata&lang=ja)                                                                                               | 163  |
| [llama.cpp](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp&lang=ja)                                                                                         | 83   |
| [TensorFold](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TensorFold&lang=ja)                                                                                       | 71   |
| [vLLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=vLLM&lang=ja)                                                                                                   | 59   |
| [oMLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=oMLX&lang=ja)                                                                                                   | 38   |
| [MLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MLX&lang=ja)                                                                                                     | 33   |
| [SGLang](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=SGLang&lang=ja)                                                                                               | 21   |
| [llama.cpp (PrismML fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28PrismML%20fork%29&lang=ja)                                                   | 14   |
| [ComfyUI](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ComfyUI&lang=ja)                                                                                             | 12   |
| [Project Maya](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Project%20Maya&lang=ja)                                                                                 | 12   |
| [Splash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Splash&lang=ja)                                                                                               | 12   |
| [MTPLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MTPLX&lang=ja)                                                                                                 | 11   |
| [ExLlama](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ExLlama&lang=ja)                                                                                             | 9    |
| [mlx-serve](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=mlx-serve&lang=ja)                                                                                         | 9    |
| [DFlash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=DFlash&lang=ja)                                                                                               | 7    |
| [Ollama](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Ollama&lang=ja)                                                                                               | 7    |
| [Radiance](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Radiance&lang=ja)                                                                                           | 7    |
| [ds4 (DwarfStar)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ds4%20%28DwarfStar%29&lang=ja)                                                                       | 6    |
| [Basalt](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Basalt&lang=ja)                                                                                               | 5    |
| [Kapitsa](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Kapitsa&lang=ja)                                                                                             | 5    |
| [Halogen](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Halogen&lang=ja)                                                                                             | 4    |
| [NVIDIA Flare](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=NVIDIA%20Flare&lang=ja)                                                                                 | 4    |
| [Radiance (fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Radiance%20%28fork%29&lang=ja)                                                                       | 4    |
| [mirai-s-ada](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=mirai-s-ada&lang=ja)                                                                                     | 4    |
| [ninfer](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ninfer&lang=ja)                                                                                               | 4    |
| [Rapid-MLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Rapid-MLX&lang=ja)                                                                                         | 3    |
| [TabbyAPI](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TabbyAPI&lang=ja)                                                                                           | 3    |
| [TandemLLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TandemLLM&lang=ja)                                                                                         | 3    |
| [gufo](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=gufo&lang=ja)                                                                                                   | 3    |
| [llama.cpp (agentionai fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28agentionai%20fork%29&lang=ja)                                             | 3    |
| [BitRun](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=BitRun&lang=ja)                                                                                               | 2    |
| [Espetero](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Espetero&lang=ja)                                                                                           | 2    |
| [FreeToken](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=FreeToken&lang=ja)                                                                                         | 2    |
| [Front_Eagle739 streaming stack](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Front_Eagle739%20streaming%20stack&lang=ja)                                           | 2    |
| [Halowin Bubo](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Halowin%20Bubo&lang=ja)                                                                                 | 2    |
| [Infernix](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Infernix&lang=ja)                                                                                           | 2    |
| [MLX Swift](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MLX%20Swift&lang=ja)                                                                                       | 2    |
| [RustingStrata](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=RustingStrata&lang=ja)                                                                                 | 2    |
| [Speedy](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Speedy&lang=ja)                                                                                               | 2    |
| [Strata (Strata-DS fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28Strata-DS%20fork%29&lang=ja)                                                     | 2    |
| [Strata (Strata-rdna3 fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28Strata-rdna3%20fork%29&lang=ja)                                               | 2    |
| [TideLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TideLM&lang=ja)                                                                                               | 2    |
| [affinity](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=affinity&lang=ja)                                                                                           | 2    |
| [capy-flash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=capy-flash&lang=ja)                                                                                       | 2    |
| [dsx](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=dsx&lang=ja)                                                                                                     | 2    |
| [edge0](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=edge0&lang=ja)                                                                                                 | 2    |
| [llama.cpp (OpenBMB fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28OpenBMB%20fork%29&lang=ja)                                                   | 2    |
| [strata-mlx](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=strata-mlx&lang=ja)                                                                                       | 2    |
| [tqLLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=tqLLM&lang=ja)                                                                                                 | 2    |
| [Betelgeuse](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Betelgeuse&lang=ja)                                                                                       | 1    |
| [BigMoeOnEdge](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=BigMoeOnEdge&lang=ja)                                                                                   | 1    |
| [Geezuz](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Geezuz&lang=ja)                                                                                               | 1    |
| [IronMLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=IronMLX&lang=ja)                                                                                             | 1    |
| [JITEngine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=JITEngine&lang=ja)                                                                                         | 1    |
| [Janas-LLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Janas-LLM&lang=ja)                                                                                         | 1    |
| [Kapitsa 0.2.19 + KFlash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Kapitsa%200.2.19%20%2B%20KFlash&lang=ja)                                                     | 1    |
| [LightX2V](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=LightX2V&lang=ja)                                                                                           | 1    |
| [MLX Swift (PrismML fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MLX%20Swift%20%28PrismML%20fork%29&lang=ja)                                                 | 1    |
| [Magnitude](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Magnitude&lang=ja)                                                                                         | 1    |
| [MoEShift](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MoEShift&lang=ja)                                                                                           | 1    |
| [NInferno](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=NInferno&lang=ja)                                                                                           | 1    |
| [NVIDIA Sol](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=NVIDIA%20Sol&lang=ja)                                                                                     | 1    |
| [Osaurus](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Osaurus&lang=ja)                                                                                             | 1    |
| [PLI](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=PLI&lang=ja)                                                                                                     | 1    |
| [PXA](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=PXA&lang=ja)                                                                                                     | 1    |
| [Paiton](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Paiton&lang=ja)                                                                                               | 1    |
| [Pithos](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Pithos&lang=ja)                                                                                               | 1    |
| [QEngine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=QEngine&lang=ja)                                                                                             | 1    |
| [Qwentin](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Qwentin&lang=ja)                                                                                             | 1    |
| [ReVolta](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ReVolta&lang=ja)                                                                                             | 1    |
| [SGLang (Penny Royal fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=SGLang%20%28Penny%20Royal%20fork%29&lang=ja)                                               | 1    |
| [SonicBoom](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=SonicBoom&lang=ja)                                                                                         | 1    |
| [Strata (TCP layer split fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28TCP%20layer%20split%20fork%29&lang=ja)                                     | 1    |
| [Strata (syoyo fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28syoyo%20fork%29&lang=ja)                                                             | 1    |
| [Strim](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strim&lang=ja)                                                                                                 | 1    |
| [Surogate](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Surogate&lang=ja)                                                                                           | 1    |
| [TensorRT Edge-LLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TensorRT%20Edge-LLM&lang=ja)                                                                       | 1    |
| [VoidInfer](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=VoidInfer&lang=ja)                                                                                         | 1    |
| [Xolotl](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Xolotl&lang=ja)                                                                                               | 1    |
| [delta-inference-engine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=delta-inference-engine&lang=ja)                                                               | 1    |
| [ds41](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ds41&lang=ja)                                                                                                   | 1    |
| [elpis (ExLlamaV3 patch)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=elpis%20%28ExLlamaV3%20patch%29&lang=ja)                                                     | 1    |
| [gbx](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=gbx&lang=ja)                                                                                                     | 1    |
| [gufo (mikealanni fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=gufo%20%28mikealanni%20fork%29&lang=ja)                                                       | 1    |
| [ik_llama.cpp (Mcniiby fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ik_llama.cpp%20%28Mcniiby%20fork%29&lang=ja)                                             | 1    |
| [libosmos](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=libosmos&lang=ja)                                                                                           | 1    |
| [llama.cpp (DavideWasTaken fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28DavideWasTaken%20fork%29&lang=ja)                                     | 1    |
| [llama.cpp (achyudh Adaptive KV Streaming fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28achyudh%20Adaptive%20KV%20Streaming%20fork%29&lang=ja) | 1    |
| [llama.cpp (mirai-s fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28mirai-s%20fork%29&lang=ja)                                                   | 1    |
| [llama.cpp (pentacoxian_dev fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28pentacoxian_dev%20fork%29&lang=ja)                                   | 1    |
| [llama.cpp (pinkmanwest fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28pinkmanwest%20fork%29&lang=ja)                                           | 1    |
| [llama.cpp (tandem.cpp fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28tandem.cpp%20fork%29&lang=ja)                                             | 1    |
| [llama.cpp (vahpetr fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28vahpetr%20fork%29&lang=ja)                                                   | 1    |
| [lxe Rust/CUDA runner](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=lxe%20Rust/CUDA%20runner&lang=ja)                                                               | 1    |
| [mflux](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=mflux&lang=ja)                                                                                                 | 1    |
| [moe-cache](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=moe-cache&lang=ja)                                                                                         | 1    |
| [moex](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=moex&lang=ja)                                                                                                   | 1    |
| [pulsar-inference-stack](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=pulsar-inference-stack&lang=ja)                                                               | 1    |
| [qwen38-megakernel](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=qwen38-megakernel&lang=ja)                                                                         | 1    |
| [rec](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=rec&lang=ja)                                                                                                     | 1    |
| [spark-ds41f](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=spark-ds41f&lang=ja)                                                                                     | 1    |
| [spark-engine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=spark-engine&lang=ja)                                                                                   | 1    |
| [sparkinfer](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=sparkinfer&lang=ja)                                                                                       | 1    |
| [sushi](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=sushi&lang=ja)                                                                                                 | 1    |
| [webyIQ](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=webyIQ&lang=ja)                                                                                               | 1    |
| [Unspecified](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Unspecified&lang=ja)                                                                                     | 82   |

<p align="center"><img src="docs/budget-tiers.ja.png" width="860" alt="棒グラフ：予算帯ごとの最速テキスト構成（実測と公称）"></p>


## 第 1 段階 · 2,500 ドルまで

*中古の 3090/4090、MI50/V100、Strix Halo、R9700* · 70 件


**📝 テキスト**

- **Bonsai-8B** · llama.cpp (PrismML fork) `1-bit Q1_0` — RTX 4090 → **368 tok/s** 📣 [出典](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
- **Qwen3.8-27B** · tqLLM `TQ3_4S-v2 · DFlash2` — RTX 3090 24GB → **273 tok/s** 🏛️ [出典](https://x.com/coffeecup2020/status/2110624499901075769)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 4090 24GB → **225 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-Flash-Next** · Strata `Strata· Swift 1.5 IQ2_XS` — RTX 4090 24GB + 32GB DDR5 → **220 tok/s** 📣 [出典](https://x.com/Knuckles_XBT/status/2105245662657011841)
- **Qwen3.8-27B** · Geezuz `Q4_K_M` — 2× RTX 3090 → **190 tok/s** ✅ [出典](https://github.com/ohgeebtw/geezuz-qwen3.8-27b-dual-gpu)
- **Recursive Flint 40B-A2.5B** · llama.cpp `NVFP4 GGUF` — RTX 4090 24GB → **179.4 tok/s** ✅ [出典](https://llm-speed.com/m/flint-40b-a2-5b)
- **Qwen3.8-27B** · tqLLM `TQ_XS· DFlash2` — RTX 5060 Ti 16GB → **175.9 tok/s** 🏛️ [出典](https://x.com/coffeecup2020/status/2110719638518526343)
- **Qwen3.6-35B-A3B** · FreeToken `FreeToken · NVFP4` — RTX 4090 → **167 tok/s** 🔁 [出典](https://x.com/shipfrontierai/status/2092602493213577481)
- **LFM2.5-24B-A2B** · llama.cpp `Q4` — RTX 5060 Ti 16GB → **162 tok/s** ✅ [出典](https://x.com/niklaslenz_ai/status/2110469931011612895)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 3090 24GB → **154 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- *…ほか 51 件は[エクスプローラー](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja)で。*

**🖼️ 画像**

- **Qwen-Image 2.1** · ComfyUI `Comfy-Org INT8 · ComfyUI` — RTX 4090 24GB → 8.1 s / 1024² (40 steps); 30.2 s / 2048×1152 (50 steps); peak 16.2GB ✅ [出典](https://x.com/yume_arasaki/status/2102176739359404499) · [手順](recipes/image-001.ja.md)
- **Qwen-Image 2.1** `INT8` — RTX 3090 → 82–96 s / 2K (public receipt) 🔁 [出典](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1** · ComfyUI `ComfyUI` — Mac M4 Pro → 3 min 52 s / image (768 edit) ✅ [出典](https://x.com/gabeciii/status/2116171024106401889)
- **Z-Image Turbo** · ComfyUI `ComfyUI` — RTX 3090 24GB → 2048px about 8 s / image; another user 12 s after warm-up ✅ [出典](https://x.com/michaelricks/status/2104959036353356058)

**🎬 動画・音声**

- **FastH3 V2 / Trim** `FP8` — RTX 4090 24GB → 480p 5s: 54.6 / 43.9 s; 768p: 154.6 / 132.8 s; 8GB limit Trim 82.0 s 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 4090 → 5 s clip ~91 s; 15 s ~8 minutes; 960×544×5s about 50 s ✅ [出典](https://x.com/yume_arasaki/status/2097790831323427046)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 3090 → 11 s video 13 minutes ✅ [出典](https://x.com/natehalko/status/2103538997146611890)
- **ACE-Step 1.5** — RTX 3090 → Whole song <10 s (promo post) 🔁 [出典](https://x.com/simplifyinAI/status/2091935190335754493)
- **MiniMax H3 Ref2VA** · ComfyUI `INT8 DiT+ NVFP4 + Turbo 4-s…` — RTX 4090 24GB → 1344×768×5.16s (24 fps / 124 frames): warm wall time ~72 s (first run… 🏛️ [出典](https://github.com/Kablex/ComfyUI-Ref2VA-VSA)

## 第 2 段階 · 2,500〜7,000 ドル

*RTX 5090 1 枚、DGX Spark 1 台、Mac Studio Max* · 170 件


**📝 テキスト**

- **Qwen3.6-35B-A3B** · sparkinfer `sparkinfer v0.4.4` — RTX 5090 → **512 tok/s** 📣 [出典](https://x.com/kysstalol/status/2105042922643321008)
- **LFM2.5-24B-A2B** · llama.cpp `Q4` — RTX 5090 32GB → **351.5 tok/s** ✅ [出典](https://x.com/niklaslenz_ai/status/2110469931011612895)
- **NVIDIA Nemotron 3.5 Bolt 74B-A9B** · llama.cpp `NVIDIA IQ2_XXS 24GB GGUF + …` — RTX 5090 32GB → **343 tok/s** ✅ [出典](https://www.reddit.com/r/LocalLLM/comments/1xap599/)
- **gpt-oss-20b** · llama.cpp `Q4_K_M` — RTX 5090 32GB → **324.2 tok/s** ✅ [出典](https://llm-speed.com/r/r_dwp5fgdapmw)
- **Qwen3-Coder-30B-A3B-Instruct** · llama.cpp `Q4_K_M` — RTX 5090 32GB → **304.9 tok/s** ✅ [出典](https://llm-speed.com/r/r_vsype4pm1ko)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 5090 32GB → **283 tok/s** 📣 [出典](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2) · [手順](recipes/hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.ja.md)
- **Qwen3.8-Flash-Next** · Basalt `NVIDIA NVFP4+ KV` — RTX 5090 32GB + Core Ultra 9 285K + 247GB DDR5 → **242 tok/s** ✅ [出典](https://www.reddit.com/r/LocalLLaMA/comments/1xcp0mf/)
- **Qwen3.8-Flash-Next** · Strata `ISTA-DASLab GSQ-RCO IQ3_S` — RTX 5090 32GB + 121GB DDR5 → **240 tok/s** ✅ [出典](https://x.com/lyesbahi/status/2113602136051458520)
- **Qwen3.8-Flash-Next** · vLLM `Intel W4A16-AutoRound + MTP` — 2× CMP 170HX+ 93GB RAM + NVMe → **226.2 tok/s** ✅ [出典](https://github.com/AlexBrandes/cmp170hx-qwen38-flash-next)
- **MiniCPM-V 4.7 35B-A3B** · llama.cpp `Q4_K_M` — RTX 5090 → **208 tok/s** ✅ [出典](https://x.com/Blackwellboy/status/2110717843121881380)
- *…ほか 142 件は[エクスプローラー](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja)で。*

**🖼️ 画像**

- **Qwen-Image 2.1** `LightX2V / BennyDaBall NVFP…` — RTX 5090 32GB → 5.93 s; NVFP4 6.7 s vs INT8 7.6 s vs BF16 15.6 s (1024²) 🔁 [出典](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image 2.1** · TensorFold `TensorFold NVFP4 / FP8 / GG…` — RTX 5090 @450W → 4.53 s / 6.94 s / 13.87 s (1024², 25 steps; NVFP4 peak 22.9GB; images… ✅ [出典](https://x.com/niklaslenz_ai/status/2106465941177487871)
- **Qwen-Image 2.1** — RTX 5090 → 13.5 s → 1.9 s / image (vendor claim) 📣 [出典](https://x.com/fractalyze_io/status/2105207217452695841)
- **Qwen-Image 2.1** · SGLang `spark-image-lab BF16 / SGLa…` — 1× DGX Spark → 52.6 s / 1024²; SGLang table: Spark 35.4 s, 4090 18.7 s 🔁 [出典](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image-2.1-Turbo** `Turbo 8 vs Base 40` — RTX 5090 → 29 s vs 108 s / image (2048²) ✅ [出典](https://x.com/niklaslenz_ai/status/2108609693941920176)
- **Z-Image Turbo vs Qwen-Image 2.1** `prompt seed 20` — RTX 5090 → Z-Image ~2× faster (no absolute times); quality: Qwen wins 9:6 ✅ [出典](https://x.com/princedoesai/status/2109376490009743713)

**🎬 動画・音声**

- **FastH3 V2** `NVFP4` — RTX 5090 32GB → 832×480×5s: 14.8 s; 1344×768×5s: 38.6 s (with audio, end-to-end) 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/) · [手順](recipes/video-audio-001.ja.md)
- **FastH3 Trim** `NVFP4` — RTX 5090 → 480p 5s: 13.4 s; 768p: 35.4 s 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 V2 / Trim** `NVFP4` — 1× / 2× DGX Spark → 1×: 480p 141.4 / 125.8 s, Trim 768p 340.1 s; 2×: 87.2 / 78.3 s 🏛️ [出典](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3** · ComfyUI `ComfyUI + SageAttention` — RTX 5090 → 1280×736×5s: 242 s → 168 s ✅ [出典](https://x.com/RKAScope/status/2084359480926503182)
- **MiniMax H3 vs FastH3 Turbo** `seed` — RTX 5090 → 15 s clip: 11 min 55 s vs 2 min 6 s ✅ [出典](https://x.com/Sogni_Protocol/status/2097254959729246550)
- **MiniMax H3** · NVIDIA Sol `NVIDIA Sol` — 1× DGX Spark → Sol: 480p 5 s ≈ 68 s (NVIDIA published 56 s); without Sol >400 s; wit… ✅ [出典](https://x.com/yume_arasaki/status/2100734364908986511)
- **MiniMax H3 vs LTX-2.3 Eros** `3 prompt` — 1× DGX Spark → 864×480×5s: H3 average 270 s; LTX 154 s (1.76× faster) ✅ [出典](https://x.com/YRSM_Simon/status/2084222856972456336)
- **LTX-2.3** · ComfyUI `ComfyUI` — RTX 5090 → 10 s about 90 s (weaker GPU about 6×) ✅ [出典](https://x.com/freshstartsnow/status/2092263835591655773)
- **LTX-2.5** `LoRA` — RTX 5090 → 720p/10 s: 61.11 s; 1080p/10 s: 189.90 s ✅ [出典](https://x.com/PhotogenicWeekE/status/2087298681137701274)
- **ACE-Step 1.5 + LTX-2.3** · ComfyUI `ComfyUI` — 1× DGX Spark → 2 min 05 s song generated in one pass; +2:28 lip-sync video end to en… 🔁 [出典](https://x.com/yume_arasaki/status/2100734364908986511)
- **Wan2.1 14B** `97% + 3 + FP8` — RTX 5090 → 720p: 4,769 s → 18 s (project claims 265×) 📣 [出典](https://x.com/thePandaily/status/2105209996648567243)
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s video + audio ≈72 s (steady state, excl. MP4 export; bas… 🏛️ [出典](https://x.com/LightX2V/status/2108769912009424976)

## 第 3 段階 · 7,000〜14,000 ドル

*DGX Spark 2 台、Mac Studio Ultra* · 63 件


**📝 テキスト**

- **Qwen3.8-27B** · TensorFold `3.0bpw EXL3 + DFlash2` — 2× DGX Spark → **190 tok/s** ✅ [出典](https://x.com/BHCC2025/status/2117272695637443025)
- **Qwen3.8-27B** · vLLM `NVFP4` — 2× RTX 5090 → **160 tok/s** 📣 [出典](https://www.reddit.com/r/LocalLLM/comments/1x5u4yf/comment/pgqv4uy/)
- **Qwen3.8-Flash-Next** · oMLX `unsloth UD-Q6_K_XL` — Mac Studio M5 Ultra 256GB → **141 tok/s** ✅ [出典](https://www.reddit.com/r/LocalLLaMA/comments/1xdp654/)
- **Qwen3.8-Flash-Next 4/8-bit** · mlx-serve `4/8-bit mixed` — Mac Studio M5 Ultra 256GB → **126 tok/s** ✅ [出典](https://x.com/LocalSilicon/status/2106175358160793817)
- **DeepSeek-V4.1-Flash** · TensorFold — 2× DGX Spark → **95 tok/s** ✅ [出典](https://x.com/Urthoo/status/2106426248759005362)
- **Qwen3.8-Flash-Next** · vLLM `nvidia FP4-Local + MTP 4` — 2× DGX Spark → **95 tok/s** 🏛️ [出典](https://github.com/atakann/dgx-spark-recipes/blob/8a15075/recipes/llm/qwen3.8-flash-next-fp4-vllm-tp2.yaml)
- **DeepSeek-V4.1-Flash-1017** · TensorFold `MiaAI EXL3 2.9bpw+ DSpark` — 2× DGX Spark → **88.7 tok/s** ✅ [出典](https://x.com/atasrb/status/2113681338532253775)
- **GLM-5.3-Flash** · TensorFold `MiaAI_lab EXL3 4 bpw` — 2× DGX Spark → **83 tok/s** ✅ [出典](https://x.com/atasrb/status/2117267112464925027)
- **DeepSeek-V4-Flash (0731 GA)** `FP8` — 2× DGX Spark → **82 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2083326111144906836)
- **Ling-3.0-flash** · SGLang `FP8 + FP8 lm_head + MTP3` — 2× DGX Spark → **82 tok/s** ✅ [出典](https://x.com/atasrb/status/2116085996965990514)
- *…ほか 53 件は[エクスプローラー](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja)で。*

## 第 4 段階 · 14,000〜30,000 ドル

*Spark 3〜4 台のクラスター、マルチ GPU ワークステーション* · 36 件


**📝 テキスト**

- **Qwen3.8-27B** · SGLang `NVFP4` — RTX PRO 6000 → **300 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2090327658508763516)
- **Qwen3.8-Flash-Next** · TensorFold `NVIDIA FP4 + MTP KV` — 1× RTX PRO 6000 Blackwell 96GB → **271.4 tok/s** ✅ [出典](https://x.com/MiaAI_lab/status/2117202027226783782)
- **Recursive Flint 40B-A2.5B** · llama.cpp `Q8_0 GGUF` — 1× RTX PRO 6000 Blackwell 96GB → **244 tok/s** ✅ [出典](https://www.reddit.com/r/nvidia/comments/1xd0f7x/)
- **Swift-1.5-Qwen3.8-Flash-Next** · ninfer `NVFP4+FP8 · MTP 3` — RTX PRO 6000 Blackwell 96GB @ 600W + 96GB DDR4 + Ryzen 5 56… → **238 tok/s** ✅ [出典](https://demietrich.com/blog/q3.8fn_engine_comparison/)
- **Qwen3.8-Flash-Next** · SGLang (Penny Royal fork) — 1× RTX PRO 6000 Blackwell 96GB → **200 tok/s** ✅ [出典](https://x.com/jhsmith409/status/2117236468871569860)
- **Qwen3.8-Flash-Next** · vLLM `NVFP4 · MTP 2` — RTX PRO 6000 Blackwell 96GB @ 600W + 96GB DDR4 + Ryzen 5 56… → **150 tok/s** ✅ [出典](https://demietrich.com/blog/q3.8fn_engine_comparison/)
- **DeepSeek-V4.1-Flash-1017** · spark-ds41f `1017` — 4× DGX Spark → **136 tok/s** ✅ [出典](https://x.com/machigurixmeru/status/2116835181558694130)
- **DeepSeek-V4.1-Flash-1017** · TensorFold `LakyFx EXL3 3.5bpw` — 3× DGX Spark → **126.1 tok/s** ✅ [出典](https://x.com/laky_fx/status/2113654994847117605)
- **DeepSeek-V4.1-Flash-1017** · TensorFold — 4× GB10 → **121 tok/s** 🏛️ [出典](https://x.com/bertholomusai/status/2113835774873600136)
- **DeepSeek-V4.1-Flash** · TensorFold — 4× DGX Spark → **111 tok/s** ✅ [出典](https://x.com/kevintheoo/status/2114654160293433558)
- *…ほか 26 件は[エクスプローラー](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja)で。*

## 価格非公開

1 枚単位で価格が出ているマルチ GPU 構成、メモリ（＝価格）が不明な Mac など、単一の公開価格がないレシピ · 456 件。tok/s 上位のテキストレシピ：

- **Qwen3.6-35B-A3B** · SGLang `NVFP4` — 1× RTX 5090 → **626 tok/s** 🏛️ [出典](https://github.com/jhsmith409/sglang-elsa)
- **Qwen3.5-2B** · webyIQ `int4 1.1GB` — RTX 5080 → **620 tok/s** 📣 [出典](https://www.reddit.com/r/LocalLLM/comments/1xmcqkb/)
- **Qwen3.8-27B** · TensorFold `z-lab DFlash2` — 1× RTX 5090 → **538.1 tok/s** ✅ [出典](https://x.com/BobClawblaw/status/2114570274511405354)
- **Gemma 4 31B** · Radiance `W4A8 + DFlash2 block-16` — 4× Radeon AI PRO R9700 32GB → **445.8 tok/s** 📣 [出典](https://codeberg.org/StillDeadcode/radiance/issues/248)
- **LFM3-1.7B** · llama.cpp — RTX 3090 24GB → **384 tok/s** ✅ [出典](https://x.com/Layton_Gott/status/2115244678056464384)
- **Gemma 4 31B** · Radiance `W4A8 + RedHatAI DFlash2` — 4× Radeon AI PRO R9700 32GB → **377.7 tok/s** 📣 [出典](https://codeberg.org/StillDeadcode/radiance/issues/247)
- **Qwen3.8-Flash-Next** · QEngine `INT4 AutoRound` — 2× RTX 5090 32GB + Threadripper PRO 3975WX + 251GB RAM → **370 tok/s** ✅ [出典](https://www.reddit.com/r/LocalLLaMA/comments/1xjx0ez/)
- **Qwen3.8-Flash-Next** · Basalt `NVIDIA NVFP4` — 1× RTX 5090+ 128GB RAM → **354 tok/s** 🏛️ [出典](https://www.reddit.com/r/LocalLLaMA/comments/1xdlunp/)
- **Qwen3.6-35B-A3B** · Kapitsa `Q4 + KFlash` — MacBook Pro 16 M5 Max 128GB → **346 tok/s** 📣 [出典](https://www.reddit.com/r/LocalLLaMA/comments/1xlgu8m/)
- **Qwen3.8-Flash-Next** · Basalt `Basalt NVFP4-DQ8` — RTX 5090 32GB + RTX 5060 Ti 16GB + 128GB RAM → **300 tok/s** 📣 [出典](https://www.reddit.com/r/LocalLLaMA/comments/1xn4qn1/)
- **Qwen3.8-Flash-Next** · vLLM `nvidia 4` — 1× RTX PRO 6000 Blackwell 96GB → **287 tok/s** ✅ [出典](https://www.reddit.com/r/LocalLLM/comments/1xj9ura/)
- **Qwen3.8-Flash-Next** · Strata `Q2_0` — RTX 5090 + Ryzen 9 9950X → **270.7 tok/s** ✅ [出典](https://github.com/Niko1221/Strata/issues/4166)
- *…全 456 件は[エクスプローラー](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=ja)で見られます。*


## エンジンとツール

| プロジェクト                                                             | ⭐ Star | ライブ                                                                                             | 最終 push    | 概要                                                                                                                                       |
| ------------------------------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [llama.cpp](https://github.com/ggml-org/llama.cpp)                 | 132.8k | ![stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat&label=)              | 2026-10-30 | GGUF の定番エンジン（CPU/CUDA/ROCm/Vulkan/Metal）。                                                                                                |
| [vLLM](https://github.com/vllm-project/vllm)                       | 95.9k  | ![stars](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&label=)               | 2026-10-30 | 高スループットな推論サーバー。Spark での MTP や同時実行のレシピに使われています。                                                                                           |
| [SGLang](https://github.com/sgl-project/sglang)                    | 38.3k  | ![stars](https://img.shields.io/github/stars/sgl-project/sglang?style=flat&label=)              | 2026-10-30 | 推論サービング用フレームワーク。DGX Spark で DFlash2 と組み合わせて使われています。                                                                                      |
| [Strata](https://github.com/Niko1221/Strata)                       | 36.3k  | ![stars](https://img.shields.io/github/stars/Niko1221/Strata?style=flat&label=)                 | 2026-10-29 | MoE のエキスパートを VRAM・RAM・SSD に分けて載せる推論エンジン。12〜24GB の GPU 向けで、ここの Flash-Next レシピの多くが使っています。0.2.8 から、12GB 以下の RTX カードでは route prior が既定でオフです。 |
| [MLX](https://github.com/ml-explore/mlx)                           | 29.0k  | ![stars](https://img.shields.io/github/stars/ml-explore/mlx?style=flat&label=)                  | 2026-10-30 | Apple の配列フレームワーク。Mac のレシピの多くはこれがベース。                                                                                                     |
| [ds4 (DwarfStar)](https://github.com/antirez/ds4)                  | 24.2k  | ![stars](https://img.shields.io/github/stars/antirez/ds4?style=flat&label=)                     | 2026-10-23 | DeepSeek 4 Flash/PRO 向けのローカル推論エンジン。Metal・CUDA・ROCm に対応。                                                                                  |
| [oMLX](https://github.com/jundot/omlx)                             | 23.2k  | ![stars](https://img.shields.io/github/stars/jundot/omlx?style=flat&label=)                     | 2026-10-30 | Apple Silicon 向けの MLX サーバー。連続バッチ処理と、KV/SSD の階層キャッシュに対応。                                                                                  |
| [WebLLM](https://github.com/mlc-ai/web-llm)                        | 19.3k  | ![stars](https://img.shields.io/github/stars/mlc-ai/web-llm?style=flat&label=)                  | 2026-10-30 | WebGPU を使ってブラウザ内で LLM を動かす。                                                                                                              |
| [MNN](https://github.com/alibaba/MNN)                              | 16.3k  | ![stars](https://img.shields.io/github/stars/alibaba/MNN?style=flat&label=)                     | 2026-10-30 | Alibaba のオンデバイス推論エンジン。スマホやエッジ機器で LLM を動かす。                                                                                               |
| [turbo-fieldfare](https://github.com/drumih/turbo-fieldfare)       | 7.1k   | ![stars](https://img.shields.io/github/stars/drumih/turbo-fieldfare?style=flat&label=)          | 2026-10-26 | M シリーズの MacBook で約 2GB のメモリで Gemma 4 26B-A4B を動かす（プロジェクトの説明）。                                                                            |
| [DFlash / DFlash 2](https://github.com/z-lab/dflash)               | 6.2k   | ![stars](https://img.shields.io/github/stars/z-lab/dflash?style=flat&label=)                    | 2026-08-18 | ブロック拡散による投機的デコーディング。DFlash 2 は Qwen3.8-27B 用のドラフトモデルを提供。                                                                                 |
| [Lemonade](https://github.com/lemonade-sdk/lemonade)               | 6.0k   | ![stars](https://img.shields.io/github/stars/lemonade-sdk/lemonade?style=flat&label=)           | 2026-10-30 | AMD Ryzen AI の NPU/iGPU などで動くローカル LLM サーバー。                                                                                              |
| [FastVideo](https://github.com/hao-ai-lab/FastVideo)               | 4.8k   | ![stars](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=flat&label=)            | 2026-10-30 | 加速動画生成の統一推論・後学習フレームワーク。VSA / FastH3 の上流。                                                                                                 |
| [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX)              | 4.1k   | ![stars](https://img.shields.io/github/stars/raullenchai/Rapid-MLX?style=flat&label=)           | 2026-10-30 | Apple Silicon 向けの OpenAI/Anthropic 互換 MLX サーバー。MTP デコードと公開コミュニティベンチマークボードあり。                                                             |
| [LightX2V](https://github.com/ModelTC/LightX2V)                    | 3.0k   | ![stars](https://img.shields.io/github/stars/ModelTC/LightX2V?style=flat&label=)                | 2026-10-30 | 動画生成の推論フレームワーク。RTX 5090 での MiniMax H3 の結果あり。                                                                                             |
| [Project Maya](https://github.com/mw00/project-maya)               | 2.3k   | ![stars](https://img.shields.io/github/stars/mw00/project-maya?style=flat&label=)               | 2026-10-30 | GLM-5.3-Flash（リポジトリ表記は 321B MoE）を NVIDIA/AMD の GPU 1〜16 枚で動かす。エンジン・サーバー・ダッシュボード・量子化ツール付き。                                                |
| [mlx-serve](https://github.com/ddalcu/mlx-serve)                   | 2.2k   | ![stars](https://img.shields.io/github/stars/ddalcu/mlx-serve?style=flat&label=)                | 2026-10-30 | Apple Silicon ネイティブの LLM サーバー（Zig バックエンド＋Swift フロントエンド）。OpenAI/Anthropic API 互換で Python 不要。                                              |
| [TensorFold](https://github.com/ashhart/TensorFold)                | 1.5k   | ![stars](https://img.shields.io/github/stars/ashhart/TensorFold?style=flat&label=)              | 2026-10-30 | OpenAI 互換 API の MoE ランタイム。投機的デコーディング付きで、ComfyUI の MiniMax H3 にも使われています。現行版は 1.1.9（2026-10-29）。コミット 3abeeff でプロンプトキャッシュのバグを修正。            |
| [halogen](https://github.com/peonist-ai/halogen-flash-server)      | 1.1k   | ![stars](https://img.shields.io/github/stars/peonist-ai/halogen-flash-server?style=flat&label=) | 2026-10-30 | Strix Halo 向けにチューニングされた Flash-Next サーバー。                                                                                                 |
| [ComfyUI-Ref2VA-VSA](https://github.com/Kablex/ComfyUI-Ref2VA-VSA) | 878    | ![stars](https://img.shields.io/github/stars/Kablex/ComfyUI-Ref2VA-VSA?style=flat&label=)       | 2026-10-17 | ComfyUI ノード：FastVideo の VSA ゲートを MiniMax H3 Ref2VA に移植。作者 RTX 4090 基準はネイティブ約 650s（50 ステップのデンス）→ ウォームアップ約 72s（4 ステップ VSA+Turbo）。          |
| [dflash-mlx](https://github.com/bstnxbt/dflash-mlx)                | 791    | ![stars](https://img.shields.io/github/stars/bstnxbt/dflash-mlx?style=flat&label=)              | 2026-08-20 | Apple Silicon（MLX）で動く DFlash 投機的デコーディング。                                                                                                 |
| [VDN-H3](https://github.com/OpenVDN/vdn-minimax-h3)                | 659    | ![stars](https://img.shields.io/github/stars/OpenVDN/vdn-minimax-h3?style=flat&label=)          | 2026-10-05 | MiniMax H3 向け Video Delta Net ハイブリッド注意（窓付き softmax + 線形アダプタ）。T2VA / I2VA / Ref2VA 系。                                                     |
| [janas](https://github.com/prabanta-dev/janas)                     | 478    | ![stars](https://img.shields.io/github/stars/prabanta-dev/janas?style=flat&label=)              | 2026-10-30 | 純 C 製の推論エンジン。RAM より大きいモデルを CPU/GPU で実行。32GB ノートで Qwen3-Next-80B が 37 tok/s（ドラフト使用）とプロジェクトは説明。                                            |
| [ComfyUI-VDN-H3](https://github.com/Saganaki22/ComfyUI-VDN-H3)     | 243    | ![stars](https://img.shields.io/github/stars/Saganaki22/ComfyUI-VDN-H3?style=flat&label=)       | 2026-09-12 | MiniMax H3 向け VDN-H3 ハイブリッド注意の ComfyUI ノード。                                                                                              |
| [Paiton](https://github.com/Eliovp-BV/paiton-vllm-plugin)          | 108    | ![stars](https://img.shields.io/github/stars/Eliovp-BV/paiton-vllm-plugin?style=flat&label=)    | 2026-10-30 | R9700 などの AMD Radeon カード向けに調整した vLLM プラグインとランタイム。                                                                                        |
| [Halowin Bubo](https://github.com/haloforge-labs/bubo)             | 18     | ![stars](https://img.shields.io/github/stars/haloforge-labs/bubo?style=flat&label=)             | 2026-10-27 | Gufo のフォーク。ネイティブ Windows で AMD HIP を使い、Strix Halo ノート向けに調整。                                                                              |
| [libstrix](https://github.com/asf0/libstrix)                       | 7      | ![stars](https://img.shields.io/github/stars/asf0/libstrix?style=flat&label=)                   | 2026-10-30 | AMD Strix Halo（gfx1151）向けの HIP カーネルと vLLM プラグイン。上流の vLLM で動きます。                                                                          |
| [FastH3](https://haoailab.com/blogs/fasth3-rtx/)                   | —      | *（サイト・ブログ）*                                                                                     | —          | Hao AI Lab による 8 ステップ蒸留版 MiniMax H3。RTX 向け（ブログ）。                                                                                         |
| [Espetero](https://github.com/JarJarFran/espetero)                 | 0      | ![stars](https://img.shields.io/github/stars/JarJarFran/espetero?style=flat&label=)             | 2026-10-27 | Apple Silicon 向けのネイティブ Metal 推論エンジン。OpenAI・Anthropic・Ollama 互換 API を提供。                                                                  |
| [Strim](https://github.com/megasoft1978/strim-engine)              | 0      | ![stars](https://img.shields.io/github/stars/megasoft1978/strim-engine?style=flat&label=)       | 2026-10-30 | Apple Silicon で Qwen3.8-27B を動かす Swift/MLX エンジン。速度の数値は作者自身によるもの。                                                                         |

<sub>⭐ スナップショットは `scripts/update_stars.py` で 2026-10-30T13:41Z（UTC）に更新 · 「ライブ」バッジは表示時に shields.io が描画します。</sub>

## 関連リスト・ベンチマーク

| プロジェクト                                                                      | ⭐ Star | ライブ                                                                                             | 最終 push    | 概要                             |
| --------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------- | ---------- | ------------------------------ |
| [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference) | 5.5k   | ![stars](https://img.shields.io/github/stars/xlite-dev/Awesome-LLM-Inference?style=flat&label=) | 2026-10-20 | 推論分野の論文とコードのまとめ。               |
| [awesome-local-llm](https://github.com/rafska/awesome-local-llm)            | 3.0k   | ![stars](https://img.shields.io/github/stars/rafska/awesome-local-llm?style=flat&label=)        | 2026-10-28 | ローカル LLM のプラットフォームとツールのまとめ。    |
| [LocalScore](https://github.com/cjpais/LocalScore)                          | 136    | ![stars](https://img.shields.io/github/stars/cjpais/LocalScore?style=flat&label=)               | 2026-10-09 | 1 GPU 向けの標準化されたベンチマーク CLI。     |
| [llamabench.ai](https://llamabench.ai/)                                     | —      | *（サイト・ブログ）*                                                                                     | —          | llama.cpp のベンチ結果を、起動コマンド付きで掲載。 |
| [llamaperf](https://llamaperf.com/leaderboard)                              | —      | *（サイト・ブログ）*                                                                                     | —          | コミュニティ投稿のリーダーボード（中央値で表示）。      |
| [canirun.ai](https://canirun.ai/)                                           | —      | *（サイト・ブログ）*                                                                                     | —          | 手持ちのハードでモデルが動くか、どれくらいの速度かを推定。  |

<sub>⭐ スナップショットは `scripts/update_stars.py` で 2026-10-30T13:41Z（UTC）に更新 · 「ライブ」バッジは表示時に shields.io が描画します。</sub>

## コントリビュート

1 レシピにつき 1 PR でお願いします。[投稿ページ](https://raytone-lab.github.io/awesome-local-inference-recipes/submit.html?lang=ja)の YAML テンプレートをコピーし、出典に書かれている内容だけを埋めてください（それ以外は `null`）。`node scripts/validate.mjs` でチェックし、元の投稿へのリンクを添えてください。その後 `python3 scripts/gen_readme.py` で README をすべて再生成します。新しいモデルや新しいハードウェアの発売後数週間以内のレシピと、主流ではない組み合わせを優先して収録します。定型の重複レシピは既存のエントリに統合します。詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

ローカル開発：`python3 -m http.server 5190` → `index.html`（トップ）· `explore.html`（絞り込み・並べ替え・散布図）· スキーマは [`schema/recipe.schema.json`](schema/recipe.schema.json)。

AI エージェント向け：スキル [`.agents/skills/local-inference-recipe-finder`](.agents/skills/local-inference-recipe-finder/SKILL.md) がハードウェアを検出し、[`data/hw_index.json`](docs/hw_index.md) からレシピを推薦します。詳しくは [AGENTS.md](AGENTS.md) を参照。

<details><summary>サイトのプレビュー</summary>

<img src="docs/screenshot.ja.png" width="760" alt="サイトのトップページ：レシピ数、エンジン数、実測数、予算帯ごとの最速の実測構成">

</details>

## ライセンス

- コード：[MIT](LICENSE)
- データ（`data/`）：[CC BY 4.0](LICENSE-DATA)。Awesome Local Inference Recipes と、各レシピに記載された元の出典を明記すれば自由に再利用できます。
