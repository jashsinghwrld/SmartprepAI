import os
import json
import sys

# Mocking the filter logic from main.py
def debug_run_filter(data_raw, cls, sub, chap):
    return [
        d for d in data_raw
        if str(d.get("class", "")).strip() == str(cls).strip()
        and (sub == "general" or str(d.get("subject", "")).lower().strip() == sub)
        and (chap == "general" or str(d.get("chapter", "")).lower().strip() == chap)
    ]

dataset_path = 'c:/Users/jashs/Desktop/SmartprepAI/SmartprepAI/dataset/pyqs.json'
with open(dataset_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total questions in JSON: {len(data)}")

# Test Case: Class 12, Physics, Electrostatics
cls_in = "12"
sub_in = "physics"
chap_in = "electrostatics"

input_class = int(cls_in)
input_subject = sub_in.lower().strip()
input_chapter = chap_in.lower().strip()

res = debug_run_filter(data, input_class, input_subject, input_chapter)
print(f"Tier 1 Results (Exact): {len(res)}")

res2 = debug_run_filter(data, input_class, input_subject, "general")
print(f"Tier 2 Results (Subject): {len(res2)}")

# If 0, let's see what a sample record looks like
if len(data) > 0:
    sample = data[0]
    print(f"Sample Record: {sample}")
    print(f"Sample Class Check: str({sample.get('class')}) == str({input_class}) -> {str(sample.get('class')).strip() == str(input_class).strip()}")
    print(f"Sample Subject Check: str({sample.get('subject')}).lower() == {input_subject} -> {str(sample.get('subject', '')).lower().strip() == input_subject}")
