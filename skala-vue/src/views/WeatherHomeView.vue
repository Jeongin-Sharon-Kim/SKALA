<!-- 메인 날씨 대시보드 화면 -->

<script setup>
import { ref, computed, watch, watchEffect, onMounted } from 'vue'

import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { fetchWeatherByCity } from '@/services/weatherApi.js'

import SearchBar from '../components/exercise/SearchBar.vue'
import BaseDashboardCard from '../components/exercise/BaseDashboardCard.vue'
import WeatherCard from '../components/exercise/WeatherCard.vue'

// Router 사용
const router = useRouter()

// 검색창 입력값
const searchQuery = ref('')

// 선택된 도시 정보
const selectedCityInfo = ref(null)

// API 요청 상태
const isLoading = ref(false)

// API에서 받은 날씨 목록
const weatherList = ref([])

// 사용자가 저장한 도시 목록
const savedCities = ref([])

// 날씨 목록 반환
const filteredWeatherList = computed(() => {
  return weatherList.value
})

// SearchBar에서 전달받은 검색어 저장
const updateSearchQuery = (newQuery) => {
  searchQuery.value = newQuery
}

// API 응답을 WeatherCard 형식으로 변환
const convertWeatherData = (data, cityName) => {
  return {
    id: String(data.id),
    name: cityName,
    temp: Math.round(data.main.temp),
    status: data.weather[0].description,
    humidity: data.main.humidity,
    wind: data.wind.speed,
  }
}

// 저장된 도시 불러오기
const loadSavedCities = async () => {
  const storedCities = JSON.parse(localStorage.getItem('savedCities') || '[]')

  savedCities.value = storedCities

  if (storedCities.length === 0) {
    return
  }

  isLoading.value = true

  try {
    const requests = storedCities.map(async (city) => {
      const data = await fetchWeatherByCity(city.name)

      return convertWeatherData(data, city.name)
    })

    weatherList.value = await Promise.all(requests)
  } catch (error) {
    console.error('저장된 도시 날씨 불러오기 실패:', error)

    ElMessage.error('저장된 도시 날씨를 불러오지 못했습니다.')
  } finally {
    isLoading.value = false
  }
}

// 도시 검색 및 저장
const handleSearchWeather = async () => {
  const cityName = searchQuery.value.trim()

  if (!cityName) {
    ElMessage.warning('도시 이름을 입력해주세요.')
    return
  }

  isLoading.value = true

  try {
    const data = await fetchWeatherByCity(cityName)

    const newWeather = convertWeatherData(data, cityName)

    // 이미 등록된 도시인지 확인
    const existingIndex = weatherList.value.findIndex((weather) => weather.id === newWeather.id)

    if (existingIndex === -1) {
      weatherList.value.push(newWeather)
    } else {
      weatherList.value[existingIndex] = newWeather
    }

    // 저장 목록에 없는 도시만 추가
    const alreadySaved = savedCities.value.some((city) => city.id === newWeather.id)

    if (!alreadySaved) {
      savedCities.value.push({
        id: newWeather.id,
        name: newWeather.name,
      })

      localStorage.setItem('savedCities', JSON.stringify(savedCities.value))
    }

    selectedCityInfo.value = null
    searchQuery.value = ''

    ElMessage.success(`${cityName} 날씨를 목록에 추가했습니다.`)
  } catch (error) {
    console.error('날씨 API 요청 실패:', error)

    if (error.response?.status === 404) {
      ElMessage.error('해당 도시를 찾을 수 없습니다.')
    } else if (error.response?.status === 401) {
      ElMessage.error('API 키가 올바르지 않거나 아직 활성화되지 않았습니다.')
    } else {
      ElMessage.error('날씨 정보를 불러오지 못했습니다.')
    }
  } finally {
    isLoading.value = false
  }
}

// 저장한 도시 삭제
const removeCity = (weather) => {
  weatherList.value = weatherList.value.filter((item) => item.id !== weather.id)

  savedCities.value = savedCities.value.filter((city) => city.id !== weather.id)

  localStorage.setItem('savedCities', JSON.stringify(savedCities.value))

  if (selectedCityInfo.value?.id === weather.id) {
    selectedCityInfo.value = null
  }

  ElMessage.success(`${weather.name}을(를) 목록에서 삭제했습니다.`)
}

// WeatherCard에서 전달받은 도시 저장
const selectCity = (weather) => {
  selectedCityInfo.value = weather
}

// 상세보기 이동
const showDetail = (weather) => {
  router.push({
    name: 'weather-detail',
    params: {
      id: weather.id,
    },
  })
}

// 선택된 도시 변경 확인
watch(selectedCityInfo, (newCity) => {
  console.log(`선택된 도시: ${newCity?.name ?? '없음'}`)
})

// 검색어와 날씨 목록 변경 확인
watchEffect(() => {
  console.log(`현재 검색어: ${searchQuery.value}`)

  console.log(
    '현재 날씨 목록:',
    filteredWeatherList.value.map((weather) => weather.name),
  )
})

// 화면이 열릴 때 저장된 도시 불러오기
onMounted(() => {
  loadSavedCities()
})
</script>

<template>
  <div class="weather-container">
    <!-- 검색 영역 -->
    <BaseDashboardCard>
      <SearchBar
        :search-query="searchQuery"
        @update-query="updateSearchQuery"
        @search-weather="handleSearchWeather"
      />

      <!-- API 오류 -->
    </BaseDashboardCard>

    <!-- 지역별 날씨 영역 -->
    <BaseDashboardCard>
      <h3>🌆 날씨 검색 히스토리</h3>

      <!-- API 요청 중 -->
      <el-skeleton v-if="isLoading" :rows="5" animated />

      <!-- 날씨 카드 목록 -->
      <div v-else-if="filteredWeatherList.length > 0" class="weather-grid">
        <WeatherCard
          v-for="weather in filteredWeatherList"
          :key="weather.id"
          :weather="weather"
          @select-card="selectCity"
          @click-detail="showDetail"
          @remove-city="removeCity"
        />
      </div>

      <!-- 표시할 날씨가 없을 때 -->
      <el-empty v-else description="표시할 날씨 정보가 없습니다." />
    </BaseDashboardCard>

    <!-- 선택된 도시 표시 -->
    <div class="selected-message">
      <p v-if="selectedCityInfo">{{ selectedCityInfo.name }}이(가) 선택되었습니다.</p>

      <p v-else>카드를 클릭하거나 검색해 보세요.</p>
    </div>
  </div>
</template>

<style scoped>
.weather-container {
  width: calc(100% - 40px);
  max-width: 1400px;
  margin: 30px auto;
}

/* 도시 카드 세로 정렬 */

.weather-container h3 {
  margin: 0 0 12px;
}

.selected-message {
  margin-top: 15px;
  padding: 10px;
  text-align: center;
  background-color: #e8f5e9;
  border-radius: 6px;
}

.selected-message p {
  margin: 0;
}

.empty-message {
  padding: 15px;
  color: #777;
  text-align: center;
}

.loading-message {
  margin: 10px 0 0;
  color: #2196f3;
}

.error-message {
  margin: 10px 0 0;
  color: #f44336;
  font-weight: bold;
}
.weather-container {
  width: calc(100% - 40px);
  max-width: 1400px;
  margin: 30px auto;
  box-sizing: border-box;
}

.weather-grid {
  display: grid;

  /* 카드 너비를 340px로 유지 */

  grid-template-columns: 1fr;

  gap: 15px 30px;
  justify-content: start;
  width: 100%;
}
</style>
