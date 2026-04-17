<template>
  <aside class="fixed left-0 top-16 bottom-0 w-64 z-30 flex flex-col" style="background: #0f1729; border-right: 1px solid rgba(255,255,255,0.05);">
    <!-- Header -->
    <div class="px-4 py-5 border-b border-white/5">
      <p class="text-[10px] font-bold text-blue-400/60 uppercase tracking-widest">Navigation</p>
    </div>

    <!-- Nav items -->
    <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="group flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200"
        :class="isActive(item.path)
          ? 'text-white'
          : 'text-gray-400 hover:text-white hover:bg-white/5'"
        :style="isActive(item.path) ? 'background: linear-gradient(135deg, rgba(37,99,235,0.3), rgba(8,145,178,0.3)); box-shadow: inset 0 0 0 1px rgba(59,130,246,0.2);' : ''"
      >
        <span class="text-base flex-shrink-0 w-5 text-center">{{ item.icon }}</span>
        <span class="flex-1">{{ item.label }}</span>
        <span v-if="item.badge"
          class="text-[10px] font-bold px-1.5 py-0.5 rounded-full text-white"
          style="background: linear-gradient(135deg, #ef4444, #f97316);">
          {{ item.badge }}
        </span>
        <span v-if="isActive(item.path)" class="w-1.5 h-1.5 rounded-full bg-blue-400"></span>
      </router-link>
    </nav>

    <!-- Bottom status -->
    <div class="p-4 border-t border-white/5">
      <div class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl bg-white/5">
        <div class="relative">
          <div class="w-2 h-2 rounded-full bg-emerald-400"></div>
          <div class="absolute inset-0 rounded-full bg-emerald-400 animate-ping opacity-40"></div>
        </div>
        <div>
          <p class="text-white text-xs font-semibold">System Online</p>
          <p class="text-gray-500 text-[10px]">All agents active</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useCasesStore } from '@/stores/cases'

const route = useRoute()
const casesStore = useCasesStore()

const pendingCount = computed(() => casesStore.cases.filter(c => c.status === 'triaged').length || null)

const navItems = computed(() => [
  { path: '/dashboard', label: 'Dashboard', icon: '⚡' },
  { path: '/cases', label: 'Case Queue', icon: '🏥', badge: pendingCount.value },
  { path: '/analytics', label: 'Analytics', icon: '📈' },
  { path: '/providers', label: 'Providers', icon: '👨‍⚕️' },
])

function isActive(path) { return route.path === path }
</script>
