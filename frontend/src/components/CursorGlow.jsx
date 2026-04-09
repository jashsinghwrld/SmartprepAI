import { useEffect, useRef } from 'react';

// "The Blood Dragon" - Red/Black themed with a larger, more imposing head
export default function DragonBody() {
  const canvasRef = useRef(null);
  const mouse = useRef({ x: 0, y: 0 });
  const points = useRef([]);
  const rafRef = useRef(null);

  const SEGMENTS = 25; 
  const GAP = 14;      

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    // Initial positioning
    const startX = window.innerWidth / 2;
    const startY = window.innerHeight / 2;
    for (let i = 0; i < SEGMENTS; i++) {
        points.current.push({ x: startX, y: startY });
    }

    const onMove = (e) => {
      mouse.current = { x: e.clientX, y: e.clientY };
    };
    window.addEventListener('mousemove', onMove);

    function draw(time) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Follow logic
      let head = points.current[0];
      head.x += (mouse.current.x - head.x) * 0.25;
      head.y += (mouse.current.y - head.y) * 0.25;

      for (let i = 1; i < SEGMENTS; i++) {
        const p = points.current[i];
        const prev = points.current[i - 1];
        const dx = prev.x - p.x;
        const dy = prev.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        
        if (dist > GAP) {
          const angle = Math.atan2(dy, dx);
          p.x = prev.x - Math.cos(angle) * GAP;
          p.y = prev.y - Math.sin(angle) * GAP;
        }
      }

      ctx.globalAlpha = 0.55; 
      ctx.lineJoin = 'round';
      ctx.lineCap = 'round';

      // 1. Draw the "Spikes" (Dorsal Fins) - Black/Red mix
      for (let i = 1; i < SEGMENTS - 5; i++) {
        const p = points.current[i];
        
        // Match the body wiggle
        const wiggleAmp = (i / SEGMENTS) * 15; 
        const frequency = 0.008;
        const wave = Math.sin(time * frequency + i * 0.4) * wiggleAmp;
        const px = p.x + wave;
        const py = p.y + wave;

        const next = points.current[i+1] || p;
        const nextWave = Math.sin(time * frequency + (i+1) * 0.4) * ((i+1) / SEGMENTS * 15);
        const npx = next.x + nextWave;
        const npy = next.y + nextWave;

        const angle = Math.atan2(npy - py, npx - px) + Math.PI / 2;
        
        const spikeSize = Math.max(0, (1 - i / SEGMENTS) * 14);
        const dynamicSpike = Math.sin(time * 0.008 + i * 0.5) * 4;

        ctx.beginPath();
        ctx.moveTo(px, py);
        ctx.lineTo(
          px + Math.cos(angle) * (spikeSize + dynamicSpike),
          py + Math.sin(angle) * (spikeSize + dynamicSpike)
        );
        ctx.strokeStyle = i % 2 === 0 ? `rgba(220, 38, 38, 0.9)` : `rgba(0, 0, 0, 0.8)`;
        ctx.lineWidth = 2.5;
        ctx.stroke();
      }

      // 2. Draw the Main Body (Tapered) - Deep Red to Black
      ctx.beginPath();
      ctx.moveTo(points.current[0].x, points.current[0].y);
      for (let i = 1; i < SEGMENTS - 1; i++) {
        const p = points.current[i];
        
        // Constant tail wiggle logic
        // Increased amplitude and frequency towards the tail
        const wiggleAmp = (i / SEGMENTS) * 15; // Increased from 8
        const frequency = 0.008;               // Increased from 0.005
        const wave = Math.sin(time * frequency + i * 0.4) * wiggleAmp;
        
        const px = p.x + wave;
        const py = p.y + wave;

        const next = points.current[i+1];
        const nextWave = Math.sin(time * frequency + (i+1) * 0.4) * ((i+1) / SEGMENTS * 15);
        const npx = next.x + nextWave;
        const npy = next.y + nextWave;

        const xc = (px + npx) / 2;
        const yc = (py + npy) / 2;
        
        const width = Math.max(3, (1 - i / SEGMENTS) * 14);
        ctx.lineWidth = width;
        
        const ratio = i / SEGMENTS;
        const redVal = Math.floor(220 * (1 - ratio));
        ctx.strokeStyle = `rgba(${redVal}, 38, 38, ${0.7 * (1 - ratio)})`;
        
        ctx.quadraticCurveTo(px, py, xc, yc);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(xc, yc);
      }

      // 3. Draw the Head (Skull / Diamond Shape) - BIGGER
      const h = points.current[0];
      const prevH = points.current[1];
      const hAngle = Math.atan2(h.y - prevH.y, h.x - prevH.x);
      
      ctx.save();
      ctx.translate(h.x, h.y);
      ctx.rotate(hAngle);
      
      // Draw a "Shield" head (Increased size from 8/4 to 14/8)
      ctx.beginPath();
      ctx.moveTo(14, 0); // Nose
      ctx.lineTo(0, 8);  // Right jaw
      ctx.lineTo(-6, 0); // Back
      ctx.lineTo(0, -8); // Left jaw
      ctx.closePath();
      ctx.fillStyle = '#111'; // Matte Black Head
      ctx.strokeStyle = '#b91c1c'; // Red trim
      ctx.lineWidth = 1;
      ctx.fill();
      ctx.stroke();
      
      // Eyes (Glowing Red)
      ctx.fillStyle = '#ef4444';
      ctx.shadowBlur = 5;
      ctx.shadowColor = '#ef4444';
      ctx.beginPath();
      ctx.arc(4, 3, 2, 0, Math.PI * 2);
      ctx.arc(4, -3, 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.shadowBlur = 0;

      // Horns - Large & Red
      ctx.strokeStyle = '#b91c1c';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(-2, -4); ctx.lineTo(-12, -10);
      ctx.moveTo(-2, 4); ctx.lineTo(-12, 10);
      ctx.stroke();
      
      ctx.restore();

      rafRef.current = requestAnimationFrame(draw);
    }

    rafRef.current = requestAnimationFrame(draw);

    return () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 9999 }}
    />
  );
}
