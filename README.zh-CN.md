<h1 align="center">本地推理配方精选 <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a></h1>

<p align="center">你的硬件到底能跑多快？798 条有出处的本地 AI 配方，从 405 美元的显卡到 3 万美元的整机。</p>

<p align="center"><a href="README.md">English</a> · <b>简体中文</b> · <a href="README.ja.md">日本語</a></p>

<p align="center"><a href="https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN"><img src="https://img.shields.io/badge/recipes-798-0891B2?style=flat-square" alt="798 recipes"></a> <img src="https://img.shields.io/badge/data%20as%20of-2026--11--05-4B5563?style=flat-square" alt="data as of 2026-11-05"> <a href="https://github.com/raytone-lab/awesome-local-inference-recipes/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/raytone-lab/awesome-local-inference-recipes/validate.yml?branch=main&style=flat-square&label=validate" alt="validate"></a> <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-22C55E?style=flat-square" alt="MIT"></a> <a href="LICENSE-DATA"><img src="https://img.shields.io/badge/data-CC%20BY%204.0-22C55E?style=flat-square" alt="CC BY 4.0"></a> <a href="https://github.com/raytone-lab/awesome-local-inference-recipes/stargazers"><img src="https://img.shields.io/github/stars/raytone-lab/awesome-local-inference-recipes?style=flat-square" alt="GitHub stars"></a> <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-7C3AED?style=flat-square" alt="PRs welcome"></a></p>

<p align="center"><a href="https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN"><b>在线配方库</b></a> · <a href="recipes/README.zh-CN.md"><b>配方指南</b></a> · <a href="docs/getting-started.zh-CN.md"><b>入门指南</b></a> · <a href="https://raytone-lab.github.io/awesome-local-inference-recipes/submit.html?lang=zh-CN"><b>提交配方</b></a></p>

<p align="center"><img src="docs/hero.zh-CN.png" width="860" alt="条形图：按模型规模分组（稠密 ≥27B；大 MoE 总参数 ≥100B；中 MoE 总参数 <100B、激活 ≥5B；小 MoE 激活 <5B；标注激活参数；仅含有官方参数卡的模型），按每 $1000 硬件对应 tok/s 排名的实测文字配置，按硬件类别着色"></p>

### X tok/s 到底有多快？

<p align="center"><a href="https://raytone-lab.github.io/awesome-local-inference-recipes/speed.html?lang=zh-CN"><img src="docs/speed-feel.gif" width="860" alt="token 输出速度演示：10、20、50、100、200 和 500 tok/s，对比人的默读速度（动图内文字为英文）"></a></p>

<p align="center">同一段回答、真实 Qwen3 token，以 10 / 20 / 50 / 100 / 200 / 500 tok/s（对数间隔）输出，对比默读速度（英文约 5 tok/s，Brysbaert 2019）和云端 API 中位速度（Artificial Analysis）。 <a href="https://raytone-lab.github.io/awesome-local-inference-recipes/speed.html?lang=zh-CN"><b>在线互动体验 →</b></a></p>

**798 条配方**（文字 757 · 图像 15 · 影音 26）· **6 类硬件** · **105 种引擎** · **17 个模型系列** · 每个数字都有出处 · 预算 **3 万美元以内**

### 亮点数据

