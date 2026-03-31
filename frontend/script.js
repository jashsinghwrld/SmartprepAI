// ================================================================
//  SmartPrepAI  ·  script.js
//  Handles: form submit · fetch with timeout · plan rendering
// ================================================================

// ── Config ──────────────────────────────────────────────────────
const API_URL        = "http://localhost:5000/generate-plan";
const FETCH_TIMEOUT  = 90000;  // 90 seconds — Claude can be slow on long plans

// ── DOM references ───────────────────────────────────────────────
const form       = document.getElementById("form");
const submitBtn  = document.getElementById("submit-btn");
const errorBox   = document.getElementById("error-box");
const errorText  = document.getElementById("error-text");
const loadingDiv = document.getElementById("loading");
const planOut    = document.getElementById("plan-out");
const planCards  = document.getElementById("plan-cards");
const pillsRow   = document.getElementById("pills");

// ── Day type display config ──────────────────────────────────────
const DAY_TYPES = {
  study:     { emoji: "📘", label: "Study",     cls: "study"     },
  revision:  { emoji: "🔁", label: "Revision",  cls: "revision"  },
  mock_test: { emoji: "✅", label: "Mock Test", cls: "mock_test" },
};

// ================================================================
//  Helpers
// ================================================================

/**
 * Escape a string before injecting into innerHTML.
 * Prevents XSS if Claude returns unexpected characters.
 */
function esc(str) {
  return String(str)
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/"/g,  "&quot;")
    .replace(/'/g,  "&#39;");
}

/**
 * Show an error message to the user.
 * FIX: Forces animation to replay on every call by removing/re-adding the class.
 */
function showError(msg) {
  errorText.textContent = msg;
  // Remove class first so the animation restarts even if already showing
  errorBox.classList.remove("show");
  void errorBox.offsetWidth;         // force reflow — triggers animation restart
  errorBox.classList.add("show");
  errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function hideError() {
  errorBox.classList.remove("show");
}

/**
 * Toggle the loading spinner and disable/enable the submit button.
 */
function setLoading(on) {
  submitBtn.disabled = on;
  submitBtn.classList.toggle("loading", on);
  loadingDiv.classList.toggle("show", on);
  if (on) {
    planOut.style.display = "none";
    loadingDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

/**
 * fetch() with an AbortController timeout.
 * FIX: Without this, if Flask hangs the spinner would spin forever.
 */
async function fetchWithTimeout(url, options, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    return res;
  } catch (err) {
    if (err.name === "AbortError") {
      throw new Error(
        "The request timed out after 90 seconds. " +
        "Try a shorter syllabus or fewer days."
      );
    }
    throw err;
  } finally {
    clearTimeout(timer);
  }
}

// ================================================================
//  Form submission
// ================================================================
form.addEventListener("submit", async (e) => {
  e.preventDefault();    // stop browser from reloading the page
  hideError();

  // Read field values
  const syllabus   = document.getElementById("syllabus").value.trim();
  const daysVal    = document.getElementById("days").value.trim();
  const hoursVal   = document.getElementById("hours").value.trim();
  const difficulty = document.getElementById("difficulty").value;

  // Client-side validation — friendly messages before hitting the server
  if (!syllabus) {
    showError("Please enter your syllabus topics.");
    return;
  }
  if (!daysVal || Number(daysVal) < 1) {
    showError("Please enter the number of days available (at least 1).");
    return;
  }
  if (!hoursVal || Number(hoursVal) <= 0) {
    showError("Please enter how many hours per day you can study.");
    return;
  }

  setLoading(true);

  try {
    const payload = {
      syllabus:      syllabus,
      days:          Number(daysVal),
      hours_per_day: Number(hoursVal),
      difficulty:    difficulty,
    };

    // Call the Flask backend
    const res = await fetchWithTimeout(
      API_URL,
      {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify(payload),
      },
      FETCH_TIMEOUT
    );

    // Parse response JSON
    let data;
    try {
      data = await res.json();
    } catch {
      throw new Error("Server returned an unreadable response. Is Flask running?");
    }

    // Handle server-side errors
    if (!res.ok || !data.success) {
      showError(data.error || "Something went wrong. Please try again.");
      return;
    }

    // FIX: null-check before rendering
    if (!data.plan || data.plan.length === 0) {
      showError("The AI returned an empty plan. Try adding more detail to your syllabus.");
      return;
    }

    renderPlan(data.plan);

  } catch (err) {
    if (err instanceof TypeError || err.message.includes("Failed to fetch")) {
      showError(
        "Cannot connect to the backend. " +
        "Make sure Flask is running: open a terminal → cd backend → python app.py"
      );
    } else {
      showError(err.message || "An unexpected error occurred.");
    }
  } finally {
    // Always re-enable the button, even if something threw
    setLoading(false);
  }
});

// ================================================================
//  Render the study plan
// ================================================================
function renderPlan(plan) {
  // Show the section
  planOut.style.display = "block";
  planCards.innerHTML   = "";

  // ── Summary pills ──────────────────────────────────────────────
  // FIX: parseFloat guards against hours_planned being a string
  const totalHrs  = plan.reduce((s, d) => s + parseFloat(d.hours_planned || 0), 0).toFixed(1);
  const studyN    = plan.filter(d => d.type === "study").length;
  const revN      = plan.filter(d => d.type === "revision").length;
  const mockN     = plan.filter(d => d.type === "mock_test").length;

  pillsRow.innerHTML = [
    `<span class="pill gold">${plan.length} days</span>`,
    `<span class="pill gold">${totalHrs} hrs total</span>`,
    studyN ? `<span class="pill blue">${studyN} study</span>`      : "",
    revN   ? `<span class="pill">${revN} revision</span>`          : "",
    mockN  ? `<span class="pill green">${mockN} mock test</span>`  : "",
  ].join("");

  // FIX: cap stagger so last card never waits more than 0.6s (30+ day plans)
  const maxDelay   = 0.6;
  const stepDelay  = Math.min(0.05, maxDelay / Math.max(plan.length, 1));

  // ── Build each day card ─────────────────────────────────────────
  plan.forEach((day, idx) => {
    const meta = DAY_TYPES[day.type] || DAY_TYPES.study;

    // FIX: topics is always a list of strings after server sanitisation,
    // but we double-check here so the frontend never crashes regardless.
    let topicList = day.topics;
    if (typeof topicList === "string") {
      topicList = topicList.split(/[,;]+/).map(t => t.trim()).filter(Boolean);
    }
    if (!Array.isArray(topicList)) {
      topicList = [];
    }

    const topicsHTML = topicList
      .map(t => `<span class="topic-tag">${esc(t)}</span>`)
      .join("");

    const card = document.createElement("div");
    card.className = `day-card ${meta.cls}`;
    card.style.animationDelay = `${idx * stepDelay}s`;

    card.innerHTML = `
      <div class="day-num">
        <span class="n">${String(day.day).padStart(2, "0")}</span>
        <span class="d">Day</span>
        <span class="type-dot"></span>
      </div>
      <div class="day-body">
        <span class="type-badge">${meta.emoji} ${meta.label}</span>
        <div class="topics-row">${topicsHTML || '<span class="topic-tag">—</span>'}</div>
        <div class="day-hrs">⏱ ${parseFloat(day.hours_planned).toFixed(1)} hrs planned</div>
        ${day.tip ? `<div class="day-tip">${esc(day.tip)}</div>` : ""}
      </div>
    `;

    planCards.appendChild(card);
  });

  // Scroll after a small delay so cards have time to paint
  setTimeout(() => {
    planOut.scrollIntoView({ behavior: "smooth", block: "start" });
  }, 80);
}
