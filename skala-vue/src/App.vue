<script setup>
import { RouterLink, RouterView } from 'vue-router'
import UnitToggler from './components/exercise/UnitToggler.vue'

</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🌤️ 오늘의 날씨</h1>

      <!-- 메뉴와 단위 변경 버튼을 같은 줄에 배치 -->
      <div class="top-bar">
        <nav class="nav">
          <RouterLink to="/">
            🌤️ 날씨 대시보드
          </RouterLink>

          <RouterLink to="/about">
            ℹ️ 서비스 소개
          </RouterLink>
        </nav>

        <UnitToggler />
      </div>
    </header>

    <main class="main">
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
  font-family: Pretendard, Arial, sans-serif;
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
  background-color: rgb(251, 249, 209);
}

/* 제목과 메뉴 영역 */
.header {
  width: 500px;
  margin: 25px auto 0;
}

.header h1 {
  margin: 0 0 15px;
  font-size: 22px;
}

/* 메뉴와 단위 설정을 같은 줄에 배치 */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #dce4ec;
}

/* 왼쪽 메뉴 */
.nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 상세보기 */
.nav a {
  padding: 10px 8px;
  color: #7b8794;
  font-size: 13px;
  font-weight: 700;
  border-bottom: 3px solid transparent;
}

/* 현재 선택된 메뉴 */
.nav a.router-link-exact-active {
  color: #2196f3;
  border-bottom-color: #2196f3;
}

/* 현재 Router 페이지 */
.main {
  width: 550px;
  margin: 15px auto 30px;
}
</style>