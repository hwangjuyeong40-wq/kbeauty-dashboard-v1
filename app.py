import streamlit as st

st.error("🔥🔥🔥 현재 실행 중인 app.py 확인용 테스트 🔥🔥🔥")

import pandas as pd
import plotly.express as px

# -----------------------
# 페이지 설정
# -----------------------
st.set_page_config(
    page_title="K-Beauty Insight Lab",
    page_icon="💄",
    layout="wide"
)

# -----------------------
# 데이터 불러오기
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_excel("data_726.xlsx")

    df.columns = [str(col).strip() for col in df.columns]

    sentiment_map = {
        "positive": "긍정",
        "neutral": "중립",
        "negative": "부정",
        "긍정": "긍정",
        "중립": "중립",
        "부정": "부정"
    }

    df["sentiment"] = (
        df["sentiment"]
        .astype(str)
        .str.strip()
        .map(sentiment_map)
        .fillna("중립")
    )

    df["product"] = (
        df["product"]
        .fillna("제품명 없음")
        .astype(str)
    )

    df["review"] = (
        df["review"]
        .fillna("")
        .astype(str)
    )

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    ).fillna(0)

    platform_labels = {
        "kbeauty_platform": "네이버 쇼핑",
        "hwahae": "화해",
        "xiaohongshu": "샤오홍슈"
    }

    df["platform_label"] = (
        df["platform"]
        .astype(str)
        .str.strip()
        .map(platform_labels)
        .fillna(df["platform"])
    )

    return df

df = load_data()

# -----------------------
# 제목
# -----------------------
st.title("💄 K-Beauty Insight Lab")
st.caption(
    "한국 소비자 리뷰 기반 K-뷰티 데이터 분석 플랫폼"
)

# -----------------------
# KPI
# -----------------------
st.subheader("📊 핵심 지표")

col1, col2, col3, col4 = st.columns(4)

positive_count = len(
    df[df["sentiment"] == "긍정"]
)

neutral_count = len(
    df[df["sentiment"] == "중립"]
)

negative_count = len(
    df[df["sentiment"] == "부정"]
)

with col1:
    st.metric("총 리뷰 수", len(df))

with col2:
    st.metric("긍정", positive_count)

with col3:
    st.metric("중립", neutral_count)

with col4:
    st.metric("부정", negative_count)

st.divider()

# -----------------------
# 감성 분석
# -----------------------
st.subheader("😊 감성 분석")

sentiment_df = (
    df["sentiment"]
    .value_counts()
    .reset_index()
)

sentiment_df.columns = [
    "sentiment",
    "count"
]

fig_sentiment = px.pie(
    sentiment_df,
    names="sentiment",
    values="count",
    color="sentiment",
    color_discrete_map={
        "긍정": "blue",
        "중립": "green",
        "부정": "red"
    }
)

st.plotly_chart(
    fig_sentiment,
    use_container_width=True
)

# -----------------------
# 별점 분석
# -----------------------
st.subheader("⭐ 별점 분석")

rating_df = (
    df["rating"]
    .value_counts()
    .sort_index()
    .reset_index()
)

rating_df.columns = [
    "rating",
    "count"
]

fig_rating = px.bar(
    rating_df,
    x="rating",
    y="count",
    title="별점 분포"
)

st.plotly_chart(
    fig_rating,
    use_container_width=True
)

# -----------------------
# 플랫폼 분석
# -----------------------
st.subheader("🌐 플랫폼 분석")

platform_df = (
    df["platform_label"]
    .value_counts()
    .reset_index()
)

platform_df.columns = [
    "platform",
    "count"
]

fig_platform = px.bar(
    platform_df,
    x="platform",
    y="count",
    title="플랫폼별 리뷰 수"
)

st.plotly_chart(
    fig_platform,
    use_container_width=True
)

# -----------------------
# 리뷰 검색
# -----------------------
st.subheader("🔍 리뷰 검색")

keyword = st.text_input(
    "검색어 입력 (예: 촉촉, 발림성, 흡수력)"
)

if keyword:

    result = df[
        df["review"]
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    st.write(
        f"검색 결과: {len(result)}건"
    )

    st.dataframe(
        result[
            [
                "product",
                "rating",
                "sentiment",
                "review"
            ]
        ].head(10),
        use_container_width=True
    )

# -----------------------
# 원본 데이터 조회
# -----------------------
st.subheader(
    "📂 감성별 원본 데이터"
)

tab1, tab2, tab3 = st.tabs(
    ["긍정", "중립", "부정"]
)

with tab1:
    st.dataframe(
        df[
            df["sentiment"] == "긍정"
        ].head(20),
        use_container_width=True
    )

with tab2:
    st.dataframe(
        df[
            df["sentiment"] == "중립"
        ].head(20),
        use_container_width=True
    )

with tab3:
    st.dataframe(
        df[
            df["sentiment"] == "부정"
        ].head(20),
        use_container_width=True
    )

st.success(
    "V1 버전 실행 중"
)