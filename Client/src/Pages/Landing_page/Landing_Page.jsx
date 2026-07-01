import React from 'react';
import Navbar from '../../Components/layouts/Navbar';
import FeaturesSection from './Feature_section';
import HeroSection from './Hero_section';


export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] selection:bg-[var(--accent)] selection:text-white">
      {/* Assuming you have a Navbar component. If not, comment this out for now */}
      <Navbar isPublic /> 
      
      <main>
        <HeroSection />
        <FeaturesSection />
      </main>
    </div>
  );
}