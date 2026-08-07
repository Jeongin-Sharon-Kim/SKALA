"""
===========================================
[실습 3] Pandas EDA · Polars Lazy · DuckDB SQL 비교
작성자 : 판교 9반 김정인 (P284)
작성일 : 2026-08-07

1) Pandas EDA 기초 탐색 + 이상치 처리
- sales_100k.csv를 불러 기본 정보 확인
- amount 컬럼의 결측치 및 IQR 기준 이상치 확인
- IQR 정상 범위:
  Q1 - 1.5 * IQR ~ Q3 + 1.5 * IQR

2) Pandas groupby
- region, category별 총매출·평균·건수 계산
- named aggregation 사용
- 총매출(total) 기준 내림차순 정렬

3) Polars Lazy API
- scan_csv → filter → group_by → agg → sort → collect

4) DuckDB SQL
- SQL GROUP BY를 이용해 동일한 집계 수행

5) 실행 시간 비교
- Pandas / Polars / DuckDB를 동일 횟수로 실행
- 각 도구가 CSV 읽기부터 집계까지 수행하도록 조건 통일
===========================================
"""

from pathlib import Path
import timeit

import pandas as pd
import polars as pl
import duckdb


CSV_PATH = Path(__file__).resolve().parent / "sales_100k.csv"
REQUIRED_COLUMNS = {"region", "category", "amount"}

# ==========================================
# 1. CSV 로드 및 Pandas EDA
# ==========================================

def load_data():
    """CSV 파일을 Pandas DataFrame으로 불러옵니다."""

    try:
        df = pd.read_csv(CSV_PATH)

    except FileNotFoundError:
        print(f"오류: CSV 파일을 찾을 수 없습니다.")
        print(f"확인 경로: {CSV_PATH}")
        raise

    except Exception as e:
        print(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        raise

    # 필요한 컬럼이 존재하는지 확인
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"필수 컬럼이 없습니다: {missing_columns}"
        )

    return df


def print_eda(df):
    """데이터의 기본 정보, 상위 행, 기술 통계, 결측치를 출력합니다."""

    print("========== 기본 정보 ==========")
    df.info()

    print("\n========== 상위 5개 행 ==========")
    print(df.head())

    print("\n========== 기술 통계 ==========")
    print(df.describe(include="all"))

    print("\n========== 결측치 개수 ==========")
    print(df.isnull().sum())


# ==========================================
# IQR 이상치 기준 계산
# ==========================================

def calculate_iqr_bounds(df):
    """amount 컬럼의 IQR 정상 범위를 계산합니다."""

    print("\n========== IQR 이상치 제거 ==========")

    # amount의 1사분위수와 3사분위수
    Q1 = df["amount"].quantile(0.25)
    Q3 = df["amount"].quantile(0.75)

    # IQR 계산
    IQR = Q3 - Q1

    # IQR 기준 정상 범위
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # amount 결측치 개수
    missing_count = df["amount"].isnull().sum()

    # 실제 IQR 이상치 개수
    outlier_count = (
        (df["amount"] < lower_bound)
        | (df["amount"] > upper_bound)
    ).sum()

    # 정상 범위 데이터
    df_clean = df[
        df["amount"].between(lower_bound, upper_bound)
    ].copy()

    print("Q1:", Q1)
    print("Q3:", Q3)
    print("IQR:", IQR)
    print("하한값:", lower_bound)
    print("상한값:", upper_bound)

    print("amount 결측치 수:", missing_count)
    print("IQR 이상치 수:", outlier_count)

    print("이상치 제거 전 행 수:", len(df))
    print("이상치 제거 후 행 수:", len(df_clean))
    print("제거된 전체 행 수:", len(df) - len(df_clean))

    return lower_bound, upper_bound


# ==========================================
# 2. Pandas groupby + named aggregation
# ==========================================

def run_pandas(csv_path, lower_bound, upper_bound):
    """
    Pandas로 CSV를 읽고 이상치를 제거한 뒤 region·category별 총매출·평균·건수를 집계합니다.
    """

    df = pd.read_csv(csv_path)
    # amount 정상 범위 + region/category 결측치 제외
    df = df[
        df["amount"].between(lower_bound, upper_bound)
        & df["region"].notna()
        & df["category"].notna()
    ]

    # named aggregation으로 결과 컬럼명 직접 지정
    result = (
        df
        .groupby(["region", "category"])
        .agg(
            total=("amount", "sum"),
            mean=("amount", "mean"),
            count=("amount", "count")
        )
        .reset_index()
        .sort_values("total", ascending=False)
    )

    return result


