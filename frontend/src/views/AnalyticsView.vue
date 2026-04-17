<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Analytics</h1>
        <p class="text-gray-400 text-sm mt-0.5">Real-time triage insights</p>
      </div>
      <button @click="load" class="btn-secondary text-sm">Refresh</button>
    </div>

    <div v-if="!data" class="flex items-center justify-center h-64">
      <div class="text-center">
        <div class="w-12 h-12 rounded-full border-4 border-blue-100 border-t-blue-600 animate-spin mx-auto mb-4"></div>
        <p class="text-gray-400 text-sm">Loading analytics...</p>
      </div>
    </div>

    <template v-else>
      <!-- KPI Row -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div v-for="k in kpis" :key="k.label" class="card text-center relative overflow-hidden group hover:-translate-y-0.5 transition-transform">
          <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity" :style="{ background: k.hoverBg }"></div>
          <div class="relative">
            <p class="text-3xl font-extrabold mb-1" :style="{ color: k.color }">{{ k.value }}</p>
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">{{ k.label }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <!-- Severity Distribution -->
        <div class="card">
          <h3 class="font-bold text-gray-900 mb-5">ESI Severity Distribution</h3>
          <div class="space-y-4">
            <div v-for="(count, level) in data.severity_distribution" :key="level">
              <div class="flex justify-between items-center mb-2">
                <div class="flex items-center gap-2">
                  <div class="w-3 h-3 rounded-full" :style="{ background: severityColor(level) }"></div>
                  <span class="text-sm font-semibold text-gray-700">{{ level }}</span>
                  <span class="text-xs text-gray-400">{{ esiLabel(level) }}</span>
                </div>
                <span class="text-sm font-bold text-gray-900">{{ count }}</span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                <div class="h-2.5 rounded-full transition-all duration-700"
                  :style="{ width: `${data.total_cases ? (count/data.total_cases*100) : 0}%`, background: severityColor(level) }"></div>
              </div>
            </div>
            <p v-if="!Object.keys(data.severity_distribution).length" class="text-sm text-gray-400 text-center py-4">No data yet</p>
          </div>
        </div>

        <!-- Care Level Distribution -->
        <div class="card">
          <h3 class="font-bold text-gray-900 mb-5">Care Level Distribution</h3>
          <div class="space-y-4">
            <div v-for="(count, level) in data.care_level_distribution" :key="level">
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-medium text-gray-700">{{ level }}</span>
                <span class="text-sm font-bold text-gray-900">{{ count }}</span>
              </div>
              <div class="w-full bg-gray-100 rounded-full h-2.5 overflow-hidden">
                <div class="h-2.5 rounded-full transition-all duration-700"
                  style="background: linear-gradient(135deg, #2563eb, #0891b2);"
                  :style="{ width: `${data.total_cases ? (count/data.total_cases*100) : 0}%` }"></div>
              </div>
            </div>
            <p v-if="!Object.keys(data.care_level_distribution).length" class="text-sm text-gray-400 text-center py-4">No data yet</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Complaints -->
        <div class="card">
          <h3 class="font-bold text-gray-900 mb-5">Top Chief Complaints</h3>
          <div class="space-y-3">
            <div v-for="(item, i) in data.top_complaints.slice(0, 8)" :key="i" class="flex items-center gap-3 group">
              <span class="w-6 h-6 rounded-lg flex items-center justify-center text-xs font-bold text-white flex-shrink-0"
                :style="{ background: i < 3 ? 'linear-gradient(135deg,#2563eb,#0891b2)' : '#e5e7eb', color: i < 3 ? 'white' : '#6b7280' }">{{ i+1 }}</span>
              <div class="flex-1 min-w-0">
                <div class="flex justify-between text-sm mb-1">
                  <span class="font-medium text-gray-800 capitalize truncate">{{ item.complaint }}</span>
                  <span class="text-gray-400 ml-2 flex-shrink-0">{{ item.count }}</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                  <div class="h-1.5 rounded-full transition-all duration-500" style="background: linear-gradient(135deg, #0891b2, #8b5cf6);"
                    :style="{ width: `${data.top_complaints[0]?.count ? (item.count/data.top_complaints[0].count*100) : 0}%` }"></div>
                </div>
              </div>
            </div>
            <p v-if="!data.top_complaints.length" class="text-sm text-gray-400 text-center py-4">No data yet</p>
          </div>
        </div>

        <!-- Hourly Heatmap -->
        <div class="card">
          <h3 class="font-bold text-gray-900 mb-5">Case Volume by Hour</h3>
          <div class="flex items-end gap-1 h-28">
            <div v-for="item in data.hourly_case_volume" :key="item.hour" class="flex-1 flex flex-col items-center gap-1 group">
              <div class="w-full rounded-t-sm transition-all duration-300 cursor-pointer relative"
                :style="{ height: `${Math.max(4, (item.count / (maxHourly || 1)) * 80)}px`, background: hourGradient(item.count, maxHourly) }"
                :title="`${item.hour}:00 — ${item.count} cases`">
                <div v-if="item.count > 0" class="absolute -top-5 left-1/2 -translate-x-1/2 text-[10px] font-bold text-gray-600 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">{{ item.count }}</div>
              </div>
              <span class="text-[9px] text-gray-400">{{ item.hour % 6 === 0 ? `${item.hour}h` : '' }}</span>
            </div>
          </div>
        </div>

        <!-- Provider Utilization -->
        <div class="card lg:col-span-2">
          <h3 class="font-bold text-gray-900 mb-5">Provider Utilization</h3>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <div v-for="p in data.provider_utilization" :key="p.id" class="p-4 rounded-xl border border-gray-100 hover:border-blue-200 transition-colors">
              <p class="text-xs font-bold text-gray-700 mb-2 truncate">{{ p.specialty }}</p>
              <div class="flex items-center gap-2 mb-2">
                <div class="flex-1 bg-gray-100 rounded-full h-2 overflow-hidden">
                  <div class="h-2 rounded-full transition-all"
                    :style="{ width: `${Math.min(100, (p.current_load/p.max_cases)*100)}%`, background: p.current_load/p.max_cases > 0.8 ? 'linear-gradient(90deg,#dc2626,#f97316)' : 'linear-gradient(90deg,#16a34a,#0891b2)' }"></div>
                </div>
              </div>
              <p class="text-xs text-gray-400">{{ p.current_load }}/{{ p.max_cases }} cases</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCasesStore } from '@/stores/cases'

