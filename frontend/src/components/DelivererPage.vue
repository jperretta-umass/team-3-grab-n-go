<script setup lang="ts">

const headers = [
  "Southwest",
  "Honors",
  "Central",
  "Northeast",
  "Orchard Hill",
  "Sylvan",
];

const orderRows = [
  ["SW Order #1", "Honors Order #1", "Central Order #1", "NE Order #1", "OHill Order #1", "Sylvan Order #1"],
  ["SW Order #2", "Honors Order #2", "Central Order #2", "NE Order #2", "OHill Order #2", "Sylvan Order #2"],
  ["SW Order #3", "Honors Order #3", "Central Order #3", "NE Order #3", "OHill Order #3", "Sylvan Order #3"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
  ["SW Order", "Honors Order", "Central Order", "NE Order", "OHill Order", "Sylvan Order"],
];

const cellColors = [
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
];
</script>

<template>
  <section class="w-full p-4">
    <table class="w-full min-h-[800px] table-fixed border-collapse border border-gray-300">
      <thead>
        <tr class="bg-gray-200">
          <th
            v-for="header in headers"
            :key="header"
            class="border border-gray-300 p-3 text-center font-medium"
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
            :class="`font-semibold p-3 text-center `"
            :style="{ backgroundColor: cellColors[rowIndex][columnIndex] }"
          >
            {{ order }}
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

