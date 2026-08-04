import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Vue 앱 생성 후 router 연결
createApp(App)
    .use(router)
    .mount('#app')