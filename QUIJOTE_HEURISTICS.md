# Don Quijote de la Mancha - Heuristics Extraction

## Overview
Extracted 20 heuristics from the complete text of Don Quijote de la Mancha (527k tokens) for use in debugging tasks.

## Heuristics

### 1. Distinguishing Reality from Illusion
**Principle**: Verify perceptions against objective reality before acting. Mental models can be wrong - test assumptions against actual conditions.
**Triggers**: verification, validation, reality_testing, assumption_checking
**Source**: Windmill episode (Part I, Ch. 8)

### 2. Pragmatic Adaptation
**Principle**: Adapt approach to match actual situation, not idealized version. Pragmatic solutions often succeed where idealism fails.
**Triggers**: pragmatism, adaptation, flexibility, practical_solutions
**Source**: Sancho's consistently practical advice throughout

### 3. Learning from Mistakes
**Principle**: Recognize when approach isn't working. Repeated failures indicate need to change strategy, not just persist harder.
**Triggers**: error_learning, feedback_loops, adaptive_behavior
**Source**: Multiple failed adventures throughout

### 4. Power of Narrative Framing
**Principle**: Internal stories shape perception and actions. Be aware how your mental narrative influences interpretation of events.
**Triggers**: self_narrative, framing, mental_models, cognitive_framing
**Source**: Don Quijote's transformation into knight-errant (Part I, Ch. 1)

### 5. Value of Reliable Partnership
**Principle**: Trusted partners provide reality checks and emotional support. Good teams have complementary perspectives.
**Triggers**: partnership, teamwork, emotional_support, reality_check
**Source**: Sancho-Don Quijote relationship throughout

### 6. Balance Idealism with Realism
**Principle**: Set ambitious goals but plan realistic execution. Pure idealism without pragmatism leads to failure.
**Triggers**: balance, goal_setting, execution_planning, strategic_thinking
**Source**: Central theme of the novel

### 7. Perseverance with Wisdom
**Principle**: Continue pursuing goals despite setbacks, but adjust approach when needed. Persistence without adaptation is just stubbornness.
**Triggers**: resilience, persistence, recovery, determination
**Source**: Multiple recoveries from defeats

### 8. Context Sensitivity
**Principle**: Same action can have different meanings in different contexts. Understand environment before acting.
**Triggers**: context_awareness, environmental_reading, situational_analysis
**Source**: Various misadventures throughout

### 9. Self-Awareness and Limitations
**Principle**: Know your strengths and weaknesses. Lack of self-awareness about limitations leads to failure.
**Triggers**: self_awareness, limitation_recognition, humility
**Source**: Don Quijote's overconfidence throughout

### 10. Importance of Rest and Recovery
**Principle**: Excessive work without rest damages judgment. Balance intellectual work with physical and mental recovery.
**Triggers**: rest, recovery, work_life_balance, burnout_prevention
**Source**: Part I, Ch. 1 - "del poco dormir y del mucho leer, se le secó el celebro"

### 11. Testing Before Deployment
**Principle**: Test your solutions before relying on them. Untested solutions may fail when needed most.
**Triggers**: testing, validation, quality_assurance, verification
**Source**: Part I, Ch. 1 - celada de encaje

### 12. Resource Management
**Principle**: Don't sacrifice long-term stability for short-term gains. Impoverishing yourself for one interest weakens overall position.
**Triggers**: resource_management, sustainability, trade_offs
**Source**: Part I, Ch. 1

### 13. Observation Before Action
**Principle**: Study the situation carefully before intervening. Acting without understanding leads to unintended consequences.
**Triggers**: analysis, planning, situational_awareness
**Source**: Multiple hasty attacks throughout

### 14. Power of Naming and Identity
**Principle**: Names shape perception and identity. Choose labels carefully as they influence how you and others perceive things.
**Triggers**: naming, identity, framing, perception
**Source**: Part I, Ch. 1 - naming of horse and self

### 15. Questioning Conventions
**Principle**: Challenge established norms when they don't serve you. Innovation requires questioning the status quo.
**Triggers**: questioning, innovation, convention_challenging
**Source**: Don Quijote's self-appointment as knight

### 16. Value of Experience Over Theory
**Principle**: Practical experience teaches what theory cannot. Real-world knowledge complements book learning.
**Triggers**: experience, practical_knowledge, learning_by_doing
**Source**: Sancho's advice throughout

### 17. Managing Expectations
**Principle**: Unrealistic expectations lead to disappointment. Align expectations with actual capabilities and conditions.
**Triggers**: expectations, reality_check, disappointment_prevention
**Source**: Throughout the novel

### 18. Danger of Obsession
**Principle**: Single-minded pursuit of one goal can blind you to other important things. Balance is key to sustainable success.
**Triggers**: obsession, balance, priority_management
**Source**: Don Quijote's transformation and its consequences

### 19. Learning from Others' Mistakes
**Principle**: You don't have to make every mistake yourself. Learn from the failures and successes of those who came before.
**Triggers**: learning, mentorship, knowledge_transfer
**Source**: Don Quijote's misguided application of book knowledge

### 20. Importance of Truth and Honesty
**Principle**: Deception and self-deception ultimately harm both deceiver and deceived. Truth, however painful, is preferable to comfortable lies.
**Triggers**: honesty, truth, integrity, self_deception
**Source**: Sancho's enchantment of Dulcinea

## Comparison with Lazarillo de Tormes

| Aspect | Lazarillo | Don Quijote |
|--------|-----------|-------------|
| Heuristics count | 8 | 20 |
| Focus | Survival, adaptation | Reality testing, balance |
| Tone | Pragmatic, cunning | Idealistic, philosophical |
| Best for | Error handling, recovery | Verification, planning |

## Files Created
- `quijote_heuristics.py` - 20 distilled heuristics
- `quijote_heuristics_full.json` - Full heuristics data
- `quijote_clean.txt` - Cleaned text (527k tokens)
- `quijote_excerpt.txt` - First 100k chars

## Next Steps
1. Test on DebugBench with both heuristic sets
2. Compare Lazarillo vs Don Quijote heuristics
3. Test on different model families
