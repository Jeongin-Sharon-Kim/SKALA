<script setup>
import { ref, computed, watch, watchEffect } from 'vue'

// 도시 검색창에 입력한 값
const searchQuery = ref('')

// 현재 선택된 도시 정보
const selectedCityInfo = ref(null)

// 날씨 데이터 배열
const weatherList = ref([
  {
    id: 'city_01',
    name: '서울',
    temp: 28,
    status: '맑음',
  },
  {
    id: 'city_02',
    name: '수원',
    temp: 24,
    status: '비',
  },
  {
    id: 'city_03',
    name: '부산',
    temp: 26,
    status: '구름',
  },
])

// 검색어가 포함된 도시만 반환
const filteredWeatherList = computed(() => {
  return weatherList.value.filter((weather) => weather.name.includes(searchQuery.value.trim()))
})

// 검색창에 입력할 때 실행
const handleSearch = (event) => {
  searchQuery.value = event.target.value
}

// 날씨 카드를 클릭하면 선택한 도시 정보 저장
const selectCity = (weather) => {
  selectedCityInfo.value = weather
}

// 상세보기 버튼을 클릭하면 알림창 출력
const showDetail = (cityName, status) => {
  window.alert(`${cityName}의 현재 날씨는 [${status}] 상태입니다.`)
}

// 선택된 도시 정보가 변경될 때마다 실행
watch(selectedCityInfo, (newCity) => {
  console.log(`👁️ [watch 감지] 상태 값이 업데이트되었습니다. -> "${newCity?.name}" 선택됨`)
})

// 처음 실행될 때와 검색어가 변경될 때 자동 실행
watchEffect(() => {
  console.log(
    `🤖 [watchEffect 자동 호출] 현재 검색어 '${searchQuery.value}'에 매칭되는 API 데이터를 필터링합니다.`,
  )

  console.log(
    '검색 결과:',
    filteredWeatherList.value.map((weather) => weather.name),
  )
})
</script>

<template>
  <div class="weather-container">
    <h1>🌤️ 과제 2: 날씨 (컴포지션)</h1>

    <hr />

    <!-- 도시 검색 영역 -->
    <section class="search-box">
      <h3>🔍 도시 검색</h3>

      <input
        type="text"
        :value="searchQuery"
        @input="handleSearch"
        placeholder="검색할 도시 이름 입력"
      />

      <p>검색 중인 도시: {{ searchQuery }}</p>
    </section>

    <!-- 날씨 카드 영역 -->
    <section class="weather-section">
      <h3>🌆 지역별 날씨 현황</h3>

      <!-- 검색 결과가 있을 때 -->
      <div
        v-for="weather in filteredWeatherList"
        :key="weather.id"
        class="weather-card"
        @click="selectCity(weather)"
      >
        <div>
          <strong> {{ weather.name }} ({{ weather.status }}) </strong>

          <p>현재 기온: {{ weather.temp }}℃</p>

          <span v-if="weather.temp >= 25" class="hot"> 🔥 더움 (25도 이상) </span>

          <span v-else class="cool"> ❄️ 선선함 (25도 미만) </span>
        </div>

        <!-- 버튼 클릭 시 부모 카드의 클릭 이벤트 실행 방지 -->
        <button @click.stop="showDetail(weather.name, weather.status)">상세보기</button>
      </div>

      <!-- 검색 결과가 없을 때 -->
      <p v-if="filteredWeatherList.length === 0" class="empty-message">
        검색 결과와 일치하는 도시가 없습니다.
      </p>
    </section>

    <!-- 선택된 도시 표시 -->
    <div class="selected-message">
      <p v-if="selectedCityInfo">{{ selectedCityInfo.name }}이(가) 선택되었습니다.</p>

      <p v-else>카드를 클릭하거나 검색해 보세요.</p>
    </div>
  </div>
</template>

<style scoped>
.weather-container {
  width: 500px;
  margin: 30px auto;
  padding: 25px;
  border: 1px solid #ddd;
  border-radius: 10px;
}

.search-box,
.weather-section {
  margin-top: 20px;
  padding: 15px;
  background-color: #f7f7f7;
  border-radius: 8px;
}

.search-box input {
  width: 95%;
  padding: 8px;
}

.weather-card {
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin-top: 12px;
  padding: 15px;

  background-color: white;
  border: 1px solid #ddd;
  border-radius: 6px;

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
  padding: 4px 8px;
  color: white;
  background-color: #ff6b6b;
  border-radius: 4px;
  font-size: 13px;
}

.cool {
  padding: 4px 8px;
  color: white;
  background-color: #74b9ff;
  border-radius: 4px;
  font-size: 13px;
}

.selected-message {
  margin-top: 15px;
  padding: 10px;
  text-align: center;
  background-color: #e8f5e9;
  border-radius: 6px;
}

.empty-message {
  padding: 15px;
  text-align: center;
  color: #777;
}
</style>
