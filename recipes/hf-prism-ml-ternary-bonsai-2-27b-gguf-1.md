# Ternary Bonsai 2 27B · llama.cpp (PrismML fork) · RTX 5090 32GB

**English** | [简体中文](hf-prism-ml-ternary-bonsai-2-27b-gguf-1.zh-CN.md) | [日本語](hf-prism-ml-ternary-bonsai-2-27b-gguf-1.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-09-16 · Numbers come from the source. This repo did not measure them again.

## Hardware

- RTX 5090 32GB (NVIDIA consumer)
- Reference cost: ≈ $5,400

## Model

- Ternary Bonsai 2 27B · `PQ2_0`
- Download: [huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)

## Engine

- llama.cpp (PrismML fork) — install: https://github.com/ggml-org/llama.cpp
- Note: PrismML-Eng/llama.cpp fork (llama-bench, batch 1, depth 0)

## Launch command

```bash
llama-cli ... -ngl 99 -fa on -c 32768 (requires the PrismML llama.cpp fork; stock llama.cpp does not work)
```

Excerpt from the source (includes `...` or placeholders). See the source for full arguments.

## Key parameters

- Context: 262K (model card); example command -c 32768
- Concurrency: batch 1 (single stream)
- Tags: `ternary`, `dense`, `long-context`

## Expected speed

- 129.9 tok/s decode; 3893 tok/s prefill; PTQ1_0 120.5 tok/s decode, 1805 tok/s prefill (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed or relayed). Your results can differ.
- Speed changes with drivers, engine version, context length, and prompt length.

## Source & attribution

- [https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- Credit to the original author. This page only summarizes and links. Data under CC BY 4.0.