const casesStore = useCasesStore()
const data = computed(() => casesStore.analytics)

const maxHourly = computed(() => Math.max(...(data.value?.hourly_case_volume?.map(h => h.count) || [1]), 1))

const kpis = computed(() => [
  { label: 'Total Cases', value: data.value?.total_cases || 0, color: '#1d4ed8', hoverBg: 'rgba(29,78,216,0.03)' },
  { label: 'Completed', value: data.value?.completed_cases || 0, color: '#059669', hoverBg: 'rgba(5,150,105,0.03)' },
  { label: 'Emergencies', value: data.value?.emergency_cases || 0, color: '#dc2626', hoverBg: 'rgba(220,38,38,0.03)' },
  { label: 'Accuracy', value: `${data.value?.triage_accuracy_rate || 0}%`, color: '#7c3aed', hoverBg: 'rgba(124,58,237,0.03)' },
])

function severityColor(level) {
  return { 'ESI-1': '#dc2626', 'ESI-2': '#d97706', 'ESI-3': '#ca8a04', 'ESI-4': '#16a34a', 'ESI-5': '#2563eb' }[level] || '#6b7280'
}
function esiLabel(level) {
  return { 'ESI-1': 'Resuscitation', 'ESI-2': 'Emergent', 'ESI-3': 'Urgent', 'ESI-4': 'Less Urgent', 'ESI-5': 'Non-Urgent' }[level] || ''
}
function hourGradient(count, max) {
  const ratio = count / max
  if (ratio > 0.7) return 'linear-gradient(180deg, #ef4444, #f97316)'
  if (ratio > 0.4) return 'linear-gradient(180deg, #f59e0b, #fbbf24)'
  if (ratio > 0.1) return 'linear-gradient(180deg, #2563eb, #0891b2)'
  return '#e5e7eb'
}

async function load() { await casesStore.fetchAnalytics() }
onMounted(load)
</script>
