# Qwen3.8-27B · llama.cpp · RTX 5090 32GB

**English** | [简体中文](hf-byteshape-qwen3-8-27b-gguf-1.zh-CN.md) | [日本語](hf-byteshape-qwen3-8-27b-gguf-1.ja.md) · [← All recipes](../README.md)

> Source level: **📣 Claimed** · Date: 2026-08-18 · Numbers come from the source. This repo did not measure them again.

## Hardware

- RTX 5090 32GB (NVIDIA consumer)
- Reference cost: ≈ $5,400

## Model

- Qwen3.8-27B · `ShapeLearn mixed quantization GPU-1 (2.56 bpw, label IQ2_XXS)`
- Download: [huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)

## Engine

- llama.cpp — install: https://github.com/ggml-org/llama.cpp
- Note: llama.cpp (-np 1 -fa on)

## Launch command

```bash
llama-server -hf byteshape/Qwen3.8-27B-GGUF:<tag> --spec-type draft-mtp --spec-draft-n-max 3
```

Excerpt from the source (includes `...` or placeholders). See the source for full arguments.

## Key parameters

- Context: —
- Concurrency: single stream (-np 1)
- Tags: `2bit`, `dense`

## Expected speed

- 119.0 tok/s decode. Other tiers on the same card: GPU-2 (2.88 bpw) 111, GPU-3 (3.01 bpw) 108, GPU-4 (3.23 bpw) 104, GPU-5 (3.84 bpw) 94. Qualification: with DFlash2 (7 drafts, text only) GPU-1 176 and GPU-5 167, not the headline (📣 Claimed)

## Caveats

- Not a first-hand measurement (claimed or relayed). Your results can differ.
- Speed changes with drivers, engine version, context length, and prompt length.

## Source & attribution

- [https://huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- Credit to the original author. This page only summarizes and links. Data under CC BY 4.0.
