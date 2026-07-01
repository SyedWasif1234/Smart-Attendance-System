import React from 'react';
import { ShieldCheck, Zap } from 'lucide-react';

const HeroSection = ({ onLogin }) => {
  return (
    // Removed bounding padding and max-width to allow full-bleed display
    <section className="relative w-full min-h-screen overflow-hidden bg-surface-card">
      
      {/* Ambient Background Glow */}
      <div className="absolute top-1/2 left-0 -translate-y-1/2 w-[500px] h-[500px] bg-neon-blue/10 rounded-full blur-[120px] pointer-events-none z-10"></div>

      {/* Decorative neon glow behind the image edges */}
      <div className="absolute inset-0 bg-gradient-to-tr from-neon-blue to-neon-cyan opacity-20 blur-sm pointer-events-none"></div>
        
      {/* Full Hero Image Container */}
      <div className="absolute inset-0 w-full h-full">
        <img 
          src="/landing_page.png" 
          alt="Smart Attendance Dashboard Preview" 
          // object-cover ensures the image fills the area without distortion
          className="w-full h-full object-cover opacity-90 hover:opacity-100 transition-opacity duration-300"
        />
      </div>

      {/* Optional: Dark overlay overlayed text grid can go here if needed */}
      
    </section>
  );
}

export default HeroSection;
