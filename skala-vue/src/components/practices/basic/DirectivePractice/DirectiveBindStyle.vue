<!---v-bind실습(style binding)--->
<script setup>
import { ref } from 'vue'
const textColor = ref('purple')
const boxWidth = ref(150) // 숫자만 제어
const baseBoxStyle = ref({
  backgroundColor: '#42b883',
  height: '100px',
  transition: 'all 0.3s ease', // 부드러운 애니메이션 효과
})
</script>
<template>
  <div style="padding: 20px">
    <h2>3-2. v-bind 고급 (스타일 바인딩)</h2>
    <hr />
    <h3>1) 인라인 스타일 변수 조작 (객체 형식)</h3>
    <p :style="{ color: textColor, fontWeight: 'bold' }">이 글자의 색상은 실시간으로 바뀝니다.</p>
    <button @click="textColor = textColor === 'purple' ? 'blue' : 'purple'">글자 색상 토글</button>
    <br /><br />
    <label>박스 가로 크기(px): </label>
    <input type="number" v-model="boxWidth" step="50" />
    <br /><br />
    <h3>2) 다중 스타일 객체 조립 (배열 형식)</h3>
    <div :style="[baseBoxStyle, { width: boxWidth + 'px' }]">
      <p style="color: white; padding: 10px; text-align: center">
        가로 크기: {{ boxWidth }}px 박스
      </p>
    </div>
  </div>
</template>
