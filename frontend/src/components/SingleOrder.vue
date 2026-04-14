<script setup lang="ts">
defineProps<{
  msg: string;
}>();
</script>

<template>
  <div class="hello">
    <p>{{ msg }}</p>
  </div>
</template>
