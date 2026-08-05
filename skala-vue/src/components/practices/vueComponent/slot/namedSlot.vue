<script setup>
import SlotNamedChild from './SlotNamedChild.vue'
</script>
<template>
  <SlotNamedChild>
    <template v-slot:header>
      <h2>시작점 주입 제목</h2>
    </template>
    <p>본문 텍스트 데이터 영역 매프 내용 기입</p>
  </SlotNamedChild>
</template>

<template>
  <div class="layout-container">
    <header class="layout-header">
      <slot name="header"></slot>
    </header>
    <main class="layout-body">
      <slot></slot>
    </main>
  </div>
</template>
