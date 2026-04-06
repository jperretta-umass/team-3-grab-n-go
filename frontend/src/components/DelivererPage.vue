<script setup lang="ts">
import { ref } from "vue"
import DelivererPopup from './DelivererPopup.vue'
import {Order} from "./Order.ts"

const order0 = new Order(0, 0, 12, 150, 15.00, "12:00", [1], [0,1,1,2], "None", "None");
const order1 = new Order(1, 1, 10, 16, 30.00, "1:00", [2], [0,1,1,2,2,2,2,0], "None", "None");
const order2 = new Order(2, 2, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");
const order3 = new Order(3, 0, 12, 150, 15.00, "12:00", [2], [0,1,1,2], "None", "None");
const order4 = new Order(4, 1, 10, 16, 30.00, "1:00", [1], [0,1,1,2,2,2,2,0], "None", "None");
const order5 = new Order(5, 2, 1, 37, 15.00, "12:00", [0], [0,2,1,2], "None", "None");

const headers = [
  "Southwest",
  "Honors",
  "Central",
  "Northeast",
  "Orchard Hill",
  "Sylvan",
];



const cellColors = ref([
  ["red", "lightblue", "red", "yellow", "yellow", "lightblue"],
  ["yellow", "lightblue", "lightgreen", "yellow", "red", "yellow"],
  ["lightblue", "yellow", "yellow", "lightblue", "red", "lightgreen"],
  ["red", "lightblue", "red", "yellow", "yellow", "lightblue"],
  ["lightblue", "yellow", "yellow", "lightblue", "red", "lightgreen"],
  ["yellow", "lightblue", "lightgreen", "yellow", "lightgreen", "yellow"],
  ["lightblue", "yellow", "yellow", "lightblue", "lightblue", "lightgreen"],
  ["yellow", "lightblue", "lightgreen", "yellow", "red", "yellow"],
  ["red", "lightblue", "red", "yellow", "yellow", "lightblue"],
  ["lightblue", "yellow", "yellow", "lightblue", "red", "lightgreen"],
  ["yellow", "red", "lightgreen", "yellow", "lightgreen", "yellow"],
  ["lightblue", "yellow", "yellow", "lightblue", "lightblue", "lightgreen"],
  ["yellow", "lightblue", "lightgreen", "yellow", "red", "yellow"],
  ["red", "lightblue", "red", "yellow", "yellow", "lightblue"],
  ["lightblue", "red", "yellow", "lightblue", "red", "lightgreen"],
  ["yellow", "lightblue", "lightgreen", "yellow", "lightgreen", "yellow"],
]);

//Berk 0, Hamp 1, Woo 2, Frank 3
const dHalls = ["Berkshire", "Hampshire", "Wocester", "Franklin"];

const colors = ["red", "green", "blue", "yellow"];

//Burger 0, Pizza 1, Salad 2
const mains = ["Burger", "Pizza", "Salad"];

//Fries 0, Chips 1, Fruit 2
const sides = ["Fries", "Chips", "Fruit"];

//Same as dhalls
const letters = ["B", "H", "W", "F"];


//SW, Honors, Central, NE, OHill, Sylvan
const dorms = ["SW", "Honors", "Central", "NE", "Ohill", "Sylvan"];



const popupOpen = ref(false);
const popOrderName = ref(order0);

function handleCellClick(row: number, col: number) {
  const originalColor = cellColors.value[row][col];
  cellColors.value[row][col] = "white";
  setTimeout(() => {
    cellColors.value[row][col] = originalColor
  }, 200);
  popOrderName.value = orderRows[row][col];
  popupOpen.value = true;
}





const orderRows = [
  [order0, order1, order2, order3, order4, order5],
  [order0, order1, order2, order3, order4, order5],
  [order0, order1, order2, order3, order4, order5],
  [order0, order1, order2, order3, order4, order5],
];

</script>

<template>
  <div class="modal" v-show="popupOpen">
    <div>
      <DelivererPopup
        :orderObj="popOrderName"
        @close="popupOpen=false"
      />
    </div>
  </div>
  <section class="w-full p-4">
    <table class="w-full min-h-[800px] table-fixed border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-200">
          <th
            v-for="header in headers"
            :key="header"
            class="border border-gray-400 p-3 text-center font-medium bg-gray-200"
          >
            {{ header }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in orderRows" :key="`row-${rowIndex}`">
          <td
            v-for="(order, columnIndex) in row"
            :key="`${rowIndex}-${columnIndex}`"
            class="border border-gray-400 p-3 text-center font-semibold"
            :style="{ backgroundColor: cellColors[rowIndex][columnIndex] }"
            @click="handleCellClick(rowIndex, columnIndex)"
          >
            {{ dorms[order.dormId] }}
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
  padding: 10px;
  border-radius: 25px;
}
</style>