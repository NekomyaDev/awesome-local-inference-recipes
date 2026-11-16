# Qwen3.8-Flash-Next · ExLlama · 1× DGX Spark

[English](text-022.md) | [简体中文](text-022.zh-CN.md) | **日本語** · [← 一覧に戻る](../README.ja.md)

> 出典レベル: **✅ 実測** · 日付: — · 数値は出典からの引用です。このリポジトリでは再計測していません。

## ハードウェア

- 1× DGX Spark (DGX Spark)
- 参考価格: ≈ $6,950

## モデル

- Qwen3.8-Flash-Next · `Cruz exllamav3 fork · EXL3 3.05bpw · draft depth 5 · 8-bit KV`
- ダウンロード: 未公開。出典を参照

## エンジン

- ExLlama — インストール： https://github.com/turboderp-org/exllamav3

## 起動コマンド

コマンドは公開されていません。出典を参照してください。

## 主なパラメータ

- コンテキスト: 262K (243K needle test 15/15)（英語）
- 同時実行: native engine only 1 stream (separate vLLM concurrent lane also exists)（英語）
- タグ: `3bit`, `MoE`, `long-context`, `speculative`

## 想定速度

- code 102.6; prose 71.7; JSON 66.2 tok/s（英語） (✅ 実測)

## 注意点

- 速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。

## 出典とクレジット

- [https://x.com/yume_arasaki/status/2101741448811229219](https://x.com/yume_arasaki/status/2101741448811229219)
- 権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。
