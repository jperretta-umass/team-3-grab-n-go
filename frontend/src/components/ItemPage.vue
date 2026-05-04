<template>
  <div class="page">
    <header class="top-bar">
      <button
        class="back-btn"
        @click="goHome"
      >
        &lt; BACK
      </button>
      <h1>Grab &amp; Go Menu</h1>
      <button
        class="start-over-btn"
        @click="startOver"
      >
        Start Over
      </button>
    </header>

    <section class="filters">
      <span class="filter-label">Filters:</span>

      <div class="filter-group">
        <label for="mealType">Meal Type:</label>
        <select
          id="mealType"
          v-model="selectedMeal"
          class="green-select"
        >
          <option value="">
            All
          </option>
          <option value="breakfast">
            Breakfast
          </option>
          <option value="lunch">
            Lunch
          </option>
          <option value="dinner">
            Dinner
          </option>
        </select>
      </div>

      <div class="filter-group">
        <label for="dietType">Diet:</label>
        <select
          id="dietType"
          v-model="selectedDiet"
          class="orange-select"
        >
          <option value="">
            None
          </option>
          <option value="no-peanuts">
            No Peanuts
          </option>
          <option value="vegan">
            Vegan
          </option>
          <option value="gluten-free">
            Gluten Free
          </option>
          <option value="vegetarian">
            Vegetarian
          </option>
        </select>
      </div>

      <button class="cart-tab-btn">
        Open Cart
      </button>
    </section>

    <main class="content">
      <section class="panel fixed-panel">
        <h2>Entrées</h2>
        <div class="panel-scroll">
          <p v-if="loading">
            Loading menu...
          </p>
          <p
            v-if="error"
            class="error"
          >
            {{ error }}
          </p>
          <ul v-if="filteredEntrees.length">
            <li
              v-for="item in filteredEntrees"
              :key="item.id"
            >
              <div class="item-info">
                <span class="item-name">{{ item.name }} - ${{ item.price }}</span>
                <span class="item-meta">{{ formatTags(item) }}</span>
              </div>
              <button
                class="add-btn green"
                @click="addToCart(item)"
              >
                Add
              </button>
            </li>
          </ul>
          <p v-else>
            No entrées match your filters.
          </p>
        </div>
      </section>

      <section class="panel fixed-panel cart-panel">
        <h2>Cart: ${{ cartTotal }}</h2>
        <div class="panel-scroll">
          <ul v-if="cart.length">
            <li
              v-for="item in cart"
              :key="item.cartId"
            >
              <span>{{ item.name }}</span>
              <button
                class="remove-btn orange"
                @click="removeFromCart(item.cartId)"
              >
                Remove
              </button>
            </li>
          </ul>
          <p v-else>
            Your cart is empty.
          </p>
        </div>
        <button v-if="cart.length" class="add-btn green" @click="handleCheckout">Checkout</button>
      </section>
    </main>

    <section class="panel fixed-panel bottom-panel">
      <h2>Snacks and Drinks</h2>
      <div class="panel-scroll">
        <ul v-if="filteredSnacksAndDrinks.length">
          <li
            v-for="item in filteredSnacksAndDrinks"
            :key="item.id"
          >
            <div class="item-info">
              <span class="item-name">{{ item.name }}</span>
              <span class="item-meta">{{ formatTags(item) }}</span>
            </div>
            <button
              class="add-btn green"
              @click="addToCart(item)"
            >
              Add
            </button>
          </li>
        </ul>
        <p v-else>
          No snacks or drinks match your filters.
        </p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { selectedMeal, selectedDiet, loading, error, filteredEntrees, filteredSnacksAndDrinks, cart, cartTotal, formatTags, addToCart, removeFromCart, fetchMenuItems} from './displayScripts/menuItems'

const router = useRouter()

function goHome() {
  router.push('/')
}

function startOver() {
  router.push('/customer')
}

onMounted(fetchMenuItems)

async function handleCheckout() {
  try {
    // Format local cart to send to the backend
    const itemsToCheckout = cart.value.map((item) => ({
      menu_item_id: item.id,
      quantity: 1 //  cart adds items individually as separate rows
    }))

    const response = await fetch("http://localhost:8000/api/payments/create-checkout-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        user_id: 1, // Hardcoded
        items: itemsToCheckout 
      }),
    })

    const data = await response.json()

    if (data.url) {
      // Redirects the browser to the stripepage
      window.location.href = data.url
    } else {
      console.error("Stripe Session Error:", data.error)
      alert("Checkout failed. Please try again.")
    }
  } catch (error) {
    console.error("Network Error:", error)
  }
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

.back-btn,
.cart-tab-btn,
.add-btn,
.remove-btn,
.start-over-btn {
  border: none;
  border-radius: 10px;
  padding: 10px 14px;
  font-weight: 600;
  cursor: pointer;
}

.back-btn,
.cart-tab-btn,
.start-over-btn {
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
