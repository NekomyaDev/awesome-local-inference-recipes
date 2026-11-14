# Ternary Bonsai 2 27B · llama.cpp (PrismML fork) · RTX 5090 32GB

[English](hf-prism-ml-ternary-bonsai-2-27b-gguf-1.md) | **简体中文** | [日本語](hf-prism-ml-ternary-bonsai-2-27b-gguf-1.ja.md) · [← 返回列表](../README.zh-CN.md)

> 来源等级: **📣 宣称** · 日期: 2026-09-16 · 数字来自来源。本仓库未复测。

## 硬件

- RTX 5090 32GB (NVIDIA 消费级)
- 参考价格: 仅显卡 $5,400 起（2026-10-11 最低追踪街价，MSRP $1,999，见 prices.json）

## 模型

- Ternary Bonsai 2 27B · `PQ2_0`
- 下载: [huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)

## 引擎

- llama.cpp (PrismML fork) — 安装见 https://github.com/ggml-org/llama.cpp
- 备注: PrismML-Eng/llama.cpp fork（llama-bench，batch 1，depth 0）

## 启动命令

```bash
llama-cli ... -ngl 99 -fa on -c 32768（需 PrismML llama.cpp fork，原生 llama.cpp 不可用）
```

命令为来源节选（含 `...` 或占位符）。完整参数见来源。

## 关键参数

- 上下文: 262K（卡称）；示例命令 -c 32768
- 并发: batch 1（单路）
- 标签: `ternary`, `dense`, `long-context`

## 预期速度

- 129.9 tok/s 生成；3893 tok/s 读入；PTQ1_0 120.5 tok/s 生成，1805 tok/s 读入 (📣 宣称)

## 注意事项

- 非一手实测（宣称或转述）。实际速度可能不同。
- HF 模型卡（作者自报）; 需 PrismML llama.cpp fork（原版 llama.cpp 不可用）
- 速度随驱动、引擎版本、上下文长度和提示长度变化。

## 来源与致谢

- [https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- 版权归原作者。本页仅摘要并链接。数据以 CC BY 4.0 发布。
