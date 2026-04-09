import os
import json
import re
import asyncio
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv
from cachetools import TTLCache
from typing import Optional, List, Dict, Any

load_dotenv()

app = FastAPI(title="SmartPrepAI Async Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Pydantic Models for Input Validation & Dataset Schema
# ---------------------------------------------------------
class PYQItemSchema(BaseModel):
    class_level: str = Field(default="General", alias="class", description="CBSE Class 9-12 or General")
    subject: str = Field(default="General", description="Physics, Chemistry, Maths, etc.")
    chapter: str = Field(default="General")
    topic: str = Field(default="General")
    difficulty: str = Field(default="medium")
    year: Optional[int] = Field(default=None)
    question: str = Field(default="")
    options: List[str] = Field(default_factory=list)
    answer: str = Field(default="")
    explanation: str = Field(default="")

class GenerateQuestionRequest(BaseModel):
    subject: str = Field(default="General")
    chapter: str = Field(default="General")
    topic: str = Field(default="General")
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    class_level: str = Field(default="General", alias="class")

from pyq_engine import analyze_data as process_pyqs, generate_insights

class AnalyzePYQRequest(BaseModel):
    class_level: str = Field(default="General", alias="class")
    subject: str = Field(default="General")
    chapter: str = Field(default="General")
    pyqs: Optional[list[dict]] = Field(default=None, description="Provide PYQs to bypass memory dataset filtering.")

class StrategyRequest(BaseModel):
    class_level: str = Field(default="12", alias="class")
    subject: str = Field(default="Physics")
    days_left: int = 30
    important_chapters: list
    important_topics: list
    difficulty_distribution: dict

class TutorRequest(BaseModel):
    class_level: str = Field(default="General", alias="class")
    subject: str = Field(default="General")
    chapter: str = Field(default="General")
    analysis_data: dict
    insights: dict
    # Context Awareness
    last_subject: str = Field(default="")
    last_chapter: str = Field(default="")
    user_performance: str = Field(default="") # 'struggling', 'strong', or empty

# ---------------------------------------------------------
# Global Dataset & Cache
# ---------------------------------------------------------
QUESTION_CACHE = TTLCache(maxsize=1000, ttl=3600)
DATASET_RAW = []

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "dataset", "pyqs.json")

def load_dataset_to_memory():
    """Load the JSON dataset synchronously once into RAM during startup."""
    global DATASET_RAW
    if not os.path.exists(DATASET_PATH):
        print("WARNING: Dataset not found during indexing run.")
        return
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            raw = json.load(f)

        # Store raw dicts directly — keep original 'class' key intact
        # so filter_dataset can match on str(d['class'])
        DATASET_RAW = raw
        print(f"Dataset loaded: {len(DATASET_RAW)} questions.")
    except Exception as e:
        print(f"Failed to load dataset: {e}")

@app.post("/refresh-dataset")
async def refresh_dataset():
    """Manual trigger to reload the JSON dataset into RAM cache."""
    load_dataset_to_memory()
    return api_response({"message": "Dataset reloaded from disk successfully."})

@app.on_event("startup")
async def startup_event():
    load_dataset_to_memory()

