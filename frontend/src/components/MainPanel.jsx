import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function MainPanel({ appState, analyticsData, loading, onAnswerComplete, isDark }) {
  const [selectedDetail, setSelectedDetail] = useState(null);

  const activeData = (analyticsData?.analysis ? analyticsData : appState?.data) || {};
  const analysis = activeData?.analysis || {};
  const insights = activeData?.insights || {};

  const {
    difficulty_distribution = { easy: 0, medium: 0, hard: 0 },
    priority_topics_list = []
  } = analysis;

  const {
    study_advice = "Analyzing pedagogical trends...",
    practice_strategy = "Formulating adaptive curriculum...",
    focus_areas = [],
    focus_label = "Crucial Modules",
    recommended_difficulty = "Medium",
    quick_tip = "",
    chapter_tips_map = {}
  } = insights;

  // Theme Helpers
  const cardBg      = isDark ? 'bg-[#141416]/80 border-white/5 shadow-none' : 'bg-white border-neutral-200 shadow-xl';
  const headingText = isDark ? 'text-neutral-500' : 'text-neutral-400';
  const mainText    = isDark ? 'text-white' : 'text-neutral-800';
  const subText     = isDark ? 'text-neutral-400' : 'text-neutral-600';
  const modalBg     = isDark ? 'bg-[#0d0d0e] border-white/10' : 'bg-white border-neutral-200';
  const itemBg      = isDark ? 'bg-white/[0.03] hover:bg-white/[0.06] border-white/5' : 'bg-neutral-50 hover:bg-neutral-100 border-neutral-200';

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-64 w-full">
        <div className="w-12 h-12 border-4 border-red-500/20 border-t-red-500 rounded-full animate-spin mb-4"></div>
        <p className={`font-medium animate-pulse ${headingText}`}>Synchronizing Intelligence...</p>
      </div>
    );
  }

  if (!activeData || Object.keys(activeData).length === 0) {
    return (
      <div className="text-center py-20 px-4">
        <div className="text-5xl mb-6">📊</div>
        <h2 className={`text-xl font-bold mb-2 ${mainText}`}>Ready to Start Analysis</h2>
        <p className="text-neutral-500 max-w-sm mx-auto">
          Select your curriculum focus on the left and type{" "}
          <span className="text-red-500 font-mono italic">"Analyze"</span> to begin.
        </p>
      </div>
    );
  }

  let currentPriorityTopics = [];
  if (selectedDetail) {
    const listEntry = priority_topics_list.find(e => e.chapter === selectedDetail);
    currentPriorityTopics = listEntry ? listEntry.priority_topics : [];
  }

  return (
    <motion.div
      key="analyze"
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-5xl px-4 md:px-8 flex flex-col gap-6 pb-32 relative"
    >
      {/* Topic Discovery Modal */}
      <AnimatePresence>
        {selectedDetail && (
          <div className="fixed inset-0 z-[100] flex items-center justify-center px-4 backdrop-blur-sm bg-black/80">
            <motion.div
              initial={{ scale: 0.9, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.9, opacity: 0, y: 20 }}
              className={`p-8 rounded-3xl max-w-lg w-full shadow-2xl relative overflow-hidden border ${modalBg}`}
            >
              <div className="flex items-center justify-between mb-6">
                <span className="text-[10px] font-bold uppercase tracking-widest text-red-500 bg-red-500/10 px-2 py-1 rounded">Discovery</span>
                <button onClick={() => setSelectedDetail(null)} className="text-neutral-500 hover:text-red-500 transition-colors">
                   <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>
              <h2 className={`text-2xl font-bold mb-6 ${mainText}`}>{selectedDetail}</h2>
              <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2">
                {currentPriorityTopics.map((topic, idx) => (
                  <div key={idx} className={`p-4 rounded-xl border flex items-center justify-between group transition-all ${itemBg}`}>
                    <span className={`text-sm font-semibold transition-colors ${isDark ? 'text-neutral-300 group-hover:text-red-400' : 'text-neutral-700 group-hover:text-red-600'}`}>{topic}</span>
                    <span className="text-[10px] font-bold text-red-500/50">#{idx + 1}</span>
                  </div>
                ))}
              </div>
              <button onClick={() => setSelectedDetail(null)} className="w-full mt-8 bg-red-600 text-white font-bold py-4 rounded-2xl hover:bg-red-500 transition-all active:scale-95">Close</button>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 flex flex-col gap-6">
          {/* Strategy Insights */}
          <motion.div className={`p-8 rounded-[2.5rem] border relative overflow-hidden backdrop-blur-sm group transition-colors duration-300 ${cardBg}`}>
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/5 blur-3xl" />
            <h3 className={`uppercase text-[10px] font-bold tracking-[0.2em] mb-6 ${headingText}`}>Strategy Insights</h3>
            <div className="space-y-6">
              <div>
                <h4 className={`text-lg font-bold mb-2 flex items-center gap-2 ${mainText}`}><span className="w-2 h-2 rounded-full bg-red-600" /> Study Advice</h4>
                <p className={`leading-relaxed ${subText}`}>{study_advice}</p>
              </div>
              <div>
                <h4 className={`text-lg font-bold mb-2 flex items-center gap-2 ${mainText}`}><span className="w-2 h-2 rounded-full bg-red-900" /> Practice Strategy</h4>
                <p className={`leading-relaxed ${subText}`}>{practice_strategy}</p>
              </div>
            </div>
          </motion.div>

          {/* Difficulty Grid */}
          <div className="grid grid-cols-3 gap-4">
            {Object.entries(difficulty_distribution).map(([label, value]) => (
              <div key={label} className={`p-6 rounded-[2rem] border transition-colors duration-300 ${cardBg}`}>
                <div className="flex items-center justify-between mb-3 text-[10px] font-bold uppercase tracking-widest">
                   <span className={headingText}>{label}</span>
                   <span className={mainText}>{value}%</span>
                </div>
                <div className="h-1.5 w-full bg-neutral-500/10 rounded-full overflow-hidden">
                   <motion.div animate={{ width: `${value}%` }} className={`h-full ${label === 'hard' ? 'bg-red-600' : label === 'medium' ? 'bg-amber-500' : 'bg-emerald-500'}`} />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Chapters Panel */}
        <div className={`p-8 rounded-[2.5rem] border flex flex-col gap-6 shadow-xl transition-colors duration-300 ${cardBg}`}>
          <h3 className={`uppercase text-[10px] font-bold tracking-[0.2em] mb-2 ${headingText}`}>{focus_label}</h3>
          <div className="space-y-3">
            {focus_areas.map(item => (
              <button key={item} onClick={() => setSelectedDetail(item)} className={`w-full text-left p-4 rounded-2xl border transition-all flex items-center justify-between group ${itemBg}`}>
                <span className={`text-sm font-medium transition-colors ${isDark ? 'text-neutral-300 group-hover:text-red-400' : 'text-neutral-700 group-hover:text-red-600'}`}>{item}</span>
                <svg className={`w-4 h-4 transition-colors ${isDark ? 'text-neutral-600 group-hover:text-red-500' : 'text-neutral-300 group-hover:text-red-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            ))}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
