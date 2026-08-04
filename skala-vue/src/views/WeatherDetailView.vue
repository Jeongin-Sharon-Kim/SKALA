    <script setup>
    import { computed } from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    import BaseDashboardCard from '../components/exercise/BaseDashboardCard.vue'

    // 현재 주소 정보
    const route = useRoute()

    // 페이지 이동 기능
    const router = useRouter()

    // 도시 상세 Mock Data
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

    // 이전 페이지로 이동
    const goBack = () => {
    router.back()
    }
    </script>

    <template>
    <div class="detail-container">
        <!-- 도시 정보가 있는 경우 -->
        <BaseDashboardCard v-if="selectedWeather">
        <h2>
        📊 지역별 상세 기상 관측 정보 
        </h2>

        <div class="detail-box">
            <p>
            <span>📍 도시 </span>
            <strong>{{ selectedWeather.name }}</strong>
            </p>

            <p>
            <span>현재 온도</span>
            <strong>{{ selectedWeather.temp }}℃</strong>
            </p>

            <p>
            <span>기상 현황 </span>
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

        <p>
            요청한 도시 ID와 일치하는 날씨 정보가 없습니다.
        </p>

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
    padding: 9px 15px;
    color: white;
    background-color: #5db1ff;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    }
    </style>