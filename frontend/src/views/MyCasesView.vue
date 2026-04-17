<template>
  <div class="max-w-3xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">My Cases</h1>
      <router-link to="/patient/intake" class="btn-primary text-sm">+ New Triage</router-link>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-3"></div>
      <p class="text-gray-500">Loading your cases...</p>
    </div>

    <div v-else-if="!cases.length" class="card text-center py-12">
      <span class="text-5xl mb-4 block">🏥</span>
      <h3 class="font-semibold text-gray-900 mb-2">No cases yet</h3>
      <p class="text-gray-500 text-sm mb-4">Submit your first triage to get AI-powered care guidance</p>
      <router-link to="/patient/intake" class="btn-primary">Start Triage Assessment</router-link>
    </div>

    <div v-else class="space-y-4">
      <div v-for="c in cases" :key="c.id" class="card hover:shadow-md transition-shadow cursor-pointer" @click="selectedCase = c">
        <div class="flex items-start justify-between">
          <div class="flex items-start gap-4">
            <SeverityBadge :severity="c.severity" />
            <div>
              <div class="flex items-center gap-2">
                <p class="font-semibold text-gray-900">{{ c.chief_complaint }}</p>
                <span v-if="c.is_emergency" class="text-red-500 text-xs">🚨 EMERGENCY</span>
              </div>
              <p class="text-sm text-gray-500 mt-1">{{ c.case_number }} · {{ formatDate(c.created_at) }}</p>
              <div class="flex flex-wrap gap-2 mt-2">
                <span v-for="s in c.symptoms.slice(0, 4)" :key="s" class="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full">{{ s }}</span>
                <span v-if="c.symptoms.length > 4" class="text-xs text-gray-400">+{{ c.symptoms.length - 4 }} more</span>
              </div>
            </div>
          </div>
          <div class="text-right">
            <span class="px-2 py-1 rounded-full text-xs font-medium" :class="statusClass(c.status)">{{ c.status.replace('_', ' ') }}</span>
            <p class="text-xs text-gray-400 mt-1">{{ c.care_level }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Case Detail Modal -->
    <div v-if="selectedCase" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="selectedCase = null">
      <div class="bg-white rounded-2xl max-w-lg w-full max-h-[85vh] overflow-y-auto">
        <div class="p-6 border-b flex items-center justify-between">
          <h2 class="font-bold text-lg">{{ selectedCase.case_number }}</h2>
          <button @click="selectedCase = null" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
        </div>
        <div class="p-6 space-y-4">
          <TriageResult :result="selectedCase" @new-triage="selectedCase = null" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTriageStore } from '@/stores/triage'
import SeverityBadge from '@/components/triage/SeverityBadge.vue'
import TriageResult from '@/components/triage/TriageResult.vue'
import { format } from 'date-fns'

const triageStore = useTriageStore()
const loading = ref(true)
const selectedCase = ref(null)
const cases = ref([])

function statusClass(s) {
  return { pending: 'bg-gray-100 text-gray-600', triaged: 'bg-yellow-100 text-yellow-700', assigned: 'bg-purple-100 text-purple-700', completed: 'bg-green-100 text-green-700' }[s] || 'bg-gray-100 text-gray-600'
}
function formatDate(d) { return d ? format(new Date(d), 'MMM d, yyyy') : '—' }

onMounted(async () => {
  cases.value = await triageStore.fetchMyCases()
  loading.value = false
})
</script>
