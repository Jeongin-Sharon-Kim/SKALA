<script setup></script>
import SlotDefaultChild from '@/components/practices/component/SlotDefaultChild.vue'
<template>
  <div style="padding: 20px; max-width: 400px; margin: 0 auto">
    <h2>🧱 슬롯 레이아웃 주입 실습</h2>
    <hr />
    <SlotDefaultChild>
      <p>단순한 텍스트 문장을 주입합니다.</p>
    </SlotDefaultChild>
    <br />
    <SlotDefaultChild>
      <h3 style="color: #e74c3c">🔥 경고 상태</h3>
      <button>확인</button>
    </SlotDefaultChild>
  </div>
</template>

<template>
  <div class="base-card">
    <slot>
      <p>기본 콘텐츠 영역입니다.</p>
    </slot>
  </div>
</template>
<style scoped>
.base-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
</style>
