    <script setup>
    import { computed } from 'vue'
    import { useRoute, useRouter } from 'vue-router'
    import { useConfigStore } from '@/stores/configStore.js'

    import BaseDashboardCard from '../components/exercise/BaseDashboardCard.vue'

    const route = useRoute()
    const router = useRouter()

    // Pinia 단위 설정 Store
    const configStore = useConfigStore()

    // 상세 페이지용 날씨 데이터
    const weatherList = [
    {
        id: 'city_01',
        name: '서울',
        temp: 28,
        status: '맑음',
        humidity: 55,
        wind: 2.4,
    },
    {
        id: 'city_02',
        name: '수원',
        temp: 24,
        status: '비',
        humidity: 78,
        wind: 3.1,
    },
    {
        id: 'city_03',
        name: '부산',
        temp: 26,
        status: '구름',
        humidity: 68,
        wind: 4.2,
    },
    ]

    // URL의 id와 일치하는 도시 찾기
    const selectedWeather = computed(() => {
    return weatherList.find(
        (weather) => weather.id === route.params.id
    )
    })

    // 현재 단위 설정에 맞게 온도 계산
    const displayTemp = computed(() => {
    // 잘못된 도시 ID일 때 오류 방지
    if (!selectedWeather.value) {
        return ''
    }

    const rawTemp = selectedWeather.value.temp

    // 화씨로 설정된 경우
    if (configStore.unit === 'fahrenheit') {
        return Math.round(rawTemp * 9 / 5 + 32)
    }

    // 섭씨일 때 원본 온도 반환
    return rawTemp
    })

    // 이전 페이지로 이동
    const goBack = () => {
    router.back()
    }
    </script>

    <template>
    <div class="detail-container">
        <BaseDashboardCard v-if="selectedWeather">
        <h2>📊 지역별 상세 기상 관측 정보</h2>

        <div class="detail-box">
            <p>
            <span>📍 도시</span>
            <strong>{{ selectedWeather.name }}</strong>
            </p>

            <p>
            <span>현재 온도</span>

            <!-- 변환된 온도와 현재 단위 기호 출력 -->
            <strong>
                {{ displayTemp }}{{ configStore.unitSymbol }}
            </strong>
            </p>

            <p>
            <span>기상 현황</span>
            <strong>{{ selectedWeather.status }}</strong>
            </p>

            <p>
            <span>습도</span>
            <strong>{{ selectedWeather.humidity }}%</strong>
            </p>

            <p>
            <span>풍속</span>
            <strong>{{ selectedWeather.wind }}m/s</strong>
            </p>
        </div>

        <button
            type="button"
            class="back-button"
            @click="goBack"
        >
            🔙 이전 페이지로 돌아가기
        </button>
        </BaseDashboardCard>

        <!-- 잘못된 도시 ID인 경우 -->
        <BaseDashboardCard v-else>
        <h2>도시 정보를 찾을 수 없습니다.</h2>

        <RouterLink
            class="home-link"
            to="/"
        >
            날씨 대시보드로 이동
        </RouterLink>
        </BaseDashboardCard>
    </div>
    </template>

    <style scoped>
    .detail-container {
    width: 500px;
    margin: 30px auto;
    }

    h2 {
    margin-top: 0;
    }

    .detail-box {
    padding: 10px 18px;
    background-color: #f5f7fa;
    border-radius: 6px;
    }

    .detail-box p {
    display: flex;
    justify-content: space-between;
    margin: 0;
    padding: 13px 0;
    border-bottom: 1px solid #ddd;
    }

    .detail-box p:last-child {
    border-bottom: none;
    }

    .detail-box span {
    color: #666;
    }

    .back-button,
    .home-link {
    display: inline-block;
    margin-top: 18px;
    padding: 9px 14px;
    color: white;
    background-color: #5faaf5;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    }
    </style>