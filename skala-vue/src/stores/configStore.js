import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

export const useConfigStore = defineStore('config', () => {
  // 현재 날씨 단위
    const unit = ref('celsius')

    // 현재 단위에 맞는 기호
    const unitSymbol = computed(() => {
        return unit.value === 'celsius' ? '℃' : '℉'
    })

    // 섭씨와 화씨 전환
    const toggleUnit = () => {
        unit.value =
        unit.value === 'celsius'
            ? 'fahrenheit'
            : 'celsius'
    }

    return {
        unit,
        unitSymbol,
        toggleUnit,
    }
    })