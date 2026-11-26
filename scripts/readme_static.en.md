{{HERO}}

## Contents

{{TOC}}

## Legend

| Source level | Meaning | Format |
|---|---|---|
| 🏛️ **Official** | vendor or project number | **Model** · Engine `quant` — Hardware → **key number** level \[source\] |
| ✅ **Measured** | poster ran it, with log or screenshot; an engine or recipe author must also publish raw data and reproduction steps | **tok/s** = single-stream generation (not prefill, not aggregate) |
| 🔁 **Relayed** | second-hand, verify upstream | Tiers use the lowest published hardware price (USD) |
| 📣 **Claimed** | projection, no reproduction | Unknown values are never estimated |

{{SCOPE}}
<!--RECIPES-->

## Engines & Tools

<!--ENGINES-->

## Related Lists & Benchmarks

<!--RELATED-->

## Contributing

One recipe = one PR. Copy the YAML template from [submit.html](submit.html), fill only what the source shows (`null` otherwise), run `node scripts/validate.mjs`, and link the post. Then run `python3 scripts/gen_all.py` to regenerate the READMEs and site pages. Add new models and new hardware in the first few weeks after launch, and non-mainstream combinations, first. Merge a new result into an existing entry only for the same tester, machine, model and engine. A routine repeat by a different tester stays a separate entry. See [CONTRIBUTING.md](CONTRIBUTING.md).

Dev: `python3 -m http.server 5190` → `index.html` (landing) · `explore.html` (filter/sort/scatter) · schema in [`schema/recipe.schema.json`](schema/recipe.schema.json).

For AI agents: the skill [`.agents/skills/local-inference-recipe-finder`](.agents/skills/local-inference-recipe-finder/SKILL.md) detects your hardware and recommends recipes from [`data/hw_index.json`](docs/hw_index.md). See [AGENTS.md](AGENTS.md).

<details><summary>Site preview</summary>

<img src="docs/screenshot.png" width="760" alt="Site home page: recipe, engine and measured counts, and the fastest measured setup in each budget tier">

</details>

## License

- Code: [MIT](LICENSE)
- Data (`data/`): [CC BY 4.0](LICENSE-DATA). Reuse it freely with attribution to Awesome Local Inference Recipes and the original sources linked in each recipe.
