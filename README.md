# SmartPrepAI: Premium CBSE Intelligence Pipeline 🐉

SmartPrepAI is a high-performance, data-driven intelligence platform designed to revolutionize how students prepare for CBSE Class 9-12 examinations. By combining a robust FastAPI backend with a premium React/Vite frontend, it provides deep pedagogical insights, chapter-wise topic prioritization, and adaptive study strategies based on thousands of Previous Year Questions (PYQs).

## 🚀 The Vision

I built SmartPrepAI to solve a simple problem: **Academic Information Overload.** Students often have all the resources but lack the "signal" within the noise. This project was developed to move beyond generic study guides and provide a dynamic, AI-powered bridge that identifies exactly what a student needs to focus on for their specific Class, Subject, and Chapter.

## ✨ Key Features

- **CBSE-Standardized Intelligence**: A hierarchical dataset (Class 9-12 → Subject → Chapter) that ensures analytics are hyper-specific and curriculum-aligned.
- **Predatory Red/Black Theme**: A premium, high-contrast UI designed for focus and aesthetic excellence. Includes a full Light/Dark mode toggle.
- **"The Blood Dragon" Trail**: A custom, canvas-based interactive cursor trail with procedural slither physics that keeps the UI feeling alive.
- **Top Chapter Analytics**: Automated ranking of chapters and modules based on their historical frequency and importance in CBSE exams.
- **Adaptive Strategy Insights**: Tailored Study Advice and Practice Strategies generated per chapter module.
- **Zero-Setup Execution**: Automated local launch workflow via optimized Windows batch scripts.

## 🛠️ Technology Stack

- **Frontend**: React (Vite), Tailwind CSS, Framer Motion (Animations), Canvas API.
- **Backend**: FastAPI (Python), Procedural Analytics Engine.
- **Dataset**: Hierarchical JSON structure indexing 2,240+ academic data points.

## 📦 Local Setup & Installation

### Prerequisites
- [Node.js](https://nodejs.org/) (Project built on v18+)
- [Python 3.10+](https://www.python.org/)
- A `GEMINI_API_KEY` (Required for dynamic strategy generation)

### Configuration
1. Clone the repository:
   ```bash
   git clone https://github.com/jashsinghwrld/SmartprepAI.git
   cd SmartprepAI
   ```
2. Set up your environment variables:
   Create a `.env` file in the `backend/` directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## 🚦 How to Run

I have automated the entire startup process for ease of use.

### 1. Automatic Launch (Windows)
Simply run the root-level batch file:
```powershell
.\start.bat
```
This script will:
- Check for Python and Node.js.
- Install backend dependencies (`requirements.txt`).
- Install frontend dependencies (`npm install`).
- Launch both the FastAPI server (Port 8000) and the Vite development server (Port 5173).
- Automatically open the dashboard in your default browser.

### 2. Manual Launch
**Backend**:
```bash
cd backend
pip install -r requirements.txt
python main.py
```
**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

---

## 🤖 Built with Intelligence

This project was developed in close collaboration with **Antigravity**, an advanced agentic AI coding assistant. The process involved a unique pair-programming dynamic where the architecture, premium UI design (including the custom "Blood Dragon" canvas interaction), and the data-driven backend were iteratively refined through a dialogue between human creativity and AI execution.

---

*“Success is the sum of small efforts, repeated day in and day out.”*
Built with passion for the modern student. 🚀
