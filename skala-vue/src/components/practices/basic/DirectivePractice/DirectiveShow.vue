
<!---v-show--->
<script setup>
import { ref } from 'vue'
const isVisible = ref(true)
</script>
<template>
<div style="padding: 20px">
<h1>5. v-show 디렉티브 학습</h1>
<hr />
<h3>현재 상태: {{ isVisible ? '보임(true)' : '숨김(false)' }}</h3>
<button @click="isVisible = !isVisible">화면 토글하기</button>
<br />
<div v-show="isVisible" class="box">
<h3>v-show 상자</h3>
<p>조건이 false가 되면 CSS display: none이 붙습니다.</p>
</div>
</div>
</template>
<style scoped>
.box {
padding: 15px; margin-top: 15px; color: white; border-radius: 5px;background-color: #3498db; /* 파란색 */
}
</style>
