import React from 'react';
import { Activity, Cpu, FileBarChart2 } from 'lucide-react';

const FeatureSection = () => {
  const features = [
    { 
      title: "Real-Time Tracking", 
      desc: "Instant sync across all devices and dashboards. Monitor attendance live as it happens.",
      icon: Activity,
      glowColor: "group-hover:shadow-[0_0_30px_rgba(0,163,255,0.15)]",
      iconColor: "text-neon-blue",
      borderColor: "group-hover:border-neon-blue/50"
    },
    { 
      title: "Hardware Agnostic", 
      desc: "Seamlessly integrates with webcams, RFID scanners, and existing biometric hardware.",
      icon: Cpu,
      glowColor: "group-hover:shadow-[0_0_30px_rgba(255,179,0,0.15)]",
      iconColor: "text-neon-orange",
      borderColor: "group-hover:border-neon-orange/50"
    },
    { 
      title: "Automated Reports", 
      desc: "Export detailed logs directly to HR and payroll systems with a single click.",
      icon: FileBarChart2,
      glowColor: "group-hover:shadow-[0_0_30px_rgba(0,240,255,0.15)]",
      iconColor: "text-neon-cyan",
      borderColor: "group-hover:border-neon-cyan/50"
    }
  ];

  return (
    <section className="py-24 px-6 max-w-7xl mx-auto relative z-10">
      
      {/* Section Header */}
      <div className="text-center mb-16">
        <h2 className="text-3xl lg:text-5xl font-black text-white tracking-tight mb-4">
          Powered by <span className="text-transparent bg-clip-text bg-gradient-to-r from-neon-blue to-neon-cyan">Intelligence</span>
        </h2>
        <p className="text-content-muted text-lg max-w-2xl mx-auto">
          Everything you need to manage workforce attendance at scale, built into one lightning-fast platform.
        </p>
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full text-left">
        {features.map((feature, idx) => {
          const Icon = feature.icon;
          return (
            <div 
              key={idx} 
              className={`p-8 bg-surface-card rounded-3xl border border-border-subtle transition-all duration-300 group hover:-translate-y-1 ${feature.glowColor} ${feature.borderColor}`}
            >
              {/* Icon Container */}
              <div className="w-12 h-12 rounded-2xl bg-surface-base flex items-center justify-center mb-6 border border-border-subtle group-hover:border-transparent transition-colors">
                <Icon size={24} className={feature.iconColor} />
              </div>
              
              <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
              <p className="text-content-muted text-base leading-relaxed font-medium">{feature.desc}</p>
            </div>
          );
        })}
      </div>
      
    </section>
  );
};

export default FeatureSection;