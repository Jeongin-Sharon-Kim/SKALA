"""
CSV 판매 데이터를 안전하게 불러온 뒤 Pydantic 모델로 검증하고,
정상 데이터와 오류 데이터를 분리하여 각각 CSV와 JSON 파일로 저장하는 프로그램입니다.
"""

import csv
import json
import logging
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


# 로그 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


# 현재 파이썬 파일이 있는 폴더
BASE_DIR = Path(__file__).resolve().parent


# 1) 예외 처리 + CSV 파일 읽기
def safe_load_csv(file_path):
    """CSV 파일을 안전하게 읽어 딕셔너리 리스트로 반환"""

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            reader = csv.DictReader(file)
            data = list(reader)

        logger.info("CSV 파일 로딩 성공: %d건", len(data))
        return data

    except FileNotFoundError:
        logger.error("파일을 찾을 수 없습니다: %s", file_path)
        return None

    finally:
        print("로딩 종료")


# 존재하지 않는 파일 테스트
missing_data = safe_load_csv(BASE_DIR / "없는파일.csv")

assert missing_data is None
print("없는 파일 assert 통과")


# 실제 CSV 파일 읽기
input_path = BASE_DIR / "Python_Practice1_Data.csv"
raw_data = safe_load_csv(input_path)

if raw_data is None:
    raise SystemExit("입력 CSV 파일이 없어 프로그램을 종료합니다.")


# 2) Pydantic v2 스키마 정의
class SalesRecord(BaseModel):
    month: str
    region: str
    amount: float = Field(gt=0, description="0보다 큰 금액")
    category: Optional[str] = None

    @field_validator("month", "region")
    @classmethod
    def not_empty(cls, value):
        """month와 region의 빈 문자열 방지"""

        if not value.strip():
            raise ValueError("빈 문자열은 허용되지 않습니다.")

        return value.strip()

    @field_validator("category", mode="before")
    @classmethod
    def empty_category_to_none(cls, value):
        """빈 category는 None으로 변환"""

        if value is None or str(value).strip() == "":
            return None

        return str(value).strip()


# 3) 검증 파이프라인
valid = []
errors = []

for row_number, row in enumerate(raw_data, start=2):
    try:
        record = SalesRecord(**row)

        # Pydantic 모델을 딕셔너리로 변환
        valid.append(record.model_dump())

    except ValidationError as error:
        print(f"\n{row_number}행 검증 오류")
        print(error)

        errors.append({
            "row": row,
            "error": error.errors()
        })


print("\n정상 데이터 개수:", len(valid))
print("오류 데이터 개수:", len(errors))


# 체크포인트 검증
assert len(valid) == 4
assert len(errors) == 3

print("valid 4건 / errors 3건 assert 통과")


# 4) 결과 파일 저장
valid_path = BASE_DIR / "valid_sales.csv"
error_path = BASE_DIR / "errors.json"


# 정상 데이터 CSV 저장
with open(
    valid_path,
    "w",
    encoding="utf-8-sig",
    newline=""
) as file:

    fieldnames = [
        "month",
        "region",
        "amount",
        "category"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(valid)


# 오류 데이터 JSON 저장
with open(
    error_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        errors,
        file,
        ensure_ascii=False,
        indent=2
    )


logger.info("정상 데이터 저장 완료: %s", valid_path.name)
logger.info("오류 데이터 저장 완료: %s", error_path.name)


# 저장된 정상 CSV 다시 읽기
reloaded = safe_load_csv(valid_path)

assert reloaded is not None
assert len(reloaded) == 4

print("재로딩 데이터 개수:", len(reloaded))
print("재로딩 assert 통과")