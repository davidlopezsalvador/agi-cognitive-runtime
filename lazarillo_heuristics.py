"""
Distilled Heuristics from Lazarillo de Tormes
Extracted for use in debugging and problem-solving tasks
"""

HEURISTICS = {
    "lazarillo.distilled.v1": {
        "name": "Picaresque Iterative Adaptation",
        "principle": "Treat adversarial environments as default condition, extract specific lessons from each failure, accumulate lessons across attempts",
        "triggers": [
            "debugging",
            "error_handling", 
            "failure_recovery",
            "iterative_improvement"
        ],
        "source": "Lazarillo de Tormes - Tratado Primero",
        "context": "Lázaro learns from each abusive master, adapting his behavior to survive"
    },
    
    "lazarillo.distilled.v2": {
        "name": "Practical Wisdom Over Theory",
        "principle": "Real learning comes from hands-on experience, not abstract knowledge. Apply lessons immediately to concrete situations.",
        "triggers": [
            "problem_solving",
            "skill_acquisition",
            "knowledge_transfer"
        ],
        "source": "Lazarillo de Tormes - Ciego as teacher",
        "context": "The blind man teaches survival skills through practice, not theory"
    },
    
    "lazarillo.distilled.v3": {
        "name": "Resourcefulness Under Constraints",
        "principle": "When resources are scarce, find creative alternatives. Use what's available, not what's ideal.",
        "triggers": [
            "resource_management",
            "constraint_satisfaction",
            "creative_solutions"
        ],
        "source": "Lazarillo de Tormes - stealing food, finding workarounds",
        "context": "Lázaro survives by stealing food and finding clever workarounds"
    },
    
    "lazarillo.distilled.v4": {
        "name": "Observation Before Action",
        "principle": "Study the environment carefully before acting. Learn the rules of the game before playing.",
        "triggers": [
            "exploration",
            "analysis",
            "planning"
        ],
        "source": "Lazarillo de Tormes - learning each master's habits",
        "context": "Lázaro observes each master's patterns to exploit them"
    },
    
    "lazarillo.distilled.v5": {
        "name": "Strategic Deception Detection",
        "principle": "Others may mislead you. Verify claims independently. Test assumptions against reality.",
        "triggers": [
            "verification",
            "validation",
            "skepticism"
        ],
        "source": "Lazarillo de Tormes - the bull incident, the grapes",
        "context": "Lázaro learns to verify claims rather than trust appearances"
    },
    
    "lazarillo.distilled.v6": {
        "name": "Incremental Skill Building",
        "principle": "Build capabilities step by step. Master one skill before moving to the next.",
        "triggers": [
            "skill_development",
            "progressive_complexity",
            "mastery"
        ],
        "source": "Lazarillo de Tormes - progression through masters",
        "context": "Lázaro advances from simple tasks to complex social navigation"
    },
    
    "lazarillo.distilled.v7": {
        "name": "Self-Preservation Through Cunning",
        "principle": "Use intelligence to survive hostile environments. Outsmart opponents rather than confront them directly.",
        "triggers": [
            "survival",
            "conflict_resolution",
            "strategic_thinking"
        ],
        "source": "Lazarillo de Tormes - outwitting the blind man",
        "context": "Lázaro survives by being cleverer than his adversaries"
    },
    
    "lazarillo.distilled.v8": {
        "name": "Learning from Failure Patterns",
        "principle": "When something fails repeatedly, identify the pattern. Fix the root cause, not just symptoms.",
        "triggers": [
            "pattern_recognition",
            "root_cause_analysis",
            "systematic_debugging"
        ],
        "source": "Lazarillo de Tormes - repeated abuse patterns",
        "context": "Lázaro recognizes patterns of abuse and adapts accordingly"
    }
}

# Export for use in experiments
if __name__ == "__main__":
    for key, heuristic in HEURISTICS.items():
        print(f"\n{heuristic['name']}:")
        print(f"  Principle: {heuristic['principle']}")
        print(f"  Source: {heuristic['source']}")
        print(f"  Context: {heuristic['context']}")