def filter_dataset(class_level: str = "General", subject: str = "General", chapter: str = "General") -> list[dict]:
    """
    Hierarchical Cascading Filter:
    Chapter Match -> Subject Match -> Class Match
    Ensures analysis never returns empty if the class exists.
    """
    # 1. Normalize input
    try:
        input_class = int(class_level)
    except:
        input_class = class_level
        
    input_subject = str(subject).lower().strip()
    input_chapter = str(chapter).lower().strip()

    def run_filter(cls, sub, chap):
        return [
            d for d in DATASET_RAW
            if str(d.get("class", d.get("class_level", ""))).strip() == str(cls).strip()
            and (sub == "general" or str(d.get("subject", "")).lower().strip() == sub)
            and (chap == "general" or str(d.get("chapter", "")).lower().strip() == chap)
        ]

    # Tier 1: Exact Match (Chapter-level)
    print(f"[FATAL_TRACE] CLASS_LEVEL RAW: '{class_level}' TYPE: {type(class_level)}")
    print(f"[TRACE] Tier 1 Filter: Class={input_class} ({type(input_class)}), Subject={input_subject}, Chapter={input_chapter}")
    results = run_filter(input_class, input_subject, input_chapter)
    print(f"[TRACE] Tier 1 Results Found: {len(results)}")

    # Tier 2 Fallback: Subject-level (Skip Chapter)
    if len(results) == 0 and input_chapter != "general":
        print(f"[TRACE] Fallback Tier 2: No data for '{input_chapter}'. Widening to Subject '{input_subject}'...")
        results = run_filter(input_class, input_subject, "general")
        print(f"[TRACE] Tier 2 Results Found: {len(results)}")

    # Tier 3 Fallback: Class-level (Skip Subject)
    if len(results) == 0 and input_subject != "general":
        print(f"[TRACE] Fallback Tier 3: No data for '{input_subject}'. Widening to Class '{input_class}'...")
        results = run_filter(input_class, "general", "general")
        print(f"[TRACE] Tier 3 Results Found: {len(results)}")

    print(f"[STATUS] Active Questions in RAM Archive: {len(DATASET_RAW)}")
    print("Final Analysis Results count:", len(results))
    return results

def load_question_from_dataset(req: GenerateQuestionRequest) -> dict | None:
    """Retrieves a single optimal match from the dataset using robust unified filtering."""
    matches = filter_dataset(
        class_level=req.class_level, 
        subject=req.subject, 
        chapter=req.chapter, 
        topic=req.topic, 
        difficulty=req.difficulty
    )
    if matches:
        return random.choice(matches)
    return None

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def get_gemini_model():
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_key_here":
        raise Exception("GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")

async def call_gemini_async(prompt: str) -> str:
    model = get_gemini_model()
    try:
        response = await model.generate_content_async(prompt)
        return response.text.strip()
    except AttributeError:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text.strip()

def parse_json_from_llm(raw_text: str) -> dict:
    raw = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$", "", raw, flags=re.MULTILINE)
    return json.loads(raw.strip())


def api_response(data: dict = None, error: str = None) -> dict:
    """Standardized response format wrapper"""
    if error:
        return {"status": "error", "data": {}, "error": error}
    return {"status": "success", "data": data or {}, "error": None}

# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.get("/health")
async def health_check():
    return api_response({"message": "SmartPrepAI API is running optimized in memory!"})


@app.post("/generate-question")
async def generate_question(req: GenerateQuestionRequest):
    try:
        class_str = req.class_level
        cache_key = f"{req.subject.lower()}_{class_str.lower()}_{req.chapter.lower()}_{req.topic.lower()}_{req.difficulty.lower()}"
        
        # 0. Fast TTLCache Check
        if cache_key in QUESTION_CACHE:
            return api_response(QUESTION_CACHE[cache_key])

        # 1. Attempt RAM dataset
        dataset_match = load_question_from_dataset(req)
        if dataset_match:
            res_data = {
                "question": dataset_match.get("question", ""),
                "options": dataset_match.get("options", []),
                "answer": dataset_match.get("answer", ""),
                "explanation": dataset_match.get("explanation", "")
            }
            QUESTION_CACHE[cache_key] = res_data
            return api_response(res_data)

        # 2. Fallback to AI
        prompt = (
            f"You are an academic expert. Generate a {req.difficulty} multiple choice question for Subject: {req.subject} (Class {class_str}), focusing on Chapter: {req.chapter}, Topic: {req.topic}.\n"
            "Return ONLY valid JSON with the following exact keys:\n"
            "{\n"
            '  "question": "The question text",\n'
            '  "options": ["Option A", "Option B", "Option C", "Option D"],\n'
            '  "answer": "The exact string of the correct option",\n'
            '  "explanation": "Brief explanation of why the answer is correct"\n'
            "}"
        )
        
        raw_response = await call_gemini_async(prompt)
        res_data = parse_json_from_llm(raw_response)
        
        # Ensure fallback clean structure
        clean_data = {
            "question": res_data.get("question", ""),
            "options": res_data.get("options", []),
            "answer": res_data.get("answer", ""),
            "explanation": res_data.get("explanation", "")
        }
        
        QUESTION_CACHE[cache_key] = clean_data
        return api_response(clean_data)

    except Exception as e:
        return api_response(error=str(e))


