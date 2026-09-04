# BBEH Test: 35 Heuristics vs No Heuristics

**Date**: 2026-09-04  
**Model**: muse-spark-1.3-contributor-free  
**Benchmark**: BIG-Bench Extra Hard (BBEH) - 15 problems  
**Result**: TIE 15/15 vs 15/15

## Problems (3 tasks × 5)

| Q | Task | Without | With 35 | Correct |
|---|------|---------|---------|---------|
| 1 | Zebra Puzzles (7 people) | 6 ✓ | 6 ✓ | 6 |
| 2 | Zebra Puzzles (7 people) | 5 ✓ | 5 ✓ | 5 |
| 3 | Zebra Puzzles (5 people) | 4 ✓ | 4 ✓ | 4 |
| 4 | Zebra Puzzles (7 people) | 1 ✓ | 1 ✓ | 1 |
| 5 | Zebra Puzzles (7 people) | 1 ✓ | 1 ✓ | 1 |
| 6 | Shuffled Objects (7 people) | F ✓ | F ✓ | F |
| 7 | Shuffled Objects (7 people) | B ✓ | B ✓ | B |
| 8 | Shuffled Objects (7 people) | B ✓ | B ✓ | B |
| 9 | Shuffled Objects (7 people) | E ✓ | E ✓ | E |
| 10 | Shuffled Objects (7 people) | A ✓ | A ✓ | A |
| 11 | Multistep Arithmetic | -52 ✓ | -52 ✓ | -52 |
| 12 | Multistep Arithmetic | 36 ✓ | 36 ✓ | 36 |
| 13 | Multistep Arithmetic | 8749 ✓ | 8749 ✓ | 8749 |
| 14 | Multistep Arithmetic | -67517 ✓ | -67517 ✓ | -67517 |
| 15 | Multistep Arithmetic | -314 ✓ | -314 ✓ | -314 |
| | **Score** | **15/15** | **15/15** | |

## Key Observations

1. **Model too capable**: muse-spark-1.3 solves all BBEH problems correctly regardless of heuristics
2. **Heuristics produced more methodical reasoning**: Session 2 used 43 messages (vs 18) — solved each problem step-by-step with code
3. **No accuracy difference, but process difference**: Heuristics made the model more thorough, not more accurate
4. **To see accuracy difference**: Need problems that challenge this specific model's limits
