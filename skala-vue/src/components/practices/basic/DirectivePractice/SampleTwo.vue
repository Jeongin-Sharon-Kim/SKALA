<script setup>
import {ref} from 'vue'
let normalCount = ref(0)
const vueCount = ref(0)
const welcomeMessage = 'Welcome to Skala-Vue'
</script>

<template>
    <h1>{{ welcomeMessage }}</h1>
    <p>{{ welcomeMessage.toUpperCase() }}</p>
    <p>{{ 'Random number: ' + Math.ceil(Math.random() * 100) }}</p>
    <h2>일반 변수 클릭: {{ normalCount }}</h2>
    <button @click="normalCount++">일반 변수 증가</button>
    <br />
    <h2>Vue 반응성 변수 클릭: {{ vueCount }}</h2>
    <button @click="vueCount++">Vue 변수 증가</button>

</template>