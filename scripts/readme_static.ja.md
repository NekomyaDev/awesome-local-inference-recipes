{{HERO}}

## 目次

{{TOC}}

## 凡例

| 出典レベル | 意味 | 表記 |
|---|---|---|
| 🏛️ **公式** | 開発元やベンダーが公表した数字 | **モデル** · エンジン `量子化` — ハードウェア → **主要な数字** レベル \[出典\] |
| ✅ **実測** | 投稿者本人が計測（ログやスクリーンショットあり）。エンジンまたはレシピの作者は生データと再現手順も公開する | **tok/s** は 1 ストリームの生成速度（プリフィルや合計値は含まない） |
| 🔁 **伝聞** | 他人の結果の引用。元の投稿で確認を | 価格帯は公開されている最安のハードウェア価格（米ドル）で区分 |
| 📣 **主張** | 見込み値で、再現条件なし | 不明な値は推定しません |

{{SCOPE}}
<!--RECIPES-->

## エンジンとツール

<!--ENGINES-->

## 関連リスト・ベンチマーク

<!--RELATED-->

## コントリビュート

1 レシピにつき 1 PR でお願いします。[投稿ページ](submit.html)の YAML テンプレートをコピーし、出典に書かれている内容だけを埋めてください（それ以外は `null`）。`node scripts/validate.mjs` でチェックし、元の投稿へのリンクを添えてください。その後 `python3 scripts/gen_readme.py` で README をすべて再生成します。新しいモデルや新しいハードウェアの発売後数週間以内のレシピと、主流ではない組み合わせを優先して収録します。テスター、マシン、モデル、エンジンがすべて同じ場合にだけ既存のエントリに統合し、別のテスターによる定型の重複レシピは別のエントリにします。詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

ローカル開発：`python3 -m http.server 5190` → `index.html`（トップ）· `explore.html`（絞り込み・並べ替え・散布図）· スキーマは [`schema/recipe.schema.json`](schema/recipe.schema.json)。

AI エージェント向け：スキル [`.agents/skills/local-inference-recipe-finder`](.agents/skills/local-inference-recipe-finder/SKILL.md) がハードウェアを検出し、[`data/hw_index.json`](docs/hw_index.md) からレシピを推薦します。詳しくは [AGENTS.md](AGENTS.md) を参照。

<details><summary>サイトのプレビュー</summary>

<img src="docs/screenshot.ja.png" width="760" alt="サイトのトップページ：レシピ数、エンジン数、実測数、予算帯ごとの最速の実測構成">

</details>

## ライセンス

- コード：[MIT](LICENSE)
- データ（`data/`）：[CC BY 4.0](LICENSE-DATA)。Awesome Local Inference Recipes と、各レシピに記載された元の出典を明記すれば自由に再利用できます。
