<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-900 via-primary-700 to-teal-600 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-white/20 rounded-2xl mb-4">
          <span class="text-3xl">🏥</span>
        </div>
        <h1 class="text-3xl font-bold text-white">HealthTriage AI</h1>
        <p class="text-primary-200 mt-2">Create your account</p>
      </div>

      <div class="bg-white rounded-2xl shadow-2xl p-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">Register</h2>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="label">Full Name</label>
            <input v-model="form.full_name" class="input" placeholder="John Doe" required />
          </div>
          <div>
            <label class="label">Email</label>
            <input v-model="form.email" type="email" class="input" placeholder="john@example.com" required />
          </div>
          <div>
            <label class="label">Password</label>
            <input v-model="form.password" type="password" class="input" placeholder="Min 8 characters" required minlength="6" />
          </div>
          <div>
            <label class="label">Phone (optional)</label>
            <input v-model="form.phone" class="input" placeholder="+1 555 000 0000" />
          </div>
          <div>
            <label class="label">Register as</label>
            <select v-model="form.role" class="input">
              <option value="patient">Patient</option>
              <option value="doctor">Doctor</option>
              <option value="nurse">Nurse</option>
            </select>
          </div>

          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">{{ error }}</div>
          <div v-if="success" class="p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">Registration successful! Redirecting...</div>

          <button type="submit" class="btn-primary w-full py-3" :disabled="loading">
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          Already have an account?
          <router-link to="/login" class="text-primary-600 font-medium hover:underline">Sign in</router-link>
        </p>
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
const success = ref(false)
const form = ref({ full_name: '', email: '', password: '', phone: '', role: 'patient' })

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await auth.register(form.value)
    success.value = true
    setTimeout(() => router.push('/login'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Registration failed.'
  } finally {
    loading.value = false
  }
}
</script>
