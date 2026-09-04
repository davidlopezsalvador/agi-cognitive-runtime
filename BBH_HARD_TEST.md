# BBH Hard Test: 35 Heuristics vs No Heuristics

**Date**: 2026-09-04  
**Model**: muse-spark-1.3-contributor-free  
**Result**: TIE 5/5 vs 5/5

## Problems

| Q | Problem | Without | With 35 | Correct |
|---|---------|---------|---------|---------|
| 1 | Einstein's riddle (5 houses) | (E) ✓ | E ✓ | (E) German |
| 2 | Hard arithmetic (powers, mod, floor div) | -46 ✓ | -46 ✓ | -46 |
| 3 | 8-person web of lies | C,D,G ✓ | C,D,G ✓ | Charlie/Diana/George |
| 4 | 7 dancers, 8 swaps | A-6 ✓ | A-6 ✓ | A-6 |
| 5 | Complex boolean (and/or/xor) | True ✓ | True ✓ | True |
| | **Score** | **5/5** | **5/5** | |

## Key Finding

Both sessions correctly identified that Q3 and Q4's multiple-choice options DON'T contain the correct answer. This model (muse-spark-1.3) is too capable for these problems - it solves them all correctly regardless of heuristics.

## Conclusion

Heuristics neither help nor hurt on reasoning problems this model can already solve perfectly. To see a difference we need problems that challenge the model's reasoning limits - not problems it can solve trivially.
