<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <main class="register-page">
    <section class="register-card">
      <h2>Create Account</h2>
      <p class="subtitle">Register to start using My Delivery App</p>

      <form class="form" @submit.prevent="onSubmit">
        <div class="field">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" placeholder="Enter username" autocomplete="username">
        </div>

        <div class="field">
          <label for="email">Email</label>
          <input id="email" v-model="email" type="email" placeholder="Enter email" autocomplete="email">
        </div>

        <div class="field">
          <label for="phone_num">Phone Number</label>
          <input id="phone_num" v-model="phone_num" type="text" placeholder="Enter phone number">
        </div>

        <label class="checkbox-field">
          <input v-model="isDeliverer" type="checkbox">
          Register as a deliverer
        </label>

        <div class="field">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" placeholder="Enter password" autocomplete="new-password">
        </div>

        <div class="field">
          <label for="confirmPassword">Confirm Password</label>
          <input id="confirmPassword" v-model="confirmPassword" type="password" placeholder="Re-enter password" autocomplete="new-password">
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" class="register-button" :disabled="loading">
          {{ loading ? 'Creating account...' : 'Register Account' }}
        </button>

        <button type="button" class="login-button" @click="router.push('/login')">
          Already have an account? Login
        </button>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const phone_num = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const isDeliverer = ref(false)

const API_BASE = (import.meta.env.VITE_API_BASE as string | undefined) ?? 'http://localhost:8000'

const router = useRouter()

async function onSubmit() {
  error.value = null

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        phone_num: phone_num.value,
        is_deliverer: isDeliverer.value,
        password: password.value,
      }),
    })

    const data = await res.json().catch(() => null)
    if (!res.ok) {
      error.value = (data && (data.detail as string)) || 'Registration failed'
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

<style scoped>
.register-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f4f6f8, #e5e7eb);
  padding: 24px;
}

.register-card {
  width: 100%;
  max-width: 460px;
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

.checkbox-field {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
}

.checkbox-field input {
  width: 18px;
  height: 18px;
}

.register-button,
.login-button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 10px;
}

.register-button {
  background-color: #374151;
  color: white;
}

.register-button:hover {
  background-color: #1f2937;
}

.login-button {
  background-color: #e5e7eb;
  color: #1f2937;
}

.login-button:hover {
  background-color: #d1d5db;
}

.error {
  color: #b91c1c;
  background: #fee2e2;
  padding: 10px;
  border-radius: 8px;
}
</style>