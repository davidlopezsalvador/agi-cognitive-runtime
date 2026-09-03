# Literary Heuristics Research - Complete Summary

## Objective
Investigate whether literary-derived reasoning patterns can improve LLM agent reasoning on debugging tasks.

## Methodology
- **Benchmark**: DebugBench (LeetCode-style debugging problems)
- **Model**: ling-3.0-flash-fin-free
- **Literary Source**: Lazarillo de Tormes
- **Metric**: Pass@1 (exact match with oracle code)

## Key Findings

### 1. Raw Literary Text Always Hurts Performance

| Condition | No Literary | With Literary | Delta |
|-----------|-------------|---------------|-------|
| 500 tokens (clean) | 67% | 53% | **-13%** |
| 1000 tokens (clean) | 67% | 53% | **-13%** |
| 2000 tokens (clean) | 67% | 53% | **-13%** |
| Full book (27k tokens) | 60% | 40% | **-20%** |

**Conclusion**: Raw literary text, regardless of size or cleanliness, degrades LLM performance.

### 2. Distilled Heuristics Improve Performance

| Condition | No Literary | With Literary | Delta |
|-----------|-------------|---------------|-------|
| 5 bullets | 60% | 67% | **+7%** |
| **8 heuristics with context** | **47%** | **67%** | **+20%** |

**Conclusion**: Distilled heuristics with literary context significantly improve performance.

### 3. The Extraction Process Matters More Than Source Material

```
Raw text (27k tokens)    → -20% (hurts)
Distilled heuristics     → +20% (helps most)
```

## The 8 Heuristics from Lazarillo de Tormes

1. **Iterative Adaptation**: Treat adversarial environments as default. Extract specific lessons from each failure. Accumulate lessons across attempts.

2. **Practical Wisdom**: Real learning comes from hands-on experience, not abstract knowledge. Apply lessons immediately to concrete situations.

3. **Resourcefulness**: When resources are scarce, find creative alternatives. Use what's available, not what's ideal.

4. **Observation**: Study the environment carefully before acting. Learn the rules of the game before playing.

5. **Verification**: Others may mislead you. Verify claims independently. Test assumptions against reality.

6. **Incremental Building**: Build capabilities step by step. Master one skill before moving to the next.

7. **Cunning**: Use intelligence to survive hostile environments. Outsmart opponents rather than confront them directly.

8. **Pattern Recognition**: When something fails repeatedly, identify the pattern. Fix the root cause, not just symptoms.

## Implications for AI Systems

### DO:
- Distill literary knowledge into 5-10 actionable heuristics
- Include context and source attribution
- Keep heuristics balanced in length (~1000 chars)

### DON'T:
- Inject raw literary text
- Use more than 2000 tokens of literary content
- Skip the extraction/distillation process

## Files Created

### Experiment Results
- `DEBUGBENCH_RESULTS.md` - Easy + Medium results
- `DEBUGBENCH_FULL_BOOK_RESULTS.md` - Full book context results
- `DEBUGBENCH_EXCERPT_RESULTS.md` - Excerpt size comparison
- `DEBUGBENCH_HEURISTICS_RESULTS.md` - Heuristic extraction results

### Data Files
- `debugbench_all_results.json` - Easy results
- `debugbench_medium_results.json` - Medium results
- `debugbench_full_book_results.json` - Full book results
- `debugbench_clean500_results.json` - 500 token clean results
- `debugbench_clean1000_results.json` - 1000 token clean results
- `debugbench_clean2000_results.json` - 2000 token clean results
- `debugbench_8heuristics_results.json` - 8 heuristic results

### Source Files
- `lazarillo_clean.txt` - Cleaned text of Lazarillo de Tormes
- `lazarillo_heuristics.py` - 8 distilled heuristics
- `analyze_debugbench.py` - Analysis scripts
- `analyze_medium.py`
- `analyze_full_book.py`
- `analyze_excerpts.py`
- `analyze_clean_results.py`
- `analyze_heuristics.py`

## Next Steps

1. Test with Don Quijote de la Mancha
2. Test with other literary works
3. Test on different model families
4. Optimize heuristic extraction process
5. Create automated heuristic extraction pipeline

## GitHub Commits

- `d405f12` - LITERARY_EXPERIMENT_FINAL.md
- `35d4c3b` - LITERARY_COMPARISON_CLEAN.md
- `c50cb1c` - Runtime fix + .gitignore
- `40c61b8` - DebugBench Easy + Medium
- `ce8bbdc` - Full book context results
- `4185b91` - Clean excerpt results
- `62af2ec` - 8 heuristics results
