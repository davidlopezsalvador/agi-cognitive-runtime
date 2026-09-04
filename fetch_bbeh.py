from datasets import load_dataset
import json

ds = load_dataset('BBEH/bbeh', split='train')

tasks = ['zebra puzzles', 'shuffled objects', 'multistep arithmetic']
problems = []

for task in tasks:
    task_data = [ex for ex in ds if ex['task'] == task]
    for ex in task_data[:5]:
        problems.append({
            'task': ex['task'],
            'input': ex['input'],
            'target': ex['target']
        })

with open('bbeh_sample.json', 'w') as f:
    json.dump(problems, f, indent=2)

for i, p in enumerate(problems):
    print(f"=== Problem {i+1} ({p['task']}) ===")
    print(f"Input: {p['input'][:500]}")
    print(f"Target: {p['target']}")
    print()
