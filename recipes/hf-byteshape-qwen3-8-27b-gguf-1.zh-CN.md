# Qwen3.8-27B · llama.cpp · RTX 5090 32GB

[English](hf-byteshape-qwen3-8-27b-gguf-1.md) | **简体中文** | [日本語](hf-byteshape-qwen3-8-27b-gguf-1.ja.md) · [← 返回列表](../README.zh-CN.md)

> 来源等级: **📣 宣称** · 日期: 2026-08-18 · 数字来自来源。本仓库未复测。

## 硬件

- RTX 5090 32GB (NVIDIA 消费级)
- 参考价格: 仅显卡 $5,400 起（2026-10-11 最低追踪街价，MSRP $1,999，见 prices.json）

## 模型

- Qwen3.8-27B · `ShapeLearn 混合量化 GPU-1（2.56 bpw，标签 IQ2_XXS）`
- 下载: [huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)

## 引擎

- llama.cpp — 安装见 https://github.com/ggml-org/llama.cpp
- 备注: llama.cpp（-np 1 -fa on）

## 启动命令

```bash
llama-server -hf byteshape/Qwen3.8-27B-GGUF:<tag> --spec-type draft-mtp --spec-draft-n-max 3
```

命令为来源节选（含 `...` 或占位符）。完整参数见来源。

## 关键参数

- 上下文: —
- 并发: 单流（-np 1）
- 标签: `2bit`, `dense`, `speculative`

## 预期速度

- 119.0 tok/s 生成。同卡其他档：GPU-2（2.88 bpw）111、GPU-3（3.01 bpw）108、GPU-4（3.23 bpw）104、GPU-5（3.84 bpw）94；开 DFlash2（7 个草稿 token，仅文本）后 GPU-1 176、GPU-5 167 (📣 宣称)

## 注意事项

- 非一手实测（宣称或转述）。实际速度可能不同。
- HF 模型卡（作者自报）; 思考模式采样；混合 coding/math/IF/常识 prompt; 单流、无投机
- 速度随驱动、引擎版本、上下文长度和提示长度变化。

## 来源与致谢

- [https://huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- 版权归原作者。本页仅摘要并链接。数据以 CC BY 4.0 发布。
