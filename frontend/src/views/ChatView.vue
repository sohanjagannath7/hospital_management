<template>
  <div class="max-w-2xl mx-auto p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">AI Health Assistant</h1>
      <p class="text-gray-400 text-sm mt-0.5">Chat with MedAssist before your triage</p>
    </div>

    <div class="rounded-2xl overflow-hidden flex flex-col h-[600px]" style="box-shadow: 0 8px 40px rgba(0,0,0,0.1); border: 1px solid rgba(0,0,0,0.06);">
      <!-- Header -->
      <div class="flex items-center gap-4 p-4" style="background: linear-gradient(135deg, #1e40af, #0891b2);">
        <div class="w-11 h-11 rounded-2xl bg-white/20 flex items-center justify-center text-2xl">🤖</div>
        <div class="flex-1">
          <p class="font-bold text-white">MedAssist AI</p>
          <p class="text-blue-200/80 text-xs flex items-center gap-1">
            <span class="w-1.5 h-1.5 bg-emerald-400 rounded-full"></span>
            Online · Powered by Gemini AI
          </p>
        </div>
        <router-link to="/patient/intake" class="text-xs px-3 py-2 bg-white/15 hover:bg-white/25 text-white rounded-lg font-medium transition-colors">
          Start Triage →
        </router-link>
      </div>

      <!-- Messages -->
      <div ref="messagesEl" class="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50">
        <!-- Welcome -->
        <div class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-sm flex-shrink-0">🤖</div>
          <div class="rounded-2xl rounded-tl-sm p-4 max-w-sm text-sm text-gray-800 leading-relaxed shadow-sm" style="background: white; border: 1px solid rgba(0,0,0,0.06);">
            Hello! I'm <strong>MedAssist</strong>, your AI health assistant. I can help you understand your symptoms and guide you on when and where to seek care. <br/><br/>How are you feeling today?
          </div>
        </div>

        <div v-for="msg in messages" :key="msg.id" class="flex items-end gap-3" :class="msg.role === 'user' ? 'flex-row-reverse' : ''">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center text-sm flex-shrink-0"
            :style="msg.role === 'user' ? 'background: linear-gradient(135deg, #2563eb, #0891b2);' : 'background: white; border: 1px solid rgba(0,0,0,0.08);'">
            {{ msg.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="rounded-2xl p-4 max-w-sm text-sm leading-relaxed shadow-sm"
            :style="msg.role === 'user'
              ? 'background: linear-gradient(135deg, #2563eb, #0891b2); color: white; border-radius: 18px 4px 18px 18px;'
              : 'background: white; color: #1f2937; border: 1px solid rgba(0,0,0,0.06); border-radius: 4px 18px 18px 18px;'">
            {{ msg.content }}
          </div>
        </div>

        <!-- Typing indicator -->
        <div v-if="aiTyping" class="flex items-end gap-3">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center text-sm" style="background: white; border: 1px solid rgba(0,0,0,0.08);">🤖</div>
          <div class="rounded-2xl p-4 shadow-sm" style="background: white; border: 1px solid rgba(0,0,0,0.06);">
            <div class="flex gap-1.5 items-center h-4">
              <div v-for="i in 3" :key="i" class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" :style="`animation-delay: ${(i-1)*0.15}s`"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="p-4 bg-white border-t border-gray-100">
        <!-- Quick prompts -->
        <div class="flex flex-wrap gap-2 mb-3">
          <button v-for="p in quickPrompts" :key="p" @click="sendQuick(p)"
            class="text-xs px-3 py-1.5 rounded-full border border-gray-200 text-gray-600 hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50 transition-all">
            {{ p }}
          </button>
        </div>
        <div class="flex gap-2">
          <input v-model="inputText" @keydown.enter="sendMessage" :disabled="aiTyping"
            class="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-sm outline-none transition-all focus:border-blue-400 focus:bg-white focus:shadow-sm"
            placeholder="Describe your symptoms..." />
          <button @click="sendMessage" :disabled="!inputText.trim() || aiTyping"
            class="w-12 h-12 rounded-xl flex items-center justify-center text-white transition-all disabled:opacity-40"
            style="background: linear-gradient(135deg, #2563eb, #0891b2);">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/></svg>
          </button>
        </div>
        <p class="text-[10px] text-gray-400 text-center mt-2">Not a substitute for professional medical advice</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import api from '@/utils/api'

const messages = ref([])
const inputText = ref('')
const aiTyping = ref(false)
const messagesEl = ref(null)
const sessionId = ref(null)

const quickPrompts = ['I have chest pain', 'High fever', 'Difficulty breathing', 'Severe headache', 'Dizziness']

async function scrollToBottom() {
  await nextTick()
  if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight
}

function sendQuick(p) { inputText.value = p; sendMessage() }

async function sendMessage() {
  if (!inputText.value.trim() || aiTyping.value) return
  const content = inputText.value.trim()
  inputText.value = ''
  messages.value.push({ id: Date.now(), role: 'user', content })
  await scrollToBottom()
  aiTyping.value = true
  try {
    if (!sessionId.value) {
      const { data } = await api.post('/chat/sessions')
      sessionId.value = data.id
    }
    const { data } = await api.post(`/chat/sessions/${sessionId.value}/messages`, { content })
    messages.value.push({ id: data.id, role: 'assistant', content: data.content })
  } catch {
    messages.value.push({ id: Date.now(), role: 'assistant', content: 'Sorry, I encountered an issue. Please try again.' })
  } finally {
    aiTyping.value = false
    await scrollToBottom()
  }
}
onMounted(scrollToBottom)
</script>
