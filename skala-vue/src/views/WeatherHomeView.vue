<!-- 메인 날씨 대시보드 화면 -->

<script setup>
import { ref, computed, watch, watchEffect } from 'vue'
import { useRouter } from 'vue-router'

import SearchBar from '../components/exercise/SearchBar.vue'
import BaseDashboardCard from '../components/exercise/BaseDashboardCard.vue'
import WeatherCard from '../components/exercise/WeatherCard.vue'

// Router 사용
const router = useRouter()

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
    } ,
])

// 검색어가 포함된 도시만 반환
const filteredWeatherList = computed(() => {
    return weatherList.value.filter((weather) =>
        weather.name.includes(searchQuery.value.trim())
    )
})

// SearchBar에서 전달받은 검색어 저장
const updateSearchQuery = (newQuery) => {
    searchQuery.value = newQuery
}

// WeatherCard에서 전달받은 도시 정보 저장
const selectCity = (weather) => {
    selectedCityInfo.value = weather
}

// 상세보기 버튼 클릭 시 상세 페이지로 이동
const showDetail = (weather) => {
    router.push({
        name: 'weather-detail',
        params: {
        id: weather.id,
        },
    })
}

// 선택된 도시가 변경될 때 실행
watch(selectedCityInfo, (newCity) => {
    console.log(
        `👁️ [watch 감지] 상태 값이 업데이트되었습니다. -> "${newCity?.name}" 선택됨`
    )
})

// 처음 실행될 때와 검색어가 변경될 때 자동 실행
watchEffect(() => {
console.log(
    `🤖 [watchEffect 자동 호출] 현재 검색어 '${searchQuery.value}'에 매칭되는 API 데이터를 필터링합니다.`
)

    console.log(
    '검색 결과:',
    filteredWeatherList.value.map((weather) => weather.name)
    )
})
</script>

<template>
    <div class="weather-container">
    <h1>🌤️ 과제 4: 라우터 적용</h1>

    <hr />

    <!-- 검색 영역 -->
    <BaseDashboardCard>
        <SearchBar
            :search-query="searchQuery"
            @update-query="updateSearchQuery"
        />
        </BaseDashboardCard>

        <!-- 날씨 현황 영역 -->
        <h3>🌆 지역별 날씨 현황</h3>

        <BaseDashboardCard
        v-for="weather in filteredWeatherList"
        :key="weather.id"
        >
        <WeatherCard
        :weather="weather"
        @select-card="selectCity"
        @click-detail="showDetail"
        />
        </BaseDashboardCard>

        <!-- 검색 결과가 없을 때 -->
        <p
        v-if="filteredWeatherList.length === 0"
        class="empty-message"
        >
        검색 결과와 일치하는 도시가 없습니다.
        </p>

        <!-- 선택된 도시 표시 -->
        <div class="selected-message">
        <p v-if="selectedCityInfo">
            {{ selectedCityInfo.name }}이(가) 선택되었습니다.
        </p>

        <p v-else>
            카드를 클릭하거나 검색해 보세요.
        </p>
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

.weather-container h1 {
    font-size: 22px;
}

.weather-container h3 {
    margin-top: 20px;
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