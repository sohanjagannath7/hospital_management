<template>
  <div>
    <!-- Progress Steps -->
    <div class="flex items-center gap-2 mb-6">
      <div v-for="(s, i) in steps" :key="i" class="flex items-center gap-2 flex-1">
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all"
            :style="step > i + 1 ? 'background: linear-gradient(135deg,#16a34a,#22c55e); color: white;' : step === i + 1 ? 'background: linear-gradient(135deg,#2563eb,#0891b2); color: white; box-shadow: 0 4px 12px rgba(37,99,235,0.4);' : 'background: #f3f4f6; color: #9ca3af;'">
            <svg v-if="step > i + 1" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/></svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <span class="text-xs font-semibold hidden sm:block" :class="step === i + 1 ? 'text-blue-600' : 'text-gray-400'">{{ s }}</span>
        </div>
        <div v-if="i < steps.length - 1" class="flex-1 h-0.5 mx-2 rounded-full transition-all" :style="step > i + 1 ? 'background: linear-gradient(90deg,#16a34a,#22c55e)' : '#e5e7eb'"></div>
      </div>
    </div>

    <div class="card">
      <!-- Step 1 -->
      <transition name="fade" mode="out-in">
      <div v-if="step === 1" key="step1">
        <h2 class="text-lg font-bold text-gray-900 mb-5">Describe Your Symptoms</h2>
        <div class="space-y-5">
          <div>
            <label class="label">Chief Complaint *</label>
            <input v-model="form.chief_complaint" class="input" placeholder="e.g., Chest pain, difficulty breathing, severe headache..." required />
          </div>

          <div>
            <label class="label">Symptoms</label>
            <div class="grid grid-cols-2 gap-2 mt-2">
              <label v-for="s in symptomOptions" :key="s"
                class="flex items-center gap-2.5 p-2.5 rounded-xl cursor-pointer transition-all border"
                :class="form.symptoms.includes(s) ? 'border-blue-300 bg-blue-50' : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'">
                <input type="checkbox" :value="s" v-model="form.symptoms" class="hidden" />
                <div class="w-4 h-4 rounded flex items-center justify-center flex-shrink-0 transition-all"
                  :style="form.symptoms.includes(s) ? 'background: linear-gradient(135deg,#2563eb,#0891b2);' : 'border: 1.5px solid #d1d5db;'">
                  <svg v-if="form.symptoms.includes(s)" class="w-2.5 h-2.5 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                </div>
                <span class="text-sm text-gray-700 font-medium">{{ s }}</span>
              </label>
            </div>
            <div class="flex gap-2 mt-3">
              <input v-model="customSymptom" @keydown.enter.prevent="addCustom" class="input flex-1 text-sm" placeholder="+ Add custom symptom" />
              <button @click="addCustom" class="btn-secondary text-sm px-4">Add</button>
            </div>
            <div class="flex flex-wrap gap-2 mt-2">
              <span v-for="s in customSymptoms" :key="s" class="flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium text-blue-700" style="background: rgba(37,99,235,0.1); border: 1px solid rgba(37,99,235,0.2);">
                {{ s }}<button @click="removeCustom(s)" class="ml-1 text-blue-400 hover:text-blue-700 font-bold">&times;</button>
              </span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Duration</label>
              <select v-model="form.symptom_duration" class="input">
                <option value="">Select...</option>
                <option>Less than 1 hour</option><option>1–6 hours</option><option>6–24 hours</option>
                <option>1–3 days</option><option>3–7 days</option><option>More than 1 week</option>
              </select>
            </div>
            <div>
              <label class="label">Pain Scale — <span :class="painColor" class="font-bold">{{ form.pain_scale }}/10</span></label>
              <input type="range" v-model.number="form.pain_scale" min="0" max="10" class="w-full mt-2 accent-blue-600" />
              <div class="flex justify-between text-[10px] text-gray-400 mt-1"><span>No Pain</span><span>Worst</span></div>
            </div>
          </div>
        </div>

        <div class="flex justify-end mt-6">
          <button @click="step = 2" class="btn-primary" :disabled="!form.chief_complaint">
            Next: Vital Signs
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
      </div>

      <!-- Step 2 -->
      <div v-else-if="step === 2" key="step2">
        <h2 class="text-lg font-bold text-gray-900 mb-1">Vital Signs</h2>
        <p class="text-sm text-gray-400 mb-5">Optional — enter if you have a monitoring device</p>

        <div class="grid grid-cols-2 gap-4">
          <div v-for="v in vitalFields" :key="v.key">
            <label class="label">{{ v.label }}</label>
            <div class="relative">
              <input v-model.number="vitals[v.key]" type="number" :step="v.step || 1" class="input pr-14" :placeholder="v.placeholder" />
              <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400 font-medium">{{ v.unit }}</span>
            </div>
          </div>
          <div class="col-span-2">
            <label class="label">Onset Description</label>
            <textarea v-model="form.onset_description" class="input h-20 resize-none" placeholder="e.g., Symptoms started suddenly after exercise..."></textarea>
          </div>
        </div>

        <div class="flex justify-between mt-6">
          <button @click="step = 1" class="btn-secondary">← Back</button>
          <button @click="handleSubmit" class="btn-primary min-w-40" :disabled="loading">
            <span v-if="loading" class="flex items-center gap-2">
              <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              AI Analyzing...
            </span>
            <span v-else class="flex items-center gap-2">🤖 Run AI Triage</span>
          </button>
        </div>
      </div>
      </transition>

      <div v-if="error" class="mt-4 p-3 rounded-xl text-sm text-red-700" style="background: rgba(220,38,38,0.06); border: 1px solid rgba(220,38,38,0.2);">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useTriageStore } from '@/stores/triage'