# ==========================================
# 3. Polars Lazy API
# ==========================================

def run_polars(csv_path, lower_bound, upper_bound):
    """
    Polars Lazy API를 이용하여 Pandas와 동일한 집계를 수행
    scan_csv → filter → group_by → agg → sort → collect
    """

    result = (
        pl.scan_csv(str(csv_path))
        .filter(
            pl.col("amount").is_not_null()
            & pl.col("amount").is_between(
                lower_bound,
                upper_bound
            )
            & pl.col("region").is_not_null()
            & pl.col("category").is_not_null()
        )
        .group_by(["region", "category"])
        .agg(
            pl.col("amount").sum().alias("total"),
            pl.col("amount").mean().alias("mean"),
            pl.col("amount").count().alias("count")
        )
        .sort("total", descending=True)
        .collect()
    )

    return result


# ==========================================
# 4. DuckDB SQL
# ==========================================

def run_duckdb(csv_path, lower_bound, upper_bound):
    """
    DuckDB SQL을 이용하여 Pandas와 동일한 집계 수행
    """
    result = duckdb.sql(
        f"""
        SELECT
            region,
            category,
            SUM(amount) AS total,
            AVG(amount) AS mean,
            COUNT(amount) AS count

        FROM read_csv_auto('{csv_path}')

        WHERE amount IS NOT NULL
            AND amount BETWEEN {lower_bound} AND {upper_bound}
            AND region IS NOT NULL
            AND category IS NOT NULL

        GROUP BY
            region,
            category

        ORDER BY
            total DESC
        """
    ).df()

    return result

# ==========================================
# 메인 프로그램 : Pandas EDA · Polars Lazy · DuckDB SQL 비교
# ==========================================

def main():

    # 1. Pandas EDA
    df = load_data()
    print_eda(df)

    lower_bound, upper_bound = calculate_iqr_bounds(df) # IQR 정상 범위 계산


    # 2. Pandas 집계 결과
    print("\n========== Pandas groupby ==========")

    pandas_result = run_pandas(
        CSV_PATH,
        lower_bound,
        upper_bound
    )

    print(pandas_result)

    # 3. Polars Lazy API 결과
    print("\n========== Polars Lazy API ==========")

    polars_result = run_polars(
        CSV_PATH,
        lower_bound,
        upper_bound
    )

    print(polars_result)

    # 4. DuckDB SQL 결과
    print("\n========== DuckDB SQL ==========")

    duckdb_result = run_duckdb(
        CSV_PATH,
        lower_bound,
        upper_bound
    )

    print(duckdb_result)


    # 5. 실행 시간 비교

    print("\n========== 실행 시간 비교 ==========")

    # 세 도구 모두 동일하게 3회 반복
    repeat_count = 3

    pandas_time = timeit.timeit(
        lambda: run_pandas(
            CSV_PATH,
            lower_bound,
            upper_bound
        ),
        number=repeat_count
    )

    polars_time = timeit.timeit(
        lambda: run_polars(
            CSV_PATH,
            lower_bound,
            upper_bound
        ),
        number=repeat_count
    )

    duckdb_time = timeit.timeit(
        lambda: run_duckdb(
            CSV_PATH,
            lower_bound,
            upper_bound
        ),
        number=repeat_count
    )

    print(f"반복 횟수: {repeat_count}회")
    print(f"Pandas 실행 시간: {pandas_time:.4f}초")
    print(f"Polars 실행 시간: {polars_time:.4f}초")
    print(f"DuckDB 실행 시간: {duckdb_time:.4f}초")


# 해당 파일을 실행했을 때만 main() 실행
if __name__ == "__main__":

    try:
        main()

    except Exception as e:
        print("\n========== 프로그램 실행 오류 ==========")
        print(f"오류 내용: {e}")





