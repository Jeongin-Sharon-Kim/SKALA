<script setup>
const userAge = 20

if (userAge === 20) {
  console.log('20살입니다.')
}

const apiUrl = import.meta.env.VITE_API_URL

console.log('현재 API URL:', apiUrl)

const myRegion = 'Suwon'
const regionGreeting = `웰컴 투 ${myRegion}`
</script>
