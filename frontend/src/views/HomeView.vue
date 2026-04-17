<template>
  <div class="min-h-screen overflow-hidden" style="background: #020818;">
    <!-- Animated background orbs -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-[-20%] left-[-10%] w-96 h-96 rounded-full opacity-20 blur-3xl" style="background: radial-gradient(circle, #3b82f6, transparent)"></div>
      <div class="absolute top-[30%] right-[-5%] w-80 h-80 rounded-full opacity-15 blur-3xl" style="background: radial-gradient(circle, #0891b2, transparent)"></div>
      <div class="absolute bottom-[10%] left-[30%] w-64 h-64 rounded-full opacity-10 blur-3xl" style="background: radial-gradient(circle, #8b5cf6, transparent)"></div>
    </div>

    <!-- Navbar -->
    <nav class="relative z-10 flex items-center justify-between px-8 py-6 max-w-7xl mx-auto">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg, #3b82f6, #0891b2);">
          <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/><path d="M11 6h2v2h-2zm-4 6h2v2H7zm8 0h2v2h-2z" fill="none"/></svg>
        </div>
        <span class="text-white font-bold text-xl tracking-tight">Health<span style="background: linear-gradient(135deg, #60a5fa, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Triage</span> AI</span>
      </div>
      <div class="flex items-center gap-3">
        <router-link to="/login" class="px-5 py-2.5 text-blue-200 hover:text-white border border-white/10 hover:border-white/30 rounded-xl text-sm font-medium transition-all duration-200">
          Sign In
        </router-link>
        <router-link to="/register" class="px-5 py-2.5 text-sm font-semibold text-white rounded-xl transition-all duration-200" style="background: linear-gradient(135deg, #3b82f6, #0891b2); box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);">
          Get Started Free
        </router-link>
      </div>
    </nav>

    <!-- Hero -->
    <section class="relative z-10 max-w-6xl mx-auto px-8 pt-16 pb-24 text-center">
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-blue-500/30 bg-blue-500/10 mb-8">
        <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse"></span>
        <span class="text-blue-200 text-sm font-medium">Powered by Gemini AI · Real-time Triage</span>
      </div>

      <h1 class="text-6xl font-extrabold text-white leading-tight mb-6 tracking-tight">
        AI That Triages<br/>
        <span style="background: linear-gradient(135deg, #60a5fa 0%, #22d3ee 50%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Every Patient Instantly</span>
      </h1>
      <p class="text-xl text-blue-200/80 max-w-2xl mx-auto mb-10 leading-relaxed">
        Five specialized AI agents analyze symptoms, score severity with ESI protocol, check drug interactions, and route patients to the right care — all in seconds.
      </p>

      <div class="flex items-center justify-center gap-4">
        <router-link to="/register" class="inline-flex items-center gap-2 px-8 py-4 text-white font-bold text-lg rounded-2xl transition-all duration-200" style="background: linear-gradient(135deg, #3b82f6, #0891b2); box-shadow: 0 8px 30px rgba(59,130,246,0.4);">
          Start Triage Now
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
        </router-link>
        <router-link to="/login" class="inline-flex items-center gap-2 px-8 py-4 text-white font-semibold text-lg rounded-2xl border border-white/15 hover:bg-white/10 transition-all duration-200">
          Provider Login
        </router-link>
      </div>

      <!-- Stats row -->
      <div class="flex items-center justify-center gap-12 mt-16">
        <div v-for="s in stats" :key="s.label" class="text-center">
          <p class="text-3xl font-extrabold text-white">{{ s.value }}</p>
          <p class="text-blue-300/70 text-sm mt-1">{{ s.label }}</p>
        </div>
      </div>
    </section>

    <!-- Feature Cards -->
    <section class="relative z-10 max-w-6xl mx-auto px-8 pb-24">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        <div v-for="f in features" :key="f.title"
          class="group relative rounded-2xl p-6 cursor-default transition-all duration-300 hover:-translate-y-1"
          style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);"
          :style="{ '--hover-glow': f.glow }">
          <!-- Gradient icon -->
          <div class="w-12 h-12 rounded-xl flex items-center justify-center mb-4 text-2xl" :style="{ background: f.gradient }">
            {{ f.icon }}
          </div>
          <h3 class="text-white font-bold text-lg mb-2">{{ f.title }}</h3>
          <p class="text-blue-200/60 text-sm leading-relaxed">{{ f.desc }}</p>

          <!-- Hover border glow -->
          <div class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
            :style="{ boxShadow: `inset 0 0 0 1px ${f.glow}` }"></div>
        </div>
      </div>
    </section>

    <!-- Bottom CTA -->
    <section class="relative z-10 max-w-3xl mx-auto px-8 pb-24 text-center">
      <div class="rounded-3xl p-10" style="background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(8,145,178,0.15)); border: 1px solid rgba(59,130,246,0.25);">
        <h2 class="text-3xl font-bold text-white mb-3">Ready to transform patient care?</h2>
        <p class="text-blue-200/70 mb-6">Join healthcare providers using AI-powered triage today.</p>
        <router-link to="/register" class="inline-flex items-center gap-2 px-8 py-4 text-white font-bold rounded-2xl" style="background: linear-gradient(135deg, #3b82f6, #0891b2); box-shadow: 0 8px 30px rgba(59,130,246,0.4);">
          Create Free Account →
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
const stats = [
  { value: '< 3s', label: 'Avg. Triage Time' },
  { value: '5', label: 'AI Agents' },
  { value: 'ESI 1–5', label: 'Severity Scoring' },
  { value: '99.9%', label: 'Uptime' },
]

const features = [
  { icon: '🧠', title: 'Multi-Agent AI Triage', desc: 'Five specialized agents work in parallel: symptom analysis, ESI scoring, routing, recommendations, and drug interaction checking.', gradient: 'linear-gradient(135deg, #3b82f6, #8b5cf6)', glow: 'rgba(139,92,246,0.5)' },
  { icon: '🚨', title: 'Emergency Detection', desc: 'Instantly identifies ESI-1 and ESI-2 emergencies with real-time alerts and immediate routing to emergency services.', gradient: 'linear-gradient(135deg, #ef4444, #f97316)', glow: 'rgba(239,68,68,0.5)' },
  { icon: '💊', title: 'Drug Interaction Checker', desc: 'Analyzes current medications against presenting conditions to flag dangerous interactions before treatment starts.', gradient: 'linear-gradient(135deg, #f59e0b, #10b981)', glow: 'rgba(245,158,11,0.5)' },
  { icon: '📊', title: 'Real-time Analytics', desc: 'Live dashboard with severity distribution, hourly volume heatmap, provider utilization, and triage accuracy metrics.', gradient: 'linear-gradient(135deg, #06b6d4, #3b82f6)', glow: 'rgba(6,182,212,0.5)' },
  { icon: '💬', title: 'MedAssist AI Chat', desc: 'Conversational AI guides patients through symptom assessment in natural language before formal triage submission.', gradient: 'linear-gradient(135deg, #10b981, #06b6d4)', glow: 'rgba(16,185,129,0.5)' },
  { icon: '🏥', title: 'Smart Care Routing', desc: 'Routes patients to Emergency Room, Urgent Care, Primary Care, Telehealth, or Specialist based on clinical presentation.', gradient: 'linear-gradient(135deg, #8b5cf6, #ec4899)', glow: 'rgba(236,72,153,0.5)' },
]
</script>
