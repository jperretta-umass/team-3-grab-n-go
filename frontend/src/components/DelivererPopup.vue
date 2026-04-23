<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import {Order} from "./Order.ts"

defineProps({
    orderObj: Order
})

defineEmits("['close', 'accept']")

//Berk 0, Hamp 1, Woo 2, Frank 3
const dHalls = ["Berkshire", "Hampshire", "Wocester", "Franklin"];

//SW, Honors, Central, NE, OHill, Sylvan
//const dorms = ["SW", "Honors", "Central", "NE", "Ohill", "Sylvan"];
</script>

<template>
  <h1 class="text-2xl font-sans font-bold text-gray-900"> Order ID: {{ orderObj.oId }} </h1>
  <p class="pt-1"> Dining Hall: {{dHalls[orderObj.dId]}} </p>
  <p class="pt-1"> Items: {{orderObj.items[0].menu_item_id}} </p>
  <p class="pt-1"> Price ${{orderObj.price}} </p>
  <nav class="flex gap-3 justify-center pt-3">
    <button class="rounded-lg p-2 text-center text-slate-900 font-semibold bg-red-400" @click="$emit('close')"> 
      Cancel 
    </button>
    <button class="rounded-lg p-2 text-center text-slate-900 font-semibold bg-green-400" @click="$emit('accept')">
      Accept
    </button>
  </nav>
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