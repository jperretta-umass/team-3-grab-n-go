<template>
  <div class="page">
    <div class="page-shell">
      <p class="welcome-banner">
        Welcome{{ currentUsername ? `, ${currentUsername}` : '' }}
      </p>
      <h1 class="page-title">Customer Landing Page</h1>
      <p class="page-subtitle">
        Check your current order, review past orders, or start a new one.
      </p>

      <section class="top-row">
        <div class="panel current-order-panel">
          <div class="panel-header">
            <h2>Current Order Status</h2>
            <span class="status-pill">Preparing</span>
          </div>

          <div class="order-details">
            <p><strong>Dining Hall:</strong> Hampshire</p>
            <p><strong>Order #:</strong> 1024</p>
            <p><strong>Pickup Estimate:</strong> 10–15 min</p>
            <p><strong>Items:</strong> Grilled Chicken Bowl, Fruit Cup</p>
          </div>

          <div class="panel-actions">
            <button class="secondary-btn">View Current Order</button>
          </div>
        </div>

        <div class="panel quick-actions-panel">
          <h2>Quick Actions</h2>

          <div class="action-stack">
            <button class="action-btn neutral-btn">Past Orders</button>
            <button class="action-btn neutral-btn">Track Current Order</button>
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
          <div class="history-item">
            <div>
              <p class="history-title">Berkshire Dining Hall</p>
              <p class="history-meta">Order #1018 • Completed</p>
            </div>
            <button class="small-btn">Reorder</button>
          </div>

          <div class="history-item">
            <div>
              <p class="history-title">Franklin Dining Hall</p>
              <p class="history-meta">Order #1009 • Completed</p>
            </div>
            <button class="small-btn">Reorder</button>
          </div>

          <div class="history-item">
            <div>
              <p class="history-title">Worcester Dining Hall</p>
              <p class="history-meta">Order #998 • Cancelled</p>
            </div>
            <button class="small-btn">View</button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getAuthUser } from '../utils/auth'

const authUser = getAuthUser()
const currentUsername = computed(() => authUser?.username ?? '')
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

.welcome-banner {
  margin: 0 0 12px 0;
  text-align: center;
  font-size: 0.95rem;
  font-weight: 700;
  color: #4caf50;
  letter-spacing: 0.03em;
  text-transform: uppercase;
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