<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Location, Position } from '@element-plus/icons-vue'

import { fetchWeatherByCoords } from '@/services/weatherApi.js'

const currentWeather = ref(null)
const isLoading = ref(false)

// 현재 위치 가져오기
const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    ElMessage.error('현재 브라우저에서는 위치 기능을 지원하지 않습니다.')
    return
  }

  isLoading.value = true

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const latitude = position.coords.latitude
      const longitude = position.coords.longitude

      try {
        const data = await fetchWeatherByCoords(latitude, longitude)

        currentWeather.value = {
          id: String(data.id),
          name: data.name,
          temp: Math.round(data.main.temp),
          feelsLike: Math.round(data.main.feels_like),
          status: data.weather[0].description,
          humidity: data.main.humidity,
          wind: data.wind.speed,
        }

        ElMessage.success('현재 위치의 날씨를 불러왔습니다.')
      } catch (error) {
        console.error('현재 위치 날씨 조회 실패:', error)

        ElMessage.error('현재 위치의 날씨를 불러오지 못했습니다.')
      } finally {
        isLoading.value = false
      }
    },
    (error) => {
      console.error('위치 오류 전체:', error)
      console.error('위치 오류 코드:', error.code)
      console.error('위치 오류 메시지:', error.message)

      if (error.code === 1) {
        ElMessage.error('위치 정보 사용 권한이 거부되었습니다.')
      } else if (error.code === 2) {
        ElMessage.error('Mac이 현재 위치를 계산하지 못했습니다. Wi-Fi를 켠 뒤 다시 시도해주세요.')
      } else if (error.code === 3) {
        ElMessage.error('위치 확인 시간이 초과되었습니다.')
      } else {
        ElMessage.error('위치 정보를 가져오지 못했습니다.')
      }

      isLoading.value = false
    },

    {
      enableHighAccuracy: false,
      timeout: 20000,
      maximumAge: 300000,
    },
  )
}
</script>

<template>
  <div class="location-page">
    <el-card class="location-search-card" shadow="hover">
      <div class="title-area">
        <el-icon>
          <Position />
        </el-icon>

        <div>
          <h2>현재 위치 날씨</h2>
          <p>위치 권한을 허용하면 현재 지역의 날씨를 확인할 수 있습니다.</p>
        </div>
      </div>

      <el-button
        type="primary"
        size="large"
        :icon="Location"
        :loading="isLoading"
        @click="getCurrentLocation"
      >
        내 위치 날씨 확인
      </el-button>
    </el-card>

    <el-skeleton v-if="isLoading" :rows="5" animated class="loading-area" />

    <el-card v-else-if="currentWeather" class="weather-result-card" shadow="hover">
      <div class="weather-header">
        <h3>📍 {{ currentWeather.name }}</h3>

        <el-tag type="primary" round>
          {{ currentWeather.status }}
        </el-tag>
      </div>

      <div class="temperature">{{ currentWeather.temp }}°C</div>

      <el-divider />

      <el-descriptions :column="1" border>
        <el-descriptions-item label="체감온도">
          {{ currentWeather.feelsLike }}°C
        </el-descriptions-item>

        <el-descriptions-item label="습도"> {{ currentWeather.humidity }}% </el-descriptions-item>

        <el-descriptions-item label="풍속"> {{ currentWeather.wind }}m/s </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-empty v-else description="버튼을 눌러 현재 위치의 날씨를 확인하세요." />
  </div>
</template>

<style scoped>
.location-page {
  width: calc(100% - 40px);
  max-width: 900px;
  margin: 30px auto;
}

.location-search-card,
.weather-result-card {
  border: none;
  border-radius: 22px;
}

.title-area {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
}

.title-area .el-icon {
  font-size: 38px;
  color: #409eff;
}

.title-area h2 {
  margin: 0 0 8px;
}

.title-area p {
  margin: 0;
  color: #777;
}

.location-search-card .el-button {
  width: 100%;
}

.loading-area {
  margin-top: 30px;
}

.weather-result-card {
  margin-top: 30px;
}

.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.weather-header h3 {
  margin: 0;
}

.temperature {
  padding: 50px 0;
  font-size: 64px;
  font-weight: 700;
  text-align: center;
}
</style>
