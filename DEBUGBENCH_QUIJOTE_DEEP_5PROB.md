# DebugBench Experiment: Don Quijote 10 Deep Heuristics - 5 Easy Problems

**Date**: 2026-09-03  
**Model**: ling-3.0-flash-fin-free  
**Benchmark**: DebugBench (5 easy Python problems)  
**Sessions**: 2 parallel (no-heuristics vs deep-heuristics)

## Result: TIE (5/5 vs 5/5) — Both approaches solve all problems correctly

Both approaches find correct fixes. The difference is in **reasoning depth**.

---

## Problem-by-Problem Comparison

### 1. Binary Search
| | No Heuristics | Deep Heuristics |
|---|---|---|
| **Bug found** | `right = mid`, `if target not in nums` | Same + Dulcinea Delusion for O(n) scan |
| **Fix** | `right = mid - 1` | Same |
| **Reasoning** | Direct fix | "Dulcinea Delusion — `if target not in nums` is an O(n) linear scan masquerading as part of an O(log n) algorithm" |

### 2. Partition Array into Three Parts
| | No Heuristics | Deep Heuristics |
|---|---|---|
| **Bug found** | `if count == 2: return True` too early | Same + Dulcinea Delusion + Celada Paradox trace |
| **Fix** | `return count >= 3` | Same |
| **Reasoning** | "without verifying that a third non-empty partition actually exists" | "Dulcinea Delusion — `if count == 2: return True` is the delusion: it pretends finding two parts implies a valid three-part partition" |

### 3. Minimum Bit Flips to Convert
| | No Heuristics | Deep Heuristics |
|---|---|---|
| **Bug found** | `range(51)` should be `range(50)` | Same + Windmill Epistemology |
| **Fix** | `return bin(start ^ goal).count('1')` | Same |
| **Reasoning** | "the strings are length 50, so index 50 causes an IndexError" | "Windmill Epistemology — Mental model: compare bits of start and goal. The strings are 50 chars (indices 0–49), but `range(51)` accesses index 50 → IndexError" |

### 4. Make Array Zero
| | No Heuristics | Deep Heuristics |
|---|---|---|
| **Bug found** | `if num != 0: continue` inverted | Same + Windmill Epistemology |
| **Fix** | `len(set(num for num in nums if num != 0))` | `if num == 0: continue` (preserves original structure) |
| **Reasoning** | "skips non-zero numbers instead of adding them" | "Windmill Epistemology — Mental model: each operation subtracts the smallest non-zero value, eliminating one distinct value per operation. Bug: `if num != 0: continue` skips non-zero elements — the condition is inverted" |

### 5. Next Greater Element
| | No Heuristics | Deep Heuristics |
|---|---|---|
| **Bug found** | `nums2[j]` access before bounds check | Same + Windmill Epistemology + multi-perspective trace |
| **Fix** | `while j < len(nums2) and nums2[j] <= nums1[i]` | `for j in range(idx + 1, len(nums2))` (cleaner) |
| **Reasoning** | "the while loop accesses nums2[j] before checking if j == len(nums2)" | "Celada Paradox — Trace with nums1=[7], nums2=[1,7,3,5]: For 7: idx=1, j=2, nums2[2]=3 < 7, j=3, nums2[3]=5 < 7, j=4, nums2[4] → IndexError!" |

---

## Key Observations

1. **Same correctness**: Both approaches solve 100% of easy problems
2. **Deeper reasoning with heuristics**: Session 2 traces specific test cases, names the heuristics applied, and provides multi-step justification
3. **Cleaner fixes sometimes**: Deep heuristics approach used `for j in range(...)` instead of `while` for next-greater-element (arguably cleaner)
4. **Educational value**: Heuristic approach teaches debugging methodology, not just the fix
5. **For easy problems**: The bonus is pedagogical, not correctness
6. **Next step**: Test on medium/hard problems where structured reasoning may matter more

---

## Cumulative Results (All Experiments)

| Condition | No Literary | With Literary | Delta | Tokens (lit) |
|-----------|-------------|---------------|-------|--------------|
| 5 bullets (easy+medium) | 60% | 67% | **+7%** | ~400k |
| 500 tokens raw text | 67% | 53% | -13% | 420k |
| 1000 tokens raw text | 67% | 53% | -13% | 830k |
| 2000 tokens raw text | 67% | 53% | -13% | 1,407k |
| Full book (27k) | 60% | 40% | **-20%** | 1,618k |
| **8 heuristics (Lazarillo)** | **47%** | **67%** | **+20%** | 541k |
| **10 deep heuristics (Quijote)** | **5/5** | **5/5** | **TIE** (deeper reasoning) | ~3.8k/prompt |

## GitHub Commits
- `081d1ae` - Don Quijote 10 deep heuristics + initial 2-problem test
- This experiment (pending) - 5-problem full test with verification
