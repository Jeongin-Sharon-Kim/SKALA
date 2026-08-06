"""
====================
[종합 실습] P284 김정인 (2026-08-06)
1. 비동기 수집
- asyncio + httpx를 사용해 위 3개 API를 동시에 수집하는 파이프라인 작성
(asyncio.gather() 활용)
2. 스키마 검증
- 수집한 JSON에서 필요한 필드를 추출하여 Pydantic v2 모델로 타입·범위 검증
3. 저장 및 성능 비교
- 검증 통과한 데이터를 CSV와 Parquet 두 형식으로 저장하고 읽기/쓰기 시간 측정·비교
4. 테스트 및 Git 커밋
- pytest로 스키마 검증 테스트 작성, ruff로 코드 스타일 검사 결과 정리
=====================
"""

import asyncio
import csv
import json
import httpx
import pandas as pd

from pathlib import Path
from pydantic import BaseModel, Field, ValidationError


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


async def fetch_json(client, url):
    response = await client.get(url)
    response.raise_for_status()
    return response.json()

#api 3개 동시에 받기
async def collect_all():
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude=37.5665&longitude=126.9780&hourly=temperature_2m,precipitation_probability&forecast_days=3&timezone=Asia/Seoul"
    country_url = "https://countries.dev/alpha/KOR"
    ip_url = "http://ip-api.com/json/8.8.8.8"

    async with httpx.AsyncClient() as client:
        weather, country, ip_info = await asyncio.gather(
            fetch_json(client, weather_url),
            fetch_json(client, country_url),
            fetch_json(client, ip_url)
        )

    return weather, country, ip_info


#####################Pydantic 모델########################

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


###타입 오류시 예외 처리####
def validate_records(model, rows):
    valid, errors = [], []
    for row in rows:  # rows의 각 행(dict)을 하나씩 model로 검증
        try:
            record = model(**row)

            # 검증 성공 데이터
            valid.append(record.model_dump())

        except ValidationError as error:
            # 검증 실패 내용 출력
            print("\n검증 오류 내용:")
            print(error)

            # 실패한 원본 행과 오류 내용 저장
            errors.append({
                "row": row,
                "error": error.errors()
            })
    return valid, errors


if __name__ == "__main__":
    weather, country, ip_info = asyncio.run(collect_all())

    # open-meteo는 hourly 배열들을 따로 주기 때문에 행 단위로 묶어줌
    weather_rows = [
        {"time": t, "temperature": temp, "precipitation_probability": precip}
        for t, temp, precip in zip(
            weather["hourly"]["time"],
            weather["hourly"]["temperature_2m"],
            weather["hourly"]["precipitation_probability"],
        )
    ]

    valid_weather, errors_weather = validate_records(WeatherRecord, weather_rows)
    valid_country, errors_country = validate_records(CountryRecord, [country])
    valid_ip, errors_ip = validate_records(IpRecord, [ip_info])

    print(f"weather: {len(valid_weather)} valid / {len(errors_weather)} errors")
    print(f"country: {len(valid_country)} valid / {len(errors_country)} errors")
    print(f"ip_info: {len(valid_ip)} valid / {len(errors_ip)} errors")


# 결과 파일 경로
valid_path = fetch_json / "valid_weather.csv"
errors_path = fetch_json / "errors.json"


# 정상 데이터 CSV 저장
with open(
    valid_path,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:
    fieldnames = ["month", "region", "amount", "category"]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(valid)


# 오류 데이터 JSON 저장
with open(
    errors_path,
    "w",
    encoding="utf-8"
) as file:
    json.dump(
        errors,
        file,
        ensure_ascii=False,
        indent=2
    )


print("valid_sales.csv 저장 완료")
print("errors.json 저장 완료")