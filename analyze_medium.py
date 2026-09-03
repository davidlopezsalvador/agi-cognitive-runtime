import json
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load medium results
with open('debugbench_medium_results.json', 'r') as f:
    results = json.load(f)

print("=== DebugBench Medium Results ===\n")

def extract_code(response_str):
    try:
        response = json.loads(response_str)
        parts = response.get('parts', [])
        for part in parts:
            if part.get('type') == 'text':
                text = part.get('text', '')
                if '```python' in text:
                    code = text.split('```python')[1].split('```')[0].strip()
                    return code
        return None
    except:
        return None

def normalize_code(code):
    if code is None:
        return ""
    return code.strip().replace('\n', '').replace(' ', '').replace('\t', '')

def get_tokens(response_str):
    try:
        response = json.loads(response_str)
        info = response.get('info', {})
        tokens = info.get('tokens', {})
        return {
            'total': tokens.get('total', 0),
            'input': tokens.get('input', 0),
            'output': tokens.get('output', 0),
            'reasoning': tokens.get('reasoning', 0)
        }
    except:
        return {'total': 0, 'input': 0, 'output': 0, 'reasoning': 0}

correct_no_lit = 0
correct_lit = 0
total_no_lit_tokens = 0
total_lit_tokens = 0

for r in results:
    print(f"=== {r['slug']} ({r['bug_type']}) ===")
    
    code_no_lit = extract_code(r['response_no_lit'])
    code_lit = extract_code(r['response_lit'])
    
    oracle_norm = normalize_code(r['oracle_code'])
    no_lit_norm = normalize_code(code_no_lit)
    lit_norm = normalize_code(code_lit)
    
    match_no_lit = oracle_norm == no_lit_norm
    match_lit = oracle_norm == lit_norm
    
    if match_no_lit:
        correct_no_lit += 1
    if match_lit:
        correct_lit += 1
    
    tokens_no_lit = get_tokens(r['response_no_lit'])
    tokens_lit = get_tokens(r['response_lit'])
    total_no_lit_tokens += tokens_no_lit['total']
    total_lit_tokens += tokens_lit['total']
    
    print(f"  No literary: {'✅' if match_no_lit else '❌'}")
    print(f"  With literary: {'✅' if match_lit else '❌'}")
    print(f"  Tokens: no_lit={tokens_no_lit['total']}, lit={tokens_lit['total']}")
    print()

print("=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Correct solutions:")
print(f"  No literary: {correct_no_lit}/{len(results)} ({correct_no_lit/len(results)*100:.0f}%)")
print(f"  With literary: {correct_lit}/{len(results)} ({correct_lit/len(results)*100:.0f}%)")
print(f"\nTotal tokens used:")
print(f"  No literary: {total_no_lit_tokens:,}")
print(f"  With literary: {total_lit_tokens:,}")
print(f"  Difference: {total_lit_tokens - total_no_lit_tokens:+,} ({(total_lit_tokens/total_no_lit_tokens - 1)*100:+.1f}%)")