# ============================================================
# Practice 4
# 시각화 4종 · 통계 검정 · sklearn Pipeline · Plotly
# ============================================================
"""
[실습 4 설명]
실습 3에서 사용한 sales_100k.csv를 연계하여 다음 작업을 수행한다.

1) IQR 이상치가 제거된 데이터를 이용한 EDA 시각화 4종
    - 히스토그램 + KDE
    - 박스플롯
    - 월별 매출 라인 차트
    - 상관관계 히트맵
    - 하나의 2x2 subplot으로 구성

2) 통계 검정
    - 서울과 부산의 평균 매출 차이를 독립표본 t-test로 검정
    - region과 category의 독립성을 카이제곱 검정으로 확인
    - 각 검정의 p-value와 유의 여부를 출력

3) sklearn Pipeline
    - ColumnTransformer로 수치형/범주형 변수를 전처리
    - Pipeline에 전처리 + 모델을 함께 구성
    - fit / predict / score 수행
    - joblib로 모델 저장 후 다시 로딩

4) Plotly
    - region·category별 총매출 막대 차트 생성
    - HTML 파일로 저장
"""

import matplotlib.pyplot as plt
import seaborn as sns

from scipy import stats
from scipy.stats import chi2_contingency

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

import joblib
import plotly.express as px


# ============================================================
# 실습 4 데이터 준비
# ============================================================

def prepare_practice4_data():
    """
    sales_100k.csv를 불러온 후
    실습 3처럼 amount의 IQR 정상 범위만 남긴다.
    """

    try:
        df = pd.read_csv(CSV_PATH)

        # 날짜 컬럼을 datetime으로 변환
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

        # amount 기준 IQR 계산
        q1 = df["amount"].quantile(0.25)
        q3 = df["amount"].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        # amount 결측치 및 IQR 이상치 제거
        clean_df = df[
            df["amount"].between(lower, upper)
        ].copy()

        print("\n========== Practice 4 데이터 준비 ==========")
        print("원본 데이터:", len(df), "행")
        print("IQR 이상치 제거 후:", len(clean_df), "행")

        return clean_df

    except FileNotFoundError:
        print(f"오류: CSV 파일을 찾을 수 없습니다.")
        print(f"경로: {CSV_PATH}")
        raise

    except Exception as e:
        print(f"Practice 4 데이터 준비 중 오류 발생: {e}")
        raise


# ============================================================
# 1. EDA 시각화 4종
# ============================================================

def create_visualizations(df):
    """
    하나의 2x2 subplot에 다음 4가지 시각화를 출력합니다.

    1. amount 히스토그램 + KDE
    2. amount 박스플롯
    3. 월별 총매출 라인 차트
    4. 수치형 변수 상관관계 히트맵
    """

    print("\n========== 1. EDA 시각화 4종 ==========")

    # 반드시 2x2 subplot 사용
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(16, 11)
    )

    # --------------------------------------------------------
    # 1) 히스토그램 + KDE
    # --------------------------------------------------------

    sns.histplot(
        data=df,
        x="amount",
        kde=True,
        bins=40,
        ax=axes[0, 0]
    )

    axes[0, 0].set_title("Amount Distribution")
    axes[0, 0].set_xlabel("Amount")


    # --------------------------------------------------------
    # 2) 박스플롯
    # --------------------------------------------------------

    sns.boxplot(
        data=df,
        x="amount",
        ax=axes[0, 1]
    )

    axes[0, 1].set_title("Amount Boxplot")
    axes[0, 1].set_xlabel("Amount")


    # --------------------------------------------------------
    # 3) 월별 총매출 라인 차트
    # --------------------------------------------------------

    # order_date에서 월 단위 값 생성
    monthly_sales = (
        df
        .dropna(subset=["order_date"])
        .assign(
            month=lambda x:
            x["order_date"].dt.to_period("M").astype(str)
        )
        .groupby("month")["amount"]
        .sum()
    )

    axes[1, 0].plot(
        monthly_sales.index,
        monthly_sales.values,
        marker="o"
    )

    axes[1, 0].set_title("Monthly Total Sales")
    axes[1, 0].set_xlabel("Month")
    axes[1, 0].set_ylabel("Total Amount")

    # x축 날짜가 겹치지 않도록 회전
    axes[1, 0].tick_params(
        axis="x",
        rotation=90
    )

    # --------------------------------------------------------
    # 4) 상관관계 히트맵
    # --------------------------------------------------------

    numeric_columns = [
        "quantity",
        "unit_price",
        "customer_age",
        "amount"
    ]

    correlation = (
        df[numeric_columns]
        .corr()
    )

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=axes[1, 1]
    )

    axes[1, 1].set_title("Correlation Heatmap")


    # 그래프 간격 자동 조절
    plt.tight_layout()

    # 4개의 차트를 하나의 figure로 출력
    plt.show()


