<!---
<script setup>
import WeatherHomeView from '../views/WeatherHomeView.vue/index.js'
</script>

<template>
  <WeatherHo--> meView />


<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🌤️ 과제 4: 라우터 활용</h1>

      <!-- 페이지 이동 메뉴 -->
      <nav class="nav">
        <RouterLink to="/">🌤️ 날씨 대시보드</RouterLink>
        <RouterLink to="/about">📘 서비스 소개</RouterLink>
      </nav>
    </header>

    <main class="main">
      <!-- 현재 URL에 해당하는 페이지 표시 -->
      <RouterView />
    </main>
  </div>
</template>

<style>
/* 전체 공통 스타일 */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
  background-color: #f4f7fb;
  color: #263238;
  font-family:
    Pretendard, Arial, sans-serif;
}

button,
input {
  font: inherit;
}

button {
  cursor: pointer;
}

a {
  color: inherit;
  text-decoration: none;
}

.app {
  width: 100%;
  min-height: 100vh;
}

.header {
  padding: 24px 20px 0;
  text-align: center;
}

.header h1 {
  margin: 0 0 22px;
  font-size: 28px;
}

.nav {
  display: flex;
  justify-content: center;
  gap: 16px;
  border-bottom: 1px solid #dce4ec;
}

.nav a {
  padding: 12px 18px;
  color: #7b8794;
  font-weight: 700;
  border-bottom: 3px solid transparent;
}

/* 현재 선택된 메뉴 */
.nav a.router-link-exact-active {
  color: #2196f3;
  border-bottom-color: #2196f3;
}

.main {
  width: min(900px, calc(100% - 32px));
  margin: 25px auto;
}
</style>