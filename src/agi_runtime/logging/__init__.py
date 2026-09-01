import logging
import json
import os
from datetime import datetime
from typing import Any

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

class CognitiveLogger:
    def __init__(self, task_id: str = None):
        self.task_id = task_id or datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(LOG_DIR, f'cognitive_{self.task_id}.log')
        self.json_file = os.path.join(LOG_DIR, f'cognitive_{self.task_id}.json')
        self.steps = []
        self.metrics = {
            'hypotheses_generated': 0,
            'hypotheses_verified': 0,
            'memory_queries': 0,
            'knowledge_applied': 0,
            'tool_calls': 0,
            'verification_checks': 0,
            'lessons_learned': 0,
            'duration_ms': 0,
        }
        
        self.logger = logging.getLogger(f'agi_runtime.{self.task_id}')
        self.logger.setLevel(logging.DEBUG)
        
        handler = logging.FileHandler(self.log_file, encoding='utf-8')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        ))
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console)
    
    def log_step(self, step_type: str, description: str, data: Any = None):
        step = {
            'timestamp': datetime.now().isoformat(),
            'step': len(self.steps),
            'type': step_type,
            'description': description,
            'data': data
        }
        self.steps.append(step)
        
        self.logger.info(f'[{step["step"]:3d}] {step_type}: {description}')
        if data:
            self.logger.debug(f'      Data: {json.dumps(data, default=str, ensure_ascii=False)}')
    
    def log_classification(self, depth: str, complexity: float, keywords: list):
        self.log_step('CLASSIFY', f'Depth={depth} Complexity={complexity:.2f}', {
            'depth': depth,
            'complexity': complexity,
            'keywords': keywords
        })
    
    def log_memory_search(self, query: str, results: int, top_relevance: float = 0):
        self.metrics['memory_queries'] += 1
        self.log_step('MEMORY', f'Query="{query}" Results={results} TopRelevance={top_relevance:.2f}', {
            'query': query,
            'results_count': results,
            'top_relevance': top_relevance
        })
    
    def log_knowledge_applied(self, entries: list, source: str = 'search'):
        self.metrics['knowledge_applied'] += len(entries)
        names = [e.get('name', e) if isinstance(e, dict) else getattr(e, 'name', str(e)) for e in entries[:5]]
        self.log_step('KNOWLEDGE', f'Applied {len(entries)} entries from {source}', {
            'entries': names,
            'count': len(entries)
        })
    
    def log_hypothesis(self, hypothesis: str, confidence: float):
        self.metrics['hypotheses_generated'] += 1
        self.log_step('HYPOTHESIS', f'{hypothesis} (conf={confidence:.2f})', {
            'hypothesis': hypothesis,
            'confidence': confidence
        })
    
    def log_plan(self, steps: list):
        self.log_step('PLAN', f'Generated {len(steps)} steps', {
            'steps': steps
        })
    
    def log_tool_call(self, tool: str, args: dict, result: str):
        self.metrics['tool_calls'] += 1
        self.log_step('TOOL', f'{tool}({str(args)[:50]}...)', {
            'tool': tool,
            'args': args,
            'result_preview': str(result)[:100]
        })
    
    def log_verification(self, claim: str, result: str, passed: bool):
        self.metrics['verification_checks'] += 1
        status = 'PASS' if passed else 'FAIL'
        self.log_step('VERIFY', f'[{status}] {claim}', {
            'claim': claim,
            'result': result,
            'passed': passed
        })
    
    def log_lesson(self, lesson: str):
        self.metrics['lessons_learned'] += 1
        self.log_step('LEARN', lesson)
    
    def log_metacognition(self, confidence: float, state: dict):
        self.log_step('METACOG', f'Confidence={confidence:.2f}', {
            'confidence': confidence,
            'state': state
        })
    
    def log_transfer(self, source: str, target: str, strategy: str):
        self.log_step('TRANSFER', f'{source} -> {target}: {strategy}')
    
    def summary(self, duration_ms: float = 0):
        self.metrics['duration_ms'] = duration_ms
        
        summary = {
            'task_id': self.task_id,
            'total_steps': len(self.steps),
            'metrics': self.metrics,
            'steps': self.steps
        }
        
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info('')
        self.logger.info('=' * 60)
        self.logger.info('RESUMEN DE EJECUCION')
        self.logger.info('=' * 60)
        self.logger.info(f'  Total pasos: {len(self.steps)}')
        self.logger.info(f'  Hipotesis generadas: {self.metrics["hypotheses_generated"]}')
        self.logger.info(f'  Consultas a memoria: {self.metrics["memory_queries"]}')
        self.logger.info(f'  Conocimiento aplicado: {self.metrics["knowledge_applied"]}')
        self.logger.info(f'  Tool calls: {self.metrics["tool_calls"]}')
        self.logger.info(f'  Verificaciones: {self.metrics["verification_checks"]}')
        self.logger.info(f'  Lecciones aprendidas: {self.metrics["lessons_learned"]}')
        self.logger.info(f'  Duracion: {duration_ms:.1f}ms')
        self.logger.info('=' * 60)
        
        return summary
    
    def get_logs(self):
        return self.steps, self.metrics
