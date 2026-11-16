# DeepSeek-V4.1-Flash-1017 · Strata (Strata-DS fork) · 1× DGX Spark（GB10，128GB 统一内存，4TB NVMe）

[English](comm-056.md) | **简体中文** | [日本語](comm-056.ja.md) · [← 返回列表](../README.zh-CN.md)

> 来源等级: **✅ 实测** · 日期: 2026-10-18 · 数字来自来源。本仓库未复测。

## 硬件

- 1× DGX Spark（GB10，128GB 统一内存，4TB NVMe） (DGX Spark)
- 参考价格: $6,950（128GB，2026-10-11）

## 模型

- DeepSeek-V4.1-Flash-1017 · `LibertAIDAI EXL3 2.9bpw（专家；dense 5 / head 6）+ 官方 1017 其余张量与 Engram（单机，DSpark 每步起草，SSD 尾部跳过）`
- 下载: [huggingface.co/LibertAIDAI/DeepSeek-V4.1-Flash-1017-EXL3-2.9bpw](https://huggingface.co/LibertAIDAI/DeepSeek-V4.1-Flash-1017-EXL3-2.9bpw) · [huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)

## 引擎

- Strata (Strata-DS fork) — 安装见 https://github.com/Jackwwg83/Strata-DS
- 备注: Strata-DS（Strata 分支，自带 DeepSeek 引擎 ds41_serve，C++/CUDA；热专家放在统一内存的 RAM 层，由 GPU 原地计算；冷专家按需从 SSD 读取；使用 sudoingX 的 exl3_smoe 与 exl3_mrow EXL3 内核）

## 启动命令

```bash
git clone https://github.com/Jackwwg83/Strata-DS.git && cd Strata-DS && ./setup.sh --setup --yes --family deepseek --no-start && ./run-deepseek-1017-exl3-2.9bpw.sh
```

## 关键参数

- 上下文: 256K（262,144）
- 并发: 单路
- 标签: `2bit`, `MoE`, `long-context`, `speculative`, `offload`

## 预期速度

- 真实编码智能体会话 48 轮（上下文 10K–91K）共 70,211 token 平均 30.8 tok/s（每轮 23.6–36.4，中位 28.6）；单次测：上下文 8K/32K/64K/128K/250K 解码 24.2/27.4/27.4/27.3/22.9；智能体每轮新增 ≤50 token 首字中位 0.57 s，同一 10K 系统提示开新会话 0.25 s；冷预填充约 500 tok/s（250K 8.3 分钟）；vs 官方 MXFP4 KL 0.074 / top-1 88.6% (✅ 实测)

## 注意事项

- Strata-DS 配方页，作者实测（原始数据 ds41/bench/results/2026-10-18-spark；setup 在 GB10 上自动选此配方，从 LibertAIDAI/DeepSeek-V4.1-Flash-1017-EXL3-2.9bpw 与 deepseek-ai/DeepSeek-V4.1-Flash-1017 下载 414.8 GB 并打包；新 clone 复现的包与…
- 速度随驱动、引擎版本、上下文长度和提示长度变化。

## 来源与致谢

- [https://github.com/Jackwwg83/Strata-DS/blob/main/docs/DEEPSEEK_SPARK.md](https://github.com/Jackwwg83/Strata-DS/blob/main/docs/DEEPSEEK_SPARK.md)
- 版权归原作者。本页仅摘要并链接。数据以 CC BY 4.0 发布。
