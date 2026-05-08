<template>
  <div class="page">
    <div class="page-shell">
      <div class="top-bar">
        <p class="welcome-banner">
          Welcome{{ currentUsername ? `, ${currentUsername}` : '' }}
        </p>
        <div class="top-actions">
          <button
            class="switch-btn"
            type="button"
            @click="goToCustomerLanding"
          >
            Go to Customer Page
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
      <h1 class="page-title">Deliverer Landing Page</h1>
      <p class="page-subtitle">
        Check your current order, review past orders, or start a new one.
      </p>

      <section class="top-row">
        <div class="panel current-order-panel">
          <div class="panel-header">
            <h2>Current Order Status</h2>
            <span class="status-pill">{{ delivererCurrentOrder?.status ?? 'No active order' }}</span>
          </div>

          <div class="order-details">
            <p v-if="delivererCurrentOrderLoading" class="order-details-placeholder">
              Loading active order...
            </p>
            <template v-if="delivererCurrentOrder">
              <p><strong>Dining Hall:</strong> {{ delivererCurrentOrder.dining_hall }}</p>
              <p><strong>Order #:</strong> {{ delivererCurrentOrder.id }}</p>
              <p><strong>To:</strong> {{ delivererCurrentOrder.delivery_address }}</p>
              <p><strong>Items:</strong> {{ delivererCurrentOrder.items.length }} line(s)</p>
            </template>
            <p v-else-if="!delivererCurrentOrderLoading" class="order-details-placeholder">
              Claim an order on Available Orders to see it here.
            </p>
            <p v-if="delivererCurrentOrderError" class="status-error">
              {{ delivererCurrentOrderError }}
            </p>
          </div>
        </div>

        <div class="panel claim-order-panel">
          <div class="claim-order-section">
            <h3 class="claim-order-title">
              Claim New Order
            </h3>
            <RouterLink to="/DelivererPage" class="action-btn primary-btn">
              View Available Orders
            </RouterLink>
            <h3 class="claim-order-title">
              Update Current Order Status
            </h3>
            <button
              class="action-btn secondary-btn"
              type="button"
              :disabled="statusUpdating || !delivererCurrentOrder"
              @click="handleUpdateOrderStatus"
            >
              {{ statusUpdating ? 'Updating...' : nextStatusLabel }}
            </button>
            <p v-if="statusError" class="status-error">{{ statusError }}</p>
          </div>
        </div>
      </section>

      <section class="panel history-panel">
        <div class="panel-header">
          <h2>Recently Delivered Orders</h2>
        </div>

        <div class="history-list">
          <div v-if="pastOrdersLoading" class="history-item">
            <p>Loading order history...</p>
          </div>
          <div v-else-if="pastOrders.length == 0" class="history-item">
            <p>No past orders found.</p>
          </div>
          <div v-else v-for="order in pastOrders" :key="order.id" class="history-item">
            <div>
              <p class="history-title">Order to {{ order.dining_hall }}</p>
              <p class="history-meta">
                Order #{{ order.id }} - {{ order.status }}
              </p>
            </div>
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
import {
  delivererCurrentOrder,
  delivererCurrentOrderError,
  delivererCurrentOrderLoading,
  fetchDelivererCurrentOrder,
  updateOrderStatus,
  pastOrders, 
  pastOrdersLoading,
  fetchPastOrders
} from './displayScripts/Order'

const router = useRouter()
const authUser = getAuthUser()
const currentUsername = computed(() => authUser?.username ?? '')
const statusUpdating = ref(false)
const statusError = ref<string | null>(null)
const nextStatus = computed(() => {
  if (delivererCurrentOrder.value?.status === 'claimed') {
    return 'on the way'
  }

  if (delivererCurrentOrder.value?.status === 'on the way') {
    return 'delivered'
  }

  return null
})
const nextStatusLabel = computed(() => {
  if (nextStatus.value === 'on the way') {
    return 'Mark on the way'
  }

  if (nextStatus.value === 'delivered') {
    return 'Mark delivered'
  }

  return 'No active order'
})

onMounted(() => {
  fetchPastOrders()
  fetchDelivererCurrentOrder()
})

function logout() {
  clearAuthSession()
  router.replace('/Login')
}

async function handleUpdateOrderStatus() {
  const order = delivererCurrentOrder.value
  if (!order) {
    statusError.value = 'No active order. Claim one from Available Orders first.'
    return
  }

  if (!nextStatus.value) {
    statusError.value = 'This order cannot be updated from its current status.'
    return
  }

  statusError.value = null
  statusUpdating.value = true
  try {
    await updateOrderStatus(order.id, nextStatus.value)
  } catch (e) {
    statusError.value =
      e instanceof Error ? e.message : 'Failed to update order status.'
  } finally {
    statusUpdating.value = false
  }
}

function goToCustomerLanding() {
  router.push('/CustomerLanding')
}

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

.claim-order-panel {
  min-height: 280px;
}

.order-details p {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: #222;
}

.order-details-placeholder,
.status-error {
  margin: 0;
  font-size: 0.95rem;
  color: #666;
}

.status-error {
  color: #c0392b;
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

.claim-order-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.claim-order-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #111;
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