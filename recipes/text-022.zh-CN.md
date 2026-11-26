# Qwen3.8-Flash-Next · ExLlama · 1× DGX Spark

[English](text-022.md) | **简体中文** | [日本語](text-022.ja.md) · [← 返回列表](../README.zh-CN.md)

> 来源等级: **✅ 实测** · 日期: — · 数字来自来源。本仓库未复测。

## 硬件

- 1× DGX Spark (DGX Spark)
- 参考价格: $6,950（128GB，2026-10-11）

## 模型

- Qwen3.8-Flash-Next · `Cruz exllamav3 fork · EXL3 3.05bpw · 草稿深度5 · 8-bit KV`
- 下载: 未公开。见来源

## 引擎

- ExLlama — 安装见 https://github.com/turboderp-org/exllamav3

## 启动命令

命令未公开。见来源。

## 关键参数

- 上下文: 262K（243K 针测 15/15）
- 并发: 原生引擎仅 1 路（另有 vLLM 同时处理多个请求的通道）
- 标签: `3bit`, `MoE`, `long-context`, `speculative`

## 预期速度

- 代码 102.6；散文 71.7；JSON 66.2 tok/s (✅ 实测)

## 注意事项

- @yume_arasaki 自测
- 速度随驱动、引擎版本、上下文长度和提示长度变化。

## 来源与致谢

- [https://x.com/yume_arasaki/status/2101741448811229219](https://x.com/yume_arasaki/status/2101741448811229219)
- 版权归原作者。本页仅摘要并链接。数据以 CC BY 4.0 发布。
