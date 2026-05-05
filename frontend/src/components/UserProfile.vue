<script setup lang="ts">
import { ref, onMounted } from "vue";

type ProfileUser = {
  username: string
  email: string
}

const user = ref<ProfileUser | null>(null);
const message = ref("");
const oldPassword = ref("");
const newPassword = ref("");
const showChangePassword = ref(false);

async function fetchUser() {
  const token = localStorage.getItem("token");

  if (!token) {
    user.value = null;
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      user.value = null;
      return;
    }

    user.value = await response.json();
  } catch (error) {
    console.error(error);
    message.value = "Failed to load user";
  }
}

function handleLogout() {
  localStorage.removeItem("token");
  user.value = null;
  message.value = "Logged out";
}

async function changePass() {
  const token = localStorage.getItem("token");

  if (!token) {
    message.value = "You must be logged in to change your password";
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/auth/change-password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        old_password: oldPassword.value,
        new_password: newPassword.value,
      }),
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      message.value = data?.detail || "Failed to change password";
      return;
    }

    message.value = "Password changed successfully";
    oldPassword.value = "";
    newPassword.value = "";
    showChangePassword.value = false;
  } catch {
    message.value = "Network error. Is the backend running?";
  }
}

onMounted(() => {
  fetchUser();
});
</script>

<template>
  <div class="profile-container">
    <div v-if="user">
      <h2>Welcome, {{ user.username }}</h2>
      <p>{{ user.email }}</p>

      <button @click="showChangePassword = !showChangePassword">
        Change Password
      </button>

      <form
        v-if="showChangePassword"
        class="password-form"
        @submit.prevent="changePass"
      >
        <input
          v-model="oldPassword"
          type="password"
          placeholder="Current password"
          required
        >

        <input
          v-model="newPassword"
          type="password"
          placeholder="New password"
          required
        >

        <button type="submit">
          Save New Password
        </button>
      </form>
      <button @click="handleLogout">
        Logout
      </button>
    </div>

    <div v-else>
      <p>Not logged in</p>
    </div>

    <p v-if="message">
      {{ message }}
    </p>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 400px;
  margin: 24px auto;
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 10px;
  text-align: center;
}

.password-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 16px;
}

.password-form input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

button {
  margin-top: 10px;
  padding: 8px 12px;
  cursor: pointer;
}
</style>
