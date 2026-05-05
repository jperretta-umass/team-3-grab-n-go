import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import './style.css'

import DelivererPage from "./components/DelivererPage.vue"; 
import ItemPage from "./components/ItemPage.vue"
import Login from "./components/Login.vue"
import Register from "./components/Register.vue"
import CustomerLandingPage from "./components/CustomerLandingPage.vue";
import Success from "./components/SuccessPage.vue";
import UserProfile from "./components/UserProfile.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', redirect: "/Login" },
        { path: "/Register", component: Register },
        { path: "/Login", component: Login },

        { path: "/CustomerLanding", component: CustomerLandingPage, meta: { requiresAuth: true } },
        { path: "/DelivererLanding", component: DelivererLanding, meta: { requiresAuth: true, requiresDeliverer: true } },
        { path: "/DelivererPage", component: DelivererPage, meta: { requiresAuth: true, requiresDeliverer: true } },
        { path: "/ItemPage", component: ItemPage, meta: { requiresAuth: true } },
        { path: "/success", component: Success, meta: { requiresAuth: true } },
    ]
});

router.beforeEach(async (route) => {
    const user = await fetchAuthUser();
    const isLoggedIn = !!user;
  
    if (route.meta.requiresAuth && !isLoggedIn) {
      return "/Login";
    }

    if (route.meta.requiresDeliverer && !user?.is_deliverer) {
      return "/CustomerLanding";
    }

    if (isLoggedIn && (route.path === "/Login" || route.path === "/Register")) {
      return getPostAuthRoute(user);
    }
  });

const app = createApp(App);
app.use(router);
app.mount('#app');
