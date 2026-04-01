<template>
  <div class="page">
    <header class="top-bar">
      <button class="back-btn">&lt; BACK</button>
      <h1>Grab &amp; Go Menu</h1>
      <div class="hall">Dining Hall:
        <select class="red-select" v-model="selectedHall">
          <option value="Hampshire">Hampsire</option>
          <option value="Berkshire">Berkshire</option>
          <option value="Franklin">Franklin</option>
          <option value="Worcester">Worcester</option>
        </select>
      </div>
    </header>

    <section class="filters">
      <span class="filter-label">Filters:</span>

      <div class="filter-group">
        <label for="mealType">Meal Type:</label>
        <select id="mealType" class="green-select" v-model="selectedMeal">
          <option value="">All</option>
          <option value="breakfast">Breakfast</option>
          <option value="lunch">Lunch</option>
          <option value="dinner">Dinner</option>
        </select>
      </div>

      <div class="filter-group">
        <label for="dietType">Diet:</label>
        <select id="dietType" class="orange-select" v-model="selectedDiet">
          <option value="">None</option>
          <option value="no-peanuts">No Peanuts</option>
          <option value="vegan">Vegan</option>
          <option value="gluten-free">Gluten Free</option>
          <option value="vegetarian">Vegetarian</option>
        </select>
      </div>

      <button class="cart-tab-btn">Open Cart</button>
    </section>

    <main class="content">
      <section class="panel fixed-panel">
        <h2>Entrées</h2>
        <div class="panel-scroll">
          <ul v-if="filteredEntrees.length">
            <li v-for="item in filteredEntrees" :key="item.id">
              <div class="item-info">
                <span class="item-name">{{ item.name }}</span>
                <span class="item-meta">{{ formatTags(item) }}</span>
              </div>
              <button class="add-btn green" @click="addToCart(item)">Add</button>
            </li>
          </ul>
          <p v-else>No entrées match your filters.</p>
        </div>
      </section>

      <section class="panel fixed-panel cart-panel">
        <h2>Cart: ${{ cartTotal }}</h2>
        <div class="panel-scroll">
          <ul v-if="cart.length">
            <li v-for="item in cart" :key="item.cartId">
              <span>{{ item.name }}</span>
              <button class="remove-btn orange" @click="removeFromCart(item.cartId)">
                Remove
              </button>
            </li>
          </ul>
          <p v-else>Your cart is empty.</p>
        </div>
      </section>
    </main>

    <section class="panel fixed-panel bottom-panel">
      <h2>Snacks and Drinks</h2>
      <div class="panel-scroll">
        <ul v-if="filteredSnacksAndDrinks.length">
          <li v-for="item in filteredSnacksAndDrinks" :key="item.id">
            <div class="item-info">
              <span class="item-name">{{ item.name }}</span>
              <span class="item-meta">{{ formatTags(item) }}</span>
            </div>
            <button class="add-btn green" @click="addToCart(item)">Add</button>
          </li>
        </ul>
        <p v-else>No snacks or drinks match your filters.</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type MealType = 'breakfast' | 'lunch' | 'dinner'
type DietType = 'no-peanuts' | 'vegan' | 'gluten-free' | 'vegetarian'
type DiningHall = 'Hampshire' | 'Berkshire' | 'Franklin' | 'Worcester' 

type MenuItem = {
  id: number
  name: string
  mealType: MealType[]
  diets: DietType[]
  category: 'entree' | 'snack' | 'drink'
  diningHall: DiningHall
}

type CartItem = {
  cartId: number
  id: number
  name: string
  price: number
}

const selectedMeal = ref('')
const selectedDiet = ref('')
const selectedHall = ref('Hampshire')

const menuItems = ref<MenuItem[]>([])
const cart = ref<CartItem[]>([])
const loading = ref(false)
const error = ref('')

let nextCartId = 0

async function loadMenuItems(): Promise<void> {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch('http://localhost:8000/menu-items')

    if (!response.ok) {
      throw new Error(`Failed to fetch menu items: ${response.status}`)
    }

    const data: MenuItem[] = await response.json()
    menuItems.value = data
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unknown error occurred'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  void loadMenuItems()
})

function matchesFilters(item: MenuItem): boolean {
  const mealMatches =
    !selectedMeal.value || item.mealType.includes(selectedMeal.value as MealType)

  const dietMatches =
    !selectedDiet.value || item.diets.includes(selectedDiet.value as DietType)

  const hallMatches = item.diningHall === selectedHall.value

  return mealMatches && dietMatches && hallMatches
}

const entrees = computed(() => {
  return menuItems.value.filter(item => item.category === 'entree')
})

const snacksAndDrinks = computed(() => {
  return menuItems.value.filter(item => item.category === 'snack' || item.category === 'drink')
})

const filteredEntrees = computed(() => {
  return entrees.value.filter(matchesFilters)
})

const filteredSnacksAndDrinks = computed(() => {
  return snacksAndDrinks.value.filter(matchesFilters)
})

const cartTotal = computed(() => {
  return cart.value.reduce((total, item) => total + item.price, 0).toFixed(2)
})

function addToCart(item: MenuItem): void {
  cart.value.push({
    cartId: nextCartId++,
    id: item.id,
    name: item.name,
    price: item.category === 'entree' ? 13.25 : 3.00,
  })
}

function removeFromCart(cartId: number): void {
  cart.value = cart.value.filter(item => item.cartId !== cartId)
}

function formatTags(item: MenuItem): string {
  const meals = item.mealType.join(', ')
  const diets = item.diets.length ? item.diets.join(', ') : 'none'
  return `Meal: ${meals} | Diet: ${diets}`
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  padding: 20px;
  font-family: Arial, sans-serif;
  background: #f7f7f7;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.top-bar h1 {
  margin: 0;
  font-size: 1.7rem;
}

.hall {
  font-weight: 600;
}

.back-btn,
.cart-tab-btn,
.add-btn,
.remove-btn {
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 600;
  cursor: pointer;
}

.back-btn,
.cart-tab-btn {
  background: #e4e4e4;
}

.green {
  background: #4caf50;
  color: white;
}

.orange {
  background: #f39c12;
  color: white;
}

.filters {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.filter-label {
  font-weight: 700;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-weight: 600;
}

.filter-group select {
  padding: 10px 12px;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
}

.green-select {
  background: #4caf50;
  color: white;
}

.orange-select {
  background: #f39c12;
  color: white;
}

.red-select {
  background: red;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
}

.content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.panel {
  background: white;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.fixed-panel {
  height: 360px;
  display: flex;
  flex-direction: column;
}

.bottom-panel {
  height: 400px;
}

.panel h2 {
  margin-top: 0;
  margin-bottom: 14px;
  flex-shrink: 0;
}

.panel-scroll {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  min-height: 0;
  padding-right: 6px;
}

.panel ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.panel li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #ececec;
}

.panel li:last-child {
  border-bottom: none;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.item-name {
  font-weight: 600;
}

.item-meta {
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 850px) {
  .content {
    grid-template-columns: 1fr;
  }

  .top-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .fixed-panel,
  .bottom-panel {
    height: 300px;
  }
}
</style>