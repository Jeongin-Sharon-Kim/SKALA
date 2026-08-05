    <!-- 메인 날씨 대시보드 화면 -->

    <script setup>
    import { ref, computed, watch, watchEffect } from 'vue'
    import { useRouter } from 'vue-router'
    import { fetchWeatherByCity } from '@/services/weatherApi.js'
    import { ElMessage } from 'element-plus'

    import SearchBar from '../components/exercise/SearchBar.vue'
    import BaseDashboardCard from '../components/exercise/BaseDashboardCard.vue'
    import WeatherCard from '../components/exercise/WeatherCard.vue'

    // Router 사용
    const router = useRouter()

    // 도시 검색창에 입력한 값
    const searchQuery = ref('')

    // 현재 선택된 도시 정보
    const selectedCityInfo = ref(null)

    // API 요청 중인지 확인
    const isLoading = ref(false)

    // API 오류 메시지
    const errorMessage = ref('')

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

    // API에서 검색된 날씨 목록 반환
    const filteredWeatherList = computed(() => {
    return weatherList.value
    })

    // SearchBar에서 전달받은 검색어 저장
    const updateSearchQuery = (newQuery) => {
    searchQuery.value = newQuery
    }


    const handleSearchWeather = async () => {
    const cityName = searchQuery.value.trim()

    // 빈 검색어 검사
    if (!cityName) {
        ElMessage.warning('도시 이름을 입력해주세요.')
        return
    }

    isLoading.value = true

    try {
    // OpenWeather API 호출
        const data = await fetchWeatherByCity(cityName)

        console.log('API 응답:', data)

        // API 응답을 WeatherCard 형식으로 변환
        const newWeather = {
        id: String(data.id),

        // 사용자가 한글로 입력했다면 입력한 이름 유지
        name: cityName,

        temp: Math.round(data.main.temp),
        status: data.weather[0].description,
        humidity: data.main.humidity,
        wind: data.wind.speed,
        }

        // 검색된 도시만 화면에 표시
        weatherList.value = [newWeather]

        // 이전 선택 상태 초기화
        selectedCityInfo.value = null

        // 검색 성공 메시지
        ElMessage.success(`${cityName} 날씨를 불러왔습니다.`)
    } catch (error) {
        console.error('날씨 API 요청 실패:', error)

        if (error.response?.status === 404) {
        ElMessage.error('해당 도시를 찾을 수 없습니다.')
        } else if (error.response?.status === 401) {
        ElMessage.error(
            'API 키가 올바르지 않거나 아직 활성화되지 않았습니다.',
        )
        } else {
        ElMessage.error('날씨 정보를 불러오지 못했습니다.')
        }
    } finally {
        isLoading.value = false
    }
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

    // 검색어와 날씨 목록 변경 시 실행
    watchEffect(() => {
    console.log(
        `🤖 [watchEffect 자동 호출] 현재 검색어: '${searchQuery.value}'`
    )

    console.log(
        '현재 날씨 목록:',
        filteredWeatherList.value.map((weather) => weather.name)
    )
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
        <el-alert
            v-if="errorMessage"
            :title="errorMessage"
            type="error"
            show-icon
            :closable="false"
            class="error-alert"
        />
        </BaseDashboardCard>

        <!-- 지역별 날씨 영역 -->
        <BaseDashboardCard>
        <h3>🌆 지역별 날씨 현황</h3>

        <!-- API 요청 중 -->
        <el-skeleton
            v-if="isLoading"
            :rows="5"
            animated
        />

        <!-- 날씨 카드 목록 -->
        <el-row
            v-else-if="filteredWeatherList.length > 0"
            :gutter="20"
        >
            <el-col
            v-for="weather in filteredWeatherList"
            :key="weather.id"
            :xs="24"
            :sm="12"
            :md="8"
            class="weather-column"
            >
            <WeatherCard
                :weather="weather"
                @select-card="selectCity"
                @click-detail="showDetail"
            />
            </el-col>
        </el-row>

        <!-- 표시할 날씨가 없을 때 -->
        <el-empty
            v-else
            description="표시할 날씨 정보가 없습니다."
        />
        </BaseDashboardCard>

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
    }

    /* 도시 카드 세로 정렬 */
    .weather-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
    }

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

    .error-alert {
    margin-top: 10px;

    .weather-column {
    margin-bottom: 50px;
}
}



</style>