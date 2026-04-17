import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'

export const useTriageStore = defineStore('triage', () => {
  const cases = ref([])
  const currentCase = ref(null)
  const loading = ref(false)

  async function submitTriage(payload) {
    loading.value = true
    try {
      const { data } = await api.post('/triage/submit', payload)
      currentCase.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function fetchMyCases() {
    const { data } = await api.get('/triage/my-cases')
    cases.value = data
    return data
  }

  async function fetchCase(id) {
    const { data } = await api.get(`/triage/${id}`)
    currentCase.value = data
    return data
  }

  return { cases, currentCase, loading, submitTriage, fetchMyCases, fetchCase }
})
