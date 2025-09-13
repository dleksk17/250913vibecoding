import streamlit as st
import pandas as pd
import altair as alt
import os

# 앱 제목
st.title("🌍 MBTI 유형별 국가 TOP10 시각화")

# 기본 파일 경로
default_file = "countriesMBTI_16types.csv"

# 데이터 로드 함수
def load_data():
    if os.path.exists(default_file):
        st.success("기본 데이터 파일을 불러왔습니다 ✅")
        return pd.read_csv(default_file)
    else:
        uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])
        if uploaded_file is not None:
            st.success("업로드한 파일을 불러왔습니다 📂")
            return pd.read_csv(uploaded_file)
        else:
            st.warning("데이터 파일이 없습니다. 업로드해주세요.")
            return None

# 데이터 불러오기
df = load_data()

if df is not None:
    # MBTI 유형 목록 추출 (첫 번째 열은 'Country'이므로 제외)
    mbti_types = df.columns[1:].tolist()

    # 사용자에게 MBTI 유형 선택 옵션 제공
    selected_type = st.selectbox("MBTI 유형을 선택하세요", mbti_types)

    # 선택한 MBTI 유형 기준 TOP10 국가 추출
    top10 = df.nlargest(10, selected_type)[["Country", selected_type]]

    # Altair 그래프 그리기
    chart = (
        alt.Chart(top10)
        .mark_bar()
        .encode(
            x=alt.X(selected_type, title="비율"),
            y=alt.Y("Country", sort="-x", title="국가"),
            tooltip=["Country", selected_type]
        )
        .interactive()
    )

    st.subheader(f"📊 {selected_type} 유형 비율이 높은 국가 TOP10")
    st.altair_chart(chart, use_container_width=True)
