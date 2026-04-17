<template>
  <div class="p-6 ml-0">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p class="text-gray-400 text-sm mt-0.5">{{ greeting }}, <span class="font-medium text-gray-600">{{ auth.user?.full_name?.split(' ')[0] }}</span></p>
      </div>
      <button @click="refresh" class="btn-secondary text-sm">
        <svg class="w-4 h-4" :class="loading ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        Refresh
      </button>
    </div>

    <!-- Stat Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <div v-for="s in statCards" :key="s.label" class="stat-card" :style="{ background: s.gradient }">
        <div class="flex items-start justify-between">
          <div>
            <p class="text-white/70 text-xs font-semibold uppercase tracking-wide mb-1">{{ s.label }}</p>
            <p class="text-3xl font-extrabold text-white counter">{{ s.value }}</p>
            <p v-if="s.sub" class="text-white/50 text-xs mt-1">{{ s.sub }}</p>
          </div>
          <div class="text-3xl opacity-70">{{ s.icon }}</div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
      <!-- Recent Cases -->
      <div class="card lg:col-span-2">
        <div class="flex items-center justify-between mb-5">
          <h3 class="font-bold text-gray-900">Recent Cases</h3>
          <router-link to="/cases" class="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1">
            View all <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </router-link>
        </div>
        <div class="space-y-2">
          <div v-for="c in recentCases" :key="c.id"
            class="flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 transition-colors cursor-pointer group">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-xs text-white flex-shrink-0"
              :style="{ background: severityGradient(c.severity) }">
              {{ c.severity?.replace('ESI-', '') || '?' }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-semibold text-gray-900 truncate">{{ c.chief_complaint }}</p>
              <p class="text-xs text-gray-400 mt-0.5">{{ c.case_number }} · {{ formatDate(c.created_at) }}</p>
            </div>
            <div class="text-right flex-shrink-0">
              <span class="text-xs px-2.5 py-1 rounded-full font-semibold" :class="statusClass(c.status)">{{ c.status }}</span>
            </div>
          </div>
          <p v-if="!recentCases.length" class="text-center text-gray-400 text-sm py-8">No cases yet</p>
        </div>
      </div>

      <!-- Active Alerts -->
      <div class="card">
        <div class="flex items-center justify-between mb-5">
          <h3 class="font-bold text-gray-900">Active Alerts</h3>
          <span v-if="alerts.length" class="text-xs font-bold px-2 py-1 text-white rounded-full" style="background: linear-gradient(135deg, #ef4444, #f97316);">{{ alerts.length }}</span>
        </div>
        <div class="space-y-3">
          <div v-for="alert in alerts.slice(0, 4)" :key="alert.id"
            class="rounded-xl p-3 relative overflow-hidden"
            :style="alert.alert_type === 'emergency' ? 'background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.2);' : 'background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.2);'">
            <div class="flex items-start gap-2">
              <span class="text-base flex-shrink-0">{{ alert.alert_type === 'emergency' ? '🚨' : '⚠️' }}</span>
              <div class="flex-1 min-w-0">
                <p class="text-xs text-gray-700 leading-relaxed">{{ alert.message }}</p>
                <div class="flex items-center justify-between mt-1.5">
                  <p class="text-[10px] text-gray-400">{{ formatDate(alert.created_at) }}</p>
                  <button @click="casesStore.acknowledgeAlert(alert.id)" class="text-[10px] text-blue-500 font-semibold hover:text-blue-700">Dismiss</button>
                </div>
              </div>
            </div>
          </div>
          <div v-if="!alerts.length" class="text-center py-8">
            <div class="w-10 h-10 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-2">
              <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            </div>
            <p class="text-xs text-gray-400 font-medium">All clear</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Provider Status -->
    <div class="card">
      <h3 class="font-bold text-gray-900 mb-5">Provider Availability</h3>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
        <div v-for="p in casesStore.providers.slice(0, 8)" :key="p.id"
          class="flex items-center gap-3 p-3 rounded-xl border border-gray-100 hover:border-blue-200 hover:bg-blue-50/50 transition-all">
          <div class="relative">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-white text-xs font-bold">
              {{ p.user?.full_name?.split(' ').map(n=>n[0]).join('').slice(0,2) || 'DR' }}
            </div>
            <div class="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-white"
              :class="p.status === 'available' ? 'bg-emerald-400' : p.status === 'busy' ? 'bg-amber-400' : 'bg-gray-300'"></div>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-semibold text-gray-900 truncate">{{ p.user?.full_name?.split(' ').slice(-1)[0] || '—' }}</p>
            <p class="text-[10px] text-gray-400 truncate">{{ p.specialty }}</p>
          </div>
          <span class="text-xs text-gray-400 font-mono">{{ p.current_load }}/{{ p.max_cases }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCasesStore } from '@/stores/cases'
import { format } from 'date-fns'

const auth = useAuthStore()
const casesStore = useCasesStore()
const loading = ref(false)

const greeting = computed(() => {
  const h = new Date().getHours()
  return h < 12 ? 'Good morning' : h < 17 ? 'Good afternoon' : 'Good evening'
})

const analytics = computed(() => casesStore.analytics || {})
const recentCases = computed(() => casesStore.cases.slice(0, 6))
const alerts = computed(() => casesStore.alerts)

const statCards = computed(() => [
  { label: 'Total Cases', value: analytics.value.total_cases || 0, icon: '🏥', gradient: 'linear-gradient(135deg, #1e40af, #2563eb)' },
  { label: 'Pending Triage', value: analytics.value.pending_cases || 0, icon: '⏳', gradient: 'linear-gradient(135deg, #b45309, #d97706)', sub: 'Awaiting assignment' },
  { label: 'Emergencies', value: analytics.value.emergency_cases || 0, icon: '🚨', gradient: 'linear-gradient(135deg, #b91c1c, #dc2626)' },
  { label: 'Accuracy', value: `${analytics.value.triage_accuracy_rate || 0}%`, icon: '🎯', gradient: 'linear-gradient(135deg, #065f46, #059669)' },
])

function severityGradient(s) {
  return { 'ESI-1': 'linear-gradient(135deg,#dc2626,#ef4444)', 'ESI-2': 'linear-gradient(135deg,#d97706,#f97316)', 'ESI-3': 'linear-gradient(135deg,#ca8a04,#eab308)', 'ESI-4': 'linear-gradient(135deg,#16a34a,#22c55e)', 'ESI-5': 'linear-gradient(135deg,#1d4ed8,#3b82f6)' }[s] || 'linear-gradient(135deg,#6b7280,#9ca3af)'
}
function statusClass(s) {
  return { pending: 'bg-gray-100 text-gray-500', triaging: 'bg-blue-50 text-blue-600', triaged: 'bg-amber-50 text-amber-700', assigned: 'bg-purple-50 text-purple-700', in_progress: 'bg-orange-50 text-orange-700', completed: 'bg-emerald-50 text-emerald-700', escalated: 'bg-red-50 text-red-700' }[s] || 'bg-gray-100 text-gray-500'
}
function formatDate(d) { return d ? format(new Date(d), 'MMM d, HH:mm') : '—' }

async function refresh() {
  loading.value = true
  await Promise.all([casesStore.fetchAllCases({ limit: 20 }), casesStore.fetchAlerts(), casesStore.fetchAnalytics(), casesStore.fetchProviders()])
  loading.value = false
}
onMounted(refresh)
</script>
