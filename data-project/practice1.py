"""
============================================================
[심화 실습] P284 김정인
============================================================

목적
----
Python_Practice1_Data.json 파일의 지역·카테고리·월별 매출
거래 데이터 100건을 읽어 다음 기능을 수행한다.

1) amount가 1000 이상인 거래를 필터링하고,
    지역별 총매출을 컴프리헨션으로 계산한다.

2) Counter와 defaultdict를 사용해
    지역별 거래 건수와 카테고리별 amount 리스트를 집계한다.

3) amount가 1000보다 큰 거래를 반환하는 제너레이터를 작성하고,
    동일 조건의 리스트와 메모리 사용량을 비교한다.

4) month와 category를 기준으로 매출을 그룹화하고,
    월별·카테고리별 총매출과 매출 상위 3개 항목을 출력한다.

"""

import json
import sys
from collections import Counter, defaultdict

"""
판매 데이터를 JSON 파일에서 불러와
거래 필터링, 지역별 거래 집계, 제너레이터 메모리 비교,
월별·카테고리별 매출과 매출 TOP3를 계산한다.
"""


# JSON 파일 읽기
try:
    with open(
        "Python_Practice1_Data.json",
        "r",
        encoding="utf-8"
    ) as file:
        sales = json.load(file)

except FileNotFoundError:
    print("오류: Python_Practice1_Data.json 파일을 찾을 수 없습니다.")
    sys.exit()

print("전체 거래 건수:", len(sales))


# 1번 문제: 리스트/딕셔너리 컴프리헨션
"""
    amount>= 1000인 거래만 필터링,
    딕셔너리로 지역별 총매출 계산
"""

amount_filter = [deal for deal in sales 
                if deal["amount"] >= 1000]
regions = {deal["region"] for deal in amount_filter}

region_total = {
    region: 
    sum(deal["amount"] for deal in amount_filter
        if deal["region"] == region)for region in regions}


print("\n매출 1000 이상 거래")
print(amount_filter)

print("\n지역별 총매출")
print(region_total)


# 2번 문제: counter + defaultdict
# Counter로 지역별 거래 건수 계산
region_count = Counter(deal["region"] for deal in sales)
category_amounts = defaultdict(list)

for deal in sales:category_amounts[deal["category"]].append(deal["amount"])

print("\n지역별 거래 건수")
print(region_count)

print("\n지역별 거래 건수 순위")
print(region_count.most_common())

print("\n카테고리별 amount 리스트")
print(dict(category_amounts))

# 3번 문제: 제네레이터-메모리 비교
# amount가 1000보다 큰 거래만 yield
def high_amount_generator(sales):
    """amount가 1000보다 큰 거래를 하나씩 반환"""

    for deal in sales:
        if deal["amount"] > 1000:
            yield deal
            
def compare_memory(sales):
    """리스트, 제너레이터의 메모리 크기 비교"""

    high_amount_list = [deal for deal in sales
                        if deal["amount"] > 1000]

    high_amount_gen = high_amount_generator(sales)

    list_memory = sys.getsizeof(high_amount_list)
    generator_memory = sys.getsizeof(high_amount_gen)

    print("\n리스트 메모리:", list_memory, "bytes")
    print("제너레이터 메모리:", generator_memory, "bytes")

compare_memory(sales)

# 4) 종합 - 월별 카테고리 매출 집계
def calculate_monthly_sales(sales):
    """
    month와 category를 기준으로 총매출 계산,
    월별 중첩 딕셔너리 형태로 반환하는 함수
    """

    monthly_category = {
        (deal["month"], deal["category"])
        for deal in sales
    }

    month_category_total = {
        pair: sum(
            deal["amount"]
            for deal in sales
            if deal["month"] == pair[0]
            and deal["category"] == pair[1]
        )
        for pair in monthly_category
    }

    monthly_sales = defaultdict(dict)

    for (month, category), total in month_category_total.items():
        monthly_sales[month][category] = total

    return monthly_sales, month_category_total

# 함수 호출 및 반환값 저장
monthly_sales, month_category_total = calculate_monthly_sales(sales)

# 월별 카테고리 총매출 출력
print("\n월별 카테고리 총매출")

for month in sorted(monthly_sales):
    print(f"\n[{month}]")

    for category in sorted(monthly_sales[month]):
        print(f"{category}: {monthly_sales[month][category]}")


# 금액 내림차순 TOP3
top3 = sorted(
    month_category_total.items(),
    key=lambda item: item[1],
    reverse=True
)[:3]

print("\n월별 카테고리 매출 TOP3")

for rank, ((month, category), total) in enumerate(top3, start=1):
    print(f"{rank}위: {month} / {category} / {total}")