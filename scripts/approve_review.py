#!/usr/bin/env python3
"""把 review.json 中 decision=收录 的条目写入 data/recipes.json（幂等），并同步候选状态。
用法: python3 scripts/approve_review.py data/candidates/hf-YYYY-MM-DD.review.json"""
from pathlib import Path
import json, os, sys, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prices as sourced_prices
LEGACY_MODEL = {"hf-prism-ml--Ternary-Bonsai-2-27B-gguf": "Ternary Bonsai 2 27B", "hf-prism-ml--Bonsai-27B-mlx-1bit": "Bonsai 27B 1-bit",
                "hf-cdiamond--Qwen3.8-27B-iMatrix-NVFP4-MTP-GGUF": "Qwen3.8-27B"}
def fam(hw):
    if re.search(r"V100|P40|MI50|A100", hw): return "二手数据中心卡"
    if re.search(r"Mac|Apple|\bM[1-5]\b", hw): return "Mac"
    if re.search(r"iPhone|Samsung|RTX PRO|未写|待确认", hw): return "其他"
    if re.search(r"RTX|GTX|\d{4}", hw): return "NVIDIA 消费级"
    return "其他"
def model_name(cid):
    if cid in LEGACY_MODEL: return LEGACY_MODEL[cid]
    n = cid.split("--", 1)[1]
    return re.sub(r"(?i)[-_](gguf|mlx(-\w+)?|gguf-mtp|\d-?bit|mlx-coreml)$", "", re.sub(r"(?i)-GGUF$", "", n))
def main():
    rp = sys.argv[1]; rev = json.load(open(rp))
    recipes = json.load(open(f"{ROOT}/data/recipes.json")); ids = {r["id"] for r in recipes}
    cand_file = rp.replace(".review.json", ".json"); cand = json.load(open(cand_file))
    st = {v["id"]: v for v in rev["reviews"]}
    added = 0
    for x in rev["reviews"]:
        if x["decision"] != "收录": continue
        slug = re.sub(r"[^a-z0-9]+", "-", x["id"][3:].lower()).strip("-")
        for i, y in enumerate(x["recipes"], 1):
            rid = f"hf-{slug}-{i}"
            if rid in ids: continue
            hw = y["hardware"]; ct, cu = sourced_prices.cost_for_hardware(hw)
            notes = "; ".join(filter(None, ["HF 模型卡（" + ("卡内转载第三方数据" if y.get("level") == "转述" else "作者自报") + "）",
                    x.get("note_all"), y.get("note"), *(x.get("caveats") or []), "原文: " + y["quote"]]))
            metric = f"{y['gen_tok_s']} tok/s 生成" + (f"；{y['prefill_tok_s']} tok/s 读入" if y["prefill_tok_s"] else "")
            recipes.append({"id": rid, "category": "text", "model": model_name(x["id"]), "quant": y["quant"], "engine": y["engine"],
                "hardware": hw, "hardware_family": fam(hw), "hardware_cost_text": ct, "hardware_cost_usd": cu,
                "metric": metric, "tok_s": y["gen_tok_s"], "concurrency": y.get("concurrency") or x.get("concurrency"),
                "context": x.get("context"), "launch_command": x.get("launch_command"),
                "source_url": x["url"], "source_note": notes, "source_level": y.get("level") or x.get("source_level", "宣称"),
                "date": (x.get("card_date") or "")[:10] or None,
                "metric_en": f"{y['gen_tok_s']} tok/s decode" + (f"; {y['prefill_tok_s']} tok/s prefill" if y["prefill_tok_s"] else "")})
            added += 1
    for c in cand["candidates"]:
        v = st.get(c["id"])
        if not v: continue
        c["status"] = {"收录": "approved", "拒绝": "rejected", "补充后收录": "pending"}[v["decision"]]
        if v["decision"] == "拒绝": c["reject_reason"] = v["reason"]
        if v["decision"] == "补充后收录": c["missing"] = v.get("missing")
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import normalize_engines, tag_recipes
    tag_recipes.apply(normalize_engines.normalize(recipes))
    Path(f"{ROOT}/data/recipes.json").write_text(json.dumps(recipes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.dump(cand, open(cand_file, "w"), ensure_ascii=False, indent=1)
    close_merged_candidates(rev["reviews"])
    print(f"新增 {added}，总计 {len(recipes)}")
def close_merged_candidates(reviews):
    for v in reviews:
        if v.get("closes"):
            for f in os.listdir(f"{ROOT}/data/candidates"):
                if f.endswith(".json") and not f.endswith(".review.json"):
                    p = f"{ROOT}/data/candidates/{f}"; d = json.load(open(p)); ch = False
                    for c in d["candidates"]:
                        if c["id"] == v["closes"] and c.get("status") != "merged":
                            c["status"] = "merged"; c["merged_into"] = v["id"]; ch = True
                    if ch: json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
if __name__ == "__main__": main()
