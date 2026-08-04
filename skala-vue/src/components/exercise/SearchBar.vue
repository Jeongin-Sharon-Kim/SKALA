
<script setup>
// 부모에게서 검색어 받기
defineProps({
    searchQuery: {
        type: String,
        default: '',
    },
})

// 부모에게 전달할 이벤트 선언
const emit = defineEmits(['update-query'])

// 입력값을 부모에게 전달
const handleInput = (event) => {
    emit('update-query', event.target.value)
}
</script>

<template>
    <div class="search-box">
    <h3>🔍 도시 검색 </h3>

    <input
        type="text"
        :value="searchQuery"
        placeholder="검색할 도시 이름 입력"
        @input="handleInput"
    />

    <p>검색 중인 도시: {{ searchQuery }}</p>
    </div>
</template>

<style scoped>
.search-box h3 {
    margin-top: 0;
}

.search-box input {
    box-sizing: border-box;
    width: 100%;
    padding: 8px;
}

.search-box p {
    margin-bottom: 0;
}
</style>