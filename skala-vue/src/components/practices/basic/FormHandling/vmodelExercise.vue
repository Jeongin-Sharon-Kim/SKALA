<script setup>
import { ref } from 'vue'

const text1 = ref('')
const text2 = ref('')
</script>

<template>
  <div style="padding: 20px">
    <h2>1. v-model 양방향 데이터 바인딩</h2>

    <hr />

    <section style="margin-bottom: 20px">
      <h3>🟢 1) v-model 축약 문법 (양방향)</h3>

      <input v-model="text1" type="text" placeholder="여기에 입력하세요" />

      <p>
        입력된 값:
        <strong>{{ text1 }}</strong>
      </p>
    </section>

    <section>
      <h3>🔴 2) v-model의 내부 작동 원리 (단방향 + 이벤트)</h3>

      <input
        type="text"
        :value="text2"
        placeholder="원리 파악용 입력창"
        @input="text2 = $event.target.value"
      />

      <p>
        입력된 값:
        <strong>{{ text2 }}</strong>
      </p>
    </section>
  </div>
</template>
