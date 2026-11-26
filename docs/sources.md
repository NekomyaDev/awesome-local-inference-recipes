# Data sources

Where recipes come from and how they are checked. Every recipe links to its original source; we store only a link, a short summary and the numbers.

| Source | Role | What it gives | Notes |
|---|---|---|---|
| X (Twitter) | Primary | Measured tok/s, hardware, community heat | Many reposts — we trace back to the original post |
| Hugging Face model cards | Primary | Benchmark tables from quant authors (prefill / decode t/s) | Hardware often missing; reviewed by hand |
| r/LocalLLaMA | Primary (manual) | Consumer-hardware reports | Manual review only |
| GitHub (engine repos, llama.cpp discussions) | Primary | Official bench threads, release notes | |
| llamabench.ai / LocalScore | Cross-check | Benchmarks with commands | Linked, not copied |
| Hacker News | Discovery | New engines and projects | |
| arXiv | Discovery (methods) | Speculative decoding, quantization, KV cache | Datacenter numbers are not added as recipes |

## Source levels
- 🏛️ **Official** (stored as `官方`) — published by the model/engine/hardware vendor or a big lab, or by an engine author or KOL who has original work (for example their own engine, fork or recipe), a real following and public credibility (for example many followers, a starred project, a long GitHub history or maintainer status). The Strata author is one such engine author: figures that the Strata author publishes in Strata releases or notes are Official. Figures that Strata users report follow the rules below. A figure is Official only when its test data is complete (see Claimed).
- ✅ **Measured** (stored as `实测`) — the poster ran it themselves and shows a screenshot or log of the run. Some authors test their own engine or recipe and do not meet the Official conditions above. Such a result is Measured only when the author publishes the raw benchmark data and the reproduction steps.
- 🔁 **Relayed** (stored as `转述`) — second-hand report of someone else's result.
- 📣 **Claimed** (stored as `宣称`) — marketing, a prediction, or an unverified claim with no screenshot/log or no way to reproduce it (e.g. an unpublished private build). An author-run result that is not Official and is missing the raw benchmark data or the reproduction steps is Claimed. A result from a single public run is Measured only when the author is credible, for example an account with a real following, a long GitHub history or starred projects, maintainer status, or replies that confirm the run. If the author is not credible, it is Claimed. Incomplete test data or an author who is not credible gives Claimed. The test data is incomplete when the source does not give, for example, the quant, the engine version, the test method or the number of simultaneous requests, or does not say whether the model fits fully in VRAM. Such a figure is Claimed even when its author counts as Official. Add such a recipe as Claimed. Do not leave it out, as long as it meets the scope rules and the original-source rule. The Official and Claimed rules for authors and incomplete test data apply to recipes added or changed from 2026-11-26. An llm-speed result (a signed run, a model page, an @llmspeed post or a blog median) is Claimed, because it has no raw data for each run. It is Measured only when a different original source publishes raw files for each run and the reproduction steps for the main value.

## Original sources only
Use only an original source for a new recipe. The original source comes from the person or team that ran the test, and it gives the measured numbers. A relayed report (a repost, summary or article that quotes the result of a different person) is not a valid source. Find the original source of the relayed report and link that source. If you cannot find an original source with measured numbers, do not add the recipe.

The Relayed level is kept only for recipes added before this rule.

## Inclusion focus
From 2026-10-27, add these recipes first. First: a recipe for a new model or new hardware, in the first few weeks after launch. Second: a recipe for a non-mainstream combination. Examples are multi-GPU, multi-machine, AMD and Apple mixed, and budget builds. Merge a new result into an existing entry only when the tester, the machine, the model and the engine are all the same. The merged entry keeps the newest reliable value as its main value, with that date and source link, and lists older values and sources briefly in the notes. A routine repeat by a different tester (a new result for a model × engine × hardware combination that is already in the list) stays a separate entry. Do not merge it into another tester's entry. The inclusion focus above decides whether to add it. The scope rules and the original-source rule apply to every recipe.

## Hugging Face ingestion (maintainers)
`python3 scripts/ingest_hf.py --limit 40` (optional `HF_TOKEN`) scans trending GGUF/MLX cards and writes candidates to `data/candidates/` (git-ignored). It never writes `data/recipes.json`. Candidates are reviewed with `python3 scripts/review_candidates.py list | show <id> | approve <id> | reject <id>`; only approved items enter the dataset. Batch approval: `python3 scripts/approve_review.py <review.json>`.

## Rules
No estimates, no invented values — unknown fields are `null`. No full-text copies of posts.

Field rules (CONTRIBUTING rule 10): `tok_s` is single-stream only; a total over several requests goes in the notes. Unstated concurrency is written `未写` (`not stated`). `context` is the configured limit or `null`. Versions are never inferred. Offload rows state the RAM size. Chinese text uses 解码 / 预填充 / 智能体, avoids 并发, and never puts 。 directly after a URL.

## Gone or moved sources
When a source moves (a renamed repo, a new blog path, a Codeberg issue that became a pull request), point `source_url` at the new address after checking that the numbers are still there. When a source is gone (deleted post, suspended or protected account) and no archive copy exists, say so in `source_note`, with the date of the check. The @llamaperf X account was suspended in 2026-11; its links no longer open.
