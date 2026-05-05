<template>
  <div class="page">
    <div class="panel">
      <h1 class="success-text">
        Payment Successful!
      </h1>
      <p>Your order has been placed and sent to the dining hall.</p>
      <button
        class="add-btn green"
        @click="$router.push('/')"
      >
        Return Home
      </button>
    </div>
  </div>
</template>
  
  <style scoped>
  .page {
    min-height: 100vh;
    padding: 20px;
    background: #f7f7f7;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: Arial, sans-serif;
  }
  .panel {
    background: white;
    border-radius: 12px;
    padding: 40px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  }
  .success-text {
    color: #4caf50;
    margin-top: 0;
  }
  .green {
    background: #4caf50;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 20px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 20px;
  }
  </style>