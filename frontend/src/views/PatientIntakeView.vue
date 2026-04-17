<template>
  <div class="max-w-3xl mx-auto p-6">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">AI Triage Assessment</h1>
      <p class="text-gray-500 mt-1">Describe your symptoms for intelligent triage and care routing</p>
    </div>

    <!-- Quick nav for patient -->
    <div class="grid grid-cols-3 gap-4 mb-8">
      <router-link to="/patient/cases" class="card text-center hover:border-primary-300 hover:shadow-md transition-all cursor-pointer">
        <div class="text-2xl mb-2">📋</div>
        <p class="text-sm font-medium text-gray-700">My Cases</p>
      </router-link>
      <router-link to="/patient/chat" class="card text-center hover:border-primary-300 hover:shadow-md transition-all cursor-pointer">
        <div class="text-2xl mb-2">💬</div>
        <p class="text-sm font-medium text-gray-700">AI Chat</p>
      </router-link>
      <router-link to="/patient/profile" class="card text-center hover:border-primary-300 hover:shadow-md transition-all cursor-pointer">
        <div class="text-2xl mb-2">👤</div>
        <p class="text-sm font-medium text-gray-700">My Profile</p>
      </router-link>
    </div>

    <!-- Triage form / Result -->
    <transition name="fade" mode="out-in">
      <TriageResult v-if="result" :result="result" @new-triage="reset" />
      <TriageForm v-else @submitted="handleResult" />
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import TriageForm from '@/components/triage/TriageForm.vue'
import TriageResult from '@/components/triage/TriageResult.vue'

const route = useRoute()
const result = ref(null)

function handleResult(data) {
  result.value = data
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function reset() {
  result.value = null
}

onMounted(() => {
  if (route.query.emergency === 'true') {
    // Pre-select emergency mode
  }
})
</script>
