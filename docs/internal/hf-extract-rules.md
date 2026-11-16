# Hugging Face model-card speed extraction rules

Rules implemented by `scripts/hf_extract.py`; regression cases live in `tests/test_ingest_hf*.py` and `tests/test_hf_extract_formats.py`. Fixture cards live in `tests/fixtures/hf/`; expected values in the batch tests come from the 2026-10-14 human review.

## v3 规则（2026-10-14）

表格
- 逐行解析：一行 = 硬件 × 量化/配置；按表头区分 生成 / 读入 / 聚合吞吐(并发) / 峰值；延迟列(TTFT/TPOT/ms/latency)忽略
- 表头没有 tok/s 但单元格带单位（"33.1 tokens/s"）的列也算速度列；表头的 decode/prefill/generation 词决定类别
- 对照列（FP16/BF16/4-bit/8-bit 基线、original/reference）跳过；同一表多个生成列（如 投机 关/开、new text/code）拆成多条，variant=列名
- 转置表（首列是 "Token generation / Prompt processing / Generation (mean of 6)" 等指标名）：按列出记录；
  若列名不像配置开关（on/off/with/without/MTP/spec/helper），只取第一列（其余视为对比模型）
- 评测/任务表（Task|Verdict|PASS|ID）与延迟表（arrival rate / TTFT p50 / TPOT）整体跳过
- 单元格支持 "**283 tok/s**[^x]"、"14.9–17.7 tok/s"（取下限，保留区间）、"113 / 140 tok/s"（冷/热，读入取后者）、"~2,670 tok/s @ bs 32"
- 行内上下文（"4k tokens of context"、"16,384" 在 prompt/context 列）写入 row.context_tokens，不污染卡级上下文
硬件
- 行标签 > 表前最近的硬件提及（含 "## Measured" 标题后首行、"Machine:"、"Hardware:"）> 卡级声明句 > 表后声明句
- 机房卡/服务器 CPU（H100/A100/L40S/L4/Xeon/EPYC…）与工作站卡（RTX PRO/RTX 6000 Ada/A6000）默认排除
来源与说明
- 表前文字或列名出现 "their numbers / not ours / community benchmark / X's numbers / by <name>" → 该表行 level=转述
- "up to" 峰值说法 → row.peak_claim=True 并进 caveats；pending re-measurement 等保留说明进 caveats
- 句子抽取：段落合并后，同句有硬件+速度才算；取离硬件最近的速度数字
其他
- OCR/嵌入/语音、<3B、占位链接 → flags 降分；flags 含「非通用 LLM」时 primary=None（交给过滤）
- 行级 dup_key 供跨卡去重（seen_rows 参数；ingest_hf.py 会把历史候选批次的 dup_key 一并载入）

## v4 增补（2026-10-14）
- 对照列：成对列 "A tg | B tg" 中，A 在卡内写作 "vs (uniform) A" → 跳过 A；表头裸 tg/pp 也算速度列
- 多档上下文表有 Mean/Average/Median 行时只取汇总行
- Bits/Weight、bpw 列 → quant 写成 "<行名> (<bpw> bpw)"（如 byteshape 的 GPU-1..5 是量化档 ID）
- Headline/Highlights 表 → peak_claim=True，primary 优先非峰值行；"prose **140**, code 209" 取 prose 值
- 前缀配对：多生成列时 "X prefill" 只配 "X decode"
- 硬件补 RTX A 系列 / A6000（工作站，默认排除）、Radeon AI PRO R9700、Radeon RX
- 噪声：encoder/embedding throughput、tokens per second of video/audio 整行丢弃
- 句子：链接到别的 HF 模型的句子丢弃；列表项各自成句；优先取数字前面最近的硬件