const emit = defineEmits(['submitted'])
const triageStore = useTriageStore()

const step = ref(1)
const loading = ref(false)
const error = ref('')
const customSymptom = ref('')
const steps = ['Symptoms', 'Vitals']

const form = ref({ chief_complaint: '', symptoms: [], symptom_duration: '', pain_scale: 0, onset_description: '' })
const vitals = ref({ temperature_c: null, heart_rate: null, blood_pressure_systolic: null, blood_pressure_diastolic: null, oxygen_saturation: null, respiratory_rate: null, glucose_mg_dl: null })

const symptomOptions = ['Chest pain', 'Shortness of breath', 'Fever', 'Headache', 'Nausea', 'Vomiting', 'Diarrhea', 'Dizziness', 'Fatigue', 'Cough', 'Abdominal pain', 'Back pain', 'Joint pain', 'Rash', 'Swelling', 'Confusion', 'Palpitations', 'Chills', 'Loss of appetite', 'Vision changes']

const vitalFields = [
  { key: 'temperature_c', label: 'Temperature', placeholder: '37.0', unit: '°C', step: 0.1 },
  { key: 'heart_rate', label: 'Heart Rate', placeholder: '72', unit: 'bpm' },
  { key: 'blood_pressure_systolic', label: 'Systolic BP', placeholder: '120', unit: 'mmHg' },
  { key: 'blood_pressure_diastolic', label: 'Diastolic BP', placeholder: '80', unit: 'mmHg' },
  { key: 'oxygen_saturation', label: 'O₂ Saturation', placeholder: '98', unit: '%', step: 0.1 },
  { key: 'respiratory_rate', label: 'Respiratory Rate', placeholder: '16', unit: '/min' },
]

const customSymptoms = computed(() => form.value.symptoms.filter(s => !symptomOptions.includes(s)))
const painColor = computed(() => { const p = form.value.pain_scale; return p <= 3 ? 'text-emerald-600' : p <= 6 ? 'text-amber-600' : 'text-red-600' })

function addCustom() {
  if (customSymptom.value.trim() && !form.value.symptoms.includes(customSymptom.value.trim())) {
    form.value.symptoms.push(customSymptom.value.trim())
  }
  customSymptom.value = ''
}
function removeCustom(s) { form.value.symptoms = form.value.symptoms.filter(x => x !== s) }

async function handleSubmit() {
  loading.value = true; error.value = ''
  try {
    const hasVitals = Object.values(vitals.value).some(v => v !== null)
    const result = await triageStore.submitTriage({ ...form.value, vital_signs: hasVitals ? vitals.value : null })
    emit('submitted', result)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to submit triage. Please try again.'
  } finally { loading.value = false }
}
</script>
