# Qwen3.8-27B · llama.cpp · RTX 5090 32GB

[English](hf-byteshape-qwen3-8-27b-gguf-1.md) | [简体中文](hf-byteshape-qwen3-8-27b-gguf-1.zh-CN.md) | **日本語** · [← 一覧に戻る](../README.ja.md)

> 出典レベル: **📣 主張** · 日付: 2026-08-18 · 数値は出典からの引用です。このリポジトリでは再計測していません。

## ハードウェア

- RTX 5090 32GB (NVIDIA コンシューマー)
- 参考価格: ≈ $5,400

## モデル

- Qwen3.8-27B · `ShapeLearn mixed quantization GPU-1 (2.56 bpw, label IQ2_XXS)`
- ダウンロード: [huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)

## エンジン

- llama.cpp — インストール： https://github.com/ggml-org/llama.cpp
- 備考: llama.cpp (-np 1 -fa on)（英語）

## 起動コマンド

```bash
llama-server -hf byteshape/Qwen3.8-27B-GGUF:<tag> --spec-type draft-mtp --spec-draft-n-max 3
```

出典からの抜粋です（`...` またはプレースホルダーを含みます）。全引数は出典を参照してください。

## 主なパラメータ

- コンテキスト: —
- 同時実行: single stream (-np 1)（英語）
- タグ: `2bit`, `dense`

## 想定速度

- 119.0 tok/s decode. Other tiers on the same card: GPU-2 (2.88 bpw) 111, GPU-3 (3.01 bpw) 108, GPU-4 (3.23 bpw) 104, GPU-5 (3.84 bpw) 94. Qualification: with DFlash2 (7 drafts, text only) GPU-1 176 and GPU-5 167, not the headline（英語） (📣 主張)

## 注意点

- 本人による実測ではありません（主張または伝聞）。実際の速度は異なる場合があります。
- 速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。

## 出典とクレジット

- [https://huggingface.co/byteshape/Qwen3.8-27B-GGUF](https://huggingface.co/byteshape/Qwen3.8-27B-GGUF)
- 権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。
