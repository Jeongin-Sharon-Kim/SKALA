<script setup>
import { ref } from 'vue'

// 도시 검색창에 입력한 값
const searchCity = ref('')

// 현재 선택된 도시
const selectedCity = ref('')

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

    // 검색창에 입력할 때 실행
    const handleSearch = (event) => {
    // 입력된 값을 searchCity에 저장
    searchCity.value = event.target.value
    }

    // 날씨 카드를 클릭하면 선택된 도시 표시
    const selectCity = (cityName) => {
    selectedCity.value = cityName
    }

    // 상세보기 버튼을 클릭하면 알림창 출력
    const showDetail = (cityName, status) => {
    window.alert(`${cityName}의 현재 날씨는 [${status}] 상태입니다.`)
    }
    </script>

    <template>
    <div class="weather-container">
        <h1>🌤️ 과제 1: 날씨 Mockup</h1>

        <hr />

        <!-- 도시 검색 영역 -->
        <section class="search-box">
        <h3>🔍 도시 검색</h3>

        <!--
            :value는 입력창의 값을 searchCity와 연결
            @input은 사용자가 입력할 때 handleSearch 함수 실행
        -->
        <input
            type="text"
            :value="searchCity"
            @input="handleSearch"
            placeholder="검색할 도시 이름 입력"
        />

        <p>검색 중인 도시: {{ searchCity }}</p>
        </section>

        <!-- 날씨 카드 영역 -->
        <section class="weather-section">
        <h3>🗺️ 지역별 날씨 현황</h3>

        <!--
            weatherList 배열을 반복
            :key에는 고유한 id 사용
        -->
        <div
            v-for="weather in weatherList"
            :key="weather.id"
            class="weather-card"
            @click="selectCity(weather.name)"
        >
            <div>
            <strong>{{ weather.name }} ({{ weather.status }})</strong>

            <p>현재 기온: {{ weather.temp }}℃</p>

            <!-- 기온이 25도 이상인 경우 -->
            <span
                v-if="weather.temp >= 25"
                class="hot"
            >
                🔥 더움 (25도 이상)
            </span>

            <!-- 기온이 25도 미만인 경우 -->
            <span
                v-else
                class="cool"
            >
                ❄️ 선선함 (25도 미만)
            </span>
            </div>

            <!--
            .stop을 사용하여 부모 카드의 클릭 이벤트가 실행되지 않게 함
            -->
            <button
            @click.stop="showDetail(weather.name, weather.status)"
            >
            상세보기
            </button>
        </div>
        </section>

        <!-- 선택된 도시 표시 -->
        <div class="selected-message">
        <p v-if="selectedCity">
            {{ selectedCity }}이(가) 선택되었습니다.
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
    </style>