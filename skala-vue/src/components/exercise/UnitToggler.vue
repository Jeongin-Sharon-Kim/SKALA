    <script setup>
    import { useConfigStore } from '@/stores/configStore.js'

    // 전역 날씨 단위 Store
    const configStore = useConfigStore()
    </script>

    <template>
    <div class="unit-toggler">
        <span>
        날씨단위:
        {{ configStore.unit === 'celsius' ? '섭씨' : '화씨' }}
        ({{ configStore.unitSymbol }})
        </span>

        <button
        type="button"
        @click="configStore.toggleUnit"
        >
        단위변경
        </button>
    </div>
    </template>

    <style scoped>
    .unit-toggler {
    display: flex;
    align-items: center;
    gap: 7px;
    white-space: nowrap;
    }

    .unit-toggler span {
    color: #546e7a;
    font-size: 12px;
    font-weight: 600;
    }

    .unit-toggler button {
    padding: 5px 8px;
    color: white;
    font-size: 11px;
    font-weight: 700;
    background-color: #455a64;
    border: none;
    border-radius: 4px;
    }

    .unit-toggler button:hover {
    background-color: #37474f;
    }
    </style>