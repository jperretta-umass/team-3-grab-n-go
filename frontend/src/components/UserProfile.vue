<script setup lang="ts">
import { ref, onMounted } from "vue";

const user = ref<any>(null);
const message = ref("");

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

onMounted(() => {
  fetchUser();
});
</script>

<template>
  <div class="profile-container">
    <div v-if="user">
      <h2>Welcome, {{ user.username }}</h2>
      <p>{{ user.email }}</p>

      <button @click="handleLogout">Logout</button>
    </div>

    <div v-else>
      <p>Not logged in</p>
    </div>

    <p v-if="message">{{ message }}</p>
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

button {
  margin-top: 10px;
  padding: 8px 12px;
  cursor: pointer;
}
</style>