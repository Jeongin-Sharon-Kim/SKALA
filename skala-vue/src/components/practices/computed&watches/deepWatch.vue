<script setup>
import { ref, watch } from 'vue'
const user = ref({
name: '홍길동'
,
age: 20,
})
const logDeep = ref('아직 반응 없음')
const logTarget = ref('아직 반응 없음')
watch(user, (newVal) => {
// newVal과 oldVal의 주소값이 같아서 두 인자가 똑같은 값을 가집니다.
logDeep.value = `[deep 감지] 누군가 변경됨! 현재 이름: ${newVal.name}, 나이: ${newVal.age}`
},
{ deep: true },
)
watch(() => user.value.age,(newAge, oldAge) => {
// 특정 원시값만 추적하므로 이전 값(oldAge)이 칼같이 보존됩니다.
logTarget.value = `[타겟 감지] 나이가 ${oldAge}세 ➡️ ${newAge}세로 변경됨!`
},
)
</script>

<template>
<div style="padding: 20px">
<h2>6. ref 객체/배열 감시의 정석</h2>
<hr />
<div class="box">
<h3>👨‍💻 회원 데이터 조작 panel</h3>
<p>이름: {{ user.name }} / 나이: {{ user.age }}세</p>
<button @click="user.name =
'이순신'">이름만 변경</button> &nbsp;
<button @click="user.age++">나이만 변경 (age++)</button>
</div>
<div class="box monitor">
<h3>👁️‍🗨️ 1) deep: true 모니터 (전체 감시)</h3>
<p>{{ logDeep }}</p>
</div>
<div class="box monitor target">
<h3>🎯 2) 화살표 함수 모니터 (나이만 타겟 감시)</h3>
<p>{{ logTarget }}</p>
</div>
</div>
</template>