
<!---v-for실습--->
<script setup>
import { ref } from 'vue'
const fruits = ref(['사과',
const user = ref({
name: '홍길동',
age: 25,
role: '개발자',
'바나나','딸기'])
})
const items = ref([
{ id: 'prod_101', name: '아이폰' },
{ id: 'prod_102', name: '갤럭시' },
])
</script>
<template>
<div style="padding: 20px">
<h1>6. v-for 디렉티브 학습</h1>

<hr />

<h3>1) 배열 렌더링</h3>
<ul>
</ul>

<h3>2) 객체 렌더링</h3>
<ul>
</ul>

<h3>3) 배열 내 객체 렌더링</h3>
<ul>
</ul>

</div>
</template>
<li v-for="(fruit, index) in fruits" :key="index">{{ index + 1 }}번 과일: {{ fruit }}</li>
<li v-for="(value, key, index) in user" :key="key">[{{ index }}] {{ key }} : {{ value }}</li>
<li v-for="(item, index) in items" :key="item.id">[{{ index }}] {{ item.name }}</li>