# ============================================================
# 2-1. 서울 vs 부산 독립표본 t-test
# ============================================================

def run_t_test(df):
    """
    서울과 부산의 평균 amount 차이가
    통계적으로 유의한지 독립표본 t-test로 확인합니다.
    """

    print("\n========== 2-1. 서울 vs 부산 t-test ==========")

    # 서울과 부산의 amount 값 추출
    seoul = (
        df.loc[df["region"] == "서울", "amount"]
        .dropna()
    )

    busan = (
        df.loc[df["region"] == "부산", "amount"]
        .dropna()
    )

    if len(seoul) == 0 or len(busan) == 0:
        print("오류: 서울 또는 부산 데이터가 없습니다.")
        return

    # Welch's t-test
    # 두 집단의 분산이 같다고 가정하지 않음
    t_stat, p_value = stats.ttest_ind(
        seoul,
        busan,
        equal_var=False
    )

    print(f"서울 평균 매출: {seoul.mean():,.2f}")
    print(f"부산 평균 매출: {busan.mean():,.2f}")

    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_value:.6f}")

    # p-value 해석
    if p_value < 0.05:
        print(
            "해석: p-value < 0.05이므로 서울과 부산의 평균 매출 차이는 통계적으로 유의하다."
        )

    else:
        print(
            "해석: p-value >= 0.05이므로 서울과 부산의 평균 매출 차이는 통계적으로 유의하다고 보기 어렵다."
        )


# ============================================================
# 2-2. region × category 카이제곱 검정
# ============================================================

def run_chi_square(df):
    """
    region과 category 두 범주형 변수가
    서로 독립적인지 카이제곱 검정으로 확인합니다.
    """

    print("\n========== 2-2. 카이제곱 검정 ==========")

    # region과 category 결측치 제거
    chi_df = df.dropna(
        subset=["region", "category"]
    )

    # 분할표 생성
    contingency_table = pd.crosstab(
        chi_df["region"],
        chi_df["category"]
    )

    print("\n[region × category 분할표]")
    print(contingency_table)

    # 카이제곱 독립성 검정
    chi2, p_value, dof, expected = chi2_contingency(
        contingency_table
    )

    print(f"\nChi-square statistic: {chi2:.4f}")
    print(f"자유도: {dof}")
    print(f"p-value: {p_value:.6f}")

    # p-value 해석
    if p_value < 0.05:
        print(
            "해석: p-value < 0.05이므로 "
            "region과 category는 서로 독립적이지 않으며 "
            "통계적으로 유의한 관련성이 있다고 판단합니다."
        )

    else:
        print(
            "해석: p-value >= 0.05이므로 "
            "region과 category 사이에 "
            "통계적으로 유의한 관련성이 있다고 보기 어렵습니다."
        )


# ============================================================
# 3. sklearn Pipeline 구성 + 저장
# ============================================================

