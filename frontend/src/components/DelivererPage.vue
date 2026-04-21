<script setup lang="ts">
import { ref } from "vue"
import DelivererPopup from './DelivererPopup.vue'
import {Order} from "./displayScripts/Order"

const order0 = new Order(0, 0, 12, 150, 15.00, "12:00", [1], [0,1,1,2], "None", "None");
const order1 = new Order(1, 1, 10, 16, 30.00, "1:00", [2], [0,1,1,2,2,2,2,0], "None", "None");
const order2 = new Order(2, 2, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");
const order3 = new Order(3, 3, 12, 150, 15.00, "12:00", [2], [0,1,1,2], "None", "None");
const order4 = new Order(1, 4, 10, 16, 30.00, "1:00", [1], [0,1,1,2,2,2,2,0], "None", "None");
const order5 = new Order(0, 5, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");
const order6 = new Order(3, 0, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");
const order7 = new Order(1, 1, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");
const order8 = new Order(0, 2, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");
const order9 = new Order(1, 3, 12, 150, 15.00, "12:00", [2], [0,1,1,2], "None", "None");
const order10 = new Order(2, 4, 10, 16, 30.00, "1:00", [1], [0,1,1,2,2,2,2,0], "None", "None");
const order11 = new Order(1, 5, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");


const headers = [
  "Southwest",
  "Honors",
  "Central",
  "Northeast",
  "Orchard Hill",
  "Sylvan",
];

//Berk 0, Hamp 1, Woo 2, Frank 3
//const dHalls = ["Berkshire", "Hampshire", "Worcester", "Franklin"];

const colors = ["red", "lightgreen", "lightblue", "yellow"];

//Burger 0, Pizza 1, Salad 2
//const mains = ["Burger", "Pizza", "Salad"];

//Fries 0, Chips 1, Fruit 2
//const sides = ["Fries", "Chips", "Fruit"];



//SW, Honors, Central, NE, OHill, Sylvan
const dorms = ["Prince Hall", "Oak Hall", "Central Hall", "NE Apartment", "Ohill", "Sylvan"];


const popupOpen = ref(false);
const popOrderName = ref(order0);
const curInd = ref(0);
const curCol = ref(0);

function handleCellClick(order: Order, currentIndex : number, currentColumn : number) {
  popOrderName.value = order;
  popupOpen.value = true;
  curInd.value = currentColumn;
  curCol.value = currentIndex;
}

const orderRows = ref([
  [order0, order6, order0, order6, order0, order0, order0, order6, order0, order0, order0, order0],
  [order1, order1, order7, order1, order1, order7],
  [order8, order2, order2, order2, order8, order2],
  [order3, order9, order3, order3, order3, order3],
  [order10, order4, order4],
  [order5,order5,order11,order5,order5,order11]
]);

const longest = ref(orderRows.value.reduce((num, arr) => Math.max(num, arr.length), 0));

const claimNotifVis = ref(false);
// code for alert found here! https://v1.tailwindcss.com/components/alerts

function handleAccept() {
  claimNotifVis.value = true;
  setTimeout(() => {
      claimNotifVis.value = false;
    }, 3000);
  orderRows.value[curInd.value].splice(curCol.value,1);
  popupOpen.value = false;
}

</script>

<template>
  <header class="bg-white shadow-lg">
    <nav aria-label="Global" class="flex mx-auto items-center justify-between p-5 lg:px-7">
      <div class="flex lg:flex-1">
        <a href="/" class="-m-1.5 p-1.5">
          <span class="sr-only">MinuteMeals</span>
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/UMass_Amherst_athletics_logo.svg/1280px-UMass_Amherst_athletics_logo.svg.png" alt="" class="h-8 w-auto" />
        </a>
      </div><div class="flex lg:flex-15">
        <a class="text-4xl/6 font-sans font-semibold text-gray-900">Available Orders</a>
      </div>
      <div>
        <a class="text-lg/6 font-sans font-semibold text-gray-900">My Account</a>
      </div>
    </nav>
  </header>
  <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative shadow-md" role="alert" v-if="claimNotifVis">
    <strong class="font-bold">Order Claimed!</strong>
    <span class="block sm:inline"> You have claimed this order. </span>
  </div>
  <div class="modal flex justify-between p-5 lg:px-7" v-show="popupOpen">
    <div>
      <DelivererPopup
        :orderObj="popOrderName"
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
        <tr v-for="i in longest" :key="i">
          <td
            v-for="(col, j) in orderRows"
            :key="`${i}-${j}`"
            class="rounded-xl overflow-hidden p-3 text-center font-semibold shadow-md"
            :style="col[i - 1] ? { backgroundColor: colors[col[i - 1].dId] } : { backgroundColor : 'lightgrey'}"
            @click="col[i - 1] && handleCellClick(col[i - 1], i - 1, j)"
          >
            {{ col[i - 1] ? dorms[col[i - 1].dormId] : ' ' }}
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