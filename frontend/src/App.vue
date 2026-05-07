<!-- Works like a container of all pages -->
<script setup lang = "ts">
import {onMounted} from 'vue';
import {items, fetchMenuItems } from './components/displayScripts/menuItems.ts';
onMounted(async () => {
  if (items.value.length === 0) {
    await fetchMenuItems()
  }
})
</script>

<template>
  <router-view />
</template>
