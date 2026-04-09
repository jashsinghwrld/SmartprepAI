import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function CommandBar({ setAppState, setLoading, userDifficulty, userClass, userSubject, userChapter, fetchAnalysis }) {
  const [focused, setFocused] = useState(false);
  const [val, setVal] = useState("");
  const debounceRef = useRef(null);

  const handleLaunch = async () => {
    if (!val.trim()) return;
    if (debounceRef.current && Date.now() - debounceRef.current < 300) return; // 300ms debounce
    debounceRef.current = Date.now();
    
    setLoading(true);
    const cmd = val.toLowerCase();

    // 1. Debug State Tracking
    console.log("Launching Command:", {
      command: cmd,
      class: userClass,
      subject: userSubject,
      chapter: userChapter,
      difficulty: userDifficulty
    });

    try {
      if (cmd.includes("generate")) {
        // Parse semantics or fallback to adaptive difficulty state
        let difficulty = userDifficulty;
        if (cmd.includes("easy")) difficulty = "easy";
        else if (cmd.includes("medium")) difficulty = "medium";
        else if (cmd.includes("hard")) difficulty = "hard";

        const topic = cmd.replace(/generate|questions|hard|medium|easy|about|on|for/g, "").trim() || "Mystery Topic";

        const res = await fetch("http://localhost:8000/generate-question", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            topic, 
            difficulty,
            class: userClass,
            subject: userSubject,
            chapter: userChapter
          })
        });
        const dataRaw = await res.json();
        setAppState({ type: "generate", data: dataRaw.data || dataRaw });

      } else {
        // Automatically utilize the active frontend selectors via centralized pipeline
        await fetchAnalysis(userClass, userSubject, userChapter);
      }
    } catch (e) {
      console.error(e);
      alert("Failed to hit API. Ensure FastAPI is running on port 8000.");
    } finally {
       setLoading(false);
       setVal(""); // Clear UI after execution
    }
  };

  const handleKeyDown = (e) => {
     if (e.key === "Enter") handleLaunch();
     if (e.key === "Escape") setVal("");
  };

  return (
    <motion.div 
      initial={{ y: 50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", damping: 25, stiffness: 200, delay: 0.1 }}
      className="relative w-full"
    >
      <motion.div 
        animate={{ 
          boxShadow: focused 
            ? "0 0 0 1px rgba(239,68,68,0.5), 0 10px 40px -10px rgba(239,68,68,0.2)" 
            : "0 0 0 1px rgba(255,255,255,0.1), 0 10px 30px -10px rgba(0,0,0,0.5)"
        }}
        className="bg-[#141416]/95 backdrop-blur-2xl rounded-2xl overflow-hidden transition-shadow duration-300 flex flex-col"
      >
        <AnimatePresence>
          {focused && (
             <motion.div 
               initial={{ height: 0, opacity: 0 }}
               animate={{ height: 'auto', opacity: 1 }}
               exit={{ height: 0, opacity: 0 }}
               className="px-4 py-2 border-b border-white/5 flex gap-2 text-[11px] text-neutral-400 bg-white/[0.01] items-center"
             >
               <span className="bg-white/10 px-1.5 py-0.5 rounded text-neutral-300 font-mono tracking-tight shadow-sm">Enter</span> 
               <span>to execute command</span>
               <span className="bg-white/10 px-1.5 py-0.5 rounded text-neutral-300 font-mono tracking-tight shadow-sm ml-auto">Esc</span> 
               <span>clear</span>
             </motion.div>
          )}
        </AnimatePresence>

        <div className="flex items-center px-4 py-3">
          <svg className="w-5 h-5 text-red-400 mr-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
          <input
            type="text"
            className="flex-1 bg-transparent border-none outline-none text-neutral-100 placeholder-neutral-500 font-medium text-sm"
            placeholder='Try "Analyze Thermodynamics PYQs" or "Generate hard questions about React"'
            value={val}
            onChange={(e) => setVal(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            onKeyDown={handleKeyDown}
          />
          
          <AnimatePresence>
            {val.length > 0 && (
              <motion.button
                onClick={handleLaunch}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.8, opacity: 0 }}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-white text-black rounded-lg px-4 py-1.5 text-xs font-bold tracking-wide shadow-lg ml-2 hover:bg-neutral-200 transition-colors"
              >
                Launch
              </motion.button>
            )}
          </AnimatePresence>
        </div>
      </motion.div>
    </motion.div>
  );
}
