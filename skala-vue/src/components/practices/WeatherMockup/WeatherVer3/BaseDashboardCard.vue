//부모가 전달하는 내용은 slot으로 표시 //검색박스와 리스트박스의 디자인 공통화

<template>
  <section class="dashboard-card">
    <slot name="header"></slot>
    <slot></slot>
  </section>
</template>

<style scoped>
.dashboard-card {
  margin-top: 12px;
  padding: 15px;
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>
