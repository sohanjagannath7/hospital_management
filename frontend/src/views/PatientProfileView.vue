<template>
  <div class="max-w-2xl mx-auto p-6">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">My Health Profile</h1>

    <div class="space-y-6">
      <!-- Basic Info -->
      <div class="card">
        <h3 class="font-semibold mb-4">Personal Information</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="label">Date of Birth</label>
            <input v-model="profile.date_of_birth" type="date" class="input" />
          </div>
          <div>
            <label class="label">Gender</label>
            <select v-model="profile.gender" class="input">
              <option>Male</option><option>Female</option><option>Non-binary</option><option>Prefer not to say</option>
            </select>
          </div>
          <div>
            <label class="label">Blood Type</label>
            <select v-model="profile.blood_type" class="input">
              <option v-for="bt in ['A+','A-','B+','B-','AB+','AB-','O+','O-']" :key="bt">{{ bt }}</option>
            </select>
          </div>
          <div>
            <label class="label">Height (cm)</label>
            <input v-model.number="profile.height_cm" type="number" class="input" />
          </div>
          <div>
            <label class="label">Weight (kg)</label>
            <input v-model.number="profile.weight_kg" type="number" class="input" />
          </div>
          <div>
            <label class="label">Insurance Provider</label>
            <input v-model="profile.insurance_provider" class="input" />
          </div>
        </div>
        <button @click="saveProfile" class="btn-primary mt-4">Save Profile</button>
      </div>

      <!-- Medical History -->
      <div class="card">
        <h3 class="font-semibold mb-4">Medical History</h3>

        <div class="space-y-4">
          <div>
            <label class="label">Chronic Conditions</label>
            <TagInput v-model="history.chronic_conditions" placeholder="e.g. Diabetes, Hypertension" />
          </div>
          <div>
            <label class="label">Allergies</label>
            <TagInput v-model="history.allergies" placeholder="e.g. Penicillin, Peanuts" />
          </div>
          <div>
            <label class="label">Current Medications</label>
            <div class="space-y-2">
              <div v-for="(med, i) in history.current_medications" :key="i" class="flex gap-2">
                <input v-model="med.name" class="input flex-1" placeholder="Medication name" />
                <input v-model="med.dose" class="input w-32" placeholder="Dose" />
                <button @click="removeMed(i)" class="text-red-400 hover:text-red-600 text-xl">&times;</button>
              </div>
              <button @click="addMed" class="text-sm text-primary-600 hover:underline">+ Add Medication</button>
            </div>
          </div>
          <div>
            <label class="label">Past Surgeries</label>
            <TagInput v-model="history.past_surgeries" placeholder="e.g. Appendectomy 2020" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Smoking Status</label>
              <select v-model="history.smoking_status" class="input">
                <option>Never</option><option>Former</option><option>Current</option>
              </select>
            </div>
            <div>
              <label class="label">Exercise Frequency</label>
              <select v-model="history.exercise_frequency" class="input">
                <option>Sedentary</option><option>1-2x/week</option><option>3-4x/week</option><option>Daily</option>
              </select>
            </div>
          </div>
        </div>
        <button @click="saveHistory" class="btn-primary mt-4">Save Medical History</button>
      </div>
    </div>

    <div v-if="saved" class="fixed bottom-6 right-6 bg-green-600 text-white px-4 py-3 rounded-lg shadow-lg">
      ✓ Saved successfully
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'

const profile = ref({})
const history = ref({ chronic_conditions: [], allergies: [], current_medications: [], past_surgeries: [] })
const saved = ref(false)

function addMed() { history.value.current_medications.push({ name: '', dose: '' }) }
function removeMed(i) { history.value.current_medications.splice(i, 1) }

async function saveProfile() {
  await api.put('/patients/me', profile.value)
  showSaved()
}

async function saveHistory() {
  await api.put('/patients/me/history', history.value)
  showSaved()
}

function showSaved() {
  saved.value = true
  setTimeout(() => saved.value = false, 2500)
}

// Inline TagInput component
const TagInput = {
  props: ['modelValue', 'placeholder'],
  emits: ['update:modelValue'],
  template: `
    <div class="space-y-2">
      <div class="flex flex-wrap gap-2">
        <span v-for="(t, i) in modelValue" :key="i" class="flex items-center gap-1 px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm">
          {{ t }}<button @click="remove(i)" class="text-primary-400 hover:text-primary-600">&times;</button>
        </span>
      </div>
      <div class="flex gap-2">
        <input v-model="input" @keydown.enter.prevent="add" class="input flex-1 text-sm" :placeholder="placeholder" />
        <button @click="add" class="btn-secondary text-sm px-3">Add</button>
      </div>
    </div>
  `,
  setup(props, { emit }) {
    const input = ref('')
    function add() { if (input.value.trim()) { emit('update:modelValue', [...props.modelValue, input.value.trim()]); input.value = '' } }
    function remove(i) { const arr = [...props.modelValue]; arr.splice(i, 1); emit('update:modelValue', arr) }
    return { input, add, remove }
  }
}

onMounted(async () => {
  try {
    const [p, h] = await Promise.all([api.get('/patients/me'), api.get('/patients/me/history')])
    profile.value = p.data
    if (h.data) history.value = { ...history.value, ...h.data }
  } catch {}
})
</script>
