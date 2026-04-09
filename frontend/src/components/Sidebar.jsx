import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const CHAPTER_MAP = {
  9: {
    Physics: ['Motion', 'Force and Laws of Motion', 'Gravitation', 'Work Energy Power', 'Sound'],
    Chemistry: ['Matter in Our Surroundings', 'Is Matter Around Us Pure', 'Atoms and Molecules', 'Structure of Atom'],
    Maths: ['Number Systems', 'Polynomials', 'Linear Equations in Two Variables', 'Triangles', 'Statistics'],
    Biology: ['Cell - Basic Unit of Life', 'Tissues', 'Diversity in Living Organisms', 'Why Do We Fall Ill', 'Natural Resources']
  },
  10: {
    Physics: ['Light Reflection and Refraction', 'Human Eye and Colourful World', 'Electricity', 'Magnetic Effects of Current', 'Sources of Energy'],
    Chemistry: ['Chemical Reactions and Equations', 'Acids Bases and Salts', 'Metals and Non-metals', 'Carbon and Its Compounds', 'Periodic Classification'],
    Maths: ['Real Numbers', 'Polynomials', 'Quadratic Equations', 'Arithmetic Progressions', 'Coordinate Geometry', 'Introduction to Trigonometry', 'Surface Areas and Volumes', 'Statistics'],
    Biology: ['Life Processes', 'Control and Coordination', 'Reproduction', 'Heredity and Evolution', 'Our Environment']
  },
  11: {
    Physics: ['Units and Measurement', 'Motion in a Straight Line', 'Motion in a Plane', 'Laws of Motion', 'Work Energy Power', 'Thermodynamics', 'Oscillations', 'Waves'],
    Chemistry: ['Atomic Structure', 'Chemical Bonding', 'States of Matter', 'Thermodynamics', 'Equilibrium', 'Hydrocarbons'],
    Maths: ['Sets', 'Relations and Functions', 'Trigonometric Functions', 'Complex Numbers', 'Permutations and Combinations', 'Binomial Theorem', 'Limits and Derivatives', 'Statistics'],
    Biology: ['Cell Structure and Function', 'Cell Division', 'Photosynthesis', 'Respiration in Plants', 'Plant Growth', 'Neural Control', 'Chemical Coordination']
  },
  12: {
    Physics: ['Electrostatics', 'Current Electricity', 'Magnetic Effects of Current', 'Electromagnetic Induction', 'Alternating Current', 'Optics', 'Dual Nature of Matter', 'Atoms and Nuclei', 'Semiconductor Electronics'],
    Chemistry: ['Solutions', 'Electrochemistry', 'Chemical Kinetics', 'd and f Block Elements', 'Coordination Compounds', 'Haloalkanes and Haloarenes', 'Alcohols Phenols Ethers', 'Aldehydes Ketones Acids'],
    Maths: ['Relations and Functions', 'Inverse Trigonometry', 'Matrices', 'Determinants', 'Continuity and Differentiability', 'Applications of Derivatives', 'Integrals', 'Differential Equations', 'Vector Algebra', 'Probability'],
    Biology: ['Sexual Reproduction in Plants', 'Human Reproduction', 'Reproductive Health', 'Principles of Inheritance', 'Molecular Basis of Inheritance', 'Evolution', 'Human Health and Disease', 'Biotechnology', 'Ecosystem']
  }
};

