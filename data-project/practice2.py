"""
===================================
[실습 2] 파일 I/O, 예외 처리, Pydantic 검증 파이프라인 
P284 김정인 (2026-08-06)
프로그램 설명: 
    1) safe_load_csv(): try-expectt-finally, logging을 사용한 파일 읽기 예외 처리
    2) Pydantic v2 스키마 정의
    3) 검증 파이프라인 구축(valid / errors 분리)
    4) 결과 파일 저장 및 재로딩 확인 : valid는 CSV로, errors는 JSON으로 저장 및 건수 검증
================
"""

import csv
import json
import logging
from pathlib import Path
from typing import Annotated, Optional
from pydantic import BaseModel, Field, StringConstraints, ValidationError, field_validator

# 앞뒤 공백 제거 후 최소 1글자 이상이어야 하는 문자열 (빈 문자열/공백만 입력 시 자동으로 오류 처리)
NonBlankStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


# 기준 경로
BASE_DIR = Path(__file__).resolve().parent

#로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)


def safe_load_csv(file_path):
    """JSON 판매 데이터를 안전하게 읽어 dict 리스트로 반환"""

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        logger.info("파일 로딩 성공: 전체 %d건", len(data))
        return data

    except FileNotFoundError:
        # 파일이 없어도 프로그램이 죽지 않도록 None을 반환하고 호출부에서 처리하게 함
        logger.error("파일을 찾을 수 없습니다: %s", file_path)
        return None

    finally:
        # try에서 성공하든 except로 빠지든 항상 마지막에 한 번 실행됨
        print("로딩 종료")


# 실제 JSON 파일 읽기
raw_data = safe_load_csv(
    BASE_DIR / "Edit_Data.json"
)

print("실제 데이터 건수:", len(raw_data))


# 존재하지 않는 파일 테스트
missing_data = safe_load_csv(
    BASE_DIR / "없는파일.json"
)

assert missing_data is None
print("없는 파일 assert 통과")






class SalesRecord(BaseModel):
    """"
    dict 형태의 원본 row 하나를 이 클래스에 넣으면 타입/조건에 맞는지 자동 검증됨
    """
    month: NonBlankStr  
    region: NonBlankStr
    amount: float = Field(gt=0, description="0보다 큰 금액")  # amount가 0 이하면 검증 실패
    category: Optional[str] = None  # 없어도 되는 값

    @field_validator("category", mode="before")
    @classmethod
    def empty_category_to_none(cls, value):
        # category가 빈 문자열이면 None으로 처리
        value = str(value).strip() if value is not None else ""
        return value or None




# 검증 통과한 행은 valid, 실패한 행은 원본+오류내용을 errors에 모음
valid = []
errors = []


if raw_data is not None:
    for row in raw_data:  # raw_data의 각 행(dict)을 하나씩 SalesRecord로 검증
        try:
            # 각 딕셔너리를 SalesRecord 모델로 검증
            record = SalesRecord(**row)

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


print("\n정상 데이터 개수:", len(valid))
print("오류 데이터 개수:", len(errors))


assert len(valid) == 4
assert len(errors) == 3

print("valid 4건 / errors 3건 assert 통과")



# 결과 파일 경로
valid_path = BASE_DIR / "valid_sales.csv"
errors_path = BASE_DIR / "errors.json"


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


# 저장된 정상 CSV 재로딩
with open(
    valid_path,
    "r",
    encoding="utf-8-sig",
    newline=""
) as file:
    reloaded = list(csv.DictReader(file))


print("재로딩 데이터 개수:", len(reloaded))

assert len(reloaded) == 4
print("재로딩 후 4건 assert 통과")