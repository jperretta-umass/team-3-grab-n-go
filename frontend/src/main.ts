import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";
import './style.css'


import DelivererPage from "./components/DelivererPage.vue"; 
import SingleOrder from "./components/SingleOrder.vue";
import HomeView from "./components/HomeView.vue"
import ItemPage from "./components/ItemPage.vue"
<<<<<<< HEAD
import Login from "./components/Login.vue"
import Register from "./components/Register.vue"
=======
import CustomerLandingPage from "./components/CustomerLandingPage.vue";

>>>>>>> fa19b05 (Add customer landing page prototype with routing)


const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: HomeView },
        { path: "/customer", component: CustomerLandingPage },
        {path: "/DelivererPage", component: DelivererPage },
        {path: "/SingleOrder", component: SingleOrder },
        {path: "/ItemPage", component: ItemPage },
        {path: "/Register", component: Register },
        {path: "/Login", component: Login }
    ]
});

const app = createApp(App);
app.use(router)
app.mount('#app')
