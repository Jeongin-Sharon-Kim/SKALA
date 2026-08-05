import { createRouter, createWebHistory } from 'vue-router'
import CurrentLocationView from '@/views/CurrentLocationView.vue'

// Lazy Loading 방식으로 페이지 불러오기
const WeatherHomeView = () => import('../views/WeatherHomeView.vue')
const WeatherAboutView = () => import('../views/WeatherAboutView.vue')
const WeatherDetailView = () => import('../views/WeatherDetailView.vue')
const NotFoundView = () => import('../views/NotFoundView.vue')

const routes = [
  {
    path: '/',
    name: 'home',
    component: WeatherHomeView,
  },
  {
    path: '/about',
    name: 'about',
    component: WeatherAboutView,
  },
  {
    path: '/current-location',
    name: 'current-location',
    component: CurrentLocationView,
  },
  {
    // id 값에 따라 다른 도시 상세 페이지 표시
    path: '/weather/:id',
    name: 'weather-detail',
    component: WeatherDetailView,
  },
  {
    // 위 주소에 해당하지 않는 모든 경로 처리
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
  },
]

const router = createRouter({
  // 일반적인 URL 형식 사용
  history: createWebHistory(),

  routes,

  // 페이지 이동 시 화면 위로 이동
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
