# DebugBench Experiment: Full Book Results

## Critical Finding

**Injecting the full literary text (32k tokens) DECREASED performance by 20% and increased token usage by 354%.**

## Results Comparison

| Condition | Easy | Medium | Total | Tokens |
|-----------|------|--------|-------|--------|
| No literary | 2/5 (40%) | 7/10 (70%) | 9/15 (60%) | 356k |
| With literary | 2/5 (40%) | 4/10 (40%) | 6/15 (40%) | 1.6M |

### Delta
- Accuracy: **-20%** (60% → 40%)
- Tokens: **+354%** (356k → 1.6M)

## Interpretation

1. **Context pollution**: The 32k token literary text overwhelms the LLM's attention mechanism
2. **Distraction effect**: Literary content competes with debugging task for context window
3. **Diminishing returns**: More context ≠ better performance
4. **Optimal injection**: 5 bullet points (previous experiment) performed better than full book

## Comparison of All Experiments

| Experiment | No Literary | With Literary | Delta | Tokens |
|------------|-------------|---------------|-------|--------|
| 5 bullets (Easy) | 20% | 40% | +20% | +14% |
| 5 bullets (Medium) | 80% | 80% | 0% | +5% |
| Full book (15) | 60% | 40% | -20% | +354% |

## Conclusion

**Less is more**: A distilled summary (5 bullet points) improves performance, while the full text overwhelms the model. The literary knowledge helps when compressed into actionable heuristics, but hurts when injected as raw prose.

## Files
- `debugbench_full_book_prompts_no_lit.json`
- `debugbench_full_book_prompts_lit.json`
- `debugbench_full_book_results.json`
- `analyze_full_book.py`
- `lazarillo_tormes_full.txt`
