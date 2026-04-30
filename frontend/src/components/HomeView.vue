<template>
  <header>
    <h1>My Delivery App</h1>
    <nav>
      <br />
      <!-- These will now ONLY show when the URL is "/" -->
      <RouterLink to="/SingleOrder">--Order Details</RouterLink>
      <br />
      <RouterLink to="/DelivererPage">--Deliverer Table</RouterLink>
      <br />
      <RouterLink to="/ItemPage">--Item Table</RouterLink>
      <br />
      <RouterLink to="/CustomerLanding">--Customer Landing</RouterLink>
      <br />
      <RouterLink to="/DelivererLanding">--Deliver Landing</RouterLink>
    </nav>
  </header>
  <br />
  <div>Welcome to the Home Page!</div>
</template>