"""
====================
[종합 실습] P284 김정인 (2026-08-06)
1. 비동기 수집
- asyncio + httpx를 사용해 3개 API를 동시에 수집
- asyncio.gather() 활용

2. 스키마 검증
- 수집한 JSON에서 필요한 필드를 추출
- Pydantic v2 모델로 타입과 범위 검증

3. 저장 및 성능 비교
- 검증을 통과한 데이터를 CSV와 Parquet 형식으로 저장
- 읽기 및 쓰기 시간을 측정하여 비교

4. 테스트 및 Git 커밋
- pytest로 스키마 검증 테스트 작성
- ruff로 코드 스타일 검사
====================
"""

import asyncio
import time
from pathlib import Path

import httpx
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# API 요청 후 JSON 반환
async def fetch_json(client, url):
    response = await client.get(url)
    response.raise_for_status()
    return response.json()


# API 3개 동시 호출
async def collect_all():
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&forecast_days=3&timezone=Asia/Seoul"
    country_url = "https://countries.dev/alpha/KOR"
    ip_url = "http://ip-api.com/json/8.8.8.8"
    

    async with httpx.AsyncClient(timeout=20.0) as client:
        weather, country, ip_info = await asyncio.gather(
            fetch_json(client, weather_url),
            fetch_json(client, country_url),
            fetch_json(client, ip_url),
        )

    print("API 호출 성공!")
    return weather, country, ip_info


# Pydantic 모델
class WeatherRecord(BaseModel):
    time: str
    temperature: float = Field(ge=-50, le=60)
    precipitation_probability: float = Field(ge=0, le=100)


class CountryRecord(BaseModel):
    name: str
    capital: str
    region: str
    population: int = Field(gt=0)


class IpRecord(BaseModel):
    country: str
    city: str
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    isp: str


# Pydantic 검증
def validate_records(model, rows):
    valid = []
    errors = []

    for row in rows:
        try:
            record = model(**row)
            valid.append(record.model_dump())

        except ValidationError as error:
            print("\n검증 오류 내용:")
            print(error)

            errors.append(
                {
                    "row": row,
                    "error": error.errors(),
                }
            )

    return valid, errors


# CSV와 Parquet 저장 및 성능 비교
def save_and_compare(records, file_name):
    """검증된 데이터를 CSV와 Parquet로 저장하고 성능 비교"""

    if not records:
        print(f"{file_name}: 저장할 데이터가 없습니다.")
        return

    dataframe = pd.DataFrame(records)

    csv_path = OUTPUT_DIR / f"{file_name}.csv"
    parquet_path = OUTPUT_DIR / f"{file_name}.parquet"

    # CSV 쓰기 시간
    start = time.perf_counter()

    dataframe.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
    )

    csv_write_time = time.perf_counter() - start

    # Parquet 쓰기 시간
    start = time.perf_counter()

    dataframe.to_parquet(
        parquet_path,
        index=False,
    )

    parquet_write_time = time.perf_counter() - start

    # CSV 읽기 시간
    start = time.perf_counter()
    csv_reloaded = pd.read_csv(csv_path)
    csv_read_time = time.perf_counter() - start

    # Parquet 읽기 시간
    start = time.perf_counter()
    parquet_reloaded = pd.read_parquet(parquet_path)
    parquet_read_time = time.perf_counter() - start

    print(f"\n[{file_name} 저장 및 성능 비교]")
    print(f"CSV 쓰기 시간: {csv_write_time:.6f}초")
    print(f"Parquet 쓰기 시간: {parquet_write_time:.6f}초")
    print(f"CSV 읽기 시간: {csv_read_time:.6f}초")
    print(f"Parquet 읽기 시간: {parquet_read_time:.6f}초")

    print(f"CSV 재로딩 건수: {len(csv_reloaded)}")
    print(f"Parquet 재로딩 건수: {len(parquet_reloaded)}")

    assert len(csv_reloaded) == len(records)
    assert len(parquet_reloaded) == len(records)

    print("저장 및 재로딩 검증 완료")

def main():
    weather, country, ip_info = asyncio.run(collect_all())

    # Open-Meteo 응답을 행 단위 데이터로 변환
    weather_rows = [
        {
            "time": time_value,
            "temperature": temperature,
            "precipitation_probability": precipitation,
        }
        for time_value, temperature, precipitation in zip(
            weather["hourly"]["time"],
            weather["hourly"]["temperature_2m"],
            weather["hourly"]["precipitation_probability"],
        )
    ]

    # 국가 API 응답에서 필요한 필드 추출
    country_row = {
        "name": country["name"],
        "capital": country["capital"],
        "region": country["region"],
        "population": country["population"],
    }

    # IP API 응답에서 필요한 필드 추출
    ip_row = {
        "country": ip_info["country"],
        "city": ip_info["city"],
        "lat": ip_info["lat"],
        "lon": ip_info["lon"],
        "isp": ip_info["isp"],
    }

    # Pydantic 검증
    valid_weather, errors_weather = validate_records(
        WeatherRecord,
        weather_rows,
    )

    valid_country, errors_country = validate_records(
        CountryRecord,
        [country_row],
    )

    valid_ip, errors_ip = validate_records(
        IpRecord,
        [ip_row],
    )

    print(
        f"weather: {len(valid_weather)} valid / "
        f"{len(errors_weather)} errors"
    )
    print(
        f"country: {len(valid_country)} valid / "
        f"{len(errors_country)} errors"
    )
    print(
        f"ip_info: {len(valid_ip)} valid / "
        f"{len(errors_ip)} errors"
    )

    # CSV 및 Parquet 저장과 성능 비교
    save_and_compare(valid_weather, "weather")
    save_and_compare(valid_country, "country")
    save_and_compare(valid_ip, "ip_info")


# pipeline.py 파일을 직접 실행한 경우에만 main() 실행
# test_pipeline.py에서 import할 때는 자동 실행되지 않음
if __name__ == "__main__":
    main()