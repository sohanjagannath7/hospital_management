<template>
  <div class="space-y-5">
    <!-- Emergency Banner -->
    <div v-if="result.is_emergency"
      class="relative overflow-hidden rounded-2xl p-5 flex items-center gap-4"
      style="background: linear-gradient(135deg, #7f1d1d, #dc2626); box-shadow: 0 8px 30px rgba(220,38,38,0.4);">
      <div class="absolute inset-0 opacity-10" style="background: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,.1) 10px, rgba(255,255,255,.1) 20px);"></div>
      <span class="text-4xl relative z-10">🚨</span>
      <div class="relative z-10">
        <p class="font-black text-white text-lg">EMERGENCY — Immediate Care Required</p>
        <p class="text-red-200 text-sm mt-0.5">Call 911 or go to the nearest Emergency Room immediately.</p>
      </div>
    </div>

    <!-- Result Header Card -->
    <div class="card overflow-hidden relative">
      <div class="absolute top-0 left-0 right-0 h-1" :style="{ background: severityGradient(result.severity) }"></div>
      <div class="flex items-start justify-between gap-4 pt-2">
        <div class="flex-1">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Case {{ result.case_number }}</p>
          <h2 class="text-xl font-bold text-gray-900">{{ result.chief_complaint }}</h2>
          <p v-if="result.assessment?.clinical_summary" class="text-sm text-gray-500 mt-1">{{ result.assessment?.clinical_summary }}</p>
        </div>
        <SeverityBadge :severity="result.severity" size="lg" />
      </div>

      <div class="grid grid-cols-3 gap-3 mt-5">
        <div class="rounded-xl p-3 text-center" style="background: rgba(37,99,235,0.06); border: 1px solid rgba(37,99,235,0.12);">
          <p class="text-[10px] font-bold text-blue-500 uppercase tracking-wide mb-1">Care Level</p>
          <p class="text-sm font-bold text-blue-800">{{ result.care_level || 'Urgent Care' }}</p>
        </div>
        <div class="rounded-xl p-3 text-center" style="background: rgba(124,58,237,0.06); border: 1px solid rgba(124,58,237,0.12);">
          <p class="text-[10px] font-bold text-purple-500 uppercase tracking-wide mb-1">AI Confidence</p>
          <p class="text-sm font-bold text-purple-800">{{ Math.round((result.assessment?.confidence_score || 0.8) * 100) }}%</p>
        </div>
        <div class="rounded-xl p-3 text-center" style="background: rgba(5,150,105,0.06); border: 1px solid rgba(5,150,105,0.12);">
          <p class="text-[10px] font-bold text-emerald-600 uppercase tracking-wide mb-1">Status</p>
          <p class="text-sm font-bold text-emerald-800 capitalize">{{ result.status }}</p>
        </div>
      </div>
    </div>

    <!-- Assessment -->
    <div class="card" v-if="result.assessment">
      <h3 class="font-bold text-gray-900 mb-4 flex items-center gap-2">
        <span class="w-6 h-6 rounded-lg bg-blue-100 flex items-center justify-center text-sm">🧠</span>
        AI Clinical Assessment
      </h3>

      <div v-if="result.assessment.possible_conditions?.length" class="mb-4">
        <p class="section-label mb-2">Possible Conditions</p>
        <div class="flex flex-wrap gap-2">
          <span v-for="(c, i) in result.assessment.possible_conditions.slice(0, 5)" :key="i"
            class="px-3 py-1.5 rounded-xl text-sm font-medium"
            :style="i === 0 ? 'background: rgba(37,99,235,0.1); color: #1d4ed8; border: 1px solid rgba(37,99,235,0.2);' : 'background: #f3f4f6; color: #374151;'">
            {{ c }}
          </span>
        </div>
      </div>

      <div v-if="result.assessment.risk_factors?.length" class="mb-4">
        <p class="section-label mb-2">Risk Factors</p>
        <div class="grid grid-cols-1 gap-1">
          <div v-for="r in result.assessment.risk_factors" :key="r" class="flex items-center gap-2 text-sm text-gray-700">
            <svg class="w-4 h-4 text-amber-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
            {{ r }}
          </div>
        </div>
      </div>

      <div v-if="result.assessment.severity_reasoning" class="p-4 rounded-xl text-sm text-gray-700 leading-relaxed" style="background: #f8fafc; border: 1px solid #e2e8f0;">
        <p class="section-label mb-1.5">Severity Reasoning</p>
        {{ result.assessment.severity_reasoning }}
      </div>

      <!-- Drug Interactions -->
      <div v-if="result.assessment.drug_interactions?.length" class="mt-4 rounded-xl p-4" style="background: rgba(234,88,12,0.05); border: 1px solid rgba(234,88,12,0.2);">
        <p class="font-bold text-orange-800 flex items-center gap-2 mb-3">
          <span>⚗️</span> Drug Interaction Alert
        </p>
        <div v-for="(item, i) in result.assessment.drug_interactions" :key="i" class="flex items-start gap-2 text-sm">
          <span class="px-2 py-0.5 rounded-full text-xs font-bold text-white capitalize flex-shrink-0"
            :style="item.severity === 'contraindicated' ? 'background:#dc2626' : item.severity === 'major' ? 'background:#ea580c' : 'background:#d97706'">
            {{ item.severity }}
          </span>
          <p class="text-orange-900">{{ item.description }}</p>
        </div>
      </div>
    </div>

    <!-- Recommendations -->
    <div class="card" v-if="result.recommendations?.length">
      <h3 class="font-bold text-gray-900 mb-4 flex items-center gap-2">
        <span class="w-6 h-6 rounded-lg bg-emerald-100 flex items-center justify-center text-sm">📋</span>
        Recommended Actions
      </h3>
      <div class="space-y-3">
        <div v-for="rec in result.recommendations" :key="rec.id"
          class="flex items-start gap-3 p-4 rounded-xl border transition-all hover:-translate-y-0.5"
          :class="recBg(rec.priority)">
          <span class="text-xl mt-0.5 flex-shrink-0">{{ recIcon(rec.recommendation_type) }}</span>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <p class="font-semibold text-gray-900 text-sm">{{ rec.title }}</p>
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide" :class="priorityBadge(rec.priority)">{{ rec.priority }}</span>
            </div>
            <p class="text-gray-600 text-sm mt-0.5">{{ rec.description }}</p>
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-3">
      <button @click="$emit('new-triage')" class="btn-secondary flex-1">New Assessment</button>
      <router-link to="/patient/cases" class="btn-primary flex-1 text-center">View My Cases</router-link>
    </div>
  </div>
