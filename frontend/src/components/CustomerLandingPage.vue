<template>
  <div class="page">
    <div class="page-shell">
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
              <p><strong>Order #:</strong> {{ activeOrder.id }}</p>
              <p><strong>Items:</strong> {{ activeOrder.items.map((i) => i.name).join(', ') }}</p>
              <p><strong>Total:</strong> ${{ activeOrder.total_price.toFixed(2) }}</p>
            </template>
            <p v-else>No active orders.</p>
          </div>

          <div class="panel-actions">
            <button class="secondary-btn" :disabled="!activeOrder">View Current Order</button>
          </div>
        </div>

        <div class="panel quick-actions-panel">
          <h2>Quick Actions</h2>

          <div class="action-stack">
            <button class="action-btn neutral-btn">Past Orders ({{ profile ? profile.past_orders_count : 0 }})</button>
            <button class="action-btn neutral-btn" :disabled="!activeOrder">Track Current Order</button>
            <RouterLink to="/ItemPage" class="action-btn primary-btn">
              Start New Order
            </RouterLink>
          </div>
        </div>
      </section>

      <section class="panel history-panel">
        <div class="panel-header">
          <h2>Recent Orders</h2>
        </div>

        <div class="history-list">
          <p v-if="pastOrders.length === 0" style="color: #666;">No past orders yet.</p>
          <div v-for="order in pastOrders" :key="order.id" class="history-item">
            <div>
              <p class="history-title">{{ order.dining_hall }} Dining Hall</p>
              <p class="history-meta">Order #{{ order.id }} • {{ order.status }}</p>
            </div>
            <button class="small-btn">Reorder</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const USER_ID = 1
const BASE = 'http://localhost:8000'

const profile = ref<any>(null)
const activeOrder = ref<any>(null)
const pastOrders = ref<any[]>([])

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