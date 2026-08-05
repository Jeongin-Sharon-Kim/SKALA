import axios from 'axios'

const WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

const API_KEY = import.meta.env.VITE_OPENWEATHER_API_KEY

// 한국어 도시명을 API용 영어 이름으로 변경
const cityNameMap = {
  서울: 'Seoul,KR',

  대전: 'Daejeon,KR',
  청주: 'Cheongju,KR',
  충주: 'Chungju,KR',
  예산: 'Yesan,KR',
  서산: 'Seosan,KR',
  충북: 'Chungcheongbuk-do,KR',
  제천: 'Jecheon,KR',
  단양: 'Danyang,KR',
  충남: 'Chungcheongnam-do,KR',
  보령: 'Boryeong,KR',
  태안: 'Taean,KR',
  홍성: 'Hongseong,KR',
  음성: 'Eumseong,KR',

  경기: 'Gyeonggi-do,KR',
  수원: 'Suwon,KR',
  광명: 'Gwangmyeong,KR',
  인천: 'Incheon,KR',
  김포: 'Gimpo,KR',
  남양주: 'Namyangju,KR',
  용인: 'Yongin,KR',
  평택: 'Pyeongtaek,KR',
  성남: 'Seongnam,KR',
  안산: 'Ansan,KR',
  안양: 'Anyang,KR',
  고양: 'Goyang,KR',
  오산: 'Osan,KR',
  의정부: 'Uijeongbu,KR',
  하남: 'Hanam,KR',
  가평: 'Gapyeong,KR',

  대구: 'Daegu,KR',
  포항: 'Pohang,KR',
  울산: 'Ulsan,KR',
  창원: 'Changwon,KR',
  부산: 'Busan,KR',
  구미: 'Gumi,KR',
  김해: 'Gimhae,KR',
  경북: 'Gyeongsangbuk-do,KR',
  안동: 'Andong,KR',
  영주: 'Yeongju,KR',
  경남: 'Gyeongsangnam-do,KR',
  진주: 'Jinju,KR',

  강원: 'Gangwon-do,KR',
  속초: 'Sokcho,KR',
  강릉: 'Gangneung,KR',
  양양: 'Yangyang,KR',
  횡성: 'Hoengseong,KR',

  광주: 'Gwangju,KR',
  전주: 'Jeonju,KR',
  전남: 'Jeollanam-do,KR',
  여수: 'Yeosu,KR',
  순천: 'Suncheon,KR',
  전북: 'Jeollabuk-do,KR',
  군산: 'Gunsan,KR',
  익산: 'Iksan,KR',

  제주도: 'Jeju-do,KR',
  제주시: 'Jeju,KR',
  서귀포시: 'Seogwipo,KR',
}

// 도시 이름으로 현재 날씨 가져오기
export const fetchWeatherByCity = async (cityName) => {
  // 매핑된 도시가 있으면 영어 이름 사용
  // 없으면 사용자가 입력한 값을 그대로 사용
  const apiCityName = cityNameMap[cityName] ?? cityName

  const response = await axios.get(WEATHER_API_URL, {
    params: {
      q: apiCityName,
      appid: API_KEY,
      units: 'metric',
      lang: 'kr',
    },
  })

  return response.data
}

// 위도와 경도로 현재 위치 날씨 가져오기
export const fetchWeatherByCoords = async (latitude, longitude) => {
  const response = await axios.get(WEATHER_API_URL, {
    params: {
      lat: latitude,
      lon: longitude,
      appid: API_KEY,
      units: 'metric',
      lang: 'kr',
    },
  })

  return response.data
}
