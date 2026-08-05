<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 날씨 메인 페이지로 이동
const moveToHome = () => {
  router.push('/')
}
</script>

<template>
  <div class="not-found-container">
    <div class="icon">☀️ ❓</div>

    <h2>페이지를 찾을 수 없습니다.</h2>

    <p>
      요청하신 주소가 존재하지 않거나<br />
      잘못된 주소입니다.
    </p>

    <button type="button" @click="moveToHome">날씨 메인으로 이동</button>
  </div>
</template>

<style scoped>
.not-found-container {
  width: 450px;
  margin: 70px auto;
  padding: 50px 30px;
  text-align: center;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgb(0 0 0 / 10%);
}

.icon {
  margin-bottom: 20px;
  font-size: 50px;
}

h2 {
  margin-bottom: 15px;
  font-weight: bold;
}

p {
  color: #777;
  line-height: 1.7;
}

button {
  margin-top: 15px;
  padding: 10px 18px;
  color: white;
  background-color: #2196f3;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}
</style>
