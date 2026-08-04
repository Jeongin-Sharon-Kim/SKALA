<script setup>
import SlotScopedChild from './SlotScopedChild.vue'
</script>
<template>
<div class="parent-box">
<h2>📡 상위 컴포넌트 (Parent)</h2>
<hr />
<SlotScopedChild v-slot="slotBag">
<div class="display-panel">
<p>
알림 메시지: <strong>{{ slotBag.text }}</strong>
</p>
<p>
접속자 수: <span class="number-badge">{{ slotBag.count }}명</span>
</p>
</div>
<button>상위 전용 관리자 버튼</button>
</SlotScopedChild>
</div>
</template>
