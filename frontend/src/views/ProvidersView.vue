<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Healthcare Providers</h1>
      <div class="flex gap-3">
        <select v-model="statusFilter" class="input w-40 text-sm">
          <option value="">All Status</option>
          <option value="available">Available</option>
          <option value="busy">Busy</option>
          <option value="offline">Offline</option>
        </select>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="p in filteredProviders" :key="p.id" class="card hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between">
          <div class="flex items-start gap-3">
            <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-xl">👨‍⚕️</div>
            <div>
              <p class="font-semibold text-gray-900">{{ p.user?.full_name }}</p>
              <p class="text-sm text-gray-500">{{ p.specialty }}</p>
              <p class="text-xs text-gray-400">{{ p.department || 'General' }}</p>
            </div>
          </div>
          <div class="flex items-center gap-1">
            <div class="w-2 h-2 rounded-full" :class="statusDot(p.status)"></div>
            <span class="text-xs capitalize" :class="statusText(p.status)">{{ p.status?.replace('_', ' ') }}</span>
          </div>
        </div>

        <div class="mt-4 space-y-2">
          <div class="flex justify-between text-sm">
            <span class="text-gray-500">Case Load</span>
            <span class="font-medium">{{ p.current_load }} / {{ p.max_cases }}</span>
          </div>
          <div class="w-full bg-gray-100 rounded-full h-2">
            <div class="h-2 rounded-full transition-all"
              :class="p.current_load/p.max_cases > 0.8 ? 'bg-red-500' : p.current_load/p.max_cases > 0.5 ? 'bg-yellow-500' : 'bg-green-500'"
              :style="{ width: `${Math.min(100, (p.current_load/p.max_cases)*100)}%` }"></div>
          </div>
        </div>

        <div v-if="p.available_care_levels?.length" class="mt-3 flex flex-wrap gap-1">
          <span v-for="l in p.available_care_levels" :key="l" class="text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full">{{ l }}</span>
        </div>

        <div class="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
          <div class="flex items-center gap-1 text-yellow-500 text-sm">
            <span>⭐</span><span class="font-medium">{{ p.rating?.toFixed(1) }}</span>
          </div>
          <span class="text-xs text-gray-400">{{ p.years_experience ? p.years_experience + ' yrs exp' : '' }}</span>
        </div>
      </div>
    </div>

    <p v-if="!filteredProviders.length" class="text-center text-gray-400 py-12">No providers found</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCasesStore } from '@/stores/cases'

const casesStore = useCasesStore()
const statusFilter = ref('')

const filteredProviders = computed(() => {
  if (!statusFilter.value) return casesStore.providers
  return casesStore.providers.filter(p => p.status === statusFilter.value)
})

function statusDot(s) { return { available: 'bg-green-500', busy: 'bg-yellow-500', offline: 'bg-gray-400', on_break: 'bg-blue-400' }[s] || 'bg-gray-400' }
function statusText(s) { return { available: 'text-green-600', busy: 'text-yellow-600', offline: 'text-gray-500' }[s] || 'text-gray-500' }

onMounted(() => casesStore.fetchProviders())
</script>
