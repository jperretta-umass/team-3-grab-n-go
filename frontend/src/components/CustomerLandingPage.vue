<template>
  <div class="page">
    <div class="page-shell">
      <div class="top-bar">
        <p class="welcome-banner">
          Welcome{{ currentUsername ? `, ${currentUsername}` : '' }}
        </p>
        <div class="top-actions">
          <button
            v-if="canSwitchLanding"
            class="switch-btn"
            type="button"
            @click="goToDelivererLanding"
          >
            Go to Deliverer Page
          </button>
          <button
            class="logout-btn"
            type="button"
            @click="logout"
          >
            Logout
          </button>
        </div>
      </div>
      <h1 class="page-title">Customer Landing Page</h1>
      <p class="page-subtitle">
        Check your current order, review past orders, or start a new one.
      </p>

      <section class="top-row">
        <div class="panel current-order-panel">
          <div class="panel-header">
            <h2>Current Order Status</h2>
            <span class="status-pill">{{ activeOrder ? activeOrder.status : 'None' }}</span>
          </div>

          <div class="order-details">
            <template v-if="activeOrder">
              <p><strong>Dining Hall:</strong> {{ activeOrder.dining_hall }}</p>
              <p><strong>Delivery Address:</strong> {{ activeOrder.delivery_address || 'Not provided' }}</p>
              <p><strong>Order #:</strong> {{ activeOrder.id }}</p>
              <p><strong>Items:</strong> {{ activeOrder.items.map((i) => i.name).join(', ') }}</p>
              <p><strong>Total:</strong> ${{ activeOrder.total_price.toFixed(2) }}</p>
            </template>
            <p v-else>
              No active orders.
            </p>
          </div>
        </div>

        <div class="panel start-order-panel">
          <div class="start-order-section">
            <h3 class="start-order-title">
              Start Order
            </h3>
            <label class="hall-label">Dining Hall</label>
            <select
              v-model="hallSelection"
              class="hall-select"
            >
              <option
                value=""
                disabled
              >
                Select a dining hall
              </option>
              <option value="Hampshire">
                Hampshire
              </option>
              <option value="Berkshire">
                Berkshire
              </option>
              <option value="Franklin">
                Franklin
              </option>
              <option value="Worcester">
                Worcester
              </option>
            </select>
            <label
              class="hall-label"
              for="deliveryAddress"
            >
              Delivery Address
            </label>
            <select
              id="deliveryAddress"
              v-model="deliveryAddress"
              class="address-input"
            >
              <option
                value=""
                disabled
              >
                Select a delivery location
              </option>
              <option value="Southwest">
                Southwest
              </option>
              <option value="Honors">
                Honors
              </option>
              <option value="Central">
                Central
              </option>
              <option value="Northeast">
                Northeast
              </option>
              <option value="Orchard Hill">
                Orchard Hill
              </option>
              <option value="Sylvan">
                Sylvan
              </option>
            </select>
            <button
              class="action-btn start-order-btn"
              :disabled="!canStartOrder"
              @click="startOrder"
            >
              Start Order
            </button>
          </div>
        </div>
      </section>

      <section class="panel history-panel">
        <div class="panel-header">
          <h2>Recent Orders</h2>
        </div>

        <div class="history-list">
          <p
            v-if="pastOrders.length === 0"
            style="color: #666;"
          >
            No past orders yet.
          </p>
          <div
            v-for="order in pastOrders"
            :key="order.id"
            class="history-item"
          >
            <div>
              <p class="history-title">
                {{ order.dining_hall }} Dining Hall
              </p>
              <p class="history-meta">
                Order #{{ order.id }} • {{ order.status }}
              </p>
            </div>
            <button class="small-btn">
              Reorder
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuthSession, getAuthUser } from '../utils/auth'
import { selectedDeliveryAddress, selectedHall } from './displayScripts/menuItems'

const BASE = 'http://localhost:8000'
const router = useRouter()
const authUser = getAuthUser()
const USER_ID = authUser?.id
const currentUsername = computed(() => authUser?.username ?? '')
const canSwitchLanding = computed(() => authUser?.is_deliverer === true)
const hallSelection = ref(selectedHall.value)
const deliveryAddress = ref(selectedDeliveryAddress.value)
const canStartOrder = computed(() => Boolean(hallSelection.value && deliveryAddress.value.trim()))

function startOrder() {
  selectedHall.value = hallSelection.value
  selectedDeliveryAddress.value = deliveryAddress.value.trim()
  router.push('/ItemPage')
}

// const profile = ref<any>(null)
// const activeOrder = ref<any>(null)
// const pastOrders = ref<any[]>([])

