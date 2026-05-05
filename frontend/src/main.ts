import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import './style.css'

import DelivererPage from "./components/DelivererPage.vue";
import SingleOrder from "./components/SingleOrder.vue";
import HomeView from "./components/HomeView.vue";
import ItemPage from "./components/ItemPage.vue";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import CustomerLandingPage from "./components/CustomerLandingPage.vue";
import Success from "./components/SuccessPage.vue";
import UserProfile from "./components/UserProfile.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: "/customer", component: CustomerLandingPage },
    { path: "/DelivererPage", component: DelivererPage },
    { path: "/SingleOrder", component: SingleOrder },
    { path: "/ItemPage", component: ItemPage },
    { path: "/Register", component: Register },
    { path: "/register", redirect: "/Register" },
    { path: "/Login", component: Login },
    { path: "/login", redirect: "/Login" },
    { path: "/UserProfile", component: UserProfile },
    { path: "/success", component: Success },
  ],
});

const app = createApp(App);
app.use(router);
app.mount('#app');
