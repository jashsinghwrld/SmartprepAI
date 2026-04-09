from collections import Counter, defaultdict
import random

def analyze_data(data: list[dict]) -> dict:
    """
    Chapter-Wise Topic Prioritization Engine.

    Steps:
      1. Group all questions by chapter name.
      2. For each chapter, count topic frequency within that chapter ONLY.
      3. Rank topics by frequency (descending).
      4. Return top 3-5 unique topics per chapter.
      5. Uses ONLY the filtered dataset passed in.
    """
    if not data:
        return {
            "important_chapters": [],
            "important_topics": [],
            "difficulty_distribution": {"easy": 0, "medium": 0, "hard": 0},
            "chapter_priority_map": {},
            "priority_topics_list": []
        }

    # --- Step 1: Group questions by chapter ---
    chapter_groups: dict[str, list[dict]] = defaultdict(list)
    difficulties = Counter({'easy': 0, 'medium': 0, 'hard': 0})
    global_topic_counter = Counter()

    for item in data:
        ch = str(item.get("chapter", "Unknown")).strip()
        di = str(item.get("difficulty", "medium")).strip().lower()
        to = str(item.get("topic", "")).strip()

        if ch and ch != "Unknown":
            chapter_groups[ch].append(item)

        if di in difficulties:
            difficulties[di] += 1

        if to:
            global_topic_counter[to] += 1

    total = len(data)
    difficulty_distribution = {
        k: round((v / total * 100), 2) if total > 0 else 0
        for k, v in difficulties.items()
    }

    # --- Steps 2 & 3: Count & rank topics within each chapter ---
    priority_topics_list = []    # final structured output
    chapter_priority_map = {}    # flat dict for fast UI lookup: chapter_key -> [topics]

    print("\n--- [DATABASE_AUDIT] CHAPTER-WISE TOPIC PRIORITIZATION ---")
    for chapter_name in sorted(chapter_groups.keys()):
        questions = chapter_groups[chapter_name]

        # Step 2: count topic frequency within this chapter
        topic_counter: Counter = Counter()
        for q in questions:
            topic = str(q.get("topic", "")).strip()
            if topic:
                topic_counter[topic] += 1

        # Step 3: rank by frequency descending; deduplicate via Counter
        ranked_topics = [t for t, _ in topic_counter.most_common()]

        # Step 5: top 3-5 only, no duplicates (Counter already deduplicates)
        top_topics = list(dict.fromkeys(ranked_topics))[:5]   # dict.fromkeys preserves order & strips dupes

        print(f"[AUDIT] {chapter_name}: {len(questions)} questions -> top topics: {top_topics}")

        # Step 4: build structured output
        priority_topics_list.append({
            "chapter": chapter_name,
            "priority_topics": top_topics
        })

        # Also keep flat dict with multiple lookup keys for the frontend
        chapter_priority_map[chapter_name] = top_topics
        chapter_priority_map[chapter_name.lower().strip()] = top_topics

    print(f"--- [STATUS] {len(priority_topics_list)} chapters indexed ---\n")

    return {
        "important_chapters": sorted(chapter_groups.keys(), key=lambda c: len(chapter_groups[c]), reverse=True),
        "important_topics": [t for t, _ in global_topic_counter.most_common(10)],
        "difficulty_distribution": difficulty_distribution,
        "chapter_priority_map": chapter_priority_map,     # fast lookup dict
        "priority_topics_list": priority_topics_list       # structured list-of-objects
    }

