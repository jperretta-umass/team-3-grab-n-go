import { createApp } from "vue";
import App from "./App.vue";
import { createRouter, createWebHistory } from "vue-router";


import DelivererPage from "./components/DelivererPage.vue"; 
import SingleOrder from "./components/SingleOrder.vue";
import HomeView from "./components/HomeView.vue"


const router = createRouter({
    history: createWebHistory(),
    routes: [
       { path: '/', component: HomeView },
        {path: "/DelivererPage", component: DelivererPage },
        {path: "/SingleOrder", component: SingleOrder }
    ]
});

const app = createApp(App);
app.use(router)
app.mount('#app')
