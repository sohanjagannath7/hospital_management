<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Case Queue</h1>
      <div class="flex gap-3">
        <select v-model="filters.status" class="input w-40 text-sm">
          <option value="">All Status</option>
          <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
        </select>
        <select v-model="filters.severity" class="input w-36 text-sm">
          <option value="">All Severity</option>
          <option v-for="s in severities" :key="s" :value="s">{{ s }}</option>
        </select>
        <button @click="loadCases" class="btn-primary text-sm">Filter</button>
      </div>
    </div>

    <!-- Cases Table -->
    <div class="card p-0 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Case</th>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Severity</th>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Complaint</th>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Care Level</th>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Status</th>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Time</th>
              <th class="text-left text-xs font-semibold text-gray-500 uppercase px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="c in cases" :key="c.id" class="hover:bg-gray-50 transition-colors"
              :class="c.is_emergency ? 'bg-red-50' : ''">
              <td class="px-4 py-3">
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ c.case_number }}</p>
                  <p class="text-xs text-gray-400">ID: {{ c.id }}</p>
                </div>
              </td>
              <td class="px-4 py-3">
                <SeverityBadge :severity="c.severity" size="sm" />
              </td>
              <td class="px-4 py-3">
                <p class="text-sm text-gray-900 max-w-xs truncate">{{ c.chief_complaint }}</p>
                <p class="text-xs text-gray-400">Pain: {{ c.pain_scale ?? '—' }}/10</p>
              </td>
              <td class="px-4 py-3">
                <span class="text-sm text-gray-700">{{ c.care_level || '—' }}</span>
              </td>
              <td class="px-4 py-3">
                <span class="px-2 py-1 rounded-full text-xs font-medium" :class="statusClass(c.status)">{{ c.status }}</span>
                <span v-if="c.is_emergency" class="ml-1 text-red-500 text-xs">🚨</span>
              </td>
              <td class="px-4 py-3 text-xs text-gray-400">{{ formatDate(c.created_at) }}</td>
              <td class="px-4 py-3">
                <div class="flex gap-2">
                  <button @click="viewCase(c)" class="text-xs text-primary-600 hover:underline">View</button>
                  <button v-if="c.status === 'triaged'" @click="openAssign(c)" class="text-xs text-green-600 hover:underline">Assign</button>
                </div>
              </td>
            </tr>
            <tr v-if="!cases.length">
              <td colspan="7" class="text-center py-12 text-gray-400">No cases found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Case Detail Modal -->
    <div v-if="selectedCase" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="selectedCase = null">
      <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-xl font-bold">Case {{ selectedCase.case_number }}</h2>
          <button @click="selectedCase = null" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
        </div>
        <div class="p-6 space-y-5">
          <div class="flex items-center gap-4">
            <SeverityBadge :severity="selectedCase.severity" size="lg" />
            <div>
              <p class="font-semibold text-gray-900 text-lg">{{ selectedCase.chief_complaint }}</p>
              <p class="text-sm text-gray-500">{{ selectedCase.care_level }} · Pain {{ selectedCase.pain_scale }}/10</p>
            </div>
          </div>

          <div v-if="selectedCase.assessment">
            <p class="text-xs font-semibold text-gray-500 uppercase mb-2">AI Assessment</p>
            <div class="p-3 bg-gray-50 rounded-lg space-y-2">
              <p class="text-sm"><span class="font-medium">Conditions:</span> {{ selectedCase.assessment.possible_conditions?.join(', ') }}</p>
              <p class="text-sm"><span class="font-medium">Risk Factors:</span> {{ selectedCase.assessment.risk_factors?.join(', ') || 'None' }}</p>
              <p class="text-sm text-gray-600">{{ selectedCase.assessment.severity_reasoning }}</p>
            </div>
          </div>

          <div v-if="selectedCase.recommendations?.length">
            <p class="text-xs font-semibold text-gray-500 uppercase mb-2">Recommendations</p>
            <ul class="space-y-2">
              <li v-for="r in selectedCase.recommendations" :key="r.id" class="flex items-start gap-2 text-sm">
                <span class="text-gray-400 mt-0.5">•</span>
                <span><span class="font-medium">{{ r.title }}:</span> {{ r.description }}</span>
              </li>
            </ul>
          </div>

          <div v-if="selectedCase.status === 'triaged'" class="flex gap-3">
            <select v-model="assignProviderId" class="input flex-1">
              <option value="">Select provider</option>
              <option v-for="p in casesStore.providers" :key="p.id" :value="p.id">
                {{ p.user?.full_name }} — {{ p.specialty }} ({{ p.current_load }}/{{ p.max_cases }})
              </option>
            </select>
            <button @click="handleAssign" class="btn-primary">Assign</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCasesStore } from '@/stores/cases'
import SeverityBadge from '@/components/triage/SeverityBadge.vue'
import { format } from 'date-fns'

const casesStore = useCasesStore()
const selectedCase = ref(null)
const assignProviderId = ref('')

const filters = ref({ status: '', severity: '' })
const statuses = ['pending', 'triaging', 'triaged', 'assigned', 'in_progress', 'completed', 'escalated']
const severities = ['ESI-1', 'ESI-2', 'ESI-3', 'ESI-4', 'ESI-5']
const cases = computed(() => casesStore.cases)

async function loadCases() {
  const params = {}
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.severity) params.severity = filters.value.severity
  await casesStore.fetchAllCases(params)
}

function viewCase(c) { selectedCase.value = c }
function openAssign(c) { selectedCase.value = c }

async function handleAssign() {
  if (!assignProviderId.value) return
  await casesStore.assignCase(selectedCase.value.id, assignProviderId.value)
  selectedCase.value = null
  assignProviderId.value = ''
}

function statusClass(status) {
  return {
    pending: 'bg-gray-100 text-gray-600',
    triaging: 'bg-blue-100 text-blue-600',
    triaged: 'bg-yellow-100 text-yellow-700',
    assigned: 'bg-purple-100 text-purple-700',
    in_progress: 'bg-orange-100 text-orange-700',
    completed: 'bg-green-100 text-green-700',
    escalated: 'bg-red-100 text-red-700',
  }[status] || 'bg-gray-100 text-gray-600'
}

function formatDate(d) { return d ? format(new Date(d), 'MMM d, HH:mm') : '—' }

onMounted(async () => {
  await Promise.all([loadCases(), casesStore.fetchProviders()])
})
</script>
