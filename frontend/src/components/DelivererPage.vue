<script setup lang="ts">
import { computed, onMounted, ref } from "vue"
import DelivererPopup from './DelivererPopup.vue'
import { Order, fetchOrders, orders, ordersError, ordersLoading, claimOrder } from "./displayScripts/Order"


const headers = [
  "Southwest",
  "Honors",
  "Central",
  "Northeast",
  "Orchard Hill",
  "Sylvan",
];

const diningHallColors: Record<string, string> = {
  Berkshire: "red",
  Hampshire: "lightgreen",
  Worcester: "lightblue",
  Franklin: "yellow",
};

const deliveryAddressColumnMap: Record<string, number> = headers.reduce(
  (map, header, index) => ({
    ...map,
    [header.toLowerCase()]: index,
  }),
  {} as Record<string, number>
);

function getDeliveryAddressColumn(deliveryAddress: string) {
  const normalizedAddress = deliveryAddress.toLowerCase()
  const matchedHeader = headers.find((header) =>
    normalizedAddress.includes(header.toLowerCase())
  )

  return matchedHeader
    ? deliveryAddressColumnMap[matchedHeader.toLowerCase()]
    : headers.length - 1
}

const popupOpen = ref(false);
const popOrderName = ref<Order | null>(null);
const curInd = ref(0);
const curCol = ref(0);

function handleCellClick(order: Order, currentIndex : number, currentColumn : number) {
  popOrderName.value = order;
  popupOpen.value = true;
  curInd.value = currentColumn;
  curCol.value = currentIndex;
}

const orderRows = computed(() => {
  const columns: Order[][] = headers.map(() => [])
  const overflowColumn = headers.length - 1

  for (const order of orders.value) {
    const mappedColumn = getDeliveryAddressColumn(order.delivery_address) ?? overflowColumn
    const safeColumn = mappedColumn < headers.length ? mappedColumn : overflowColumn
    columns[safeColumn].push(order)
  }

  return columns
});

const longest = computed(() => orderRows.value.reduce((num, arr) => Math.max(num, arr.length), 0));

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

const claimNotifVis = ref(false);
// code for alert found here! https://v1.tailwindcss.com/components/alerts

async function handleAccept() {
  if (!popOrderName.value) {
    return
  }

  try {
    const claimedOrder = await claimOrder(popOrderName.value.id)
    popOrderName.value.status = claimedOrder.status
  } catch (e) {
    alert(e instanceof Error ? e.message : 'Failed to claim order.')
    return
  }

  claimNotifVis.value = true;
  setTimeout(() => {
    claimNotifVis.value = false;
  }, 3000);
  const updatedOrders = [...orders.value]
  const targetColumn = orderRows.value[curInd.value] ?? []
  const targetOrder = targetColumn[curCol.value]
  if (targetOrder) {
    const index = updatedOrders.findIndex((order) => order.id === targetOrder.id)
    if (index >= 0) {
      updatedOrders.splice(index, 1)
      orders.value = updatedOrders
    }
  }
  popupOpen.value = false;
}

onMounted(fetchOrders)

</script>

<template>
  <header class="bg-white shadow-lg">
    <nav
      aria-label="Global"
      class="flex mx-auto items-center justify-between p-5 lg:px-7"
    >
      <div class="flex lg:flex-1">
        <a
          href="/"
          class="-m-1.5 p-1.5"
        >
          <span class="sr-only">MinuteMeals</span>
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/UMass_Amherst_athletics_logo.svg/1280px-UMass_Amherst_athletics_logo.svg.png"
            alt=""
            class="h-8 w-auto"
          >
        </a>
      </div><div class="flex lg:flex-15">
        <a class="text-4xl/6 font-sans font-semibold text-gray-900">Available Orders</a>
      </div>
      <div>
        <a class="text-lg/6 font-sans font-semibold text-gray-900">My Account</a>
      </div>
    </nav>
  </header>
  <div
    v-if="claimNotifVis"
    class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative shadow-md"
    role="alert"
  >
    <strong class="font-bold">Order Claimed!</strong>
    <span class="block sm:inline"> You have claimed this order. </span>
  </div>
  <div
    v-if="ordersLoading"
    class="px-4 py-2 text-sm text-slate-700"
  >
    Loading orders...
  </div>
  <div
    v-if="ordersError"
    class="px-4 py-2 text-sm text-red-700"
  >
    {{ ordersError }}
  </div>
  <div
    v-if="popupOpen && popOrderName"
    class="modal flex justify-between p-5 lg:px-7"
  >
    <div>
      <DelivererPopup
        :order-obj="popOrderName"
        @close="popupOpen=false"
        @accept="handleAccept"
      />
    </div>
  </div>
  <section class="w-full p-4">
    <table class="border-separate border-spacing-2 w-full min-h-[800px] table-fixed border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-200">
          <th
            v-for="header in headers"
            :key="header"
            class="border border-gray-400 p-3 text-center font-medium bg-gray-200 shadow-sm"
          >
            {{ header }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="i in longest"
          :key="i"
        >
          <td
            v-for="(col, j) in orderRows"
            :key="`${i}-${j}`"
            class="rounded-xl overflow-hidden p-3 text-center font-semibold shadow-md"
            :style="col[i - 1]
              ? {
                backgroundColor: diningHallColors[col[i - 1].dining_hall] ?? 'lightgrey'
              }
              : { backgroundColor: 'lightgrey' }"
            @click="col[i - 1] && handleCellClick(col[i - 1], i - 1, j)"
          >
            <div
              v-if="col[i - 1]"
              class="leading-tight"
            >
              <div>Order #{{ col[i - 1].id }}</div>
              <div>User {{ col[i - 1].user_id }}</div>
              <div>From: {{ col[i - 1].dining_hall }}</div>
              <div>To: {{ col[i - 1].delivery_address }}</div>
              <div>${{ col[i - 1].total_price.toFixed(2) }}</div>
              <div>{{ formatCreatedAt(col[i - 1].created_at) }}</div>
              <div>Items: {{ col[i - 1].items.length }}</div>
            </div>
            <span v-else />
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<style> 

.modal {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  background-color: rgba(0, 0, 0, 0.3);
  justify-content: center;
  align-items: center;
}

.modal > div {
  position: fixed;
  background-color: #ffff;
  padding: 25px;
  border-radius: 25px;
  box-shadow: 5px 5px 10px rgba(0,0,0,0.5);
}
</style>