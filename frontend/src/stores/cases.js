import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api'

export const useCasesStore = defineStore('cases', () => {
  const cases = ref([])
  const alerts = ref([])
  const analytics = ref(null)
  const providers = ref([])

  async function fetchAllCases(params = {}) {
    const { data } = await api.get('/cases', { params })
    cases.value = data
    return data
  }

  async function fetchAlerts() {
    const { data } = await api.get('/cases/alerts/active')
    alerts.value = data
    return data
  }

  async function acknowledgeAlert(id) {
    await api.put(`/cases/alerts/${id}/acknowledge`)
    alerts.value = alerts.value.filter(a => a.id !== id)
  }

  async function fetchAnalytics() {
    const { data } = await api.get('/analytics/summary')
    analytics.value = data
    return data
  }

  async function fetchProviders() {
    const { data } = await api.get('/providers')
    providers.value = data
    return data
  }

  async function assignCase(caseId, providerId) {
    const { data } = await api.post(`/cases/${caseId}/assign/${providerId}`)
    const idx = cases.value.findIndex(c => c.id === caseId)
    if (idx !== -1) cases.value[idx] = data
    return data
  }

  async function updateStatus(caseId, status) {
    await api.put(`/cases/${caseId}/status`, null, { params: { new_status: status } })
    const idx = cases.value.findIndex(c => c.id === caseId)
    if (idx !== -1) cases.value[idx].status = status
  }

  return { cases, alerts, analytics, providers, fetchAllCases, fetchAlerts, acknowledgeAlert, fetchAnalytics, fetchProviders, assignCase, updateStatus }
})