def generate_insights(analysis: dict, subject: str = "General", chapter: str = "General") -> dict:
    """
    Dynamic pedagogical insights generator.
    """
    diff = analysis.get("difficulty_distribution", {"easy": 0, "medium": 0, "hard": 0})
    hard_pct = diff.get("hard", 0)
    easy_pct = diff.get("easy", 0)

    # Context Switch
    is_chapter_view = str(chapter).lower() == "general"
    focus_label = "Top Chapters" if is_chapter_view else "Key Topics"
    focus_areas = analysis.get("important_chapters" if is_chapter_view else "important_topics", [])[:5]

    # Rule-based advice
    state = "medium"
    if hard_pct > 35: state = "hard"
    elif easy_pct > 50: state = "easy"

    advice_templates = {
        "hard": [
            f"The examiners for {subject} currently favor deep conceptual derivations in {chapter}.",
            f"High-frequency hard questions detected in {chapter}. Prioritize multi-step proofing.",
            f"Strategic depth is key for {chapter}. Don't rush; focus on the underlying First Principles."
        ],
        "easy": [
            f"High mark-yield area for {subject}. The patterns in {chapter} are repetitive and drills are recommended.",
            f"Drill speed for {chapter}. These are 'Banker Marks'—ensure 100% accuracy here.",
            f"Mastering the basics of {chapter} will boost your confidence for the tougher modules."
        ],
        "medium": [
            f"Steady revision of {chapter} standard definitions will suffice for the medium-tier analysis.",
            f"Balance theory and numericals for {subject}. The exam pattern here is traditionally balanced.",
            f"Focus on last 3-year trends for {chapter} to isolate the most likely 3-mark questions."
        ]
    }

    # Curriculum Intelligence Map (Expert Pedagogical Tips)
    CURRICULUM_INTEL = {
        "electrostatics": "Master Gauss's Law derivations for spheres and wires; they appear in 4/5 previous years.",
        "optics": "Lens Maker's formula and Ray Diagrams for compound microscopes are high-reward derivations.",
        "motion": "Velocity-Time graph interpretation is the core mark-earner. Watch for deceleration signs.",
        "solutions": "Raoult's Law and Vant't Hoff factor are numerical favorites. Practice non-ideal behavior cases.",
        "calculus": "Focus on the Chain Rule and Integration by Parts. Most HOTS questions involve these transitions.",
        "trig": "Inverse Trigonometry identities are the baseline; memorize the principal value ranges perfectly.",
        "reproduction": "Labelled diagrams of Double Fertilization and Menstrual cycles are guaranteed mark-earners.",
        "life processes": "The Nephron diagram and Heart flowcharts are frequent 3-markers in CBSE boards.",
        "atomic structure": "Bohr's model energy transitions and Quantum numbers are high-frequency topics.",
        "force": "Newton's 2nd Law F=ma is the anchor. Practice Pulley problems with varying friction."
    }

    study_advice = random.choice(advice_templates[state])
    practice_strategy = f"Focus on {state} difficulty drills and verify with previous year 5-mark results for {chapter}."

    # Slug-based Tip Lookup
    slug = str(chapter).lower().strip()
    custom_tip = CURRICULUM_INTEL.get(slug, "Focus on NCERT fundamentals and clean, labeled diagrammatic presentations.")
    
    # Priority Topics Sync: Multi-tier fallback for perfect discovery rendering
    priority_map = analysis.get("chapter_priority_map", {})
    prioritized_topics = priority_map.get(slug, priority_map.get(chapter, []))
    
    # Secondary Fallback: If chapter map is empty, try a case-insensitive search
    if not prioritized_topics:
        for k, v in priority_map.items():
            if k.lower().strip() == slug:
                prioritized_topics = v
                break

    return {
        "focus_areas": focus_areas,
        "focus_label": focus_label,
        "recommended_difficulty": state.capitalize(),
        "study_advice": study_advice,
        "practice_strategy": practice_strategy,
        "quick_tip": custom_tip,
        "prioritized_topics": prioritized_topics,
        "chapter_priority_map": priority_map,
        "chapter_tips_map": CURRICULUM_INTEL
    }

def process_conversation(text: str, analysis: dict, insights: dict) -> dict:
    """Conversational intent parser."""
    cmd = text.lower().strip()
    if any(word in cmd for word in ["study next", "plan", "strategy"]):
        intent = "strategy"
        focus = insights.get("focus_areas", [])
        priority = focus[0] if focus else "fundamentals"
        response = f"Your highest impact module is {priority}. {insights.get('practice_strategy', '')}"
    elif any(word in cmd for word in ["question", "practice", "solve"]):
        intent = "generate"
        response = "Alright, let's test your understanding with a high-frequency question."
    else:
        intent = "analyze"
        response = "I've refreshed your intelligence map. Here are the latest trends."

    return {
        "intent": intent,
        "tutor_response": response
    }
