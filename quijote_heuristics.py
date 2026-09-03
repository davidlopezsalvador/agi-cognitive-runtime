"""
Distilled Heuristics from Don Quijote de la Mancha
Extracted for use in debugging and problem-solving tasks
"""

HEURISTICS = {
    "quijote.distilled.v1": {
        "name": "Distinguishing Reality from Illusion",
        "principle": "Verify perceptions against objective reality before acting. Mental models can be wrong - test assumptions against actual conditions.",
        "triggers": ["verification", "validation", "reality_testing", "assumption_checking"],
        "text_evidence": "Don Quijote sees windmills as giants; Sancho sees them as they are",
        "source": "Windmill episode (Part I, Ch. 8)"
    },
    
    "quijote.distilled.v2": {
        "name": "Pragmatic Adaptation",
        "principle": "Adapt approach to match actual situation, not idealized version. Pragmatic solutions often succeed where idealism fails.",
        "triggers": ["pragmatism", "adaptation", "flexibility", "practical_solutions"],
        "text_evidence": "Sancho's practical wisdom vs Don Quijote's idealism",
        "source": "Sancho's consistently practical advice throughout"
    },
    
    "quijote.distilled.v3": {
        "name": "Learning from Mistakes",
        "principle": "Recognize when approach isn't working. Repeated failures indicate need to change strategy, not just persist harder.",
        "triggers": ["error_learning", "feedback_loops", "adaptive_behavior"],
        "text_evidence": "Don Quijote's repeated failures with windmills, sheep, funerals",
        "source": "Multiple failed adventures throughout"
    },
    
    "quijote.distilled.v4": {
        "name": "Power of Narrative Framing",
        "principle": "Internal stories shape perception and actions. Be aware how your mental narrative influences interpretation of events.",
        "triggers": ["self_narrative", "framing", "mental_models", "cognitive_framing"],
        "text_evidence": "Don Quijote's knight-errant delusion transforms his world",
        "source": "Don Quijote's transformation into knight-errant (Part I, Ch. 1)"
    },
    
    "quijote.distilled.v5": {
        "name": "Value of Reliable Partnership",
        "principle": "Trusted partners provide reality checks and emotional support. Good teams have complementary perspectives.",
        "triggers": ["partnership", "teamwork", "emotional_support", "reality_check"],
        "text_evidence": "Sancho's unwavering loyalty despite Don Quijote's madness",
        "source": "Sancho-Don Quijote relationship throughout"
    },
    
    "quijote.distilled.v6": {
        "name": "Balance Idealism with Realism",
        "principle": "Set ambitious goals but plan realistic execution. Pure idealism without pragmatism leads to failure.",
        "triggers": ["balance", "goal_setting", "execution_planning", "strategic_thinking"],
        "text_evidence": "The central tension between Don Quijote's ideals and reality",
        "source": "Central theme of the novel"
    },
    
    "quijote.distilled.v7": {
        "name": "Perseverance with Wisdom",
        "principle": "Continue pursuing goals despite setbacks, but adjust approach when needed. Persistence without adaptation is just stubbornness.",
        "triggers": ["resilience", "persistence", "recovery", "determination"],
        "text_evidence": "Don Quijote gets beaten but always gets back up",
        "source": "Multiple recoveries from defeats"
    },
    
    "quijote.distilled.v8": {
        "name": "Context Sensitivity",
        "principle": "Same action can have different meanings in different contexts. Understand environment before acting.",
        "triggers": ["context_awareness", "environmental_reading", "situational_analysis"],
        "text_evidence": "Don Quijote's actions appropriate for imagined context, inappropriate for actual",
        "source": "Various misadventures throughout"
    },
    
    "quijote.distilled.v9": {
        "name": "Self-Awareness and Limitations",
        "principle": "Know your strengths and weaknesses. Lack of self-awareness about limitations leads to failure.",
        "triggers": ["self_awareness", "limitation_recognition", "humility"],
        "text_evidence": "Don Quijote never questions his own judgment or abilities",
        "source": "Don Quijote's overconfidence throughout"
    },
    
    "quijote.distilled.v10": {
        "name": "Importance of Rest and Recovery",
        "principle": "Excessive work without rest damages judgment. Balance intellectual work with physical and mental recovery.",
        "triggers": ["rest", "recovery", "work_life_balance", "burnout_prevention"],
        "text_evidence": "Don Quijote lost his mind from too much reading and too little sleep",
        "source": "Part I, Ch. 1 - 'del poco dormir y del mucho leer, se le secó el celebro'"
    },
    
    "quijote.distilled.v11": {
        "name": "Testing Before Deployment",
        "principle": "Test your solutions before relying on them. Untested solutions may fail when needed most.",
        "triggers": ["testing", "validation", "quality_assurance", "verification"],
        "text_evidence": "Don Quijote's cardboard helmet broke when he tested it with his sword",
        "source": "Part I, Ch. 1 - celada de encaje"
    },
    
    "quijote.distilled.v12": {
        "name": "Resource Management",
        "principle": "Don't sacrifice long-term stability for short-term gains. Impoverishing yourself for one interest weakens overall position.",
        "triggers": ["resource_management", "sustainability", "trade_offs"],
        "text_evidence": "Don Quijote sold 'muchas hanegas de tierra' to buy books",
        "source": "Part I, Ch. 1"
    },
    
    "quijote.distilled.v13": {
        "name": "Observation Before Action",
        "principle": "Study the situation carefully before intervening. Acting without understanding leads to unintended consequences.",
        "triggers": ["analysis", "planning", "situational_awareness"],
        "text_evidence": "Don Quijote attacks without understanding what he's attacking",
        "source": "Multiple hasty attacks throughout"
    },
    
    "quijote.distilled.v14": {
        "name": "Power of Naming and Identity",
        "principle": "Names shape perception and identity. Choose labels carefully as they influence how you and others perceive things.",
        "triggers": ["naming", "identity", "framing", "perception"],
        "text_evidence": "Don Quijote carefully chooses names for himself and Rocinante",
        "source": "Part I, Ch. 1 - naming of horse and self"
    },
    
    "quijote.distilled.v15": {
        "name": "Questioning Conventions",
        "principle": "Challenge established norms when they don't serve you. Innovation requires questioning the status quo.",
        "triggers": ["questioning", "innovation", "convention_challenging"],
        "text_evidence": "Don Quijote creates his own version of knighthood",
        "source": "Don Quijote's self-appointment as knight"
    },
    
    "quijote.distilled.v16": {
        "name": "Value of Experience Over Theory",
        "principle": "Practical experience teaches what theory cannot. Real-world knowledge complements book learning.",
        "triggers": ["experience", "practical_knowledge", "learning_by_doing"],
        "text_evidence": "Sancho's practical wisdom from real-life experience",
        "source": "Sancho's advice throughout"
    },
    
    "quijote.distilled.v17": {
        "name": "Managing Expectations",
        "principle": "Unrealistic expectations lead to disappointment. Align expectations with actual capabilities and conditions.",
        "triggers": ["expectations", "reality_check", "disappointment_prevention"],
        "text_evidence": "Don Quijote constantly disappointed by reality not matching his fantasies",
        "source": "Throughout the novel"
    },
    
    "quijote.distilled.v18": {
        "name": "Danger of Obsession",
        "principle": "Single-minded pursuit of one goal can blind you to other important things. Balance is key to sustainable success.",
        "triggers": ["obsession", "balance", "priority_management"],
        "text_evidence": "Don Quijote's obsession with chivalry ruins his life",
        "source": "Don Quijote's transformation and its consequences"
    },
    
    "quijote.distilled.v19": {
        "name": "Learning from Others' Mistakes",
        "principle": "You don't have to make every mistake yourself. Learn from the failures and successes of those who came before.",
        "triggers": ["learning", "mentorship", "knowledge_transfer"],
        "text_evidence": "Don Quijote learned from books but applied them incorrectly",
        "source": "Don Quijote's misguided application of book knowledge"
    },
    
    "quijote.distilled.v20": {
        "name": "Importance of Truth and Honesty",
        "principle": "Deception and self-deception ultimately harm both deceiver and deceived. Truth, however painful, is preferable to comfortable lies.",
        "triggers": ["honesty", "truth", "integrity", "self_deception"],
        "text_evidence": "Sancho's lies about Dulcinea eventually backfire",
        "source": "Sancho's enchantment of Dulcinea"
    }
}

# Export for use in experiments
if __name__ == "__main__":
    for key, heuristic in HEURISTICS.items():
        print(f"\n{heuristic['name']}:")
        print(f"  Principle: {heuristic['principle']}")
        print(f"  Source: {heuristic['source']}")
