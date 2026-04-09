import json
import os

dataset_path = 'c:/Users/jashs/Desktop/SmartprepAI/SmartprepAI/dataset/pyqs.json'

syllabus = {
    9: {
        'physics': ['Motion', 'Force', 'Gravitation', 'Sound'],
        'chemistry': ['Is matter pure', 'Atoms & Molecules', 'Structure of Atom'],
        'maths': ['Polynomials', 'Coordinate Geometry', 'Linear Equations'],
        'biology': ['Cell', 'Tissues']
    },
    10: {
        'physics': ['Light', 'Electricity', 'Magnetic Effects'],
        'chemistry': ['Chemical Reactions', 'Acids/Bases/Salts', 'Carbon Compounds'],
        'maths': ['Real Numbers', 'Quadratic Equations', 'Trigonometry'],
        'biology': ['Life Processes', 'Reproduction', 'Heredity']
    },
    11: {
        'physics': ['Kinematics', 'Laws of Motion', 'Thermodynamics'],
        'chemistry': ['Atomic Structure', 'Equilibrium', 'Organic Basics'],
        'maths': ['Sets', 'Relations', 'Limits'],
        'biology': ['Diversity', 'Biomolecules']
    },
    12: {
        'physics': ['Electrostatics', 'Optics', 'Atoms & Nuclei'],
        'chemistry': ['Solutions', 'Electrochemistry', 'Amines'],
        'maths': ['Matrices', 'Calculus', 'Probability'],
        'biology': ['Inheritance', 'Evolution', 'Ecosystem']
    }
}

if os.path.exists(dataset_path):
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    normalized = []
    counts = {}
    
    for d in data:
        cls = int(d.get('class', 10))
        sub = str(d.get('subject', 'maths')).lower().strip()
        
        key = (cls, sub)
        counts[key] = counts.get(key, 0) + 1
        
        # Select chapter based on syllabus map
        ch_list = syllabus.get(cls, {}).get(sub, ['General'])
        ch = ch_list[(counts[key] - 1) % len(ch_list)]
        
        d['class'] = cls
        d['subject'] = sub
        d['chapter'] = ch
        normalized.append(d)
        
    with open(dataset_path, 'w', encoding='utf-8') as f:
        json.dump(normalized, f, indent=2)
    
    print(f"Successfully redistributed {len(normalized)} items across real CBSE chapters.")
else:
    print("Dataset not found.")
