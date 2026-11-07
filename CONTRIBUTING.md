# Contributing / 贡献指南

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) first. · [中文](#中文) · [日本語](#日本語)

## Scope

This list is for setups that one person, a home or office desktop user, or a small studio can build. Datacenter setups are out of scope. Used datacenter cards in a desktop PC are in scope. A setup is in scope only when it meets all of these conditions:

- The hardware costs $30,000 or less.
- It uses at most 4 machines. Budget is the main limit: a multi-machine setup, or a setup with more than 4 GPUs in total, is in scope when the hardware cost stays at $30,000 or less. Example: 2 machines with 4× RTX 3060 each (8 GPUs in total) are in scope when they stay under budget.
- It runs on ordinary home or office power: about 2 kW in total, from up to two ordinary outlets, with no special wiring. If you use two outlets, put them on separate circuits. One US 120 V / 15 A circuit gives about 1.44 kW continuous. One Japanese 100 V / 15 A outlet is rated at about 1.5 kW.
- It uses no rack, no SXM or HGX server board, no custom liquid-cooling loop and no server liquid cooling. A DIY SXM2-to-PCIe adapter build that fits in a desktop is in scope. A consumer GPU with a factory all-in-one (AIO) liquid cooler is in scope.
- It uses at most one desktop-class network switch.
- It uses no modded GPU. A modded GPU has changed hardware, for example changed memory. Examples are an RTX 4090D with 48GB memory and a CMP 170HX with changed memory. Recipes for modded GPUs that are already in the list stay until a later review. A stock GPU with a firmware or driver unlock is in scope, for example the gpu-unlock kernel module that removes the FP16 limit on Ampere cards. These recipes get the `gpu-unlock` tag.

A setup that fails one condition is out of scope, even when it costs less than $30,000. We record the price on the date that we add the recipe. When the price goes up later, we update only the price note (`hardware_cost_text`). We do not remove the recipe.

`python3 scripts/scope_rules.py` lists the recipes that fail the cost or hardware-type check. Reviewers check the machine count by reading the source. Add `⚠️超$30k` to `hardware_cost_text` when the price on the date of inclusion is over $30,000. This includes a lower bound computed from prices published on that date. Do not add the mark for a later price rise. Reviewers check power and the network switch by reading the source.

## Add a recipe
1. Easiest: open a **[Recipe submission](../../issues/new?template=recipe.yml)** issue. Or fork → branch → append to `data/recipes.json` (fields: `schema/recipe.schema.json`, template: `submit.html`).
2. `node scripts/validate.mjs` must pass (CI runs it on every PR).
3. When you add or change an `engine` value, run `python3 scripts/normalize_engines.py` and `python3 scripts/tag_recipes.py`. Then regenerate the READMEs and site pages: `python3 scripts/gen_all.py`. CI fails when a generated file is not up to date. Maintainers: after a data update, run `python3 scripts/gen_all.py --images` to also render the README charts and the site screenshots. CI does not check the image files.
4. Link the original source; for your own runs include the command and output.
5. No estimates, no invented values: unknown → `null`. Link and summarize, don't copy posts.
6. Source level: official / measured / claimed (see [docs/sources.md](docs/sources.md)). The relayed level applies only to recipes added before rule 7. Some authors test their own engine or recipe. Such a result is measured only when the author publishes the raw benchmark data and the reproduction steps. If one of these is missing, use claimed.
7. Use only an original source. The original source is the post, page, release note or issue from the person or team that ran the test. It must give the measured numbers. Do not use a relayed report (a repost, summary or article that quotes the result of a different person) as the source. If you find a relayed report, find the original source of the relayed report and link that source. If you cannot find an original source with measured numbers, do not add the recipe.
8. Inclusion focus (from 2026-10-27). Add these recipes first. First: a recipe for a new model or new hardware, in the first few weeks after launch. Second: a recipe for a non-mainstream combination. Examples are multi-GPU, multi-machine, AMD and Apple mixed, and budget builds. A routine repeat recipe is a new result for a model × engine × hardware combination that is already in the list. Do not add a routine repeat recipe as a new entry. Merge it into the existing entry: replace the numbers, the source link and the date with the newer ones. The scope rules and rule 7 apply to every recipe.
9. Agents: do not edit `data/hw_index.json` or `.claude/skills/` by hand. `python3 scripts/gen_all.py` writes them. Edit the skill only in `.agents/skills/`. A new download host must go into `data/trusted_domains.json` before the index can show it as a link. See [AGENTS.md](AGENTS.md).

## 中文
### 收录范围

本清单只收个人、家用或办公桌面用户、小型工作室能搭起来的配置。数据中心配置不收录。装在桌面 PC 里的二手数据中心卡可以收录。配置必须同时满足以下条件：

- 硬件总价不超过 3 万美元。
- 整机不超过 4 台。预算是主要限制：多机配置，或合计超过 4 张 GPU 的配置，只要硬件总价不超过 3 万美元，就可以收录。例如：2 台机器各装 4 张 RTX 3060（合计 8 张 GPU），总价在预算内时可以收录。
- 用普通家用或办公室电源即可运行：总功率约 2 kW 以内，最多分接两个普通插座，不需要专门布线。用两个插座时，两个插座要在不同电路上。美国一路 120 V / 15 A 电路持续供电约 1.44 kW；日本一个 100 V / 15 A 插座额定约 1.5 kW。
- 不用机架，不用 SXM 或 HGX 服务器主板，不用分体式水冷或服务器液冷。装得进桌面机箱的 DIY SXM2 转 PCIe 转接方案可以收录。出厂自带一体式水冷（AIO）的消费级显卡可以收录。
- 暂不收录魔改显卡，即改过硬件（例如改过显存）的显卡，例如 48GB 显存的 RTX 4090D、改过显存的 CMP 170HX。库里已有的魔改显卡条目暂时保留，以后再复核。原厂显卡只用固件或驱动解锁时可以收录，例如解除 Ampere 卡 FP16 限速的 gpu-unlock 内核模块。这类条目加 `gpu-unlock` 标签。
- 最多用一台桌面级网络交换机。

不满足任一条件的配置不收录，即使总价低于 3 万美元。价格按收录当天记录。之后涨价时，只更新价格说明（`hardware_cost_text`），不删除条目。

`python3 scripts/scope_rules.py` 会列出未通过价格或硬件类型检查的条目。整机数量由审核人对照来源确认。收录当天的价格超过 3 万美元时，在 `hardware_cost_text` 里加 `⚠️超$30k`。用当天公开价格算出的下限超过 3 万美元时也加。之后涨价不加这个标记。功率和网络交换机由审核人对照来源确认。

### 添加配方
1. 最简单：提一个「Recipe submission」issue；或 Fork 后在 `data/recipes.json` 追加记录。
2. `node scripts/validate.mjs` 必须通过（PR 会自动跑 CI）。
3. 新增或修改 `engine` 时，先运行 `python3 scripts/normalize_engines.py` 和 `python3 scripts/tag_recipes.py`。然后运行 `python3 scripts/gen_all.py` 重新生成三份 README 和网站页面。生成的文件不是最新时，CI 会失败。维护者：每次更新数据后，运行 `python3 scripts/gen_all.py --images`，同时重画 README 图表和网站截图。CI 不检查图片文件。
4. 附原始来源链接；自测请附命令与输出。
5. 不估算、不编造，未知写 `null`；只留链接与摘要。
6. 来源等级：官方 / 实测 / 宣称，详见 [docs/sources.md](docs/sources.md)。「转述」只用于第 7 条之前收录的条目。引擎或配方作者测试自己的引擎或配方时，只有公开原始测试数据和复现步骤才记为实测。缺少其中一项，记为宣称。
7. 只用原始来源。原始来源是做测试的人或团队自己发的帖子、页面、发布说明或 issue，并且要给出实测数字。不要用转述（转发、汇总或引用别人结果的文章）作来源。看到转述时，先找到它的原始来源，再链接原始来源。找不到带实测数字的原始来源时，不收录。
8. 收录重点（2026-10-27 起）。优先收录：新模型或新硬件发布后几周内的配方；非主流组合，例如多卡、多机、AMD 与 Apple 混搭、预算受限的配置。常规重复配方是指：库里已有的「模型 × 引擎 × 硬件」组合的新结果。不要把常规重复配方作为新条目添加。把它合并进已有条目：用较新的数字、来源链接和日期替换旧的。收录范围和第 7 条适用于所有配方。
9. Agent：不要手改 `data/hw_index.json` 和 `.claude/skills/`，它们由 `python3 scripts/gen_all.py` 生成。技能只在 `.agents/skills/` 里修改。新的下载域名要先加入 `data/trusted_domains.json`，索引才会把它显示为链接。详见 [AGENTS.md](AGENTS.md)。

Maintainers: Hugging Face candidate ingestion is described in [docs/sources.md](docs/sources.md).

## 日本語
### 収録範囲

このリストは、個人、家庭やオフィスのデスクトップ利用者、小規模スタジオが組める構成だけを収録します。データセンター構成は対象外です。デスクトップ PC に載せた中古データセンター GPU は対象です。次の条件をすべて満たす構成だけを収録します：

- ハードウェアの合計価格が 3 万ドル以下。
- マシンは 4 台まで。予算が主な制限です。マルチマシン構成や、GPU 合計が 4 枚を超える構成でも、ハードウェア合計が 3 万ドル以下なら収録します。例：マシン 2 台に各 4 枚の RTX 3060（合計 8 枚）は、予算内なら収録対象です。
- 一般的な家庭用・オフィス用の電源で動く：合計約 2 kW 以内で、ふつうのコンセント 2 口までに分けてよく、専用の配線工事は不要。2 口を使うときは、別々の回路のコンセントにする。米国の 120 V / 15 A 回路 1 本は連続で約 1.44 kW、日本の 100 V / 15 A コンセント 1 口は定格で約 1.5 kW。
- ラック、SXM / HGX サーバーボード、カスタムループ水冷、サーバー用液冷を使わない。デスクトップに収まる DIY の SXM2→PCIe 変換構成は対象。メーカー出荷時から簡易水冷（AIO）付きのコンシューマー GPU も対象。
- 改造 GPU は当面対象外。ハードウェアを変更した GPU（例：メモリを変更した GPU）のことです。例：48GB メモリの RTX 4090D、メモリを変更した CMP 170HX。リストにすでにある改造 GPU のレシピは、後の見直しまで残します。市販の GPU にファームウェアまたはドライバーのロック解除だけを使った構成は対象です。例：Ampere カードの FP16 制限を外す gpu-unlock カーネルモジュール。このレシピには `gpu-unlock` タグを付けます。
- ネットワークスイッチはデスクトップ型 1 台まで。

1 つでも満たさない構成は、3 万ドル未満でも対象外です。価格は収録日の価格を記録します。後で値上がりしても、価格メモ（`hardware_cost_text`）だけを更新し、レシピは削除しません。

`python3 scripts/scope_rules.py` は、価格またはハードウェア種別のチェックに通らないレシピを一覧表示します。マシン台数は、レビュー担当者が出典を読んで確認します。収録日の価格が 3 万ドルを超えるときは、`hardware_cost_text` に `⚠️超$30k` を付けます。収録日の公開価格から計算した下限が 3 万ドルを超えるときも付けます。後の値上がりでは付けません。電力とネットワークスイッチは、レビュー担当者が出典を読んで確認します。

### レシピの追加
1. いちばん簡単なのは「Recipe submission」の issue を立てることです。または Fork して `data/recipes.json` に追記してください。
2. `node scripts/validate.mjs` が通ること（PR では CI が自動で実行します）。
3. `engine` を追加・変更したときは、先に `python3 scripts/normalize_engines.py` と `python3 scripts/tag_recipes.py` を実行してください。次に `python3 scripts/gen_all.py` で 3 つの README とサイトのページを再生成してください。生成ファイルが最新でないと CI が失敗します。メンテナー：データを更新したら `python3 scripts/gen_all.py --images` を実行し、README のグラフとサイトのスクリーンショットも描き直してください。CI は画像ファイルを確認しません。
4. 元の出典へのリンクを付けてください。自分で計測した場合はコマンドと出力も。
5. 推定や創作はしないでください。不明な値は `null` に。投稿の全文転載はせず、リンクと要約だけにします。
6. 出典レベル：公式 / 実測 / 主張（[docs/sources.md](docs/sources.md) を参照）。「伝聞」は第 7 項より前に収録したレシピだけに使います。エンジンまたはレシピの作者が自分のエンジンまたはレシピを計測した場合、生のベンチマークデータと再現手順を公開したときだけ実測にします。どちらかがない場合は主張にします。
7. 元の出典だけを使ってください。元の出典とは、テストを実行した人またはチームが自分で出した投稿、ページ、リリースノート、issue で、計測した数値を示すものです。伝聞（他の人の結果を引用した再投稿、まとめ、記事）を出典にしないでください。伝聞を見つけたら、その元の出典を探し、元の出典にリンクしてください。計測した数値のある元の出典が見つからないときは、収録しません。
8. 収録の重点（2026-10-27 から）。次のレシピを優先して追加してください：新しいモデルまたは新しいハードウェアの発売後数週間以内のレシピ、および主流ではない組み合わせ（例：マルチ GPU、マルチマシン、AMD と Apple の混在、予算を抑えた構成）。定型の重複レシピとは、リストにすでにある「モデル × エンジン × ハードウェア」の組み合わせの新しい結果のことです。定型の重複レシピを新しいエントリとして追加しないでください。既存のエントリに統合し、数値、出典リンク、日付を新しいものに置き換えてください。収録範囲と第 7 項は、すべてのレシピに適用します。
9. エージェント：`data/hw_index.json` と `.claude/skills/` を手で編集しないでください。`python3 scripts/gen_all.py` が書き出します。スキルは `.agents/skills/` だけで編集してください。新しいダウンロード用ホストは、先に `data/trusted_domains.json` に追加しないとリンクとして表示されません。詳しくは [AGENTS.md](AGENTS.md) を参照。
