<script setup>
import { computed } from 'vue'
import { useConfigStore } from '@/stores/configStore.js'

const configStore = useConfigStore()

const isFahrenheit = computed({
  get() {
    return configStore.unit === 'fahrenheit'
  },

  set(value) {
    configStore.unit = value ? 'fahrenheit' : 'celsius'
  },
})
</script>

<template>
  <div class="unit-toggler">
    <span>온도 단위</span>

    <el-switch
      v-model="isFahrenheit"
      inline-prompt
      active-text="°F"
      inactive-text="°C"
      size="large"
    />
  </div>
</template>

<style scoped>
.unit-toggler {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 1px 10px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.8);
  box-shadow: 0 6px 20px rgba(53, 94, 142, 0.1);
}

.unit-toggler span {
  font-weight: 700;
  font-size: 13px;
  color: #606266;
}
</style>
