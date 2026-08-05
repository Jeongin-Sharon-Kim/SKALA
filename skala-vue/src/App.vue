<script setup>
import { RouterLink, RouterView } from 'vue-router'
import UnitToggler from './components/exercise/UnitToggler.vue'
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🌤️ 매일의 날씨</h1>

      <div class="top-bar">
        <nav class="nav">
          <RouterLink to="/"> 🌤️ 날씨 대시보드 </RouterLink>

          <RouterLink to="/current-location"> 📍 내 위치 날씨 </RouterLink>

          <RouterLink to="/about"> ℹ️ 서비스 소개 </RouterLink>
        </nav>

        <div class="unit-area">
          <UnitToggler />
        </div>
      </div>
    </header>

    <main class="main">
      <RouterView />
    </main>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
}

html,
body,
#app {
  width: 100%;
  min-height: 100%;
  margin: 0;
}

body {
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

/* 전체 상단 영역 */
.header {
  width: calc(100% - 40px);
  max-width: 1400px;
  margin: 25px auto 0;
}

.header h1 {
  margin: 0 0 20px;
  font-size: 32px;
}

/* 메뉴와 온도 토글러를 한 줄에 배치 */
.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 30px;
  width: 100%;
  border-bottom: 1px solid #dce4ec;
}

/* 메뉴 영역 */
.nav {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.nav a {
  padding: 12px 10px;
  color: #7b8794;
  font-size: 16px;
  font-weight: 700;
  white-space: nowrap;
  border-bottom: 3px solid transparent;
}

.nav a.router-link-exact-active {
  color: #2196f3;
  border-bottom-color: #2196f3;
}

/* 온도 토글러가 줄어들거나 아래로 내려가지 않게 함 */
.unit-area {
  flex-shrink: 0;
  padding-bottom: 8px;
}

/* 페이지 출력 영역 */
.main {
  width: 100%;
  margin: 15px auto 30px;
}

/* 작은 화면에서만 세로 배치 */
@media (max-width: 700px) {
  .header {
    width: calc(100% - 24px);
    margin-top: 15px;
  }

  .header h1 {
    font-size: 26px;
  }

  .top-bar {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
    padding-bottom: 12px;
  }

  .nav {
    width: 100%;
    overflow-x: auto;
  }

  .nav a {
    padding: 10px 6px;
    font-size: 14px;
  }

  .unit-area {
    padding-bottom: 0;
  }
}
</style>
