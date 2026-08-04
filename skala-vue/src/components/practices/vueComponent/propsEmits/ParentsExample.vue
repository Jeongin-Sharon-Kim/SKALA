<script setup>
import { ref } from 'vue'
import PropsEmitsChild from './PropsEmitsChild.vue'
// 상위 컴포넌트의 로컬 반응형 상태 정의
const message = ref('Parent가 보유한 초기 데이터')
// 하위 컴포넌트의 커스텀 이벤트를 수신했을 때 실행될 핸들러 함수
const handleUpdateRequest = (newValue) => {
message.value = newValue
}
</script>

<template>
<div class="parent-container">
<h2>📡 상위 컴포넌트 (Parent)</h2>
<p>
현재 로컬 데이터(State): <strong>{{ message }}</strong>
</p>
<hr />
<PropsEmitsChild :parent-data="message" @update-request="handleUpdateRequest" />
</div>
</template>