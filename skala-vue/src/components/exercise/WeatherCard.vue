    <script setup>
    import { computed } from 'vue'
    import {
    Location,
    View,
    Sunny,
    Pouring,
    Cloudy,
    } from '@element-plus/icons-vue'

    import { useConfigStore } from '@/stores/configStore.js'

    const props = defineProps({
    weather: {
        type: Object,
        required: true,
    },
    })

    const emit = defineEmits([
    'select-card',
    'click-detail',
    ])

    const configStore = useConfigStore()

    const displayTemp = computed(() => {
    if (configStore.unit === 'fahrenheit') {
        return Math.round((props.weather.temp * 9) / 5 + 32)
    }

    return Math.round(props.weather.temp)
    })

    const unitSymbol = computed(() => {
    return configStore.unit === 'fahrenheit' ? '°F' : '°C'
    })

    const weatherIcon = computed(() => {
    if (props.weather.status === '맑음') return Sunny
    if (props.weather.status === '비') return Pouring
    return Cloudy
    })

    const tagType = computed(() => {
    if (props.weather.status === '맑음') return 'warning'
    if (props.weather.status === '비') return 'primary'
    return 'info'
    })
    </script>

    <template>
    <el-card
        class="weather-card"
        shadow="hover"
        @click="emit('select-card', weather)"
    >
        <div class="weather-card-top">
        <div class="city-name">
            <el-icon>
            <Location />
            </el-icon>

            <span>{{ weather.name }}</span>
        </div>

        <el-tag
            :type="tagType"
            effect="light"
            round
        >
            {{ weather.status }}
        </el-tag>
        </div>

        <div class="weather-main">
        <el-icon class="weather-icon">
            <component :is="weatherIcon" />
        </el-icon>

        <strong class="temperature">
            {{ displayTemp }}{{ unitSymbol }}
        </strong>
        </div>

        <el-divider />

        <el-button
        type="primary"
        plain
        round
        :icon="View"
        class="detail-button"
        @click.stop="emit('click-detail', weather)"
        >
        상세보기
        </el-button>


    </el-card>
    </template>

    <style scoped>
    .weather-card {
    border: none;
    border-radius: 22px;
    cursor: pointer;
    margin-bottom: 15px;
    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease;
    }

    .weather-card:hover {
    transform: translateY(-6px);
    }

    .weather-card-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    }

    .city-name {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 19px;
    font-weight: 700;
    }

    .weather-main {
    min-height: 150px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 18px;
    }

    .weather-icon {
    font-size: 62px;
    color: #409eff;
    }

    .temperature {
    font-size: 42px;
    color: #303133;
    }

    .detail-button {
    width: 100%;
    }
    </style>