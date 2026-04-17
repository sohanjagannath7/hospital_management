<template>
  <div class="min-h-screen flex" style="background: #020818;">
    <!-- Left panel -->
    <div class="hidden lg:flex flex-col justify-between w-1/2 p-12 relative overflow-hidden"
      style="background: linear-gradient(135deg, #0d1b3e 0%, #0c2340 50%, #071a2e 100%);">
      <!-- Orbs -->
      <div class="absolute top-[-10%] right-[-10%] w-80 h-80 rounded-full opacity-20 blur-3xl" style="background: radial-gradient(circle, #3b82f6, transparent)"></div>
      <div class="absolute bottom-[-5%] left-[-5%] w-64 h-64 rounded-full opacity-15 blur-3xl" style="background: radial-gradient(circle, #0891b2, transparent)"></div>

      <!-- Logo -->
      <div class="flex items-center gap-3 relative z-10">
        <div class="w-10 h-10 rounded-xl flex items-center justify-center" style="background: linear-gradient(135deg, #2563eb, #0891b2);">
          <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/></svg>
        </div>
        <span class="text-white font-bold text-xl">HealthTriage AI</span>
      </div>

      <!-- Middle content -->
      <div class="relative z-10">
        <h2 class="text-4xl font-extrabold text-white mb-4 leading-tight">
          Intelligent triage<br/>for every patient
        </h2>
        <p class="text-blue-200/70 text-lg mb-10">AI-powered severity scoring, care routing, and drug interaction checking — all in seconds.</p>

        <div class="space-y-4">
          <div v-for="f in highlights" :key="f.text" class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0" :style="{ background: f.bg }">{{ f.icon }}</div>
            <span class="text-blue-100/80 text-sm">{{ f.text }}</span>
          </div>
        </div>
      </div>

      <p class="text-blue-400/40 text-xs relative z-10">© 2025 HealthTriage AI</p>
    </div>

    <!-- Right panel -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <!-- Mobile logo -->
        <div class="flex items-center gap-2 mb-8 lg:hidden">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #2563eb, #0891b2);">
            <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd"/></svg>
          </div>
          <span class="font-bold text-white">HealthTriage AI</span>
        </div>

        <div class="rounded-2xl p-8" style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);">
          <h1 class="text-2xl font-bold text-white mb-1">Welcome back</h1>
          <p class="text-blue-300/60 text-sm mb-7">Sign in to your account</p>

          <form @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-blue-300/60 uppercase tracking-wide mb-2">Email</label>
              <input v-model="form.email" type="email" class="w-full px-4 py-3 rounded-xl text-sm text-white outline-none transition-all"
                style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.1);"
                placeholder="you@hospital.com" required
                @focus="e => e.target.style.borderColor = 'rgba(59,130,246,0.6)'"
                @blur="e => e.target.style.borderColor = 'rgba(255,255,255,0.1)'" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-blue-300/60 uppercase tracking-wide mb-2">Password</label>
              <input v-model="form.password" type="password" class="w-full px-4 py-3 rounded-xl text-sm text-white outline-none transition-all"
                style="background: rgba(255,255,255,0.07); border: 1px solid rgba(255,255,255,0.1);"
                placeholder="••••••••" required
                @focus="e => e.target.style.borderColor = 'rgba(59,130,246,0.6)'"
                @blur="e => e.target.style.borderColor = 'rgba(255,255,255,0.1)'" />
            </div>

            <div v-if="error" class="px-4 py-3 rounded-xl text-sm text-red-300" style="background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.2);">
              {{ error }}
            </div>

            <button type="submit" class="w-full py-3.5 rounded-xl text-white font-bold text-sm transition-all mt-2" :disabled="loading"
              style="background: linear-gradient(135deg, #2563eb, #0891b2); box-shadow: 0 4px 20px rgba(37,99,235,0.4);">
              {{ loading ? 'Signing in...' : 'Sign In →' }}
            </button>
          </form>

          <!-- Demo accounts -->
          <div class="mt-6 rounded-xl p-4" style="background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);">
            <p class="text-[10px] font-bold text-blue-400/50 uppercase tracking-widest mb-3">Demo Accounts</p>
            <div class="space-y-2">
              <button v-for="d in demos" :key="d.email" @click="fillDemo(d.email)"
                class="w-full flex items-center justify-between px-3 py-2 rounded-lg hover:bg-white/5 transition-colors group">
                <div class="flex items-center gap-2">
                  <span class="text-base">{{ d.icon }}</span>
                  <span class="text-sm font-medium text-gray-300">{{ d.label }}</span>
                </div>
                <span class="text-xs text-gray-500 group-hover:text-gray-300 transition-colors">{{ d.email }}</span>
              </button>
            </div>
          </div>

          <p class="text-center text-sm text-gray-500 mt-5">
            No account?
            <router-link to="/register" class="text-blue-400 font-semibold hover:text-blue-300 transition-colors">Register free</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const loading = ref(false)
const error = ref('')
const form = ref({ email: '', password: '' })

const highlights = [
  { icon: '🧠', text: 'ESI 1–5 severity scoring in under 3 seconds', bg: 'rgba(59,130,246,0.2)' },
  { icon: '🚨', text: 'Real-time emergency alerts and escalation', bg: 'rgba(239,68,68,0.2)' },
  { icon: '💊', text: 'Automatic drug interaction detection', bg: 'rgba(245,158,11,0.2)' },
  { icon: '📊', text: 'Live analytics and provider utilization', bg: 'rgba(16,185,129,0.2)' },
]

const demos = [
  { icon: '👨‍💼', label: 'Admin', email: 'admin@hospital.com' },
  { icon: '👨‍⚕️', label: 'Doctor', email: 'doctor@hospital.com' },
  { icon: '🧑', label: 'Patient', email: 'patient@example.com' },
]

function fillDemo(email) { form.value = { email, password: 'demo123' } }

async function handleLogin() {
  loading.value = true; error.value = ''
  try {
    const data = await auth.login(form.value.email, form.value.password)
    router.push(data.user.role === 'patient' ? '/patient/intake' : '/dashboard')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Invalid credentials'
  } finally { loading.value = false }
}
</script>
