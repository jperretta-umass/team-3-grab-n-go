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

//Same as dhalls
const letters = ["B", "H", "W", "F"];

//SW, Honors, Central, NE, OHill, Sylvan
const dorms = ["SW", "Honors", "Central", "NE", "Ohill", "Sylvan"];
</script>

<template>
  <h1> Order ID: {{ orderObj.oId }} </h1>
  <p> Dining Hall: {{dHalls[orderObj.dId]}} </p>
  <p> Main Dish: {{mains[orderObj.mainId[0]]}} </p>
  <p> Sides: {{sides[orderObj.sideId[0]]}} </p>
  <p> Price ${{orderObj.price}} </p>
  <p> Special Instructions: {{orderObj.specialInstructions}} </p>
  <p> Delivery Instructions: {{orderObj.deliveryInstructions}} </p>
  <button class="border border-gray-400 p-3 text-center font-semibold bg-red-700" @click="$emit('close')"> 
    Cancel 
  </button>
  <button class="border border-gray-400 p-3 text-center font-semibold bg-green-700" @click="$emit('accept')">
    Accept
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