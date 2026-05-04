<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <header>
    <h2>Login</h2>

    <form
      class="form"
      @submit.prevent="onSubmit"
    >
      <div class="field">
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

      <div class="field">
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
        class="error"
      >
        {{ error }}
      </p>

      <div>
        <button
          type="submit"
          class="login-button"
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
import { getPostAuthRoute, saveAuthSession, type AuthSession } from '../utils/auth'

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

    const authSession = data as AuthSession
    saveAuthSession(authSession)
    router.push(getPostAuthRoute(authSession.user))
  } catch {
    error.value = 'Network error (is the backend running?)'
  } finally {
    loading.value = false
  }
}


</script>

<style scoped>
.login-button {
  background-color:rgb(85, 90, 99);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: block;
  transition: background-color 0.2s ease, transform 0.15s ease;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 8px;          /* spacing between label and input */
  margin-bottom: 16px; /* spacing between fields */
  max-width: 300px;
}

.error {
  color: #b91c1c;
  margin: 8px 0 16px;
}
</style>