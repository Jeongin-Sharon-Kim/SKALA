    <script setup>
    defineProps({
    searchQuery: {
        type: String,
        default: '',
    },
    })

    // 검색어 변경과 검색 실행 이벤트
    const emit = defineEmits([
    'update-query',
    'search-weather',
    ])

    // 입력값 부모에게 전달
    const handleInput = (event) => {
    emit('update-query', event.target.value)
    }

    // 검색 버튼 클릭
    const handleSearch = () => {
    emit('search-weather')
    }

    // Enter 키로 검색
    const handleEnter = () => {
    emit('search-weather')
    }
    </script>

    <template>
    <div class="search-box">
        <h3>🔍 도시 검색</h3>

        <div class="input-area">
        <input
            type="text"
            :value="searchQuery"
            placeholder="검색할 도시 이름 입력"
            @input="handleInput"
            @keyup.enter="handleEnter"
        />

        <button
            type="button"
            @click="handleSearch"
        >
            검색
        </button>
        </div>

        <p>검색 중인 도시: {{ searchQuery }}</p>
    </div>
    </template>

    <style scoped>
    .search-box h3 {
    margin-top: 0;
    }

    .input-area {
    display: flex;
    gap: 8px;
    }

    .search-box input {
    box-sizing: border-box;
    flex: 1;
    padding: 8px;
    }

    .input-area button {
    padding: 8px 14px;
    color: white;
    background-color: #2196f3;
    border: none;
    border-radius: 4px;
    }

    .search-box p {
    margin-bottom: 0;
    }
    </style>