<template>
  <div class="min-h-screen bg-[#f3f3f3] p-6 font-sans">
    <div class="max-w-[1400px] mx-auto">
      <h1 class="m-0 mb-2 text-center text-[3.4rem] font-extrabold text-[#111]">
        Customer Landing Page
      </h1>
      <p class="m-0 mb-6 text-center text-[1.05rem] text-[#555]">
        Check your current order, review past orders, or start a new one.
      </p>

      <section class="grid grid-cols-[2fr_1fr] gap-[18px] mb-[18px] max-[900px]:grid-cols-1">
        <div class="bg-white rounded-[14px] p-[22px] shadow-[0_2px_8px_rgba(0,0,0,0.08)] min-h-[280px] flex flex-col justify-between">
          <div class="flex justify-between items-center gap-3 mb-[18px] max-[900px]:flex-col max-[900px]:items-start">
            <h2 class="m-0 text-[2rem] text-[#111]">Current Order Status</h2>
            <span class="bg-[#f39c12] text-white font-bold px-[14px] py-2 rounded-full text-[0.9rem]">{{ activeOrder ? activeOrder.status : 'None' }}</span>
          </div>

          <div>
            <template v-if="activeOrder">
              <p class="m-0 mb-3 text-base text-[#222]"><strong>Dining Hall:</strong> {{ activeOrder.dining_hall }}</p>
              <p class="m-0 mb-3 text-base text-[#222]"><strong>Order #:</strong> {{ activeOrder.id }}</p>
              <p class="m-0 mb-3 text-base text-[#222]"><strong>Items:</strong> {{ activeOrder.items.map((i) => i.name).join(', ') }}</p>
              <p class="m-0 mb-3 text-base text-[#222]"><strong>Total:</strong> ${{ activeOrder.total_price.toFixed(2) }}</p>
            </template>
            <p v-else>
              No active orders.
            </p>
          </div>

          <div class="mt-5">
            <button
              class="border-none rounded-[10px] px-4 py-3 font-bold cursor-pointer inline-block text-center transition-transform duration-150 hover:-translate-y-px hover:opacity-95 bg-[#e4e4e4] text-[#111] disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!activeOrder"
            >
              View Current Order
            </button>
          </div>
        </div>

        <div class="bg-white rounded-[14px] p-[22px] shadow-[0_2px_8px_rgba(0,0,0,0.08)] min-h-[280px]">
          <h2 class="m-0 text-[2rem] text-[#111]">Quick Actions</h2>

          <div class="flex flex-col gap-[14px] mt-5">
            <button class="border-none rounded-[10px] px-4 py-3 font-bold cursor-pointer text-center transition-transform duration-150 hover:-translate-y-px hover:opacity-95 bg-[#e4e4e4] text-[#111]">
              Past Orders ({{ profile ? profile.past_orders_count : 0 }})
            </button>
            <button
              class="border-none rounded-[10px] px-4 py-3 font-bold cursor-pointer text-center transition-transform duration-150 hover:-translate-y-px hover:opacity-95 bg-[#e4e4e4] text-[#111] disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="!activeOrder"
            >
              Track Current Order
            </button>
          </div>

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
            <button
              class="action-btn start-order-btn"
              :disabled="!hallSelection"
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
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { selectedHall } from './displayScripts/menuItems'

const USER_ID = 1
const BASE = 'http://localhost:8000'

const router = useRouter()
const hallSelection = ref('')

function startOrder() {
  selectedHall.value = hallSelection.value
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

onMounted(async () => {
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
.quick-actions-panel h2,
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

.quick-actions-panel {
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

.action-stack {
  display: flex;
  flex-direction: column;
  gap: 14px;
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
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-top: 1px solid #ececec;
  padding-top: 16px;
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