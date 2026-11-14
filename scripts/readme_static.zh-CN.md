{{HERO}}

## 目录

{{TOC}}

## 图例

| 来源等级 | 含义 | 格式 |
|---|---|---|
| 🏛️ **官方** | 项目方或厂商发布的数字 | **模型** · 引擎 `量化` — 硬件 → **关键数字** 等级 \[来源\] |
| ✅ **实测** | 发帖人本人跑出，附日志或截图；引擎或配方作者还要公开原始数据和复现步骤 | **tok/s** 指单路生成速度（不含读入，不含多路合计） |
| 🔁 **转述** | 二手引用，请回原帖核对 | 预算档按公开的最低硬件价格（美元）划分 |
| 📣 **宣称** | 预测值，无复现条件 | 未知字段一律不估算，显示「未见公开数据」 |

{{SCOPE}}
<!--RECIPES-->

## 引擎与工具

<!--ENGINES-->

## 相关榜单与清单

<!--RELATED-->

## 参与贡献

一条配方一个 PR。从 [提交页](submit.html) 复制 YAML 模板，只填来源里写明的内容（其余写 `null`），运行 `node scripts/validate.mjs` 校验并附上原帖链接。然后运行 `python3 scripts/gen_readme.py` 重新生成全部 README。优先收录新模型和新硬件发布后几周内的配方，以及非主流组合；只有测试者、机器、模型和引擎都相同时才合并进已有条目，其他测试者的常规重复配方单独成条。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

本地开发：`python3 -m http.server 5190` → `index.html`（首页）· `explore.html`（筛选、排序、散点图）· 数据格式见 [`schema/recipe.schema.json`](schema/recipe.schema.json)。

给 AI agent：技能 [`.agents/skills/local-inference-recipe-finder`](.agents/skills/local-inference-recipe-finder/SKILL.md) 检测本机硬件，并从 [`data/hw_index.json`](docs/hw_index.md) 推荐配方。详见 [AGENTS.md](AGENTS.md)。

<details><summary>网站预览</summary>

<img src="docs/screenshot.zh-CN.png" width="760" alt="网站首页截图：配方数、引擎数、实测数和各预算档最快的实测配置">

</details>

## 许可证

- 代码：[MIT](LICENSE)
- 数据（`data/`）：[CC BY 4.0](LICENSE-DATA)。可自由使用，需署名 Awesome Local Inference Recipes 并保留每条配方的原始来源链接。
