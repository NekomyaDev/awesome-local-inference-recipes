# Qwen3.6-35B-A3B-Escha-W2 · SGLang · RTX 5090 32GB

[English](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.md) | [简体中文](hf-eschalabs-qwen3-6-35b-a3b-escha-w2-1.zh-CN.md) | **日本語** · [← 一覧に戻る](../README.ja.md)

> 出典レベル: **📣 主張** · 日付: 2026-07-22 · 数値は出典からの引用です。このリポジトリでは再計測していません。

## ハードウェア

- RTX 5090 32GB (NVIDIA コンシューマー)
- 参考価格: ≈ $5,400

## モデル

- Qwen3.6-35B-A3B-Escha-W2 · `Escha W2 (INT8=on)`
- ダウンロード: [huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)

## エンジン

- SGLang — インストール： https://github.com/sgl-project/sglang
- 備考: SGLang (sglang/serve.sh)（英語）

## 起動コマンド

```bash
MEM=0.78 CTXLEN=32768 bash sglang/serve.sh (on 5090 add INT8=on ATTN_BACKEND=triton MEM=0.82)
```

## 主なパラメータ

- コンテキスト: 32K (16GB card 8K×16)（英語）
- 同時実行: single stream 283; bs32 about 2,670 (peak 3,017.6 @32 streams)（英語）
- タグ: `2bit`, `8bit`, `MoE`

## 想定速度

- 283 tok/s 生成 (📣 主張)

## 注意点

- 本人による実測ではありません（主張または伝聞）。実際の速度は異なる場合があります。
- 速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。

## 出典とクレジット

- [https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2](https://huggingface.co/EschaLabs/Qwen3.6-35B-A3B-Escha-W2)
- 権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。
