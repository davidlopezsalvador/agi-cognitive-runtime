# DebugBench Hard Problem: Maximum Elegance of a K-Length Subsequence

**Date**: 2026-09-04  
**Model**: ling-3.0-flash-fin-free  
**Problem**: maximum-elegance-of-a-k-length-subsequence (hard, recent contest)  
**Bug type**: operation error (binary search off-by-one + wrong approach)

## The Buggy Code

The code tries binary search on distinct category count, but elegance is NOT unimodal — binary search fails.

```python
while l<=r:  # <-- should be l<r (off-by-one)
    if elegance(mid+1)>elegance(mid) or elegance(mid+1)==-1:
        l=mid+1
    else:
        r=mid  # <-- no decrement, infinite loop risk
```

## Result: Both find correct greedy approach, but Session 2 explains WHY

| | No Heuristics | With Heuristics |
|---|---|---|
| **Found approach** | Greedy swap | Greedy swap |
| **Explains why binary search fails** | No ("fundamentally wrong") | Yes ("elegance is NOT unimodal") |
| **Concrete test case** | No | Yes (`items=[[5,1],[4,1],[3,2],[2,2],[1,3]], k=3`) |
| **Code quality** | Same | Same |

## Key Insight

Session 1 immediately declares "the approach is fundamentally wrong" and jumps to a complete rewrite. Session 2 uses **Windmill Epistemology** to verify the mental model first:

> "the code tries binary search on distinct category count, but elegance is NOT unimodal in distinct count — binary search fails"

Then uses **Celada Paradox** to trace with a concrete test:

> "Test with `items=[[5,1],[4,1],[3,2],[2,2],[1,3]], k=3`: buggy code's binary search bounds are wrong (`r=min(len(cats)-1,k-1)`), convergence has infinite loop risk (`r=mid` no decrement), and elegance isn't unimodal. Greedy swap gives correct 18."

## Updated Cumulative Results

| Problem | Difficulty | No Heuristics | Heuristics | Winner |
|---------|-----------|---------------|------------|--------|
| 5 easy problems | easy | 5/5 | 5/5 | TIE |
| minimize-the-total-price | hard | wrong DP rewrite | correct fix | Heuristics |
| maximum-elegance | hard | correct code | correct code + explanation | Heuristics (educational) |

## GitHub
- Commit: pending
