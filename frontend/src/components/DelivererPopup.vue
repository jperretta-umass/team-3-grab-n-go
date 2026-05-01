<script setup lang="ts">
import {Order} from "./displayScripts/Order"
import { items, MealType, MenuItem, DietType, DiningHall } from "./displayScripts/menuItems";

const props = defineProps<{
  orderObj: Order
}>()

defineEmits<{
  close: []
  accept: []
}>()

function matchItems(item : MenuItem) : boolean {
  if(item.diningHall === props.orderObj.dining_hall) {
    for(const currentUserItem of props.orderObj.items){
      if(currentUserItem.menu_item_id === item.id) return true;
    }
  }
  return false;
}

const currentOrderItems = items.value.filter(matchItems);

</script>

<template>
  <h1 class="text-2xl font-sans font-bold text-gray-900"> Order ID: {{ orderObj.id }} </h1>
  <p class="pt-1"> User ID: {{ orderObj.user_id }} </p>
  <p class="pt-1"> Dining Hall: {{ orderObj.dining_hall }} </p>
  <p class="pt-1"> Status: {{ orderObj.status }} </p>
  <p class="pt-1"> Created At: {{ orderObj.created_at.slice(11,16) }} </p> <!--Slice to keep time just in hh:mm format, no other data needed-->
  <p class="pt-1"> Total Price: ${{ orderObj.total_price }} </p>
  <div class="pt-1">
    <p class="font-semibold">Items:</p>
    <ul class="list-disc pl-5">
      <li v-for="curItem in orderObj.items" :key="curItem.menu_item_id">
        {{ currentOrderItems }} x {{ curItem.quantity }}
      </li>
    </ul>
  </div>
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