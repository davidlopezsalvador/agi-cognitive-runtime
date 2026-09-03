# DebugBench: Excerpt Size Experiment

## Critical Finding

**Cleaned literary text consistently DECREASES performance, regardless of excerpt size. Only distilled heuristics (5 bullets) improve performance.**

## Results

| Condition | No Literary | With Literary | Delta | Tokens (lit) |
|-----------|-------------|---------------|-------|--------------|
| 5 bullets | 60% | 67% | **+7%** | ~400k |
| 500 tokens | 67% | 53% | -13% | 420k |
| 1000 tokens | 67% | 53% | -13% | 830k |
| 2000 tokens | 67% | 53% | -13% | 1,407k |
| Full book (27k) | 60% | 40% | -20% | 1,618k |

## Interpretation

1. **Raw literary text hurts performance**: Even cleaned, the text consistently decreases accuracy by 13-20%
2. **Size doesn't matter**: 500, 1000, and 2000 tokens all show identical -13% degradation
3. **Distilled heuristics work**: Only the 5 bullet point summary improves performance (+7%)
4. **The "less is more" principle**: Compressed actionable heuristics > raw literary prose

## Why This Happens

1. **Context pollution**: Literary text competes with debugging task for attention
2. **Signal vs noise**: The useful patterns are buried in narrative prose
3. **Attention dilution**: LLMs can't extract actionable heuristics from raw text effectively
4. **Token waste**: Literary tokens don't contribute to debugging reasoning

## Implications

For using literary knowledge in AI systems:
- **DO**: Distill into 5-10 actionable heuristics
- **DON'T**: Inject raw literary text
- **The extraction process matters more than the source material**

## Files
- `debugbench_clean_500_lit.json`
- `debugbench_clean_1000_lit.json`
- `debugbench_clean_2000_lit.json`
- `debugbench_clean500_results.json`
- `debugbench_clean1000_results.json`
- `debugbench_clean2000_results.json`
- `lazarillo_clean.txt`
- `analyze_clean_results.py`
