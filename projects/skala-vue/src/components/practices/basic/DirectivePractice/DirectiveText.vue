
<!---v-text실습---->
<script setup>
const content =
<template>
<div style="padding: 20px">
<h1>2. v-text 디렉티브 학습</h1>
<hr />
<h3>1) 일반 보간법 {{}} 결과:</h3>
<p>출력: {{ content }}</p>
<br />
<h3>2) v-text 디렉티브 결과:</h3>
<p v-text="'출력: ' + content"></p>
<br />
<h3>3) v-html 결과 비교:</h3>
<p v-html="content"></p>
</div>
</template>
</script>
