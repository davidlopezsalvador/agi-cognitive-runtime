# BBH Reasoning Test: 35 Heuristics (Quijote + Lazarillo)

**Date**: 2026-09-04  
**Model**: muse-spark-1.3-contributor-free  
**Heuristics**: 25 Don Quijote + 10 Lazarillo = 35 total  
**Result**: TIE 5/5 vs 5/5

## Problem-by-Problem

| Q | Problem | Without | With 35 | Correct |
|---|---------|---------|---------|---------|
| 1 | Logical Deduction (5 birds) | (A) ✓ | A ✓ | (A) |
| 2 | Multi-step Arithmetic | 24 ✓ | 24 ✓ | 24 |
| 3 | Web of Lies | No ✓ | No ✓ | No |
| 4 | Tracking Shuffled Objects | (A) ✓ | A ✓ | (A) |
| 5 | Boolean Expressions | True ✓ | True ✓ | True |
| | **Score** | **5/5** | **5/5** | |

## Analysis

Problems are too easy for this model. Both conditions solve all 5 correctly.
Heuristics don't hurt performance (unlike raw text which hurts by -13% to -20%).
Need harder reasoning problems to see if heuristics provide advantage.

## Previous Results Comparison

| Test | Model | Without | With | Delta |
|------|-------|---------|------|-------|
| DebugBench 5 easy | ling-3.0-flash | 5/5 | 5/5 | TIE |
| DebugBench 8 heuristics | ling-3.0-flash | 47% | 67% | +20% (string match) |
| DebugBench rescored | ling-3.0-flash | 80% | 87% | +7% (exec-based) |
| BBH 5 questions | ling-3.0-flash | stuck | 5/5 | Heuristics only |
| BBH 5 questions (2) | muse-spark-1.3 | 5/5 | 5/5 | TIE |