@app.post("/analyze-pyq")
async def analyze_pyq_endpoint(req: AnalyzePYQRequest):
    """Pure Python Mathematical analysis string parsing endpoint"""
    global DATASET_RAW
    try:
        # FAILSAFE: If RAM is empty for any reason, resuscitate from disk
        if not DATASET_RAW:
            print("[RESUSCITATE] Memory empty. Reloading dataset from disk...")
            load_dataset_to_memory()

        # DEBUG: Verify incoming parameters from the UI state mapping
        print(f"Received: class={req.class_level}, subject={req.subject}, chapter={req.chapter}")
        
        # Filter DATASET_RAW on the fly if PYQs are perfectly null or empty
        target_pyqs = req.pyqs
        if not target_pyqs: # CATCH BOTH None AND []
            target_pyqs = filter_dataset(
                class_level=req.class_level,
                subject=req.subject,
                chapter=req.chapter
            )

        # 1. Fallback payload to prevent UI crashes on perfectly empty curriculum filtering
        if not target_pyqs:
            empty_analysis = {
                "important_chapters": ["Core Concepts"],
                "important_topics": ["General Syllabus Overview"],
                "difficulty_distribution": {"easy": 33, "medium": 34, "hard": 33}
            }
            empty_insights = generate_insights(empty_analysis, subject=req.subject, chapter=req.chapter)
            
            tutor_req = TutorRequest(
                class_level=req.class_level, subject=req.subject, chapter=req.chapter,
                analysis_data=empty_analysis, insights=empty_insights
            )
            tutor_res = await generate_tutor_response(tutor_req)
            
            return api_response({
                "tutor_response": tutor_res.get("data", {}),
                "analysis": empty_analysis,
                "insights": empty_insights
            })

        # 2. Executes purely mathematically from pyq_engine, strictly O(n)
        analysis_stats = process_pyqs(target_pyqs)
        insights_data = generate_insights(analysis_stats, subject=req.subject, chapter=req.chapter)
        
        # 3. Pass sequentially into the conversational AI Tutor Engine
        tutor_req = TutorRequest(
            class_level=req.class_level,
            subject=req.subject,
            chapter=req.chapter,
            analysis_data=analysis_stats,
            insights=insights_data
        )
        tutor_res = await generate_tutor_response(tutor_req)
        tutor_payload = tutor_res.get("data", {}) if isinstance(tutor_res, dict) else {}
        
        # 4. Return globally unified data object
        return api_response({
            "tutor_response": tutor_payload,
            "analysis": analysis_stats,
            "insights": insights_data
        })
    except Exception as e:
        return api_response(error=str(e))


@app.post("/generate-strategy")
async def generate_strategy(req: StrategyRequest):
    try:
        class_str = req.class_level
        
        prompt = (
            f"You are an expert CBSE study strategist. The student is in Class {class_str} studying {req.subject} and has {req.days_left} days left before the exam.\n\n"
            "Based completely on the following pure statistics calculated from past year questions (PYQs):\n"
            f"Important Chapters: {json.dumps(req.important_chapters)}\n"
            f"Important Topics: {json.dumps(req.important_topics)}\n"
            f"Difficulty Distribution: {json.dumps(req.difficulty_distribution)}\n\n"
            "Create a structured, highly realistic study strategy. DO NOT hallucinate. Strictly distribute the workload over the days left.\n"
            "Return ONLY valid JSON with exactly these keys:\n"
            "{\n"
            '  "prioritized_chapters": ["chapter A", "chapter B"],\n'
            '  "daily_study_plan": {"Day 1-5": "Master Chapter A", "Day 6-10": "Solve PYQs for Chapter B"},\n'
            '  "revision_strategy": "A brief textual explanation of how to review correctly"\n'
            "}"
        )
        
        raw_response = await call_gemini_async(prompt)
        data = parse_json_from_llm(raw_response)
        
        clean_data = {
            "prioritized_chapters": data.get("prioritized_chapters", []),
            "daily_study_plan": data.get("daily_study_plan", {}),
            "revision_strategy": data.get("revision_strategy", "Focus heavily on practicing hard logic PYQs.")
        }
        return api_response(clean_data)
        
    except Exception as e:
        return api_response(error=str(e))