const MOTIVATIONAL_QUOTES = [
  { text: "Success is the sum of small efforts, repeated day in and day out.", author: "Robert Collier" },
  { text: "The expert in anything was once a beginner.", author: "Helen Hayes" },
  { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
  { text: "Don't watch the clock; do what it does. Keep going.", author: "Sam Levenson" },
  { text: "The beautiful thing about learning is that no one can take it away from you.", author: "B.B. King" },
  { text: "It always seems impossible until it's done.", author: "Nelson Mandela" },
  { text: "Study hard, for the well is deep, and our brains are shallow.", author: "Richard Baxter" },
  { text: "Push yourself, because no one else is going to do it for you.", author: "Anonymous" },
  { text: "Great things come from hard work and perseverance. No excuses.", author: "Kobe Bryant" },
  { text: "Education is not preparation for life; education is life itself.", author: "John Dewey" },
  { text: "The secret of getting ahead is getting started.", author: "Mark Twain" },
  { text: "Your only limit is your mind.", author: "Anonymous" },
  { text: "Hardships often prepare ordinary people for an extraordinary destiny.", author: "C.S. Lewis" },
  { text: "You don't have to be great to start, but you have to start to be great.", author: "Zig Ziglar" },
  { text: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" },
  { text: "Strive for progress, not perfection.", author: "Anonymous" },
  { text: "The more that you read, the more things you will know.", author: "Dr. Seuss" },
  { text: "Learning never exhausts the mind.", author: "Leonardo da Vinci" },
  { text: "An investment in knowledge pays the best interest.", author: "Benjamin Franklin" },
  { text: "Work hard in silence. Let success make the noise.", author: "Frank Ocean" },
];

export default function Sidebar({ userClass, setUserClass, userSubject, setUserSubject, userChapter, setUserChapter, isDark, toggleTheme }) {
  const currentChapters = CHAPTER_MAP[userClass]?.[userSubject] || [];

  const [quoteIdx, setQuoteIdx] = useState(() => Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length));
  const [quoteVisible, setQuoteVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setQuoteVisible(false);
      setTimeout(() => {
        setQuoteIdx(prev => {
          let next;
          do { next = Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length); } while (next === prev);
          return next;
        });
        setQuoteVisible(true);
      }, 400);
    }, 12000);
    return () => clearInterval(interval);
  }, []);

  const quote = MOTIVATIONAL_QUOTES[quoteIdx];

  // Theme-aware class helpers (NOW RED/BLACK)
  const sidebarBg   = isDark ? 'bg-[#0d0d0e]/95 border-neutral-800' : 'bg-white border-neutral-200';
  const labelColor  = isDark ? 'text-neutral-500' : 'text-neutral-400';
  const inputBg     = isDark ? 'bg-[#141416] border-white/5 text-neutral-200' : 'bg-neutral-50 border-neutral-200 text-neutral-800';
  const btnActive   = isDark ? 'bg-red-500/20 text-red-400 border-red-500/30' : 'bg-red-50 text-red-600 border-red-200';
  const btnInactive = isDark ? 'bg-white/5 text-neutral-500 border-transparent hover:bg-white/10' : 'bg-neutral-100 text-neutral-500 border-transparent hover:bg-neutral-200';
  const bottomCard  = isDark ? 'from-neutral-900 to-black border-neutral-800' : 'from-white to-neutral-50 border-neutral-200';
  const bottomText  = isDark ? 'text-neutral-400' : 'text-neutral-500';
  const quoteCard   = isDark ? 'from-red-900/20 via-red-950/20 to-transparent border-red-900/30' : 'from-red-50 via-red-100/30 to-transparent border-red-200';
  const quoteText   = isDark ? 'text-neutral-200' : 'text-neutral-700';
  const quoteAuthor = isDark ? 'text-neutral-500' : 'text-neutral-400';

  return (
    <motion.aside
      initial={{ x: -30, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className={`hidden md:flex flex-col w-64 border-r backdrop-blur-xl h-full p-4 space-y-6 shrink-0 transition-colors duration-300 ${sidebarBg}`}
    >
      {/* Logo + Theme Toggle */}
      <div className="flex items-center justify-between px-2 mt-2">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-red-600 to-black flex items-center justify-center shadow-[0_0_15px_rgba(220,38,38,0.4)]">
            <span className="text-white font-bold text-sm leading-none">E</span>
          </div>
          <h1 className={`font-semibold tracking-wide text-lg ${isDark ? 'text-neutral-100' : 'text-neutral-800'}`}>Examforge</h1>
        </div>

        {/* Light / Dark Toggle */}
        <motion.button
          onClick={toggleTheme}
          whileTap={{ scale: 0.9 }}
          title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
          className={`w-8 h-8 rounded-lg flex items-center justify-center transition-all ${
            isDark
              ? 'bg-white/5 hover:bg-white/10 text-neutral-400 hover:text-red-500'
              : 'bg-neutral-100 hover:bg-neutral-200 text-neutral-500 hover:text-red-600'
          }`}
        >
          <AnimatePresence mode="wait" initial={false}>
            {isDark ? (
              <motion.svg
                key="sun"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707M17.657 17.657l-.707-.707M6.343 6.343l-.707-.707M12 8a4 4 0 100 8 4 4 0 000-8z" />
              </motion.svg>
            ) : (
              <motion.svg
                key="moon"
                initial={{ rotate: 90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: -90, opacity: 0 }}
                transition={{ duration: 0.2 }}
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
              </motion.svg>
            )}
          </AnimatePresence>
        </motion.button>
      </div>

      {/* Motivational Quote Card */}
      <div className="px-2">
        <div className={`relative bg-gradient-to-br border rounded-2xl p-4 overflow-hidden transition-colors duration-300 ${quoteCard}`}>
          <div className="absolute top-0 right-0 w-16 h-16 bg-red-600/15 blur-2xl rounded-full -mr-4 -mt-4 pointer-events-none" />

          <div className="flex items-center gap-1.5 mb-3">
            <span className="text-red-500 text-[9px] font-bold uppercase tracking-[0.2em]">Daily Spark</span>
            <span className="text-red-500/40 text-[10px]">✦</span>
          </div>

          <AnimatePresence mode="wait">
            {quoteVisible && (
              <motion.div
                key={quoteIdx}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -6 }}
                transition={{ duration: 0.35, ease: "easeOut" }}
              >
                <p className={`text-[12px] leading-relaxed font-medium italic mb-2 relative ${quoteText}`}>
                  <span className="text-red-500 text-lg leading-none font-serif absolute -top-1 -left-0.5">"</span>
                  <span className="pl-3">{quote.text}</span>
                  <span className="text-red-500 text-lg leading-none font-serif">"</span>
                </p>
                <p className={`text-[10px] font-semibold tracking-wide ${quoteAuthor}`}>— {quote.author}</p>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="flex gap-1 mt-3">
            {[0, 1, 2].map(i => (
              <div key={i} className={`h-0.5 rounded-full transition-all duration-300 ${i === 0 ? 'w-4 bg-red-600' : 'w-1.5 bg-red-500/10'}`} />
            ))}
          </div>
        </div>
      </div>

      {/* Controls */}
      <nav className="flex flex-col gap-5 px-2 flex-1">
        <div>
          <label className={`text-[10px] font-bold uppercase tracking-widest mb-2 block ${labelColor}`}>Class Focus</label>
          <div className="grid grid-cols-4 gap-1.5">
            {["9", "10", "11", "12"].map(cls => (
              <button
                key={cls}
                onClick={() => setUserClass(cls)}
                className={`py-1.5 text-xs font-semibold rounded-md transition-colors border shadow-sm ${
                  userClass === cls ? btnActive : btnInactive
                }`}
              >
                {cls}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className={`text-[10px] font-bold uppercase tracking-widest mb-2 block ${labelColor}`}>Subject</label>
          <select
            value={userSubject}
            onChange={(e) => { setUserSubject(e.target.value); setUserChapter("General"); }}
            className={`w-full border rounded-lg px-3 py-2.5 text-[13px] font-medium outline-none focus:border-red-500/50 transition-colors ${inputBg}`}
          >
            <option value="Physics">Physics</option>
            <option value="Chemistry">Chemistry</option>
            <option value="Maths">Maths</option>
            <option value="Biology">Biology</option>
          </select>
        </div>

        <div>
          <label className={`text-[10px] font-bold uppercase tracking-widest mb-2 block ${labelColor}`}>Chapter / Unit</label>
          <select
            value={userChapter}
            onChange={(e) => setUserChapter(e.target.value)}
            className={`w-full border rounded-lg px-3 py-2.5 text-[13px] font-medium outline-none focus:border-red-500/50 transition-colors ${inputBg}`}
          >
            <option value="General">General / Mix</option>
            {currentChapters.map(ch => (
              <option key={ch} value={ch}>{ch}</option>
            ))}
          </select>
        </div>
      </nav>

      {/* Total Analyzed */}
      <div className="px-2 pb-2">
        <motion.div
          whileHover={{ y: -2 }}
          className={`p-4 bg-gradient-to-br border rounded-xl shadow-lg transition-colors duration-300 ${bottomCard}`}
        >
          <p className={`text-xs font-medium ${bottomText}`}>Total Analyzed</p>
          <p className={`text-xl font-semibold mt-1 ${isDark ? 'text-white' : 'text-neutral-800'}`}>
            2,240 <span className="text-xs text-red-500 font-medium tracking-wide">PYQs</span>
          </p>
        </motion.div>
      </div>
    </motion.aside>
  );
}
