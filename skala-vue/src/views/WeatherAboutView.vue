<script setup>
import BaseDashboardCard from '../components/exercise/BaseDashboardCard.vue'
</script>

<template>
    <div class="about-container">
    <BaseDashboardCard>
        <h2>📘 서비스 소개</h2>
        <hr>

    <p>
        본 앱은 vue3 및 router 4기반 제작된 실습용 기상 관측 대시보드 시스템입니다.
    </p>


    <ul>
        <li>
        <span class="highlight-box">components/exercise</span> 폴더 내부의 독립 부품 연동
        </li>

        <li>
        클라이언트 사이드 라우팅을 통한 새로고침 없는 화면 전환
        </li>

        <li>
            URL 쿼리 스트링 매핑을 활용한 실시간 검색 상태 동기화
        </li>

        
    </ul>

        <!-- 메인 페이지로 이동 -->
        <RouterLink
            class="home-link"
            to="/"
        >
            날씨 대시보드로 돌아가기
        </RouterLink>
        </BaseDashboardCard>
    </div>
    </template>

<style scoped>
    .about-container {
    width: 500px;
    margin: 30px auto;
    }

    h2 {
    margin-top: 0;
}

    hr{
    color: #ddd;
    }

p,
    li {
    line-height: 1.7;
    }

    ul {
    padding: 15px 15px 15px 35px;
    background-color: #f5f7fa;
    border-radius: 6px;
}

    .highlight-box {
    padding: 2px 5px;
    color: #ff0000;
    background-color: #fff3b0;
    border-radius: 4px;
    }

    .home-link {
    display: inline-block;
    margin-top: 10px;
    padding: 9px 158px;
    color: white;
    background-color: #2196f3;
    border-radius: 5px;
    text-decoration: none;
}
</style>