import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import './style.css'


import DelivererPage from "./components/DelivererPage.vue"; 
import SingleOrder from "./components/SingleOrder.vue";
import HomeView from "./components/HomeView.vue"
import ItemPage from "./components/ItemPage.vue"
import Login from "./components/Login.vue"
import Register from "./components/Register.vue"
import CustomerLandingPage from "./components/CustomerLandingPage.vue";
import DelivererLanding from "./components/DelivererLandingPage.vue"


const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: HomeView },
        { path: "/Register", component: Register },
        { path: "/Login", component: Login },

        { path: "/CustomerLanding", component: CustomerLandingPage, meta: { requiresAuth: true, role: "customer" } },
        { path: "/DelivererLanding", component: DelivererLanding, meta: { requiresAuth: true, role: "deliverer" } },
        { path: "/DelivererPage", component: DelivererPage, meta: { requiresAuth: true, role: "deliverer" } },
        { path: "/SingleOrder", component: SingleOrder, meta: { requiresAuth: true, role: "customer" } },
        { path: "/ItemPage", component: ItemPage, meta: { requiresAuth: true, role: "deliverer" } },
    ]
});

router.beforeEach((route) => {
    const auth = localStorage.getItem("auth");
    const isLoggedIn = !!auth;
  
    if (route.meta.requiresAuth && !isLoggedIn) {
      return "/Login";
    }
    //re routes to related landing page from /login if already logged in
    /*if (isLoggedIn && (route.path === "/Login" || route.path === "/Register")) {
      const user = JSON.parse(auth!);
      return user.is_deliverer ? "/DelivererLanding" : "/CustomerLanding";
    }*/
  });

const app = createApp(App);
app.use(router)
app.mount('#app')
