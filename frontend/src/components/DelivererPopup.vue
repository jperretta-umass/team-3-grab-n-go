<script setup lang="ts">
import {Order} from "./displayScripts/Order"

defineProps<{
  orderObj: Order
}>()

defineEmits<{
  close: []
  accept: []
}>()

function formatCreatedAt(value: string) {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return value
  }

  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(date)
}

</script>

<template>
  <h1 class="text-2xl font-sans font-bold text-gray-900">
    Order ID: {{ orderObj.id }}
  </h1>
  <p class="pt-1">
    User ID: {{ orderObj.user_id }}
  </p>
  <p class="pt-1">
    Dining Hall: {{ orderObj.dining_hall }}
  </p>
  <p class="pt-1">
    Delivery Address: {{ orderObj.delivery_address }}
  </p>
  <p class="pt-1">
    Status: {{ orderObj.status }}
  </p>
  <p class="pt-1">
    Created At: {{ formatCreatedAt(orderObj.created_at) }}
  </p>
  <p class="pt-1">
    Total Price: ${{ orderObj.total_price }}
  </p>
  <div class="pt-1">
    <p class="font-semibold">
      Items:
    </p>
    <ul class="list-disc pl-5">
      <li
        v-for="item in orderObj.items"
        :key="item.menu_item_id"
      >
        Menu Item {{ item.menu_item_id }} x {{ item.quantity }}
      </li>
    </ul>
  </div>
  <nav class="flex gap-3 justify-center pt-3">
    <button
      class="rounded-lg p-2 text-center text-slate-900 font-semibold bg-red-400"
      @click="$emit('close')"
    >
      Cancel
    </button>
    <button
      class="rounded-lg p-2 text-center text-slate-900 font-semibold bg-green-400"
      @click="$emit('accept')"
    >
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
