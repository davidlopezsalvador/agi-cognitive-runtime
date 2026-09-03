# DebugBench: Heuristic Extraction Results

## Key Finding

**8 distilled heuristics with literary context achieved +20% improvement, the best result so far.**

## Results Comparison

| Condition | No Literary | With Literary | Delta |
|-----------|-------------|---------------|-------|
| 5 bullets | 60% | 67% | +7% |
| **8 heuristics** | **47%** | **67%** | **+20%** |
| 500 tokens (clean) | 67% | 53% | -13% |
| 1000 tokens (clean) | 67% | 53% | -13% |
| 2000 tokens (clean) | 67% | 53% | -13% |
| Full book (27k) | 60% | 40% | -20% |

## Why 8 Heuristics Work Better

1. **More detailed than 5 bullets**: Each heuristic includes:
   - Clear principle
   - Specific triggers
   - Literary source
   - Context from the work

2. **Actionable guidance**: Not just "extract lessons" but "identify patterns, fix root cause"

3. **Source attribution**: Knowing the heuristic comes from Lazarillo adds credibility

4. **Balanced length**: ~1000 chars vs 279 chars (5 bullets) vs 27k chars (full book)

## The Heuristics

1. **Iterative Adaptation**: Treat adversarial environments as default
2. **Practical Wisdom**: Hands-on experience over theory
3. **Resourcefulness**: Creative solutions under constraints
4. **Observation**: Study before acting
5. **Verification**: Test assumptions independently
6. **Incremental Building**: Step-by-step skill development
7. **Cunning**: Outsmart rather than confront
8. **Pattern Recognition**: Fix root causes, not symptoms

## Implications

The extraction process matters more than the source material:
- **Raw text**: -13% to -20% (hurts)
- **Simple bullets**: +7% (helps)
- **Detailed heuristics with context**: +20% (helps most)

## Files
- `lazarillo_heuristics.py`
- `debugbench_heuristics_8_heuristics.json`
- `debugbench_8heuristics_results.json`
- `analyze_heuristics.py`
