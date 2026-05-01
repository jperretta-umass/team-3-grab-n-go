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
import Success from "./components/SuccessPage.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
       { path: '/', component: HomeView },
        {path: "/DelivererPage", component: DelivererPage },
        {path: "/SingleOrder", component: SingleOrder },
        {path: "/ItemPage", component: ItemPage },
        {path: "/Register", component: Register },
        {path: "/Login", component: Login },
        { path: "/success", component: Success }
    ]
});

const app = createApp(App);
app.use(router)
app.mount('#app')
