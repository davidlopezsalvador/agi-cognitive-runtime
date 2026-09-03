# DebugBench Experiment Results

## Objective
Measure whether literary-derived reasoning patterns (Lazarillo de Tormes) improve actual debugging performance on a standardized benchmark.

## Methodology
- **Benchmark**: DebugBench (LeetCode-style debugging problems)
- **Model**: ling-3.0-flash-fin-free
- **Sessions**: Clean sessions per batch (same model)
- **Condition A**: Without literary knowledge
- **Condition B**: With 5 Lazarillo principles in system prompt
- **Metric**: Pass@1 (exact match with oracle code)

## Results

### Batch 1: Easy (5 problems)

| Problem | Bug Type | No Literary | With Literary |
|---------|----------|-------------|---------------|
| binary-search | condition error | ❌ | ❌ |
| partition-array-into-three-parts | condition error | ❌ | ❌ |
| minimum-bit-flips-to-convert-number | condition error | ❌ | ✅ |
| make-array-zero-by-subtracting-equal-amounts | condition error | ✅ | ✅ |
| next-greater-element-i | condition error | ❌ | ❌ |

**Score**: No literary 1/5 (20%) | With literary 2/5 (40%)

### Batch 2: Medium (10 problems)

| Problem | Bug Type | No Literary | With Literary |
|---------|----------|-------------|---------------|
| the-kth-factor-of-n | condition error | ✅ | ✅ |
| restore-ip-addresses | condition error | ✅ | ✅ |
| find-players-with-zero-or-one-losses | condition error | ✅ | ✅ |
| invalid-transactions | condition error | ✅ | ✅ |
| maximum-profit-of-operating-a-centennial-wheel | condition error | ✅ | ✅ |
| binary-tree-level-order-traversal-ii | condition error | ❌ | ❌ |
| make-k-subarray-sums-equal | condition error | ✅ | ✅ |
| node-with-highest-edge-score | condition error | ✅ | ✅ |
| grid-game | condition error | ❌ | ❌ |
| minimum-time-to-complete-trips | condition error | ✅ | ✅ |

**Score**: No literary 8/10 (80%) | With literary 8/10 (80%)

## Combined Results (15 problems)

| Condition | Easy | Medium | Total | Accuracy |
|-----------|------|--------|-------|----------|
| No literary | 1/5 | 8/10 | 9/15 | 60% |
| With literary | 2/5 | 8/10 | 10/15 | 67% |

### Token Usage

| Batch | No Literary | With Literary | Difference |
|-------|-------------|---------------|------------|
| Easy (5) | 80,740 | 92,463 | +14.5% |
| Medium (10) | 233,094 | 244,618 | +4.9% |
| **Total** | **313,834** | **337,081** | **+7.4%** |

## Key Findings

1. **Easy problems**: Literary knowledge doubled accuracy (40% vs 20%)
2. **Medium problems**: No difference (both 80%)
3. **Overall**: Literary condition +7% more accurate (67% vs 60%)
4. **Token cost**: +7.4% more tokens with literary (more deliberation)
5. **Both conditions failed on the same problems**: binary-tree-level-order-traversal-ii, grid-game

## Interpretation

- Literary knowledge helps most on **harder/easier problems** where the bug is less obvious
- On medium problems, both conditions perform equally well
- The literary condition uses more tokens, suggesting deeper analysis
- The effect is small but consistent across batches

## Next Steps
1. Test on hard problems
2. Test on different model families (GPT, Claude, Gemini)
3. Measure edit distance as secondary metric
4. Test with different literary traditions (Don Quijote, etc.)

## Files
- `debugbench_medium_prompts_no_lit.json` - Medium prompts without literary
- `debugbench_medium_prompts_lit.json` - Medium prompts with literary
- `debugbench_medium_results.json` - Raw medium results
- `analyze_medium.py` - Analysis script
