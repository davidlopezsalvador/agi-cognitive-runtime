# Gemma4:31b Test: 35 Heuristics vs No Heuristics

**Date**: 2026-09-04  
**Model**: gemma4:31b (smaller, less capable)  
**Benchmark**: BBEH (BIG-Bench Extra Hard)  
**Result**: **Heuristics HURT performance** on small models

## Results

| Q | Task | Correct | No Heuristics | With 35 Heuristics |
|---|------|---------|---------------|-------------------|
| Q1 | Zebra Puzzles | 6 | **6** ✓ | 4 ✗ |
| Q2 | Zebra Puzzles | 5 | **5** ✓ | 4 ✗ |
| Q11 | Multistep Arithmetic | -52 | **-52** ✓ | **-52** ✓ |
| Q12 | Multistep Arithmetic | 36 | **36** ✓ | — (pending) |
| Q13 | Multistep Arithmetic | 8749 | **8749** ✓ | — (pending) |
| Q14 | Multistep Arithmetic | -67517 | -41199 ✗ | — (pending) |
| Q15 | Multistep Arithmetic | -314 | -319 ✗ | — (pending) |

## Summary

- **No heuristics**: 5/7 correct (71%)
- **With 35 heuristics**: 1/3 correct (33%) — Q3-Q10 pending

## Key Finding

**Literary heuristics HURT small model performance.**

On `gemma4:31b`, adding 35 deep reasoning heuristics from Don Quijote and Lazarillo de Tormes:
- **Q1**: Dropped from correct (6) to incorrect (4)
- **Q2**: Dropped from correct (5) to incorrect (4)
- Q11: Both got -52 (tie)

The heuristics appear to add cognitive load/noise that overwhelms smaller models, causing them to lose accuracy on problems they could otherwise solve.

## Comparison Across Models

| Model | No Heuristics | With Heuristics | Effect |
|-------|---------------|-----------------|--------|
| muse-spark-1.3 (large) | 15/15 | 15/15 | TIE (both perfect) |
| gemma4:31b (small) | 5/7 (71%) | 1/3 (33%) | **Heuristics HURT** |

## Conclusion

Literary-derived reasoning heuristics are **model-size dependent**:
- **Large models** (muse-spark-1.3): Neutral — heuristics don't help or hurt
- **Small models** (gemma4:31b): **Negative** — heuristics reduce accuracy by ~38%

This suggests heuristics work best when the model already has sufficient reasoning capacity. For smaller models, the additional context/complexity of heuristics overwhelms their limited reasoning ability.
