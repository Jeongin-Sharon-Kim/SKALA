//이벤트 모음

<script setup>
const props = defineProps({
  weather: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['select-card', 'click-detail'])

// 카드 클릭 이벤트를 부모에게 전달
const selectCard = () => {
  emit('select-card', props.weather)
}

// 상세보기 이벤트를 부모에게 전달
const clickDetail = () => {
  emit('click-detail', props.weather)
}
</script>

<template>
  <div class="weather-card" @click="selectCard">
    <div>
      <strong> {{ weather.name }} ({{ weather.status }}) </strong>

      <p>현재 기온: {{ weather.temp }}℃</p>

      <span v-if="weather.temp >= 25" class="hot"> 🔥 더움 </span>

      <span v-else class="cool"> ❄️ 선선함 </span>
    </div>

    <!-- 카드 클릭 이벤트까지 실행되지 않도록 .stop 사용 -->
    <button @click.stop="clickDetail">상세보기</button>
  </div>
</template>

<style scoped>
.weather-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.weather-card p {
  margin: 5px 0;
}

.weather-card button {
  padding: 6px 12px;
  cursor: pointer;
}

.hot {
  display: inline-block;
  padding: 4px 8px;
  color: white;
  background-color: #ff6b6b;
  border-radius: 4px;
  font-size: 13px;
}

.cool {
  display: inline-block;
  padding: 4px 8px;
  color: white;
  background-color: #74b9ff;
  border-radius: 4px;
  font-size: 13px;
}
</style>
