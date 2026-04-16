<template>
    <header>
        <h2> Register Page </h2>
        <div>
            <label for="email">Email:</label>
                <input
                id="email"
                v-model="email"
                type="text"
                placeholder="Enter Email"
                class="border rounded px-3 py-2"
                />
        </div>
        <div>
            <label for="password">Password:</label>
                <input
                id="password"
                v-model="password"
                type="text"
                placeholder="Enter password"
                class="border rounded px-3 py-2"
                />
        </div>
        <div>
            <button type="submit" class="login-button"> 
                Login 
            </button>
        </div>
    </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const email = ref('')
const password = ref('')


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
</style>