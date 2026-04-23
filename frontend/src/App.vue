<script setup lang="ts">
import LoginForm from "./components/LoginForm.vue";
import RegisterForm from "./components/RegisterForm.vue";
import UserProfile from "./components/UserProfile.vue";
</script>

<template>
  <div id="app">
    <h1>Grab-n-Go</h1>

    <UserProfile />
    <LoginForm />
    <RegisterForm />
  </div>
</template>