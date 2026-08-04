import './assets/main.css'

import { createApp } from 'vue'
import {createPinia} from 'pinia'

import App from './App.vue'
import router from './router'

// Vue 앱 생성 후 router 연결
const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router)

app.mount('#app')

