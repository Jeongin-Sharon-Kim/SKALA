//부모가 전달하는 내용은 slot으로 표시 //검색박스와 리스트박스의 디자인 공통화
<script setup>
defineProps({
  title: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <section class="base-card">
    <h2 v-if="title" class="card-title">
      {{ title }}
    </h2>

    <slot />
  </section>
</template>

<style scoped>
/*카드 공통 디자인*/
.base-card {
  margin-bottom: 14px;
  padding: 18px;
  background-color: rgb(226, 228, 208);
  border: 1px solid #dfe5eb;
  border-radius: 8px;
}

.card-title {
  margin: 0 0 12px;
  font-size: 17px;
}
</style>
