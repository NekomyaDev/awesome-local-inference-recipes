# Ternary Bonsai 2 27B · llama.cpp (PrismML fork) · MacBook M5 Pro

[English](hf-prism-ml-ternary-bonsai-2-27b-gguf-5.md) | [简体中文](hf-prism-ml-ternary-bonsai-2-27b-gguf-5.zh-CN.md) | **日本語** · [← 一覧に戻る](../README.ja.md)

> 出典レベル: **📣 主張** · 日付: 2026-09-16 · 数値は出典からの引用です。このリポジトリでは再計測していません。

## ハードウェア

- MacBook M5 Pro (Mac)
- 参考価格: 未公開。出典を参照

## モデル

- Ternary Bonsai 2 27B · `PQ2_0`
- ダウンロード: [huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)

## エンジン

- llama.cpp (PrismML fork) — インストール： https://github.com/ggml-org/llama.cpp
- 備考: PrismML llama.cpp fork (Metal)（英語）

## 起動コマンド

```bash
llama-cli ... -ngl 99 -fa on -c 32768 (requires the PrismML llama.cpp fork; stock llama.cpp does not work)
```

出典からの抜粋です（`...` またはプレースホルダーを含みます）。全引数は出典を参照してください。

## 主なパラメータ

- コンテキスト: 262K (model card); example command -c 32768（英語）
- 同時実行: batch 1 (single stream)（英語）
- タグ: `ternary`, `dense`, `long-context`

## 想定速度

- 28.1 tok/s decode; 387 tok/s prefill（英語） (📣 主張)

## 注意点

- 本人による実測ではありません（主張または伝聞）。実際の速度は異なる場合があります。
- 速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。

## 出典とクレジット

- [https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- 権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。