def build_and_save_pipeline(df):
    """
    amount를 예측하는 회귀 Pipeline을 구성합니다.

    - 수치형 변수: 결측치 처리 + 표준화
    - 범주형 변수: 결측치 처리 + One-Hot Encoding
    - LinearRegression 모델 사용
    - fit / predict / score 수행
    - joblib 파일로 저장 후 재로딩
    """

    print("\n========== 3. sklearn Pipeline ==========")

    # --------------------------------------------------------
    # 입력 변수와 예측 대상
    # --------------------------------------------------------

    numeric_features = [
        "quantity",
        "unit_price",
        "customer_age"
    ]

    categorical_features = [
        "region",
        "category",
        "payment_method",
        "customer_gender"
    ]

    feature_columns = (
        numeric_features
        + categorical_features
    )

    X = df[feature_columns].copy()
    y = df["amount"]


    # --------------------------------------------------------
    # 학습 / 테스트 데이터 분리
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    # --------------------------------------------------------
    # 수치형 변수 전처리
    # --------------------------------------------------------

    numeric_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )


    # --------------------------------------------------------
    # 범주형 변수 전처리
    # --------------------------------------------------------

    categorical_transformer = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )


    # --------------------------------------------------------
    # ColumnTransformer
    # --------------------------------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                numeric_transformer,
                numeric_features
            ),
            (
                "cat",
                categorical_transformer,
                categorical_features
            )
        ]
    )


    # --------------------------------------------------------
    # 전처리 + 모델을 하나의 Pipeline으로 구성
    # --------------------------------------------------------

    model_pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                LinearRegression()
            )
        ]
    )


    # --------------------------------------------------------
    # 모델 학습
    # --------------------------------------------------------

    model_pipeline.fit(
        X_train,
        y_train
    )


    # --------------------------------------------------------
    # 예측
    # --------------------------------------------------------

    predictions = model_pipeline.predict(
        X_test
    )


    # --------------------------------------------------------
    # 모델 평가
    # --------------------------------------------------------

    score = model_pipeline.score(
        X_test,
        y_test
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    print(f"Pipeline score(R²): {score:.4f}")
    print(f"R²: {r2:.4f}")
    print(f"RMSE: {rmse:,.2f}")


    # --------------------------------------------------------
    # 모델 파일 저장
    # --------------------------------------------------------

    model_path = (
        Path(__file__).resolve().parent
        / "practice4_pipeline.joblib"
    )

    joblib.dump(
        model_pipeline,
        model_path
    )

    print(f"모델 저장 완료: {model_path}")


    # --------------------------------------------------------
    # 저장된 모델 다시 불러오기
    # --------------------------------------------------------

    loaded_pipeline = joblib.load(
        model_path
    )

    loaded_score = loaded_pipeline.score(
        X_test,
        y_test
    )

    print(
        f"재로딩 모델 score(R²): "
        f"{loaded_score:.4f}"
    )

    return model_pipeline


# ============================================================
# 4. Plotly 인터랙티브 차트
# ============================================================

def create_plotly_chart(df):
    """
    region·category별 총매출을 집계한 후
    Plotly Express 막대 차트를 생성하고 HTML로 저장합니다.
    """

    print("\n========== 4. Plotly 차트 ==========")

    # region / category 결측치 제거 후 집계
    group_result = (
        df
        .dropna(subset=["region", "category"])
        .groupby(
            ["region", "category"],
            as_index=False
        )
        .agg(
            total=("amount", "sum")
        )
    )


    # Plotly Express 막대 차트 생성
    fig = px.bar(
        group_result,
        x="region",
        y="total",
        color="category",
        barmode="group",
        title="Region · Category Total Sales",
        labels={
            "region": "Region",
            "total": "Total Sales",
            "category": "Category"
        }
    )


    # HTML 저장 경로
    html_path = (
        Path(__file__).resolve().parent
        / "practice4_sales_chart.html"
    )


    # 인터랙티브 HTML 파일 저장
    fig.write_html(
        str(html_path)
    )

    print(f"Plotly HTML 저장 완료: {html_path}")

    # 필요하면 브라우저 화면에도 출력
    fig.show()


# ============================================================
# Practice 4 실행
# ============================================================

def run_practice4():
    """
    Practice 4의 전체 과정을 순서대로 실행합니다.
    """

    try:
        # 실습 3과 동일한 IQR 처리 데이터 준비
        practice4_df = prepare_practice4_data()

        # 1. 2x2 EDA 시각화
        create_visualizations(
            practice4_df
        )

        # 2. 통계 검정
        run_t_test(
            practice4_df
        )

        run_chi_square(
            practice4_df
        )

        # 3. sklearn Pipeline
        build_and_save_pipeline(
            practice4_df
        )

        # 4. Plotly 차트
        create_plotly_chart(
            practice4_df
        )

        print(
            "\n========== Practice 4 완료 =========="
        )

    except Exception as e:
        print(
            "\n========== Practice 4 실행 오류 =========="
        )
        print(f"오류 내용: {e}")


# practice3 실행이 끝난 뒤 Practice 4 실행
if __name__ == "__main__":
    run_practice4()