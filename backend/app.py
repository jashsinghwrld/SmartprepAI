# ================================================================
#  SmartPrepAI  ·  backend/app.py
#  AI  :  Google Gemini (free)
#  Run :  python app.py
#  Needs: pip install flask google-generativeai python-dotenv
# ================================================================

import os
import json
import re
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

@app.route("/generate-plan", methods=["OPTIONS"])
def preflight():
    return jsonify({}), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "SmartPrepAI is running!"})


@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Request body must be JSON."}), 400

    syllabus   = str(data.get("syllabus",      "")).strip()
    days_raw   = data.get("days",          "")
    hours_raw  = data.get("hours_per_day", "")
    difficulty = str(data.get("difficulty", "medium")).strip().lower()

    errors = []
    if len(syllabus) < 5:
        errors.append("Syllabus is too short.")
    try:
        days = int(days_raw)
        if not (1 <= days <= 365):
            errors.append("Days must be between 1 and 365.")
    except (ValueError, TypeError):
        errors.append("days must be a whole number.")
        days = 0
    try:
        hours = float(hours_raw)
        if not (0 < hours <= 24):
            errors.append("Hours must be between 0 and 24.")
    except (ValueError, TypeError):
        errors.append("hours_per_day must be a number.")
        hours = 0
    if difficulty not in ("easy", "medium", "hard"):
        difficulty = "medium"

    if errors:
        return jsonify({"success": False, "error": " | ".join(errors)}), 400

    prompt = _build_prompt(syllabus, days, hours, difficulty)
    try:
        raw_plan = _call_gemini(prompt)
    except EnvironmentError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except ValueError as e:
        return jsonify({"success": False, "error": f"AI format error: {e}"}), 502
    except Exception as e:
        return jsonify({"success": False, "error": f"AI error: {e}"}), 502

    plan = _sanitise_plan(raw_plan, hours)
    return jsonify({"success": True, "plan": plan})


def _build_prompt(syllabus, days, hours, difficulty):
    pace = {
        "easy":   "Relaxed. Fewer topics per day, extra recap slots.",
        "medium": "Balanced. Mix new topics with short daily reviews.",
        "hard":   "Dense. Maximum coverage. Push hard every session.",
    }[difficulty]

    return (
        "You are an expert academic study planner.\n\n"
        "## Student inputs\n"
        f"Syllabus:\n\"\"\"\n{syllabus}\n\"\"\"\n"
        f"Total days    : {days}\n"
        f"Hours per day : {hours}\n"
        f"Difficulty    : {difficulty} - {pace}\n\n"
        "## Rules\n"
        "1. Extract every topic from the syllabus.\n"
        "2. Rank topics by complexity (high / medium / low).\n"
        f"3. Spread topics across all {days} days:\n"
        "   - Give high-complexity topics more time.\n"
        "   - Insert one revision day after every 5 study days.\n"
        "   - The final day must always be type mock_test.\n"
        f"4. hours_planned must be a NUMBER (float) between 0.5 and {hours}.\n"
        "5. topics must be an ARRAY of strings, never a single string.\n\n"
        "## Output\n"
        "Return ONLY a raw JSON array. No markdown. No explanation. No code fences.\n"
        "Every element must have exactly these keys:\n"
        "  day           : integer\n"
        "  type          : study or revision or mock_test\n"
        "  topics        : array of strings\n"
        f"  hours_planned : float max {hours}\n"
        "  tip           : string one short practical tip\n\n"
        "Return the complete array now."
    )


def _call_gemini(prompt):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_key_here":
        raise EnvironmentError(
            "GEMINI_API_KEY is not set. "
            "Get a free key at https://aistudio.google.com "
            "then add it to backend/.env as: GEMINI_API_KEY=your_key_here"
        )

    try:
        import google.generativeai as genai
    except ImportError:
        raise EnvironmentError("Run: pip install google-generativeai")

    genai.configure(api_key=api_key)
    model    = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    raw      = response.text.strip()

    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$",       "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parse error: {e}")

    if not isinstance(plan, list) or len(plan) == 0:
        raise ValueError("Gemini returned an empty plan.")

    return plan


def _sanitise_plan(plan, max_hours):
    clean = []
    for i, item in enumerate(plan):
        if not isinstance(item, dict):
            continue

        raw_topics = item.get("topics", [])
        if isinstance(raw_topics, str):
            topics = [t.strip() for t in re.split(r"[,;]+", raw_topics) if t.strip()]
        elif isinstance(raw_topics, list):
            topics = [str(t).strip() for t in raw_topics if str(t).strip()]
        else:
            topics = ["(no topics listed)"]

        try:
            hrs = float(item.get("hours_planned", max_hours))
        except (ValueError, TypeError):
            hrs = float(max_hours)
        hrs = round(min(max(hrs, 0.5), float(max_hours)), 1)

        day_type = str(item.get("type", "study")).lower().strip()
        if day_type not in ("study", "revision", "mock_test"):
            day_type = "study"

        tip = str(item.get("tip", "")).strip()
        if not tip:
            tip = "Stay consistent — every hour of study compounds."

        clean.append({
            "day":           int(item.get("day", i + 1)),
            "type":          day_type,
            "topics":        topics,
            "hours_planned": hrs,
            "tip":           tip,
        })

    return clean


if __name__ == "__main__":
    print()
    print("  SmartPrepAI  -  Backend Server (Gemini)")
    print("  Health : http://localhost:5000/health")
    print("  API    : POST http://localhost:5000/generate-plan")
    print()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
