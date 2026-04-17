<template>
  <nav class="fixed top-0 left-0 right-0 z-40 h-16" style="background: rgba(255,255,255,0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.06);">
    <div class="flex items-center justify-between h-full px-6">
      <!-- Logo -->
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #2563eb, #0891b2);">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/></svg>
        </div>
        <span class="font-bold text-gray-900 text-lg tracking-tight">
          Health<span class="gradient-text">Triage</span> AI
        </span>
      </div>

      <div class="flex items-center gap-3">
        <!-- Emergency SOS -->
        <button
          v-if="auth.isPatient"
          @click="router.push('/patient/intake?emergency=true')"
          class="emergency-pulse flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-bold text-white"
          style="background: linear-gradient(135deg, #dc2626, #f97316);"
        >
          <span class="relative flex h-2 w-2">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2 bg-white"></span>
          </span>
          SOS Emergency
        </button>

        <!-- Patient quick links -->
        <template v-if="auth.isPatient">
          <router-link to="/patient/chat" class="p-2 text-gray-500 hover:text-blue-600 rounded-lg hover:bg-blue-50 transition-colors" title="AI Chat">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          </router-link>
          <router-link to="/patient/cases" class="p-2 text-gray-500 hover:text-blue-600 rounded-lg hover:bg-blue-50 transition-colors" title="My Cases">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          </router-link>
        </template>

        <!-- Alerts bell (staff) -->
        <button
          v-if="!auth.isPatient"
          @click="toggleAlerts"
          class="relative p-2 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
          <span v-if="alertCount > 0"
            class="absolute -top-0.5 -right-0.5 w-4 h-4 text-white text-[10px] font-bold rounded-full flex items-center justify-center"
            style="background: linear-gradient(135deg, #ef4444, #f97316);">{{ alertCount }}</span>
        </button>

        <!-- User avatar -->
        <div class="flex items-center gap-2.5 pl-3 border-l border-gray-200">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center text-white text-xs font-bold"
            style="background: linear-gradient(135deg, #2563eb, #0891b2);">
            {{ initials }}
          </div>
          <div class="hidden sm:block">
            <p class="text-sm font-semibold text-gray-900 leading-tight">{{ auth.user?.full_name?.split(' ')[0] }}</p>
            <p class="text-[10px] text-gray-400 capitalize font-medium">{{ auth.user?.role }}</p>
          </div>
        </div>

        <button @click="handleLogout" class="p-2 text-gray-400 hover:text-red-500 rounded-lg hover:bg-red-50 transition-colors" title="Logout">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
        </button>
      </div>
    </div>
  </nav>
  <div class="h-16"></div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCasesStore } from '@/stores/cases'

const auth = useAuthStore()
const casesStore = useCasesStore()
const router = useRouter()

const initials = computed(() => {
  return (auth.user?.full_name || '').split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
})
const alertCount = computed(() => casesStore.alerts.length)

function toggleAlerts() {}
function handleLogout() { auth.logout(); router.push('/login') }
</script>
