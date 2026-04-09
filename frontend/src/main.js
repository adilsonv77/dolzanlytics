import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import * as bootstrap from 'bootstrap';
import './assets/main.css'

window.bootstrap = bootstrap;

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')