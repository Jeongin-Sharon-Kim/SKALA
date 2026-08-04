    <script setup>
    // 카운터 Store 가져오기
    import { useCounterStore } from '@/stores/counter.js'

    // Store 인스턴스 생성
    const counterStore = useCounterStore()
    </script>

    <template>
    <div class="practice-section">
        <h2>Counter Store 활용 실습</h2>

        <p>
        원본 카운트 데이터(state):
        <strong>{{ counterStore.count }}</strong>
        </p>

        <p>
        2배 연산 데이터(getters):
        <span>{{ counterStore.doubleCount }}</span>
        </p>

        <button @click="counterStore.increment">
        숫자 1 증가(actions)
        </button>
    </div>
    </template>

    <style scoped>
    .practice-section {
    width: 400px;
    margin: 30px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    }

    strong,
    span {
    color: #2196f3;
    }

    button {
    padding: 8px 12px;
    cursor: pointer;
    }
    </style>