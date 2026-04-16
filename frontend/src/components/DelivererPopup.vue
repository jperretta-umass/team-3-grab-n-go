<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'
import {Order} from "./Order.ts"

defineProps({
    orderObj: Order
})

defineEmits("['close', 'accept']")

//Berk 0, Hamp 1, Woo 2, Frank 3
const dHalls = ["Berkshire", "Hampshire", "Wocester", "Franklin"];

//Burger 0, Pizza 1, Salad 2
const mains = ["Burger", "Pizza", "Salad"];

//Fries 0, Chips 1, Fruit 2
const sides = ["Fries", "Chips", "Fruit"];

//SW, Honors, Central, NE, OHill, Sylvan
//const dorms = ["SW", "Honors", "Central", "NE", "Ohill", "Sylvan"];
</script>

<template>
  <h1 class="text-2xl font-sans font-bold text-gray-900"> Order ID: {{ orderObj.oId }} </h1>
  <p class="pt-1"> Dining Hall: {{dHalls[orderObj.dId]}} </p>
  <p class="pt-1"> Main Dish: {{mains[orderObj.mainId[0]]}} </p>
  <p class="pt-1"> Sides: {{sides[orderObj.sideId[0]]}} </p>
  <p class="pt-1"> Price ${{orderObj.price}} </p>
  <p class="pt-1"> Special Instructions: {{orderObj.specialInstructions}} </p>
  <p class="pt-1"> Delivery Instructions: {{orderObj.deliveryInstructions}} </p>
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