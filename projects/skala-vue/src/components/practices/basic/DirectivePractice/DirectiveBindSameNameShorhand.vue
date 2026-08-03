
<!---v-bind실습(same-name shorhand)--->
<script setup>
const id = 'user-profile-card'
const src = 'https://vuejs.org/images/logo.png'
</script>
<template>
<div style="padding: 20px">
<h2>3-3. v-bind 고급 (단축 문법)</h2>
<hr />
<div :id>
<img :src alt="Vue 로고" style="width: 50px" />
</div>
<br />
</div>
</template>
