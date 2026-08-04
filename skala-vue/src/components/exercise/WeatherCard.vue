    <script setup>
    import { computed } from 'vue'
    import { useConfigStore } from '@/stores/configStore.js'

    // 부모에게 날씨 정보 받기
    const props = defineProps({
    weather: {
        type: Object,
        required: true,
    },
    })

    // 부모에게 전달할 이벤트
    const emit = defineEmits([
    'select-card',
    'click-detail',
    ])

    // Pinia Store 사용
    const configStore = useConfigStore()

    // 현재 단위에 맞는 온도 계산
    const displayTemp = computed(() => {
    const rawTemp = props.weather.temp

    // 화씨일 때 변환
    if (configStore.unit === 'fahrenheit') {
        return Math.round(rawTemp * 9 / 5 + 32)
    }

    // 섭씨일 때 원본 반환
    return rawTemp
    })

    // 카드 클릭 이벤트
    const selectCard = () => {
    emit('select-card', props.weather)
    }

    // 상세보기 클릭 이벤트
    const clickDetail = () => {
    emit('click-detail', props.weather)
    }
    </script>

    <template>
    <div
        class="weather-card"
        @click="selectCard"
    >
        <div class="weather-info">
        <p class="city-name">
            {{ weather.name }} ({{ weather.status }})
        </p>

        <p class="temperature">
            현재 기온:
            {{ displayTemp }}{{ configStore.unitSymbol }}
        </p>

        <span
            v-if="weather.temp >= 25"
            class="hot"
        >
            🔥 더움 (25도 이상)
        </span>

        <span
            v-else
            class="cool"
        >
            ❄️ 선선함 (25도 미만)
        </span>
        </div>

        <!-- 버튼 클릭 시 카드 클릭 이벤트는 실행하지 않음 -->
        <button
        type="button"
        @click.stop="clickDetail"
        >
        상세보기
        </button>
    </div>
    </template>

    <style scoped>
    
    .weather-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 15px;

    margin-bottom: 10px;
    padding: 14px;

    background-color: white;
    border: 1px solid #dfe5eb;
    border-radius: 6px;

    cursor: pointer;
    }

    .weather-card:last-child {
    margin-bottom: 0;
    }

    .weather-card:last-child {
    margin-bottom: 0;
    }

    .weather-card p {
    margin: 5px 0;
    }

    .city-name {
    font-weight: 600;
    }

    .temperature {
    margin-bottom: 8px;
    }

    .weather-card button {
    padding: 6px 12px;
    background-color: rgb(202, 201, 201);
    border: 1px solid #7a8085;
    border-radius: 4px;
    cursor: pointer;
    }

    .weather-card button:hover {
    background-color: #f1f3f5;
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