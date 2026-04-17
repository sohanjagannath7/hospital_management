<template>
  <div class="min-h-screen bg-gray-50">
    <template v-if="isAuthenticated">
      <Navbar />
      <div class="flex">
        <Sidebar v-if="!isPatient" />
        <main :class="['flex-1 min-h-screen', !isPatient ? 'ml-64' : '']">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </main>
      </div>
    </template>
    <template v-else>
      <router-view />
    </template>

    <!-- Global Alerts Toast -->
    <div class="fixed bottom-4 right-4 space-y-2 z-50">
      <transition-group name="slide-up">
        <div
          v-for="alert in visibleAlerts"
          :key="alert.id"
          class="flex items-start gap-3 p-4 rounded-lg shadow-lg max-w-sm"
          :class="alert.type === 'emergency' ? 'bg-red-600 text-white' : 'bg-yellow-500 text-white'"
        >
          <span class="text-lg">{{ alert.type === 'emergency' ? '🚨' : '⚠️' }}</span>
          <div class="flex-1 text-sm">{{ alert.message }}</div>
          <button @click="dismissAlert(alert.id)" class="text-white/80 hover:text-white text-lg leading-none">&times;</button>
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCasesStore } from '@/stores/cases'
import { wsClient } from '@/utils/websocket'
import Navbar from '@/components/layout/Navbar.vue'
import Sidebar from '@/components/layout/Sidebar.vue'

const auth = useAuthStore()
const casesStore = useCasesStore()
const visibleAlerts = ref([])

const isAuthenticated = computed(() => auth.isAuthenticated)
const isPatient = computed(() => auth.isPatient)

function dismissAlert(id) {
  visibleAlerts.value = visibleAlerts.value.filter(a => a.id !== id)
}

function handleWsMessage(data) {
  if (data.type === 'alert') {
    visibleAlerts.value.push({ ...data.payload, id: Date.now() })
    setTimeout(() => dismissAlert(data.payload.id), 8000)
  }
}

onMounted(() => {
  if (auth.isAuthenticated) {
    wsClient.connect()
    wsClient.on(handleWsMessage)
  }
})

onUnmounted(() => {
  wsClient.off(handleWsMessage)
  wsClient.disconnect()
})
</script>
