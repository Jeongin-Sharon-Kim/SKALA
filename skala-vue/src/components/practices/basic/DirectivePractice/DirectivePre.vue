<!-----v-pre실습-->
<script setup>
import { ref } from 'vue'
const message = ref('안녕하세요!')
</script>
<template>
  <div style="padding: 20px">
    <h1>7. v-pre 디렉티브 학습</h1>
    <hr />
    <p>일반 출력: {{ message }}</p>
    <p v-pre>v-pre 출력: {{ message }}</p>
  </div>
</template>
