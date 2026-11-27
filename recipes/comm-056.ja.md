# DeepSeek-V4.1-Flash-1017 · Strata (Strata-DS fork) · 1× DGX Spark (GB10, 128GB unified memory, 4TB NVMe)

[English](comm-056.md) | [简体中文](comm-056.zh-CN.md) | **日本語** · [← 一覧に戻る](../README.ja.md)

> 出典レベル: **✅ 実測** · 日付: 2026-10-18 · 数値は出典からの引用です。このリポジトリでは再計測していません。

## ハードウェア

- 1× DGX Spark (GB10, 128GB unified memory, 4TB NVMe) (DGX Spark)
- 参考価格: ≈ $6,950

## モデル

- DeepSeek-V4.1-Flash-1017 · `LibertAIDAI EXL3 2.9bpw (experts; dense 5 / head 6) + the official 1017 checkpoint's other tensors and Engram (single machine, DSpark drafting every step, SSD tail skip)`
- ダウンロード: [huggingface.co/LibertAIDAI/DeepSeek-V4.1-Flash-1017-EXL3-2.9bpw](https://huggingface.co/LibertAIDAI/DeepSeek-V4.1-Flash-1017-EXL3-2.9bpw) · [huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)

## エンジン

- Strata (Strata-DS fork) — インストール： https://github.com/Jackwwg83/Strata-DS
- 備考: Strata-DS (Strata fork with its own DeepSeek engine ds41_serve, C++/CUDA; hot experts in a unified-memory RAM tier computed in place by the GPU, cold experts read from the SSD on demand; sudoingX's exl3_smoe and exl3_mrow EXL3 kernels)（英語）

## 起動コマンド

```bash
git clone https://github.com/Jackwwg83/Strata-DS.git && cd Strata-DS && ./setup.sh --setup --yes --family deepseek --no-start && ./run-deepseek-1017-exl3-2.9bpw.sh
```

## 主なパラメータ

- コンテキスト: 256K (262,144)
- 同時実行: Single stream（英語）
- タグ: `2bit`, `MoE`, `long-context`, `speculative`, `offload`

## 想定速度

- Real coding-agent session, 48 turns (context 10K–91K), 70,211 tokens at 30.8 tok/s 平均 (per turn 23.6–36.4, median 28.6); single runs: decode at 8K/32K/64K/128K/250K context 24.2/27.4/27.4/27.3/22.9; time to first token for an agent turn adding ≤50 tokens median 0.57 s, a new conversation with the same 10K system prompt 0.25 s; cold prefill 約 500 tok/s (250K in 8.3 min); vs official MXFP4 KL 0.074 / top-1 88.6% (✅ 実測)

## 注意点

- 速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。

## 出典とクレジット

- [https://github.com/Jackwwg83/Strata-DS/blob/main/docs/DEEPSEEK_SPARK.md](https://github.com/Jackwwg83/Strata-DS/blob/main/docs/DEEPSEEK_SPARK.md)
- 権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。
