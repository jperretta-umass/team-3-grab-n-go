import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import { fetchAuthUser, getPostAuthRoute } from "./utils/auth";
import './style.css'


import DelivererPage from "./components/DelivererPage.vue"; 
import SingleOrder from "./components/SingleOrder.vue";
import HomeView from "./components/HomeView.vue"
import ItemPage from "./components/ItemPage.vue"
import Login from "./components/Login.vue"
import Register from "./components/Register.vue"
import CustomerLandingPage from "./components/CustomerLandingPage.vue";
import Success from "./components/SuccessPage.vue"
import DelivererLanding from "./components/DelivererLandingPage.vue"


const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: HomeView },
        { path: "/Register", component: Register },
        { path: "/Login", component: Login },

        { path: "/CustomerLanding", component: CustomerLandingPage, meta: { requiresAuth: true } },
        { path: "/DelivererLanding", component: DelivererLanding, meta: { requiresAuth: true, requiresDeliverer: true } },
        { path: "/DelivererPage", component: DelivererPage, meta: { requiresAuth: true, requiresDeliverer: true } },
        { path: "/SingleOrder", component: SingleOrder, meta: { requiresAuth: true } },
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
app.use(router)
app.mount('#app')
