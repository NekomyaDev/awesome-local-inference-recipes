# 重点跟踪来源

由 `scripts/gen_watchlist.py` 根据 `data/sources.json`（2026-10-25）生成。A 级 = 参数具体且可复现；B 级 = 有具体数字但条件不全；C 级 = 多为转述或覆盖面窄。

| 等级 | 名称 | 平台 | 关注者 | 关注点 | 理由 | 示例 |
|---|---|---|---|---|---|---|
| A | [MiaAI_lab](https://x.com/MiaAI_lab) | X | 40856 | DGX Spark 1–4 台 / RTX 5090 / RTX PRO 6000；vLLM · SGLang · TensorFold · EXL3 | 每个 recipe 有 GitHub 仓库 + 启动脚本 + sparkDash 按流数基准，社区多人复现（误差 ≤8%） | [示例帖](https://x.com/MiaAI_lab/status/2105598458547646875) |
| A | [mia-ai.net](https://mia-ai.net/models) | Web | — | Mia 的 23 个 recipe 汇总（含 GitHub 星数、单流/多流/预填充/上下文） | 结构化数字，最适合定期抓取 | [示例帖](https://mia-ai.net/models/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold) |
| A | [coldniko](https://x.com/coldniko) | X | 8430 | Strata 引擎作者（GitHub Niko1221/Strata）；消费级 GPU + 内存卸载、V100/MI50 老卡 | 引擎一手发布与参数说明；回复里常给具体并行/卸载设置 | [示例帖](https://x.com/coldniko/status/2109014509063139413) |
| A | [Niko1221/Strata](https://github.com/Niko1221/Strata) | GitHub | — | Strata 引擎 README / docs/OLDER_GPUS.md | 官方基准表 | [示例帖](https://github.com/Niko1221/Strata) |
| A | [0xSero](https://x.com/0xSero) | X | 75043 | DGX Spark 多机 / RTX 3090 + NVMe 卸载 / Intel Arc | 发布带 KLD、top-token 一致率、KV 池大小的完整 recipe，互动最高（2.4k 赞） | [示例帖](https://x.com/0xSero/status/2106373861818224907) |
| A | [ashxhart](https://x.com/ashxhart) | X | 8414 | Mac Studio M3 Ultra、DGX Spark；oMLX PR、TensorFold 贡献者 | 给上下文长度、未缓存 PP 等条件，且向引擎提 PR | [示例帖](https://x.com/ashxhart/status/2099219170546028647) |
| A | [WescheNex1q](https://x.com/WescheNex1q) | X | 3141 | Mac Studio M4 Max vs DGX Spark | 受控对比：同 GGUF sha256、分项 prose/code/json、TTFT | [示例帖](https://x.com/WescheNex1q/status/2103651224650207607) |
| A | [niklaslenz_ai](https://x.com/niklaslenz_ai) | X | 870 | RTX 5090、2×5060 Ti、4×DGX Spark | 独立复现他人 recipe 并公布原始文件，30+ 组合矩阵 | [示例帖](https://x.com/niklaslenz_ai/status/2105623763018453099) |
| A | [Niko1221/Strata PRs（bench/results）](https://github.com/Niko1221/Strata/pulls) | GitHub | — | 社区基准 PR：README + results.json + 引擎日志 | 带原始数据，最适合核验 Strata 行 | [示例帖](https://github.com/Niko1221/Strata/pull/2165) |
| A | [MiaAI-Lab](https://github.com/MiaAI-Lab) | GitHub | — | Mia 的 recipe 仓库（每个配置一个 repo）+ sparkDash | 一手启动脚本和按并发流数的基准表（单流/多流、TTFT），比 X 帖子更完整，可按 owner 订阅 commits/releases | [示例帖](https://github.com/MiaAI-Lab/GLM-5.3-Flash-EXL3-2x-DGX-Sparks-TensorFold) |
| A | [Hao AI Lab blog](https://haoailab.com/blogs/) | Web | — | 视频/音频生成模型在消费级 GPU 上的加速（FastH3 等） | 实验室一手博客，给出硬件、步数和耗时 | [示例帖](https://haoailab.com/blogs/fasth3-rtx/) |
| A | [Apple Machine Learning Research](https://machinelearning.apple.com/research) | Web | — | MLX 分布式推理、Apple Silicon 官方基准 | 官方技术文章，写明机型与配置 | [示例帖](https://machinelearning.apple.com/research/mlx-distributed-inference) |
| B | [JASONMCNAB](https://x.com/JASONMCNAB) | X | 909 | DGX Spark (GB10) | 逐流数复现 Mia recipe 并列出对照值 | [示例帖](https://x.com/JASONMCNAB/status/2101367210404966460) |
| B | [sudoingX](https://x.com/sudoingX) | X | 39318 | 各显存档 GPU（6GB→256GB 双 Spark） | 按显存档整理的 bench book，覆盖面广；单条细节较少 | [示例帖](https://x.com/sudoingX/status/2095300994259100009) |
| B | [yume_arasaki](https://x.com/yume_arasaki) | X | 2495 | DGX Spark、汇总长帖 | 已是 repo 最大来源（42 条），长帖汇总他人数字，需回溯原帖 | [示例帖](https://x.com/yume_arasaki/status/2106837882870886438) |
| B | [TeksEdge](https://x.com/TeksEdge) | X | 11946 | Strix Halo / DGX Spark；llama.cpp PR 与 fork | 第一时间转述 llama.cpp 新 PR/fork 的速度，多为转述 | [示例帖](https://x.com/TeksEdge/status/2092673436904489362) |
| B | [jundotkim](https://x.com/jundotkim) | X | 3971 | oMLX 作者（Hugging Face） | 引擎 release note，适合追踪版本差异 | [示例帖](https://x.com/jundotkim/status/2103220348263227765) |
| B | [ivanfioravanti](https://x.com/ivanfioravanti) | X | 43734 | Apple MLX | MLX 生态大号，Mac 新机/新模型首测 | [示例帖](https://x.com/ivanfioravanti) |
| B | [CryptoBandit100](https://x.com/CryptoBandit100) | X | 633 | 3×DGX Spark + Mac Studio | 写清 KV 量化、MTP K、temp、引擎版本 | [示例帖](https://x.com/CryptoBandit100/status/2106374669477761493) |
| B | [llm_frontier_jp](https://x.com/llm_frontier_jp) | X | 517 | V100 / Intel Arc B570 自测；Strata 公开实测汇总（日文） | 自测写明引擎版本、输入 32,768/输出 1,024 tokens、2 次取中位数；整理 30 款 ≤16GB GPU 共 82 例 Strata 公开实测并附出处 | [示例帖](https://x.com/llm_frontier_jp/status/2110743174344044897) |
| B | [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) | Reddit | — | 多卡/单卡长上下文对比、引擎 A/B（Strata vs Infernix、vLLM vs llama.cpp） | 帖主常给完整表格（中位数、上下文、量化），可作独立复现来源 | [示例帖](https://www.reddit.com/r/LocalLLaMA/comments/1x217go/qwen_flash_next_137_toks_3497_toks_prefill_w_512k/) |
| B | [r/LocalLLM](https://www.reddit.com/r/LocalLLM/) | Reddit | — | DGX Spark 多引擎 × 投机解码对比 | 有方法说明与更正记录 | [示例帖](https://www.reddit.com/r/LocalLLM/comments/1vxs6en/benchmarks_qwen3827b_on_one_dgx_spark_across/) |
| B | [ggml-org/llama.cpp Discussions](https://github.com/ggml-org/llama.cpp/discussions) | GitHub | — | llama.cpp 硬件实测、fork 与补丁说明 | 含配置、sha256、对照组 | [示例帖](https://github.com/ggml-org/llama.cpp/discussions/30328) |
| B | [NVIDIA Developer Forums · DGX Spark / GB10](https://forums.developer.nvidia.com/c/accelerated-computing/dgx-spark-gb10/) | Web | — | 双/多 Spark recipe、内存技巧 | recipe 作者常在此发布完整设置 | [示例帖](https://forums.developer.nvidia.com/t/deepseek-v4-1-flash-for-2x-dgx-spark-exl3-3bpw-3m-kv-cache-c6-new-2gb-free-ram-unlock-for-all-gb10s/383583) |
| B | [raullenchai/Rapid-MLX](https://github.com/raullenchai/Rapid-MLX) | GitHub | — | Rapid-MLX README / docs/benchmarks（M3 Ultra、M4 Pro、M5 Max） | 写明 TTFT、prefill、decode、内存峰值和测法（3 次中位数、清缓存），但属项目方自测 | [示例帖](https://github.com/raullenchai/Rapid-MLX/blob/main/docs/benchmarks/recent-large-models-m3-ultra.md) |
| B | [MacStories](https://www.macstories.net/) | Web | — | 新 Mac 的本地 AI 评测（M5 Ultra Mac Studio 等） | 长篇评测，多引擎同机对比 | [示例帖](https://www.macstories.net/stories/m5-ultra-mac-studio-review-the-dream-mac-for-local-ai-agents/) |
| B | [demietrich.com](https://demietrich.com/blog/) | Web | — | 同机多引擎对比（Qwen3.8-Flash-Next） | 固定模型和硬件对比多个引擎，条件写得清楚 | [示例帖](https://demietrich.com/blog/q3.8fn_engine_comparison/) |
| B | [llm-speed.com](https://llm-speed.com/data) | Web | — | 签名 CLI 本地 LLM 跑分（chat-short / chat-long / agent-trace / concurrent-decode） | 固定 suite、带 run_url 与版本号的实测数据，CC BY 4.0；适合交叉核对 | [示例帖](https://llm-speed.com/r/r_dwp5fgdapmw) |
| B | [achyudh/llama.cpp Adaptive KV](https://github.com/achyudh/llama.cpp/tree/bd063a49a) | GitHub | — | Adaptive KV Streaming + RDNA4/ROCm；9070 XT 上 262k 上下文 Qwen3.8-27B 基准表 | 作者自测表写明上下文阶梯、MTP on/off、prefill/decode 与 commit | [示例帖](https://github.com/achyudh/llama.cpp/tree/bd063a49a) |
| B | [StillDeadcode/radiance](https://codeberg.org/StillDeadcode/radiance) | Codeberg | — | Radiance 引擎（ROCm / RDNA4 gfx1201）；R9700 上 Qwen3.8-27B 单卡与 TP 配方；仓库在 Codeberg，不在 GitHub | issue 里有同机多版本对比（如 #225：1.8.1→1.12.0 短提示预填 −25%），写明 quant、上下文和 KV 设置 | [示例帖](https://codeberg.org/StillDeadcode/radiance/issues/225) |
| C | [Oluwaphilemon1](https://x.com/Oluwaphilemon1) | X | 9754 | Mac vs Spark 对比 | 多为整理/转述 WescheNex1q 等数据 | [示例帖](https://x.com/Oluwaphilemon1/status/2091693026087182378) |
| C | [aartiles24](https://x.com/aartiles24) | X | 6497 | MacBook M5 Pro | TensorFold vs mlx-serve vs oMLX 同机倍率 | [示例帖](https://x.com/aartiles24/status/2104179801388884125) |
| C | [Urthoo](https://x.com/Urthoo) | X | 924 | 2× DGX Spark | vLLM→TensorFold 前后对照（1/3 流、预填充） | [示例帖](https://x.com/Urthoo/status/2106426248759005362) |
| C | [redp314](https://x.com/redp314) | X | 2102 | MacBook M3 Max | 固定提示/温度的引擎对比板 | [示例帖](https://x.com/redp314/status/2093588456396210479) |
| C | [iam_agg](https://x.com/iam_agg) | X | 2502 | Mac Studio M5 Ultra 256GB | M5 Ultra 多引擎早期数据 | [示例帖](https://x.com/iam_agg/status/2104413091996008624) |
| C | [AlicanKiraz0](https://x.com/AlicanKiraz0) | X | 39325 | 4× DGX Spark（土耳其语） | 多机 NVFP4 + DFlash2 配置 | [示例帖](https://x.com/AlicanKiraz0/status/2093843767866405145) |
| C | [vLLM / MLX / oMLX GitHub Discussions & issues](https://github.com/vllm-project/vllm/discussions) | GitHub | — | 引擎 issue 中的性能回报（另见 ml-explore/mlx-lm、oMLX 仓库 issues） | 矛盾数据和回归常先出现在 issue | [示例帖](https://github.com/vllm-project/vllm/discussions) |
