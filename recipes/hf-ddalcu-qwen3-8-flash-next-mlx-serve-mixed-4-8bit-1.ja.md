# Qwen3.8-Flash-Next-MLX-Serve-mixed-4 · mlx-serve · Mac Studio/MBP M4 Max 128GB

[English](hf-ddalcu-qwen3-8-flash-next-mlx-serve-mixed-4-8bit-1.md) | [简体中文](hf-ddalcu-qwen3-8-flash-next-mlx-serve-mixed-4-8bit-1.zh-CN.md) | **日本語** · [← 一覧に戻る](../README.ja.md)

> 出典レベル: **📣 主張** · 日付: 2026-08-27 · 数値は出典からの引用です。このリポジトリでは再計測していません。

## ハードウェア

- Mac Studio/MBP M4 Max 128GB (Mac)
- 参考価格: 未公開。出典を参照

## モデル

- Qwen3.8-Flash-Next-MLX-Serve-mixed-4 · `mixed 4/8-bit (≈75 GB resident)`
- ダウンロード: [huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit)

## エンジン

- mlx-serve
- 備考: mlx-serve 26.8.11（英語）

## 起動コマンド

```bash
mlx-serve --model ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit --serve
```

## 主なパラメータ

- コンテキスト: 268,288
- 同時実行: serial single request（英語）
- タグ: `4bit`, `8bit`, `MoE`, `long-context`

## 想定速度

- 60.0 tok/s decode; 730.0 tok/s prefill（英語） (📣 主張)

## 注意点

- 本人による実測ではありません（主張または伝聞）。実際の速度は異なる場合があります。
- 速度はドライバー、エンジンのバージョン、コンテキスト長、プロンプト長によって変わります。

## 出典とクレジット

- [https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit](https://huggingface.co/ddalcu/Qwen3.8-Flash-Next-MLX-Serve-mixed-4-8bit)
- 権利は元の投稿者にあります。このページは要約とリンクのみです。データは CC BY 4.0。
