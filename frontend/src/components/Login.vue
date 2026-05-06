<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <header>
    <h2>Login</h2>

    <form
      class="form"
      @submit.prevent="onSubmit"
    >
      <div class="flex flex-col gap-2 mb-4 max-w-[300px]">
        <label for="email">Email:</label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter Email"
          class="border rounded px-3 py-2"
          autocomplete="email"
        >
      </div>

      <div class="flex flex-col gap-2 mb-4 max-w-[300px]">
        <label for="password">Password:</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="Enter password"
          class="border rounded px-3 py-2"
          autocomplete="current-password"
        >
      </div>

      <p
        v-if="error"
        class="text-[#b91c1c] my-2 mb-4"
      >
        {{ error }}
      </p>

      <div>
        <button
          type="submit"
          class="bg-[rgb(85,90,99)] text-white px-6 py-3 border-none rounded-[10px] text-base font-semibold cursor-pointer block transition-colors duration-200 ease-in-out hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="loading"
        >
          {{ loading ? 'Signing in...' : 'Login' }}
        </button>
      </div>
    </form>
  </header>
</template>

<script setup lang="ts">

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000'

const router = useRouter()

async function onSubmit() {
  error.value = null
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    })

    const data = await res.json().catch(() => null)
    if (!res.ok) {
      error.value = (data && (data.detail as string)) || 'Login failed'
      return
    }

    localStorage.setItem('auth', JSON.stringify(data))
    router.push('/')
  } catch {
    error.value = 'Network error (is the backend running?)'
  } finally {
    loading.value = false
  }
}


</script>