type OrderItem = {
  menu_item_id: number
  name: string
  price: number
  quantity: number
  special_instructions: string | null
  delivery_instructions: string | null
}

type Order = {
  id: number
  dining_hall: string
  total_price: number
  status: string
  delivery_address: string | null
  created_at: string
  items: OrderItem[]
}

type CustomerProfile = {
  user_id: number
  username: string
  email: string
  phone_num: string | null
  has_deliverer_profile: boolean
  active_orders_count: number
  past_orders_count: number
}

const profile = ref<CustomerProfile | null>(null)
const activeOrder = ref<Order | null>(null)
const pastOrders = ref<Order[]>([])

function logout() {
  clearAuthSession()
  router.replace('/Login')
}

function goToDelivererLanding() {
  router.push('/DelivererLanding')
}

onMounted(async () => {
  if (!USER_ID) {
    router.replace('/Login')
    return
  }

  try {
    const [profileData, activeData, pastData] = await Promise.all([
      fetch(`${BASE}/api/customers/${USER_ID}/profile`).then(r => r.json()),
      fetch(`${BASE}/api/customers/${USER_ID}/active-orders`).then(r => r.json()),
      fetch(`${BASE}/api/customers/${USER_ID}/past-orders`).then(r => r.json()),
    ])
    profile.value = profileData
    activeOrder.value = activeData.length > 0 ? activeData[0] : null
    pastOrders.value = pastData
  } catch (e) {
    console.error('Failed to load customer data', e)
  }
})
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.page {
  min-height: 100vh;
  background: #f3f3f3;
  padding: 24px;
  font-family: Arial, sans-serif;
}

.page-shell {
  max-width: 1400px;
  margin: 0 auto;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.top-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.welcome-banner {
  margin: 0;
  text-align: center;
  font-size: 0.95rem;
  font-weight: 700;
  color: #4caf50;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}

.logout-btn {
  border: none;
  border-radius: 10px;
  background: #111;
  color: white;
  cursor: pointer;
  font-weight: 700;
  padding: 10px 16px;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.switch-btn {
  border: none;
  border-radius: 10px;
  background: #4caf50;
  color: white;
  cursor: pointer;
  font-weight: 700;
  padding: 10px 16px;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.switch-btn:hover,
.logout-btn:hover {
  transform: translateY(-1px);
  opacity: 0.95;
}

.page-title {
  margin: 0 0 8px 0;
  text-align: center;
  font-size: 3.4rem;
  font-weight: 800;
  color: #111;
}

.page-subtitle {
  margin: 0 0 24px 0;
  text-align: center;
  font-size: 1.05rem;
  color: #555;
}

.top-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}

.panel {
  background: white;
  border-radius: 14px;
  padding: 22px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.panel-header h2,
.history-panel h2 {
  margin: 0;
  font-size: 2rem;
  color: #111;
}

.current-order-panel {
  min-height: 280px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.start-order-panel {
  min-height: 280px;
}

.order-details p {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: #222;
}

.status-pill {
  background: #f39c12;
  color: white;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 0.9rem;
}

.panel-actions {
  margin-top: 20px;
}

.action-btn,
.secondary-btn,
.small-btn {
  border: none;
  border-radius: 10px;
  padding: 12px 16px;
  font-weight: 700;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  transition: transform 0.15s ease, opacity 0.15s ease;
}

.action-btn:hover,
.secondary-btn:hover,
.small-btn:hover {
  transform: translateY(-1px);
  opacity: 0.95;
}

.primary-btn {
  background: #4caf50;
  color: white;
}

.neutral-btn,
.secondary-btn {
  background: #e4e4e4;
  color: #111;
}

.history-panel {
  min-height: 320px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 18px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
  padding: 16px 0;
  border-bottom: 1px solid #ececec;
}

.history-item:last-child {
  border-bottom: none;
}

.history-title {
  margin: 0 0 6px 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: #111;
}

.history-meta {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.small-btn {
  background: #4caf50;
  color: white;
  min-width: 90px;
}

.start-order-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.start-order-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #111;
}

.hall-label {
  font-weight: 600;
  color: #333;
}

.hall-select {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1rem;
  cursor: pointer;
}

.address-input {
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 1rem;
}

.start-order-btn {
  background: #4caf50;
  color: white;
}

.start-order-btn:disabled {
  background: #b0b0b0;
  color: #e0e0e0;
  cursor: not-allowed;
  transform: none;
  opacity: 1;
}

@media (max-width: 900px) {
  .top-bar {
    align-items: stretch;
    flex-direction: column;
  }

  .page-title {
    font-size: 2.3rem;
  }

  .top-row {
    grid-template-columns: 1fr;
  }

  .panel-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .history-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>