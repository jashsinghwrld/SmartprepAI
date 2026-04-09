import json, sys
sys.path.insert(0, 'backend')

# Simulate exactly what the backend does
data = json.load(open('dataset/pyqs.json', encoding='utf-8'))

# Simulate filter_dataset
input_class = 12
input_subject = "physics"
input_chapter = "general"

def run_filter(d_list, cls, sub, chap):
    return [
        d for d in d_list
        if str(d.get("class", d.get("class_level", ""))).strip() == str(cls).strip()
        and (sub == "general" or str(d.get("subject", "")).lower().strip() == sub)
        and (chap == "general" or str(d.get("chapter", "")).lower().strip() == chap)
    ]

res = run_filter(data, input_class, input_subject, input_chapter)
print(f"Filter result for Class=12 Physics: {len(res)} questions")

# Show sample
if res:
    print("Sample:", res[0])

# Now run the engine on it
from pyq_engine import analyze_data

result = analyze_data(res)
print("\npriority_topics_list:")
for e in result['priority_topics_list']:
    print(f"  {e['chapter']}: {e['priority_topics']}")
print("\ndifficulty_distribution:", result['difficulty_distribution'])