@app.post("/tutor-response")
async def generate_tutor_response(req: TutorRequest):
    try:
        # Rule-based Context Awareness
        adaptive_rules = []
        if req.last_subject == req.subject and req.last_chapter == req.chapter and req.subject != "General":
            adaptive_rules.append("- The student is continuing the exact same chapter as their last query. Build securely upon previous learning. AVOID repeating introductory explanations.")
        else:
            adaptive_rules.append(f"- This is a fresh session on {req.chapter}. Provide a welcoming, structurally solid introduction.")

        # Heuristic Tone Adjustments
        perf = req.user_performance.lower()
        if perf == "struggling":
            adaptive_rules.append("- Tone constraints: Highly encouraging, patient, and deeply foundational. Break complex steps down heavily and offer maximum guidance.")
        elif perf == "strong":
            adaptive_rules.append("- Tone constraints: Challenging, fast-paced, and academic. Push to tackle High-Order Thinking Skills (HOTs) and skip basic conceptual repetition.")
        else:
            adaptive_rules.append("- Tone constraints: Balanced, warmly supportive standard CBSE teacher style.")

        rules_str = "\n".join(adaptive_rules)

        prompt = (
            f"You are an expert, supportive CBSE Tutor speaking directly to a Class {req.class_level} student studying {req.subject} ({req.chapter}).\n"
            "PERSONALITY TRAITS to strictly follow:\n"
            "- Be highly supportive, clear, and slightly motivating.\n"
            "- Be concise and NOT overly verbose. Keep sentences crisp and scannable.\n"
            "- AVOID all robotic tones and generic AI phrases (e.g., never say 'As an AI', 'It is important to note', 'In conclusion').\n\n"
            "Below is the strict mathematical data and strategic insights calculated for this curriculum section:\n"
            f"Analysis Data: {json.dumps(req.analysis_data)}\n"
            f"Insights: {json.dumps(req.insights)}\n\n"
            "Your task: Convert this pure mathematical logic into an engaging, human-like teaching response adhering perfectly to your personality.\n\n"
            "Rules:\n"
            "- DO NOT hallucinate external facts. Base your guidance purely and exclusively on the provided data.\n"
            f"{rules_str}\n"
            "- Return ONLY valid JSON with exactly the following keys structure. Do not output markdown codeblocks around the JSON.\n"
            "{\n"
            '  "explanation": "A friendly introductory paragraph analyzing their targeted area.",\n'
            '  "key_focus_areas": ["Array string 1", "Array string 2"],\n'
            '  "step_by_step_guidance": ["Step 1", "Step 2", "Step 3"],\n'
            '  "motivation": "A short, warmly encouraging closing sentence."\n'
            "}"
        )
        
        raw_response = await call_gemini_async(prompt)
        data = parse_json_from_llm(raw_response)
        
        clean_data = {
            "explanation": data.get("explanation", "Alright, let's dive into this!"),
            "key_focus_areas": data.get("key_focus_areas", []),
            "step_by_step_guidance": data.get("step_by_step_guidance", []),
            "motivation": data.get("motivation", "You've got this! Keep practicing.")
        }
        return api_response(clean_data)
        
    except Exception as e:
        return api_response(error=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
