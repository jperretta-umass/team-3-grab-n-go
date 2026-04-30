<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <main class="login-page">
    <section class="login-card">
      <h2>Welcome Back</h2>
      <p class="subtitle">Login to continue</p>

      <form class="form" @submit.prevent="onSubmit">
        <div class="field">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter email"
            autocomplete="email"
            required
          >
        </div>

        <div class="field">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter password"
            autocomplete="current-password"
            required
          >
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="login-button" :disabled="loading">
          {{ loading ? 'Signing in...' : 'Login' }}
        </button>

        <button type="button" class="register-button" @click="goToRegister">
          Need an account? Register
        </button>
      </form>
    </section>
  </main>
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

function goToRegister() {
  router.push('/register')
}

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
      error.value = data?.detail || 'Login failed'
      return
    }

    localStorage.setItem('auth', JSON.stringify(data))

    if (data?.access_token) {
      localStorage.setItem('token', data.access_token)
    }

    router.push('/')
  } catch {
    error.value = 'Network error. Is the backend running?'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f4f6f8, #e5e7eb);
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  padding: 32px;
  border-radius: 18px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

h2 {
  margin: 0;
  text-align: center;
  font-size: 2rem;
  color: #1f2937;
}

.subtitle {
  text-align: center;
  color: #6b7280;
  margin-bottom: 24px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

label {
  font-weight: 600;
  color: #374151;
}

input {
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4b5563;
  box-shadow: 0 0 0 3px rgba(75, 85, 99, 0.15);
}

.login-button,
.register-button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 10px;
}

.login-button {
  background-color: #374151;
  color: white;
}

.login-button:hover {
  background-color: #1f2937;
}

.register-button {
  background-color: #e5e7eb;
  color: #1f2937;
}

.register-button:hover {
  background-color: #d1d5db;
}

.error {
  color: #b91c1c;
  background: #fee2e2;
  padding: 10px;
  border-radius: 8px;
}
</style>