| 记录              | 模型 · 引擎                         | 硬件                                                                | 结果                | 来源                                                                       |
| --------------- | ------------------------------- | ----------------------------------------------------------------- | ----------------- | ------------------------------------------------------------------------ |
| Mac 最快          | Qwen3.8-Flash-Next · TensorFold | Mac Studio M3 Ultra（峰值；原帖未注明测试机内存，无法给出单一价格；首发价按内存为 $3,999–$9,499） | **130 tok/s** ✅   | [来源](https://x.com/ivanfioravanti/status/2104183112611614780)            |
| 单张 RTX 5090 最快  | Qwen3.8-Flash-Next · Strata     | RTX 5090 + 256GB RAM · 约 $5,400（仅显卡，不含 256GB 内存；街价，MSRP $1,999）   | **176 tok/s** ✅   | [@TechPractice1](https://x.com/TechPractice1/status/2105087037363884483) |
| AMD 最快          | Qwen3.8-Flash-Next · Strata     | AMD Radeon AI PRO R9700 · 约 $1,600                                | **100 tok/s** ✅   | [@TechPractice1](https://x.com/TechPractice1/status/2105338176055509376) |
| 二手数据中心卡         | Qwen3.8-Flash-Next · Strata     | 2× Tesla V100 32GB PCIe（无 NVLink）                                 | **120 tok/s** ✅   | [@rewin123](https://x.com/rewin123/status/2108669905616736529)           |
| 单台 DGX Spark 最快 | Qwen3.8-Flash-Next · TensorFold | 1× DGX Spark · 约 $6,950                                           | **130.1 tok/s** ✅ | [来源](https://x.com/Leoskie_L/status/2115262189506535697)                 |
| 最便宜的配置          | Qwen3.8-Flash-Next · Strata     | Tesla P40 24GB（二手） · 约 $405                                       | **30 tok/s** ✅    | [来源](https://github.com/Niko1221/Strata/blob/main/docs/OLDER_GPUS.md)    |

<sub>单路生成速度，均摘自来源；价格为公开的最低硬件价格。✅ = 发帖人实测。</sub>

## 目录

- [图例](#图例)
- [收录范围](#收录范围)
- [快速问答](#快速问答)
- [X 上的热门配方](#x-上的热门配方)
- [按硬件浏览](#按硬件浏览)
- [按模型系列浏览](#按模型系列浏览)
- [按引擎浏览](#按引擎浏览)
- [第 1 档 · 2,500 美元以内](#第-1-档--2500-美元以内)
- [第 2 档 · 2,500–7,000 美元](#第-2-档--25007000-美元)
- [第 3 档 · 7,000–14,000 美元](#第-3-档--700014000-美元)
- [第 4 档 · 14,000–30,000 美元](#第-4-档--1400030000-美元)
- [价格未公开](#价格未公开)
- [引擎与工具](#引擎与工具)
- [相关榜单与清单](#相关榜单与清单)
- [许可证](#许可证)

## 图例

| 来源等级       | 含义                                  | 格式                                         |
| ---------- | ----------------------------------- | ------------------------------------------ |
| 🏛️ **官方** | 项目方或厂商发布的数字                         | **模型** · 引擎 `量化` — 硬件 → **关键数字** 等级 \[来源\] |
| ✅ **实测**   | 发帖人本人跑出，附日志或截图；引擎或配方作者还要公开原始数据和复现步骤 | **tok/s** 指单路生成速度（不含读入，不含多路合计）             |
| 🔁 **转述**  | 二手引用，请回原帖核对                         | 预算档按公开的最低硬件价格（美元）划分                        |
| 📣 **宣称**  | 预测值，无复现条件                           | 未知字段一律不估算，显示「未见公开数据」                       |

## 收录范围

本清单只收个人、家用或办公桌面用户、小型工作室能搭起来的配置。数据中心配置不收录。装在桌面 PC 里的二手数据中心卡可以收录。

配置必须同时满足以下条件：

- 硬件总价不超过 3 万美元。
- GPU 或整机合计不超过 4 个。每张 GPU 算 1 个；没有独立 GPU 的整机每台算 1 个。例如：一台 PC 装 4 张卡算 4 个，4 台 DGX Spark 算 4 个，4 台 DGX Spark 加一台装 RTX 5090 的 PC 算 5 个。
- 用普通家用或办公室电源即可运行：总功率约 2 kW 以内，最多分接两个普通插座，不需要专门布线。用两个插座时，两个插座要在不同电路上。美国一路 120 V / 15 A 电路持续供电约 1.44 kW；日本一个 100 V / 15 A 插座额定约 1.5 kW。
- 不用机架，不用 SXM 或 HGX 服务器主板，不用分体式水冷或服务器液冷。装得进桌面机箱的 DIY SXM2 转 PCIe 转接方案可以收录。出厂自带一体式水冷（AIO）的消费级显卡可以收录。
- 最多用一台桌面级网络交换机。
- 暂不收录魔改显卡，即改过硬件（例如改过显存）的显卡，例如 48GB 显存的 RTX 4090D、改过显存的 CMP 170HX。库里已有的魔改显卡条目暂时保留，以后再复核。原厂显卡只用固件或驱动解锁时可以收录，例如解除 Ampere 卡 FP16 限速的 gpu-unlock 内核模块。这类条目加 `gpu-unlock` 标签。

不满足任一条件的配置不收录，即使总价低于 3 万美元。

价格按收录当天记录。之后涨价时，只更新价格说明（`hardware_cost_text`），不删除条目。

`python3 scripts/scope_rules.py` 会列出未通过价格、数量或硬件类型检查的条目。

## 快速问答

数据截至 2026-11-05。每条回答取数据集中最快的单路文字生成结果，并标注来源等级；✅ = 发帖人实测。不同回答的模型不同。

**单张 RTX 5090 跑本地大模型有多快？**  
实测最快：**351.5 tok/s**，LFM2.5-24B-A2B · llama.cpp，硬件 RTX 5090 32GB（✅ 实测，2026-10-15，[来源](https://x.com/niklaslenz_ai/status/2110469931011612895)）。该硬件共 50 条配方，其中实测 28 条。

**单张 RTX 4090 跑本地大模型有多快？**  
实测最快：**179.4 tok/s**，Recursive Flint 40B-A2.5B · llama.cpp，硬件 RTX 4090 24GB（✅ 实测，2026-10-22，[来源](https://llm-speed.com/m/flint-40b-a2-5b)）。该硬件共 14 条配方，其中实测 5 条。

**单张 RTX 3090 跑本地大模型有多快？**  
实测最快：**384 tok/s**，LFM3-1.7B · llama.cpp，硬件 RTX 3090 24GB（✅ 实测，2026-10-28，[来源](https://x.com/Layton_Gott/status/2115244678056464384)）。该硬件共 21 条配方，其中实测 11 条。

**Mac Studio M3 Ultra 跑本地大模型有多快？**  
实测最快：**130 tok/s**，Qwen3.8-Flash-Next · TensorFold，硬件 Mac Studio M3 Ultra（✅ 实测，日期未注明，[来源](https://x.com/ivanfioravanti/status/2104183112611614780)）。该硬件共 24 条配方，其中实测 7 条。

**一台 NVIDIA DGX Spark 跑本地大模型有多快？**  
实测最快：**130.1 tok/s**，Qwen3.8-Flash-Next · TensorFold，硬件 1× DGX Spark（✅ 实测，2026-10-28，[来源](https://x.com/Leoskie_L/status/2115262189506535697)）。该硬件共 67 条配方，其中实测 42 条。

**AMD Strix Halo（Ryzen AI Max+ 395）跑本地大模型有多快？**  
实测最快：**98 tok/s**，Recursive Flint 40B-A2.5B · Halogen，硬件 AMD Ryzen AI Max+ 395 128GB（✅ 实测，2026-10-23，[来源](https://www.reddit.com/r/StrixHalo/comments/1xcxjpv/)）。该硬件共 25 条配方，其中实测 12 条。

**2500 美元以内实测最快的配置是什么？**  
实测最快：**190 tok/s**，Qwen3.8-27B · Geezuz，硬件 2× RTX 3090（280W，PCIe，无 NVLink）（✅ 实测，2026-10-20，[来源](https://github.com/ohgeebtw/geezuz-qwen3.8-27b-dual-gpu)）。该预算内共 61 条配方，其中实测 32 条。


## X 上的热门配方

X 上互动最多的配方帖（按 点赞 + 3×转发 排序；同一帖子只列一次，不含“宣称”条目；互动数截至 2026-10-30）。

- **DeepSeek-V4.1-Flash** — 2× DGX Spark → **29 tok/s** ✅ [@0xSero](https://x.com/0xSero/status/2106373861818224907) ♥2459
- **Ternary Bonsai 2 27B（heretic 去拒答）** — RTX 3060 12GB → **50 tok/s** ✅ [@sudoingX](https://x.com/sudoingX/status/2110451458302943383) ♥811
- **Qwen3.8-Flash-Next** · vLLM — 1× DGX Spark → **48.7 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2101339268203380857) ♥800
- **GLM-5.3-Flash EXL3 4-bit** · TensorFold — 2× DGX Spark → **60.4 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2105598458547646875) ♥683
- **Qwen3.8-Flash-Next** · Strata — RTX 5090 32GB + 系统内存（部分卸载） → **204 tok/s** ✅ [@niklaslenz_ai](https://x.com/niklaslenz_ai/status/2110132306061013386) ♥503
- **Qwen3.8-Flash-Next** · TensorFold — 1× DGX Spark → **64.4 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2108203605685596490) ♥386
- **DeepSeek-V4-Flash (0731 GA)** — 2× DGX Spark → **82 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2083326111144906836) ♥365
- **Qwen3.8-27B** · vLLM — RTX 5090 32GB → **147 tok/s** ✅ [@MiaAI_lab](https://x.com/MiaAI_lab/status/2088734058842878037) ♥377

## 按硬件浏览

每种设备的配方数，以及实测最快的单路 tok/s（多卡组合取任一组合的实测最快值）。点击打开该硬件页面；配方不足 5 条的设备会打开已筛选的配方库。

| 类别              | 设备（配方数 · ⚡ 实测最快 tok/s）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| NVIDIA&nbsp;RTX | [RTX 5090](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/rtx-5090.html) (99 · ⚡**538.1**) &nbsp;·&nbsp; [RTX 3090](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/rtx-3090.html) (51 · ⚡**384**) &nbsp;·&nbsp; [RTX 4090](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/rtx-4090.html) (27 · ⚡**179.4**) &nbsp;·&nbsp; [RTX 5060 Ti](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/rtx-5060-ti.html) (23 · ⚡**162**) &nbsp;·&nbsp; [RTX 5070 / 5070 Ti](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=RTX%205070&lang=zh-CN) (20 · ⚡**141.3**) &nbsp;·&nbsp; [RTX 3060](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=RTX%203060&lang=zh-CN) (18 · ⚡**244**)        |
| Apple&nbsp;芯片   | [M5 Pro / M5 Max](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/mac-m5.html) (59 · ⚡**157**) &nbsp;·&nbsp; [M3 Ultra](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/mac-studio-m3-ultra.html) (33 · ⚡**130**) &nbsp;·&nbsp; [M5 Ultra](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=M5%20Ultra&lang=zh-CN) (33 · ⚡**141**) &nbsp;·&nbsp; [M4 Pro](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=M4%20Pro&lang=zh-CN) (31 · ⚡**127.9**) &nbsp;·&nbsp; [M4 Max](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/mac-m4-max.html) (20 · ⚡**78.7**) &nbsp;·&nbsp; [M2 Ultra](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=M2%20Ultra&lang=zh-CN) (2 · ⚡**59.9**) |
| DGX&nbsp;Spark  | [DGX Spark](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/dgx-spark.html) (150 · ⚡**130.1**)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| AMD             | [Radeon R9700 / RX 7900](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/amd-radeon.html) (47 · ⚡**109.9**) &nbsp;·&nbsp; [Strix Halo](https://raytone-lab.github.io/awesome-local-inference-recipes/hw/zh-CN/strix-halo.html) (25 · ⚡**78**) &nbsp;·&nbsp; [Instinct MI50](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=MI50&lang=zh-CN) (6 · ⚡**36.8**)                                                                                                                                                                                                                                                                                                                                                                                                                     |
| 多卡及其他           | [多卡组合](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=multi-GPU&lang=zh-CN) (203 · ⚡**370**) &nbsp;·&nbsp; [Tesla V100](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=V100&lang=zh-CN) (23 · ⚡**74.7**) &nbsp;·&nbsp; [CMP 170HX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=CMP&lang=zh-CN) (6) &nbsp;·&nbsp; [iPhone](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?q=iPhone&lang=zh-CN) (4)                                                                                                                                                                                                                                                                                                         |

## 按模型系列浏览

点击系列名即可打开已筛选的配方库。标签：[`MoE`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=MoE&lang=zh-CN) 540, [`long-context`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=long-context&lang=zh-CN) 299, [`speculative`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=speculative&lang=zh-CN) 297, [`4bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=4bit&lang=zh-CN) 271, [`dense`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=dense&lang=zh-CN) 206, [`multi-GPU`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=multi-GPU&lang=zh-CN) 203, [`MTP`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=MTP&lang=zh-CN) 154, [`3bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=3bit&lang=zh-CN) 121, [`2bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=2bit&lang=zh-CN) 110, [`offload`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=offload&lang=zh-CN) 85, [`8bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=8bit&lang=zh-CN) 53, [`1bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=1bit&lang=zh-CN) 29, [`ternary`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=ternary&lang=zh-CN) 26, [`abliterated`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=abliterated&lang=zh-CN) 14, [`bf16`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=bf16&lang=zh-CN) 12, [`few-step`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=few-step&lang=zh-CN) 12, [`6bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=6bit&lang=zh-CN) 9, [`gpu-unlock`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=gpu-unlock&lang=zh-CN) 4, [`5bit`](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?tag=5bit&lang=zh-CN) 2。`gpu-unlock` 标签表示原厂显卡使用了固件或驱动解锁（无硬件改装）。

| 系列                                                                                                                      | 配方数 | 文字  | 图像  | 影音  |
| ----------------------------------------------------------------------------------------------------------------------- | --- | --- | --- | --- |
| [Qwen](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Qwen&lang=zh-CN)               | 425 | 425 |     |     |
| [DeepSeek](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=DeepSeek&lang=zh-CN)       | 125 | 125 |     |     |
| [GLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=GLM&lang=zh-CN)                 | 42  | 42  |     |     |
| [Bonsai](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Bonsai&lang=zh-CN)           | 33  | 33  |     |     |
| [MiniMax H3](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=MiniMax%20H3&lang=zh-CN) | 18  |     |     | 18  |
| [Qwen-Image](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Qwen-Image&lang=zh-CN)   | 13  |     | 13  |     |
| [MiniMax](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=MiniMax&lang=zh-CN)         | 9   | 9   |     |     |
| [Gemma](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Gemma&lang=zh-CN)             | 8   | 8   |     |     |
| [Mistral](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Mistral&lang=zh-CN)         | 5   | 5   |     |     |
| [LTX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=LTX&lang=zh-CN)                 | 4   |     |     | 4   |
| [gpt-oss](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=gpt-oss&lang=zh-CN)         | 3   | 3   |     |     |
| [ACE-Step](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=ACE-Step&lang=zh-CN)       | 2   |     |     | 2   |
| [Edge0](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Edge0&lang=zh-CN)             | 2   | 2   |     |     |
| [Wan](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Wan&lang=zh-CN)                 | 2   |     |     | 2   |
| [Z-Image](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Z-Image&lang=zh-CN)         | 2   |     | 2   |     |
| [Kimi](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Kimi&lang=zh-CN)               | 1   | 1   |     |     |
| [Llama](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Llama&lang=zh-CN)             | 1   | 1   |     |     |
| [Other](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?family=Other&lang=zh-CN)             | 103 | 103 |     |     |

## 按引擎浏览

引擎名已统一（`scripts/normalize_engines.py`），原始写法保留在 `engine_note` 字段。

| 引擎                                                                                                                                                                                                          | 配方数 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| [Strata](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata&lang=zh-CN)                                                                                               | 163 |
| [llama.cpp](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp&lang=zh-CN)                                                                                         | 84  |
| [TensorFold](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TensorFold&lang=zh-CN)                                                                                       | 73  |
| [vLLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=vLLM&lang=zh-CN)                                                                                                   | 59  |
| [oMLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=oMLX&lang=zh-CN)                                                                                                   | 38  |
| [MLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MLX&lang=zh-CN)                                                                                                     | 33  |
| [SGLang](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=SGLang&lang=zh-CN)                                                                                               | 21  |
| [llama.cpp (PrismML fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28PrismML%20fork%29&lang=zh-CN)                                                   | 14  |
| [ComfyUI](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ComfyUI&lang=zh-CN)                                                                                             | 12  |
| [Project Maya](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Project%20Maya&lang=zh-CN)                                                                                 | 12  |
| [Splash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Splash&lang=zh-CN)                                                                                               | 12  |
| [MTPLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MTPLX&lang=zh-CN)                                                                                                 | 11  |
| [ExLlama](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ExLlama&lang=zh-CN)                                                                                             | 9   |
| [mlx-serve](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=mlx-serve&lang=zh-CN)                                                                                         | 9   |
| [DFlash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=DFlash&lang=zh-CN)                                                                                               | 7   |
| [Ollama](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Ollama&lang=zh-CN)                                                                                               | 7   |
| [Radiance](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Radiance&lang=zh-CN)                                                                                           | 7   |
| [ds4 (DwarfStar)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ds4%20%28DwarfStar%29&lang=zh-CN)                                                                       | 6   |
| [Basalt](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Basalt&lang=zh-CN)                                                                                               | 5   |
| [Kapitsa](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Kapitsa&lang=zh-CN)                                                                                             | 5   |
| [Halogen](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Halogen&lang=zh-CN)                                                                                             | 4   |
| [NVIDIA Flare](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=NVIDIA%20Flare&lang=zh-CN)                                                                                 | 4   |
| [Radiance (fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Radiance%20%28fork%29&lang=zh-CN)                                                                       | 4   |
| [mirai-s-ada](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=mirai-s-ada&lang=zh-CN)                                                                                     | 4   |
| [ninfer](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ninfer&lang=zh-CN)                                                                                               | 4   |
| [Rapid-MLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Rapid-MLX&lang=zh-CN)                                                                                         | 3   |
| [TabbyAPI](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TabbyAPI&lang=zh-CN)                                                                                           | 3   |
| [TandemLLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TandemLLM&lang=zh-CN)                                                                                         | 3   |
| [gufo](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=gufo&lang=zh-CN)                                                                                                   | 3   |
| [llama.cpp (agentionai fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28agentionai%20fork%29&lang=zh-CN)                                             | 3   |
| [BitRun](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=BitRun&lang=zh-CN)                                                                                               | 2   |
| [Espetero](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Espetero&lang=zh-CN)                                                                                           | 2   |
| [FreeToken](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=FreeToken&lang=zh-CN)                                                                                         | 2   |
| [Front_Eagle739 streaming stack](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Front_Eagle739%20streaming%20stack&lang=zh-CN)                                           | 2   |
| [Halowin Bubo](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Halowin%20Bubo&lang=zh-CN)                                                                                 | 2   |
| [Infernix](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Infernix&lang=zh-CN)                                                                                           | 2   |
| [MLX Swift](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MLX%20Swift&lang=zh-CN)                                                                                       | 2   |
| [RustingStrata](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=RustingStrata&lang=zh-CN)                                                                                 | 2   |
| [Speedy](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Speedy&lang=zh-CN)                                                                                               | 2   |
| [Strata (Strata-DS fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28Strata-DS%20fork%29&lang=zh-CN)                                                     | 2   |
| [Strata (Strata-rdna3 fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28Strata-rdna3%20fork%29&lang=zh-CN)                                               | 2   |
| [TideLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TideLM&lang=zh-CN)                                                                                               | 2   |
| [affinity](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=affinity&lang=zh-CN)                                                                                           | 2   |
| [capy-flash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=capy-flash&lang=zh-CN)                                                                                       | 2   |
| [dsx](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=dsx&lang=zh-CN)                                                                                                     | 2   |
| [edge0](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=edge0&lang=zh-CN)                                                                                                 | 2   |
| [llama.cpp (OpenBMB fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28OpenBMB%20fork%29&lang=zh-CN)                                                   | 2   |
| [strata-mlx](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=strata-mlx&lang=zh-CN)                                                                                       | 2   |
| [tqLLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=tqLLM&lang=zh-CN)                                                                                                 | 2   |
| [Betelgeuse](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Betelgeuse&lang=zh-CN)                                                                                       | 1   |
| [BigMoeOnEdge](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=BigMoeOnEdge&lang=zh-CN)                                                                                   | 1   |
| [Geezuz](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Geezuz&lang=zh-CN)                                                                                               | 1   |
| [IronMLX](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=IronMLX&lang=zh-CN)                                                                                             | 1   |
| [JITEngine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=JITEngine&lang=zh-CN)                                                                                         | 1   |
| [Janas-LLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Janas-LLM&lang=zh-CN)                                                                                         | 1   |
| [Kapitsa 0.2.19 + KFlash](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Kapitsa%200.2.19%20%2B%20KFlash&lang=zh-CN)                                                     | 1   |
| [LightX2V](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=LightX2V&lang=zh-CN)                                                                                           | 1   |
| [MLX Swift (PrismML fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MLX%20Swift%20%28PrismML%20fork%29&lang=zh-CN)                                                 | 1   |
| [Magnitude](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Magnitude&lang=zh-CN)                                                                                         | 1   |
| [MoEShift](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=MoEShift&lang=zh-CN)                                                                                           | 1   |
| [NInferno](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=NInferno&lang=zh-CN)                                                                                           | 1   |
| [NVIDIA Sol](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=NVIDIA%20Sol&lang=zh-CN)                                                                                     | 1   |
| [Osaurus](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Osaurus&lang=zh-CN)                                                                                             | 1   |
| [PLI](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=PLI&lang=zh-CN)                                                                                                     | 1   |
| [PXA](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=PXA&lang=zh-CN)                                                                                                     | 1   |
| [Paiton](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Paiton&lang=zh-CN)                                                                                               | 1   |
| [Pithos](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Pithos&lang=zh-CN)                                                                                               | 1   |
| [QEngine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=QEngine&lang=zh-CN)                                                                                             | 1   |
| [Qwentin](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Qwentin&lang=zh-CN)                                                                                             | 1   |
| [ReVolta](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ReVolta&lang=zh-CN)                                                                                             | 1   |
| [SGLang (Penny Royal fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=SGLang%20%28Penny%20Royal%20fork%29&lang=zh-CN)                                               | 1   |
| [SonicBoom](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=SonicBoom&lang=zh-CN)                                                                                         | 1   |
| [Strata (TCP layer split fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28TCP%20layer%20split%20fork%29&lang=zh-CN)                                     | 1   |
| [Strata (syoyo fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strata%20%28syoyo%20fork%29&lang=zh-CN)                                                             | 1   |
| [Strim](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Strim&lang=zh-CN)                                                                                                 | 1   |
| [Surogate](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Surogate&lang=zh-CN)                                                                                           | 1   |
| [TensorRT Edge-LLM](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=TensorRT%20Edge-LLM&lang=zh-CN)                                                                       | 1   |
| [VoidInfer](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=VoidInfer&lang=zh-CN)                                                                                         | 1   |
| [Xolotl](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Xolotl&lang=zh-CN)                                                                                               | 1   |
| [delta-inference-engine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=delta-inference-engine&lang=zh-CN)                                                               | 1   |
| [ds41](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ds41&lang=zh-CN)                                                                                                   | 1   |
| [elpis (ExLlamaV3 patch)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=elpis%20%28ExLlamaV3%20patch%29&lang=zh-CN)                                                     | 1   |
| [gbx](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=gbx&lang=zh-CN)                                                                                                     | 1   |
| [gufo (mikealanni fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=gufo%20%28mikealanni%20fork%29&lang=zh-CN)                                                       | 1   |
| [ik_llama.cpp (Mcniiby fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=ik_llama.cpp%20%28Mcniiby%20fork%29&lang=zh-CN)                                             | 1   |
| [libosmos](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=libosmos&lang=zh-CN)                                                                                           | 1   |
| [llama.cpp (DavideWasTaken fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28DavideWasTaken%20fork%29&lang=zh-CN)                                     | 1   |
| [llama.cpp (achyudh Adaptive KV Streaming fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28achyudh%20Adaptive%20KV%20Streaming%20fork%29&lang=zh-CN) | 1   |
| [llama.cpp (mirai-s fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28mirai-s%20fork%29&lang=zh-CN)                                                   | 1   |
| [llama.cpp (pentacoxian_dev fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28pentacoxian_dev%20fork%29&lang=zh-CN)                                   | 1   |
| [llama.cpp (pinkmanwest fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28pinkmanwest%20fork%29&lang=zh-CN)                                           | 1   |
| [llama.cpp (tandem.cpp fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28tandem.cpp%20fork%29&lang=zh-CN)                                             | 1   |
| [llama.cpp (vahpetr fork)](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=llama.cpp%20%28vahpetr%20fork%29&lang=zh-CN)                                                   | 1   |
| [lxe Rust/CUDA runner](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=lxe%20Rust/CUDA%20runner&lang=zh-CN)                                                               | 1   |
| [mflux](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=mflux&lang=zh-CN)                                                                                                 | 1   |
| [moe-cache](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=moe-cache&lang=zh-CN)                                                                                         | 1   |
| [moex](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=moex&lang=zh-CN)                                                                                                   | 1   |
| [pulsar-inference-stack](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=pulsar-inference-stack&lang=zh-CN)                                                               | 1   |
| [qwen38-megakernel](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=qwen38-megakernel&lang=zh-CN)                                                                         | 1   |
| [rec](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=rec&lang=zh-CN)                                                                                                     | 1   |
| [spark-ds41f](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=spark-ds41f&lang=zh-CN)                                                                                     | 1   |
| [spark-engine](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=spark-engine&lang=zh-CN)                                                                                   | 1   |
| [sparkinfer](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=sparkinfer&lang=zh-CN)                                                                                       | 1   |
| [sushi](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=sushi&lang=zh-CN)                                                                                                 | 1   |
| [webyIQ](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=webyIQ&lang=zh-CN)                                                                                               | 1   |
| [Unspecified](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?engine=Unspecified&lang=zh-CN)                                                                                     | 82  |

<p align="center"><img src="docs/budget-tiers.zh-CN.png" width="860" alt="条形图：各预算档最快的实测与宣称文字配置"></p>


## 第 1 档 · 2,500 美元以内

*二手 3090/4090、MI50/V100、Strix Halo、R9700* · 共 70 条


**📝 文字**

- **Bonsai-8B** · llama.cpp (PrismML fork) `1-bit Q1_0` — RTX 4090 → **368 tok/s** 📣 [来源](https://huggingface.co/prism-ml/Bonsai-8B-gguf)
- **Qwen3.8-27B** · tqLLM `TQ3_4S-v2 · DFlash2 草稿` — RTX 3090 24GB → **273 tok/s** 🏛️ [来源](https://x.com/coffeecup2020/status/2110624499901075769)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 4090 24GB → **225 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- **Qwen3.8-Flash-Next** · Strata `Strata（作者自改版）· Swift 1.5 IQ…` — RTX 4090 24GB + 32GB DDR5 → **220 tok/s** 📣 [来源](https://x.com/Knuckles_XBT/status/2105245662657011841)
- **Qwen3.8-27B** · Geezuz `Q4_K_M（另测 Q8_0）` — 2× RTX 3090（280W，PCIe，无 NVLink） → **190 tok/s** ✅ [来源](https://github.com/ohgeebtw/geezuz-qwen3.8-27b-dual-gpu)
- **Recursive Flint 40B-A2.5B** · llama.cpp `NVFP4 GGUF（22.86GB）` — RTX 4090 24GB → **179.4 tok/s** ✅ [来源](https://llm-speed.com/m/flint-40b-a2-5b)
- **Qwen3.8-27B** · tqLLM `TQ_XS（~11.9 GB）· DFlash2 草稿` — RTX 5060 Ti 16GB → **175.9 tok/s** 🏛️ [来源](https://x.com/coffeecup2020/status/2110719638518526343)
- **Qwen3.6-35B-A3B** · FreeToken `FreeToken · NVFP4（无投机）` — RTX 4090 → **167 tok/s** 🔁 [来源](https://x.com/shipfrontierai/status/2092602493213577481)
- **LFM2.5-24B-A2B** · llama.cpp `Q4（14.5 GB）` — RTX 5060 Ti 16GB → **162 tok/s** ✅ [来源](https://x.com/niklaslenz_ai/status/2110469931011612895)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2` — RTX 3090 24GB → **154 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- *……另有 51 条，见 [配方库](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN)。*

**🖼️ 图像**

- **Qwen-Image 2.1（7B + 8B 文本编码器）** · ComfyUI `官方 Comfy-Org INT8 · ComfyUI` — RTX 4090 24GB → 8.1 s / 1024²（40 步）；30.2 s / 2048×1152（50 步）；峰值 16.2GB ✅ [来源](https://x.com/yume_arasaki/status/2102176739359404499) · [指南](recipes/image-001.zh-CN.md)
- **Qwen-Image 2.1** `INT8` — RTX 3090 → 82–96 s / 2K（公开回执） 🔁 [来源](https://x.com/yume_arasaki/status/2102176739359404499)
- **Qwen-Image 2.1（编辑）** · ComfyUI `ComfyUI` — Mac M4 Pro → 3 分 52 秒 / 张（768 编辑） ✅ [来源](https://x.com/gabeciii/status/2116171024106401889)
- **Z-Image Turbo（6B，8 步）** · ComfyUI `ComfyUI` — RTX 3090 24GB → 2048px 约 8 s / 张；另一用户预热后 12 s ✅ [来源](https://x.com/michaelricks/status/2104959036353356058)

**🎬 影音**

- **FastH3 V2 / Trim** `FP8` — RTX 4090 24GB → 480p 5s：54.6 / 43.9 s；768p：154.6 / 132.8 s；8GB 限制 Trim 82.0 s 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3（turbo）** · ComfyUI `ComfyUI` — RTX 4090 → 5 s 片段 ~91 s；15 s ~8 分钟；960×544×5s 约 50 s ✅ [来源](https://x.com/yume_arasaki/status/2097790831323427046)
- **MiniMax H3** · ComfyUI `ComfyUI` — RTX 3090 → 11 s 视频 13 分钟 ✅ [来源](https://x.com/natehalko/status/2103538997146611890)
- **ACE-Step 1.5（音乐）** — RTX 3090 → 整首歌 <10 s（宣传帖） 🔁 [来源](https://x.com/simplifyinAI/status/2091935190335754493)
- **MiniMax H3 Ref2VA（VSA + Turbo 4 步）** · ComfyUI `INT8 DiT（pruned Ref2VA）+ NV…` — RTX 4090 24GB → 1344×768×5.16s（24 fps / 124 帧）：预热墙钟约 72 s（首跑约 95.2 s）；峰值显存约 13.5 GB。同… 🏛️ [来源](https://github.com/Kablex/ComfyUI-Ref2VA-VSA)

## 第 2 档 · 2,500–7,000 美元

*单张 RTX 5090、单台 DGX Spark、Mac Studio Max* · 共 170 条


**📝 文字**

- **Qwen3.6-35B-A3B** · sparkinfer `sparkinfer v0.4.4（Blackwell…` — RTX 5090 → **512 tok/s** 📣 [来源](https://x.com/kysstalol/status/2105042922643321008)
- **LFM2.5-24B-A2B** · llama.cpp `Q4（14.5 GB）` — RTX 5090 32GB → **351.5 tok/s** ✅ [来源](https://x.com/niklaslenz_ai/status/2110469931011612895)
- **NVIDIA Nemotron 3.5 Bolt 74B-A9B** · llama.cpp `NVIDIA 官方 IQ2_XXS 24GB GGUF…` — RTX 5090 32GB（Ubuntu，driver 570） → **343 tok/s** ✅ [来源](https://www.reddit.com/r/LocalLLM/comments/1xap599/)
- **gpt-oss-20b** · llama.cpp `Q4_K_M` — RTX 5090 32GB（主机 EPYC 7543 + 945GB RAM，CLI 报告） → **324.2 tok/s** ✅ [来源](https://llm-speed.com/r/r_dwp5fgdapmw)
- **Qwen3-Coder-30B-A3B-Instruct** · llama.cpp `Q4_K_M` — RTX 5090 32GB（主机 EPYC 7543 + 945GB RAM，CLI 报告） → **304.9 tok/s** ✅ [来源](https://llm-speed.com/r/r_vsype4pm1ko)
- **Qwen3.6-35B-A3B-Escha-W2** · SGLang `Escha W2（INT8=on）` — RTX 5090 32GB → **283 tok/s** 📣 [来源](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2) · [指南](recipes/hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.zh-CN.md)
- **Qwen3.8-Flash-Next** · Basalt `NVIDIA NVFP4（MoE）+ MTP，int8…` — RTX 5090 32GB + Core Ultra 9 285K + 247GB DDR5 → **242 tok/s** ✅ [来源](https://www.reddit.com/r/LocalLLaMA/comments/1xcp0mf/)
- **Qwen3.8-Flash-Next** · Strata `ISTA-DASLab GSQ-RCO IQ3_S（M…` — RTX 5090 32GB + 121GB DDR5 → **240 tok/s** ✅ [来源](https://x.com/lyesbahi/status/2113602136051458520)
- **Qwen3.8-Flash-Next** · vLLM `Intel W4A16-AutoRound + 原生 …` — 2× CMP 170HX（各暴露 64GB，PCIe Gen2 x4，无 x16 改装）+ 93GB RAM + NV… → **226.2 tok/s** ✅ [来源](https://github.com/AlexBrandes/cmp170hx-qwen38-flash-next)
- **MiniCPM-V 4.7 35B-A3B** · llama.cpp `Q4_K_M` — RTX 5090 → **208 tok/s** ✅ [来源](https://x.com/Blackwellboy/status/2110717843121881380)
- *……另有 142 条，见 [配方库](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN)。*

**🖼️ 图像**

- **Qwen-Image 2.1** `LightX2V / BennyDaBall NVFP…` — RTX 5090 32GB → 5.93 s；NVFP4 6.7 s vs INT8 7.6 s vs BF16 15.6 s（1024²） 🔁 [来源](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image 2.1** · TensorFold `TensorFold NVFP4 / FP8 / GG…` — RTX 5090 @450W → 4.53 s / 6.94 s / 13.87 s（1024²，25 步；NVFP4 峰值 22.9GB；图像与 Q6 不完全一致） ✅ [来源](https://x.com/niklaslenz_ai/status/2106465941177487871)
- **Qwen-Image 2.1** `厂商内核重写+步缓存` — RTX 5090 → 13.5 s → 1.9 s / 张（厂商宣称） 📣 [来源](https://x.com/fractalyze_io/status/2105207217452695841)
- **Qwen-Image 2.1** · SGLang `spark-image-lab BF16 / SGLa…` — 1× DGX Spark（对照 4090） → 52.6 s / 1024²；SGLang 表：Spark 35.4 s，4090 18.7 s 🔁 [来源](https://x.com/yume_arasaki/status/2103277400234860878)
- **Qwen-Image-2.1-Turbo（官方 8 步）** `Turbo 8 步 vs Base 40 步` — RTX 5090 → 29 s vs 108 s / 张（2048²） ✅ [来源](https://x.com/niklaslenz_ai/status/2108609693941920176)
- **Z-Image Turbo vs Qwen-Image 2.1** `同 prompt 同 seed 20 轮` — RTX 5090 → Z-Image 快约 2×（无绝对时间）；质量 Qwen 9:6 胜 ✅ [来源](https://x.com/princedoesai/status/2109376490009743713)

**🎬 影音**

- **FastH3 V2（MiniMax H3 8 步蒸馏）** `NVFP4` — RTX 5090 32GB → 832×480×5s：14.8 s；1344×768×5s：38.6 s（含音频，端到端） 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/) · [指南](recipes/video-audio-001.zh-CN.md)
- **FastH3 Trim（42 块剪枝，实验）** `NVFP4` — RTX 5090 → 480p 5s：13.4 s；768p：35.4 s 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/)
- **FastH3 V2 / Trim** `NVFP4` — 1× / 2× DGX Spark → 1×：480p 141.4 / 125.8 s，Trim 768p 340.1 s；2×：87.2 / 78.3 s 🏛️ [来源](https://haoailab.com/blogs/fasth3-rtx/)
- **MiniMax H3（基础，50 步类）** · ComfyUI `ComfyUI + SageAttention` — RTX 5090 → 1280×736×5s：242 s → 168 s ✅ [来源](https://x.com/RKAScope/status/2084359480926503182)
- **MiniMax H3 vs FastH3 Turbo** `同图同 seed` — RTX 5090 → 15 s 片段：11 分 55 秒 vs 2 分 6 秒 ✅ [来源](https://x.com/Sogni_Protocol/status/2097254959729246550)
- **MiniMax H3（Sol 加速 / 无加速）** · NVIDIA Sol `NVIDIA Sol 引擎` — 1× DGX Spark → Sol：480p 5 s 约 68 s（NVIDIA 公布 56 s）；无 Sol >400 s；无 Sol 720p 20 步：5 s … ✅ [来源](https://x.com/yume_arasaki/status/2100734364908986511)
- **MiniMax H3 vs LTX-2.3 Eros** `同条件 3 组 prompt` — 1× DGX Spark → 864×480×5s：H3 平均 270 s；LTX 154 s（快 1.76×） ✅ [来源](https://x.com/YRSM_Simon/status/2084222856972456336)
- **LTX-2.3（带口型同步）** · ComfyUI `ComfyUI` — RTX 5090 → 10 s 约 90 s（较弱 GPU 约 6×） ✅ [来源](https://x.com/freshstartsnow/status/2092263835591655773)
- **LTX-2.5（t2v）** `模板 + LoRA` — RTX 5090（500W） → 720p/10 s：61.11 s；1080p/10 s：189.90 s ✅ [来源](https://x.com/PhotogenicWeekE/status/2087298681137701274)
- **ACE-Step 1.5 + LTX-2.3** · ComfyUI `ComfyUI 串行工作流` — 1× DGX Spark → 2 分 05 秒歌曲一次生成；+2:28 口型视频端到端 32 分钟 🔁 [来源](https://x.com/yume_arasaki/status/2100734364908986511)
- **Wan2.1 14B（SparkDiffusion）** `97% 稀疏注意力 + 3 步蒸馏 + FP8` — RTX 5090 → 720p：4,769 s → 18 s（项目宣称 265×） 📣 [来源](https://x.com/thePandaily/status/2105209996648567243)
- **MiniMax H3** · LightX2V — RTX 5090 → 768×1344 15s 视频+音频 ≈72 s（稳态，不含 MP4 导出；基线 ~26 分钟） 🏛️ [来源](https://x.com/LightX2V/status/2108769912009424976)

## 第 3 档 · 7,000–14,000 美元

*双 Spark、Mac Studio Ultra* · 共 63 条


**📝 文字**

- **Qwen3.8-27B** · TensorFold `预填用 NVFP4（cuBLASLt），生成用 3.0…` — 2× DGX Spark（双机张量并行） → **190 tok/s** ✅ [来源](https://x.com/BHCC2025/status/2117272695637443025)
- **Qwen3.8-27B** · vLLM `NVFP4` — 2× RTX 5090（P2P 驱动） → **160 tok/s** 📣 [来源](https://www.reddit.com/r/LocalLLM/comments/1x5u4yf/comment/pgqv4uy/)
- **Qwen3.8-Flash-Next** · oMLX `unsloth UD-Q6_K_XL` — Mac Studio M5 Ultra 256GB → **141 tok/s** ✅ [来源](https://www.reddit.com/r/LocalLLaMA/comments/1xdp654/)
- **Qwen3.8-Flash-Next 4/8-bit** · mlx-serve `4/8-bit mixed` — Mac Studio M5 Ultra 256GB → **126 tok/s** ✅ [来源](https://x.com/LocalSilicon/status/2106175358160793817)
- **DeepSeek-V4.1-Flash** · TensorFold — 2× DGX Spark → **95 tok/s** ✅ [来源](https://x.com/Urthoo/status/2106426248759005362)
- **Qwen3.8-Flash-Next** · vLLM `nvidia FP4-Local + MTP 4` — 2× DGX Spark（QSFP 直连，TP2） → **95 tok/s** 🏛️ [来源](https://github.com/atakann/dgx-spark-recipes/blob/8a15075/recipes/llm/qwen3.8-flash-next-fp4-vllm-tp2.yaml)
- **DeepSeek-V4.1-Flash-1017** · TensorFold `MiaAI EXL3 2.9bpw（v1）+ DSpa…` — 2× DGX Spark（QSFP 直连） → **88.7 tok/s** ✅ [来源](https://x.com/atasrb/status/2113681338532253775)
- **GLM-5.3-Flash（320B/18B 激活）** · TensorFold `MiaAI_lab EXL3 4 bpw` — 2× DGX Spark → **83 tok/s** ✅ [来源](https://x.com/atasrb/status/2117267112464925027)
- **DeepSeek-V4-Flash (0731 GA)** `官方 FP8 权重` — 2× DGX Spark → **82 tok/s** ✅ [来源](https://x.com/MiaAI_lab/status/2083326111144906836)
- **Ling-3.0-flash** · SGLang `FP8 + FP8 lm_head + MTP3（不用…` — 2× DGX Spark → **82 tok/s** ✅ [来源](https://x.com/atasrb/status/2116085996965990514)
- *……另有 53 条，见 [配方库](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN)。*

## 第 4 档 · 14,000–30,000 美元

*3–4 台 Spark 集群、多卡工作站* · 共 36 条


**📝 文字**

- **Qwen3.8-27B** · SGLang `NVFP4` — RTX PRO 6000 → **300 tok/s** ✅ [来源](https://x.com/MiaAI_lab/status/2090327658508763516)
- **Qwen3.8-Flash-Next** · TensorFold `NVIDIA FP4 官方权重 + MTP 草稿，FP…` — 1× RTX PRO 6000 Blackwell 96GB → **271.4 tok/s** ✅ [来源](https://x.com/MiaAI_lab/status/2117202027226783782)
- **Recursive Flint 40B-A2.5B** · llama.cpp `Q8_0 GGUF（MoE）` — 1× RTX PRO 6000 Blackwell 96GB → **244 tok/s** ✅ [来源](https://www.reddit.com/r/nvidia/comments/1xd0f7x/)
- **Swift-1.5-Qwen3.8-Flash-Next** · ninfer `NVFP4+FP8 · MTP 3（Ninfer600…` — RTX PRO 6000 Blackwell 96GB @ 600W + 96GB DDR4 + Ryzen 5 56… → **238 tok/s** ✅ [来源](https://demietrich.com/blog/q3.8fn_engine_comparison/)
- **Qwen3.8-Flash-Next** · SGLang (Penny Royal fork) `未注明` — 1× RTX PRO 6000 Blackwell 96GB（限 300W） → **200 tok/s** ✅ [来源](https://x.com/jhsmith409/status/2117236468871569860)
- **Qwen3.8-Flash-Next** · vLLM `NVFP4 · MTP 2` — RTX PRO 6000 Blackwell 96GB @ 600W + 96GB DDR4 + Ryzen 5 56… → **150 tok/s** ✅ [来源](https://demietrich.com/blog/q3.8fn_engine_comparison/)
- **DeepSeek-V4.1-Flash-1017** · spark-ds41f `官方 1017 权重（MXFP4/FP8）` — 4× DGX Spark（GB10） → **136 tok/s** ✅ [来源](https://x.com/machigurixmeru/status/2116835181558694130)
- **DeepSeek-V4.1-Flash-1017** · TensorFold `LakyFx EXL3 3.5bpw` — 3× DGX Spark（TP3） → **126.1 tok/s** ✅ [来源](https://x.com/laky_fx/status/2113654994847117605)
- **DeepSeek-V4.1-Flash-1017** · TensorFold `原生权重` — 4× GB10（DGX Spark，TP4） → **121 tok/s** 🏛️ [来源](https://x.com/bertholomusai/status/2113835774873600136)
- **DeepSeek-V4.1-Flash** · TensorFold `官方权重（MiaAI_lab recipe）` — 4× DGX Spark（GB10，无交换机环） → **111 tok/s** ✅ [来源](https://x.com/kevintheoo/status/2114654160293433558)
- *……另有 26 条，见 [配方库](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN)。*

## 价格未公开

按张计价的多卡组合、未注明内存（因而无法定价）的 Mac 以及其他没有单一公开价格的配方 · 共 459 条。按 tok/s 排名靠前的文字配方：

- **Qwen3.6-35B-A3B** · SGLang `NVFP4` — 1× RTX 5090 → **626 tok/s** 🏛️ [来源](https://github.com/jhsmith409/sglang-elsa)
- **Qwen3.5-2B** · webyIQ `int4 GPTQ（group 32），约 1.1GB` — RTX 5080（Chrome 156，WebGPU） → **620 tok/s** 📣 [来源](https://www.reddit.com/r/LocalLLM/comments/1xmcqkb/)
- **Qwen3.8-27B** · TensorFold `z-lab DFlash2 草稿（BobClawbla…` — 1× RTX 5090 → **538.1 tok/s** ✅ [来源](https://x.com/BobClawblaw/status/2114570274511405354)
- **Gemma 4 31B** · Radiance `W4A8 + DFlash2 block-16 草稿（…` — 4× Radeon AI PRO R9700 32GB → **445.8 tok/s** 📣 [来源](https://codeberg.org/StillDeadcode/radiance/issues/248)
- **LFM3-1.7B** · llama.cpp `未注明` — RTX 3090 24GB → **384 tok/s** ✅ [来源](https://x.com/Layton_Gott/status/2115244678056464384)
- **Gemma 4 31B** · Radiance `W4A8 + RedHatAI DFlash2 草稿（…` — 4× Radeon AI PRO R9700 32GB → **377.7 tok/s** 📣 [来源](https://codeberg.org/StillDeadcode/radiance/issues/247)
- **Qwen3.8-Flash-Next** · QEngine `INT4 AutoRound（QEngine 自带）` — 2× RTX 5090 32GB + Threadripper PRO 3975WX + 251GB RAM → **370 tok/s** ✅ [来源](https://www.reddit.com/r/LocalLLaMA/comments/1xjx0ez/)
- **Qwen3.8-Flash-Next** · Basalt `NVIDIA NVFP4（引擎自行转换）` — 1× RTX 5090（限 400W）+ 128GB RAM → **354 tok/s** 🏛️ [来源](https://www.reddit.com/r/LocalLLaMA/comments/1xdlunp/)
- **Qwen3.6-35B-A3B** · Kapitsa `Q4 + KFlash` — MacBook Pro 16 M5 Max 128GB → **346 tok/s** 📣 [来源](https://www.reddit.com/r/LocalLLaMA/comments/1xlgu8m/)
- **Qwen3.8-Flash-Next** · Basalt `Basalt NVFP4-DQ8` — RTX 5090 32GB + RTX 5060 Ti 16GB + 128GB RAM → **300 tok/s** 📣 [来源](https://www.reddit.com/r/LocalLLaMA/comments/1xn4qn1/)
- **Qwen3.8-Flash-Next** · vLLM `nvidia FP4-Local（NVFP4），FP8…` — 1× RTX PRO 6000 Blackwell 96GB（限 450W） → **287 tok/s** ✅ [来源](https://www.reddit.com/r/LocalLLM/comments/1xj9ura/)
- **Qwen3.8-Flash-Next** · Strata `Q2_0（另测 IQ3_S）` — RTX 5090 + Ryzen 9 9950X（Windows） → **270.7 tok/s** ✅ [来源](https://github.com/Niko1221/Strata/issues/4166)
- *……全部 459 条见 [配方库](https://raytone-lab.github.io/awesome-local-inference-recipes/explore.html?lang=zh-CN)。*


## 引擎与工具

| 项目                                                                 | ⭐ Star | 实时                                                                                              | 最后推送       | 简介                                                                                                           |
| ------------------------------------------------------------------ | ------ | ----------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------ |
| [llama.cpp](https://github.com/ggml-org/llama.cpp)                 | 132.8k | ![stars](https://img.shields.io/github/stars/ggml-org/llama.cpp?style=flat&label=)              | 2026-10-30 | 基准 GGUF 引擎，支持 CPU/CUDA/ROCm/Vulkan/Metal。                                                                    |
| [vLLM](https://github.com/vllm-project/vllm)                       | 95.9k  | ![stars](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&label=)               | 2026-10-30 | 高吞吐推理服务；Spark 上的 MTP 和多路并发配方。                                                                                |
| [SGLang](https://github.com/sgl-project/sglang)                    | 38.3k  | ![stars](https://img.shields.io/github/stars/sgl-project/sglang?style=flat&label=)              | 2026-10-30 | 推理服务框架；DGX Spark 上与 DFlash2 搭配。                                                                              |
| [Strata](https://github.com/Niko1221/Strata)                       | 36.3k  | ![stars](https://img.shields.io/github/stars/Niko1221/Strata?style=flat&label=)                 | 2026-10-29 | 把 MoE 专家拆到显存、内存和 SSD 的推理引擎，面向 12–24GB 显卡；本库多数 Flash-Next 配方用它。从 0.2.8 起，12GB 及以下的 RTX 显卡默认关闭 route prior。    |
| [MLX](https://github.com/ml-explore/mlx)                           | 29.0k  | ![stars](https://img.shields.io/github/stars/ml-explore/mlx?style=flat&label=)                  | 2026-10-30 | Apple 的数组框架，多数 Mac 配方基于它。                                                                                    |
| [ds4 (DwarfStar)](https://github.com/antirez/ds4)                  | 24.2k  | ![stars](https://img.shields.io/github/stars/antirez/ds4?style=flat&label=)                     | 2026-10-23 | 面向 DeepSeek 4 Flash/PRO 的本地推理引擎，支持 Metal、CUDA 和 ROCm。                                                        |
| [oMLX](https://github.com/jundot/omlx)                             | 23.2k  | ![stars](https://img.shields.io/github/stars/jundot/omlx?style=flat&label=)                     | 2026-10-30 | Apple Silicon 上的 MLX 推理服务，支持连续批处理和分层 KV/SSD 缓存。                                                              |
| [WebLLM](https://github.com/mlc-ai/web-llm)                        | 19.3k  | ![stars](https://img.shields.io/github/stars/mlc-ai/web-llm?style=flat&label=)                  | 2026-10-30 | 基于 WebGPU 在浏览器里运行 LLM。                                                                                       |
| [MNN](https://github.com/alibaba/MNN)                              | 16.3k  | ![stars](https://img.shields.io/github/stars/alibaba/MNN?style=flat&label=)                     | 2026-10-30 | 阿里巴巴的端侧推理引擎，用于手机和边缘设备上的 LLM。                                                                                 |
| [turbo-fieldfare](https://github.com/drumih/turbo-fieldfare)       | 7.1k   | ![stars](https://img.shields.io/github/stars/drumih/turbo-fieldfare?style=flat&label=)          | 2026-10-26 | 在 M 系列 MacBook 上用约 2GB 内存运行 Gemma 4 26B-A4B（项目自述）。                                                           |
| [DFlash / DFlash 2](https://github.com/z-lab/dflash)               | 6.2k   | ![stars](https://img.shields.io/github/stars/z-lab/dflash?style=flat&label=)                    | 2026-08-18 | 块扩散投机解码；DFlash 2 提供 Qwen3.8-27B 草稿模型。                                                                        |
| [Lemonade](https://github.com/lemonade-sdk/lemonade)               | 6.0k   | ![stars](https://img.shields.io/github/stars/lemonade-sdk/lemonade?style=flat&label=)           | 2026-10-30 | 面向 AMD Ryzen AI NPU/核显及其他 GPU 的本地 LLM 服务。                                                                    |
| [FastVideo](https://github.com/hao-ai-lab/FastVideo)               | 4.8k   | ![stars](https://img.shields.io/github/stars/hao-ai-lab/FastVideo?style=flat&label=)            | 2026-10-30 | 统一的加速视频生成推理与后训练框架；VSA / FastH3 的上游。                                                                          |
| [Rapid-MLX](https://github.com/raullenchai/Rapid-MLX)              | 4.1k   | ![stars](https://img.shields.io/github/stars/raullenchai/Rapid-MLX?style=flat&label=)           | 2026-10-30 | Apple Silicon 上兼容 OpenAI/Anthropic API 的 MLX 推理服务，支持 MTP 解码，并有公开的社区基准榜。                                      |
| [LightX2V](https://github.com/ModelTC/LightX2V)                    | 3.0k   | ![stars](https://img.shields.io/github/stars/ModelTC/LightX2V?style=flat&label=)                | 2026-10-30 | 视频生成推理框架，有 5090 上的 MiniMax H3 结果。                                                                            |
| [Project Maya](https://github.com/mw00/project-maya)               | 2.3k   | ![stars](https://img.shields.io/github/stars/mw00/project-maya?style=flat&label=)               | 2026-10-30 | 在 1–16 张 NVIDIA 或 AMD 显卡上运行 GLM-5.3-Flash（仓库标注为 321B MoE），含引擎、服务、仪表盘和量化工具。                                   |
| [mlx-serve](https://github.com/ddalcu/mlx-serve)                   | 2.2k   | ![stars](https://img.shields.io/github/stars/ddalcu/mlx-serve?style=flat&label=)                | 2026-10-30 | Apple Silicon 原生 LLM 服务（Zig 后端 + Swift 前端），兼容 OpenAI 和 Anthropic API，不依赖 Python。                             |
| [TensorFold](https://github.com/ashhart/TensorFold)                | 1.5k   | ![stars](https://img.shields.io/github/stars/ashhart/TensorFold?style=flat&label=)              | 2026-10-30 | 兼容 OpenAI 接口的 MoE 运行时，带投机解码；也用于 ComfyUI 里的 MiniMax H3。当前版本 1.1.9（2026-10-29）；提交 3abeeff 修复了一个 prompt 缓存 bug。 |
| [halogen](https://github.com/peonist-ai/halogen-flash-server)      | 1.1k   | ![stars](https://img.shields.io/github/stars/peonist-ai/halogen-flash-server?style=flat&label=) | 2026-10-30 | 针对 Strix Halo 调优的 Flash-Next 服务。                                                                             |
| [ComfyUI-Ref2VA-VSA](https://github.com/Kablex/ComfyUI-Ref2VA-VSA) | 878    | ![stars](https://img.shields.io/github/stars/Kablex/ComfyUI-Ref2VA-VSA?style=flat&label=)       | 2026-10-17 | ComfyUI 节点：把 FastVideo VSA 门控接到 MiniMax H3 Ref2VA；作者 RTX 4090 基准约 650s（50 步稠密）→ 预热约 72s（4 步 VSA+Turbo）。      |
| [dflash-mlx](https://github.com/bstnxbt/dflash-mlx)                | 791    | ![stars](https://img.shields.io/github/stars/bstnxbt/dflash-mlx?style=flat&label=)              | 2026-08-20 | Apple Silicon（MLX）上的 DFlash 投机解码。                                                                            |
| [VDN-H3](https://github.com/OpenVDN/vdn-minimax-h3)                | 659    | ![stars](https://img.shields.io/github/stars/OpenVDN/vdn-minimax-h3?style=flat&label=)          | 2026-10-05 | 在 MiniMax H3 上的 Video Delta Net 混合注意力（窗口 softmax + 线性适配器），面向 T2VA / I2VA / Ref2VA 类任务。                       |
| [janas](https://github.com/prabanta-dev/janas)                     | 478    | ![stars](https://img.shields.io/github/stars/prabanta-dev/janas?style=flat&label=)              | 2026-10-30 | 纯 C 写的推理引擎，可在 CPU 或 GPU 上运行比内存还大的模型；项目自称 32GB 笔记本跑 Qwen3-Next-80B 可达 37 tok/s（带 draft）。                      |
| [ComfyUI-VDN-H3](https://github.com/Saganaki22/ComfyUI-VDN-H3)     | 243    | ![stars](https://img.shields.io/github/stars/Saganaki22/ComfyUI-VDN-H3?style=flat&label=)       | 2026-09-12 | MiniMax H3 上 VDN-H3 混合注意力的 ComfyUI 节点。                                                                       |
| [Paiton](https://github.com/Eliovp-BV/paiton-vllm-plugin)          | 108    | ![stars](https://img.shields.io/github/stars/Eliovp-BV/paiton-vllm-plugin?style=flat&label=)    | 2026-10-30 | 针对 R9700 等 AMD Radeon 显卡调优的 vLLM 插件和运行时。                                                                     |
| [Halowin Bubo](https://github.com/haloforge-labs/bubo)             | 18     | ![stars](https://img.shields.io/github/stars/haloforge-labs/bubo?style=flat&label=)             | 2026-10-27 | Gufo 的分支，在原生 Windows 上用 AMD HIP 运行，针对 Strix Halo 笔记本调优。                                                      |
| [libstrix](https://github.com/asf0/libstrix)                       | 7      | ![stars](https://img.shields.io/github/stars/asf0/libstrix?style=flat&label=)                   | 2026-10-30 | 面向 AMD Strix Halo（gfx1151）的 HIP 内核和 vLLM 插件，可在上游 vLLM 上运行。                                                   |
| [FastH3](https://haoailab.com/blogs/fasth3-rtx/)                   | —      | *（网站/博客）*                                                                                       | —          | Hao AI Lab 的 8 步蒸馏版 MiniMax H3，面向 RTX 显卡（博客）。                                                                |
| [Espetero](https://github.com/JarJarFran/espetero)                 | 0      | ![stars](https://img.shields.io/github/stars/JarJarFran/espetero?style=flat&label=)             | 2026-10-27 | Apple Silicon 上的原生 Metal 推理引擎，提供 OpenAI、Anthropic 和 Ollama 接口。                                               |
| [Strim](https://github.com/megasoft1978/strim-engine)              | 0      | ![stars](https://img.shields.io/github/stars/megasoft1978/strim-engine?style=flat&label=)       | 2026-10-30 | Apple Silicon 上运行 Qwen3.8-27B 的 Swift/MLX 引擎；速度数字来自作者本人。                                                     |

<sub>⭐ 快照由 `scripts/update_stars.py` 更新于 2026-10-30T13:41Z（UTC）· 「实时」徽章由 shields.io 在打开页面时实时渲染。</sub>

## 相关榜单与清单

| 项目                                                                          | ⭐ Star | 实时                                                                                              | 最后推送       | 简介                      |
| --------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------- | ---------- | ----------------------- |
| [Awesome-LLM-Inference](https://github.com/xlite-dev/Awesome-LLM-Inference) | 5.5k   | ![stars](https://img.shields.io/github/stars/xlite-dev/Awesome-LLM-Inference?style=flat&label=) | 2026-10-20 | 推理方向论文与代码合集。            |
| [awesome-local-llm](https://github.com/rafska/awesome-local-llm)            | 3.0k   | ![stars](https://img.shields.io/github/stars/rafska/awesome-local-llm?style=flat&label=)        | 2026-10-28 | 本地大模型平台与工具目录。           |
| [LocalScore](https://github.com/cjpais/LocalScore)                          | 136    | ![stars](https://img.shields.io/github/stars/cjpais/LocalScore?style=flat&label=)               | 2026-10-09 | 标准化的单卡跑分 CLI。           |
| [llamabench.ai](https://llamabench.ai/)                                     | —      | *（网站/博客）*                                                                                       | —          | llama.cpp 跑分结果，附完整启动命令。 |
| [llamaperf](https://llamaperf.com/leaderboard)                              | —      | *（网站/博客）*                                                                                       | —          | 社区自报排行榜（给中位数）。          |
| [canirun.ai](https://canirun.ai/)                                           | —      | *（网站/博客）*                                                                                       | —          | 估算模型能否在你的硬件上运行、跑多快。     |

<sub>⭐ 快照由 `scripts/update_stars.py` 更新于 2026-10-30T13:41Z（UTC）· 「实时」徽章由 shields.io 在打开页面时实时渲染。</sub>

## 参与贡献

一条配方一个 PR。从 [提交页](https://raytone-lab.github.io/awesome-local-inference-recipes/submit.html?lang=zh-CN) 复制 YAML 模板，只填来源里写明的内容（其余写 `null`），运行 `node scripts/validate.mjs` 校验并附上原帖链接。然后运行 `python3 scripts/gen_readme.py` 重新生成全部 README。优先收录新模型和新硬件发布后几周内的配方，以及非主流组合；常规重复配方合并进已有条目。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

本地开发：`python3 -m http.server 5190` → `index.html`（首页）· `explore.html`（筛选、排序、散点图）· 数据格式见 [`schema/recipe.schema.json`](schema/recipe.schema.json)。

给 AI agent：技能 [`.agents/skills/local-inference-recipe-finder`](.agents/skills/local-inference-recipe-finder/SKILL.md) 检测本机硬件，并从 [`data/hw_index.json`](docs/hw_index.md) 推荐配方。详见 [AGENTS.md](AGENTS.md)。

<details><summary>网站预览</summary>

<img src="docs/screenshot.zh-CN.png" width="760" alt="网站首页截图：配方数、引擎数、实测数和各预算档最快的实测配置">

</details>

## 许可证

- 代码：[MIT](LICENSE)
- 数据（`data/`）：[CC BY 4.0](LICENSE-DATA)。可自由使用，需署名 Awesome Local Inference Recipes 并保留每条配方的原始来源链接。
