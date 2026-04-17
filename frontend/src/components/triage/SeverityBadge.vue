<template>
  <div class="flex flex-col items-center gap-1">
    <div class="rounded-xl flex items-center justify-center font-black text-white"
      :class="size === 'lg' ? 'w-20 h-20 text-2xl' : 'w-12 h-12 text-sm'"
      :style="{ background: gradient, boxShadow: `0 4px 14px ${shadow}` }">
      {{ label }}
    </div>
    <p class="text-[10px] text-gray-400 font-semibold text-center tracking-wide">{{ description }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ severity: String, size: { type: String, default: 'md' } })

const gradient = computed(() => ({
  'ESI-1': 'linear-gradient(135deg, #b91c1c, #ef4444)',
  'ESI-2': 'linear-gradient(135deg, #c2410c, #f97316)',
  'ESI-3': 'linear-gradient(135deg, #b45309, #f59e0b)',
  'ESI-4': 'linear-gradient(135deg, #15803d, #22c55e)',
  'ESI-5': 'linear-gradient(135deg, #1d4ed8, #60a5fa)',
}[props.severity] || 'linear-gradient(135deg, #6b7280, #9ca3af)'))

const shadow = computed(() => ({
  'ESI-1': 'rgba(239,68,68,0.35)', 'ESI-2': 'rgba(249,115,22,0.35)',
  'ESI-3': 'rgba(245,158,11,0.35)', 'ESI-4': 'rgba(34,197,94,0.35)', 'ESI-5': 'rgba(59,130,246,0.35)',
}[props.severity] || 'rgba(0,0,0,0.1)'))

const label = computed(() => props.severity || 'N/A')
const description = computed(() => ({
  'ESI-1': 'Resuscitation', 'ESI-2': 'Emergent', 'ESI-3': 'Urgent', 'ESI-4': 'Less Urgent', 'ESI-5': 'Non-Urgent',
}[props.severity] || 'Pending'))
</script>
