<template>
  <header>
    <h1>My Delivery App</h1>
    <nav>
      <!-- These will now ONLY show when the URL is "/" -->
      <RouterLink to="/SingleOrder">
        Order Details
      </RouterLink>
      <RouterLink to="/DelivererPage">
        Deliverer Table
      </RouterLink>
      <RouterLink to="/ItemPage">
        Item Table
      </RouterLink>
    </nav>
  </header>

  <div>Welcome to the Home Page!</div>
</template>