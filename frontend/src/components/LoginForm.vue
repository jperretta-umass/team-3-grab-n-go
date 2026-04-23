<script setup lang="ts">
import { ref } from "vue";

const username = ref("");
const password = ref("");
const message = ref("");
const loading = ref(false);

async function handleLogin() {
  message.value = "";
  loading.value = true;

  try {
    const formData = new URLSearchParams();
    formData.append("username", username.value);
    formData.append("password", password.value);

    const response = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      message.value = data.detail || "Login failed";
      return;
    }

    localStorage.setItem("token", data.access_token);
    message.value = "Login successful";
  } catch (error) {
    console.error(error);
    message.value = "Could not connect to server";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="login-container">
    <h2>Login</h2>

    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">Username</label>
        <input id="username" v-model="username" type="text" required />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" v-model="password" type="password" required />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Logging in..." : "Login" }}
      </button>
    </form>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 24px auto;
  padding: 24px;
  border: 1px solid #ccc;
  border-radius: 12px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

input {
  padding: 10px;
  font-size: 16px;
}

button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}
</style>