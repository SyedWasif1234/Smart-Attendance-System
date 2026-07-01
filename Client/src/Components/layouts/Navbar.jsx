import React from 'react';
import { Fingerprint } from 'lucide-react';

const Navbar = ({ onLogin }) => {
  return (
    <header className="h-20 flex items-center justify-between px-8 lg:px-16 bg-surface-card border-b border-border-subtle w-full z-50 sticky top-0 bg-blue-300">
      
      {/* Brand Logo */}
      <div className="flex items-center text-white cursor-pointer transition-transform hover:scale-105">
        <div className="w-7 h-7 rounded-md bg-gradient-to-tr from-neon-blue to-neon-cyan mr-3 shadow-[0_0_15px_rgba(0,163,255,0.4)] flex items-center justify-center">
           <Fingerprint size={18} className="text-white" />
        </div>
        <span className="text-2xl font-bold tracking-tight">SmartAttend<span className="text-neon-blue">.</span></span>
      </div>

      {/* Action Button */}
      <button 
        onClick={onLogin}
        className="px-6 py-2.5 bg-surface-base text-content-main font-semibold rounded-xl border border-border-subtle hover:border-neon-cyan hover:text-neon-cyan hover:shadow-[0_0_15px_rgba(0,240,255,0.15)] transition-all"
      >
        Access System
      </button>
      
    </header>
  );
};

export default Navbar;