</template>

<script setup>
import SeverityBadge from './SeverityBadge.vue'
defineProps({ result: Object })
defineEmits(['new-triage'])

function severityGradient(s) {
  return { 'ESI-1': 'linear-gradient(90deg,#dc2626,#ef4444)', 'ESI-2': 'linear-gradient(90deg,#d97706,#f97316)', 'ESI-3': 'linear-gradient(90deg,#b45309,#f59e0b)', 'ESI-4': 'linear-gradient(90deg,#15803d,#22c55e)', 'ESI-5': 'linear-gradient(90deg,#1d4ed8,#60a5fa)' }[s] || '#e5e7eb'
}
function recBg(p) { return { urgent: 'border-red-200 bg-red-50 hover:border-red-300', high: 'border-orange-200 bg-orange-50 hover:border-orange-300', medium: 'border-amber-200 bg-amber-50', low: 'border-gray-100 bg-gray-50' }[p] || 'border-gray-100' }
function priorityBadge(p) { return { urgent: 'bg-red-100 text-red-700', high: 'bg-orange-100 text-orange-700', medium: 'bg-amber-100 text-amber-700', low: 'bg-gray-100 text-gray-600' }[p] || 'bg-gray-100 text-gray-600' }
function recIcon(t) { return { diagnostic_test: '🔬', consultation: '👨‍⚕️', medication: '💊', self_care: '🏠', monitoring: '📊', follow_up: '📅' }[t] || '📋' }
</script>
