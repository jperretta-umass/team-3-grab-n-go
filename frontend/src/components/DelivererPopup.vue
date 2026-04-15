<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

defineProps({
    orderNumber: String,
    content: String
})

defineEmits("['close']")

</script>
<template>
  <h1> {{ orderNumber }} </h1>
  <p> {{ content }} </p>
  <button class="popButton" @click="$emit('close')"> 
    Close 
  </button>
</template>

<style>

.popButton {
  background-color: #a0a0a0;
  padding: 5px 15px;
  border-radius: 5px;
  cursor: pointer;
  align: center;
}

</style>