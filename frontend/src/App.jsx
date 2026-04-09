import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import CommandBar from './components/CommandBar';
import MainPanel from './components/MainPanel';
import Sidebar from './components/Sidebar';
import ErrorBoundary from './components/ErrorBoundary';
import CursorGlow from './components/CursorGlow';

export default function App() {
  const [appState, setAppState] = useState(null);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isDark, setIsDark] = useState(true); // Default: dark mode
  
  const [userClass, setUserClass] = useState("12");
  const [userSubject, setUserSubject] = useState("Physics");
  const [userChapter, setUserChapter] = useState("General");
  const [userDifficulty, setUserDifficulty] = useState("medium");

  // Apply / remove 'dark' class on <html>
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  const toggleTheme = () => setIsDark(prev => !prev);

  const API_BASE = "http://localhost:8000";

  const fetchAnalysis = async (currentClass, currentSubject, currentChapter) => {
    // Clear stale data immediately so the UI shows loading state
    setAnalyticsData(null);
    setAppState(null);
    setLoading(true);

    try {
      const analyzeRes = await fetch(`${API_BASE}/analyze-pyq`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
           class: currentClass,
           subject: currentSubject,
           chapter: currentChapter,
           pyqs: null 
        })
      });
      const analyzeRaw = await analyzeRes.json();
      // /analyze-pyq returns { status, data: { analysis, insights, tutor_response } }
      const analyticsPayload = analyzeRaw?.data || analyzeRaw || {};

      const finalAnalytics = { ...analyticsPayload };
      
      setAnalyticsData(finalAnalytics);
      setAppState({ type: "analyze", data: finalAnalytics });

    } catch (e) {
      console.error("Critical State Error:", e);
      alert("Intelligence engine offline. Verify FastAPI (Port 8000) is running.");
    } finally {
      setLoading(false);
    }
  };

  // Re-fetch whenever the user changes class, subject, or chapter
  useEffect(() => {
    fetchAnalysis(userClass, userSubject, userChapter);
  }, [userClass, userSubject, userChapter]);

  return (
    <ErrorBoundary>
      <CursorGlow />
      <div className={`flex h-screen w-full overflow-hidden font-sans selection:bg-red-500/30 transition-colors duration-300 ${
        isDark ? 'bg-[#0B0B0C] text-neutral-300' : 'bg-slate-50 text-neutral-700'
      }`}>
        <Sidebar 
          userClass={userClass} setUserClass={setUserClass}
          userSubject={userSubject} setUserSubject={setUserSubject}
          userChapter={userChapter} setUserChapter={setUserChapter}
          isDark={isDark} toggleTheme={toggleTheme}
        />
        
        <main className="flex-1 relative h-full flex flex-col items-center pt-8 md:pt-16 overflow-y-auto w-full pb-40">
          <AnimatePresence mode="wait">
            <MainPanel 
              key={`${userClass}-${userSubject}-${userChapter}`}
              appState={appState} 
              analyticsData={analyticsData}
              loading={loading} 
              onAnswerComplete={setUserDifficulty}
              isDark={isDark}
            />
          </AnimatePresence>
        </main>

        <div className="fixed bottom-4 md:bottom-8 w-full right-0 md:w-[calc(100%-16rem)] max-w-4xl px-4 z-50 pointer-events-none flex justify-center mx-auto">
           <div className="w-full max-w-2xl pointer-events-auto">
              <CommandBar 
                setAppState={setAppState} 
                setLoading={setLoading} 
                userDifficulty={userDifficulty}
                userClass={userClass} 
                userSubject={userSubject} 
                userChapter={userChapter}
                fetchAnalysis={fetchAnalysis}
                isDark={isDark}
              />
           </div>
        </div>
      </div>
    </ErrorBoundary>
  );
}
