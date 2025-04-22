# bookmark.py (즐겨찾기 페이지)
import streamlit as st
import pandas as pd
import os
import json
import requests
import sqlite3

API_URL = "http://localhost:8000/api/games/"

# sqlite 연결 함수
def load_data_from_sqlite(db_path="db.sqlite3"):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM games_game;"  # 테이블 이름이 games_game인 경우
    df = pd.read_sql_query(query, conn)
    conn.close()

@st.cache_data
def load_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df = df.rename(columns={
            "game_name": "게임이름",
            "original_price": "정가",
            "discount_price": "할인가",
            "discount_startdate": "할인시작일",
            "discount_enddate": "할인종료일",
            "genre": "장르",
            "release_date": "발매일",
            "maker": "메이커",
            "play_number": "플레이인원",
            "product_type": "상품유형",
            "game_language": "언어",
            "game_image_url": "이미지",
            "game_url": "링크"
        })
        df["할인율"] = ((df["정가"] - df["할인가"]) / df["정가"] * 100).round(2)
        return df
    else:
        st.error("게임 데이터를 불러오지 못했습니다.")
        return pd.DataFrame()

def save_favorites():
    with open("data/favorites.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.favorites, f, ensure_ascii=False, indent=2)

if "favorites" not in st.session_state:
    if os.path.exists("data/favorites.json"):
        with open("data/favorites.json", "r", encoding="utf-8") as f:
            st.session_state.favorites = json.load(f)
    else:
        st.session_state.favorites = []

df = load_data()
# df = load_data_from_sqlite() # sqlite DB 사용 시
df = df[df["게임이름"].isin(st.session_state.favorites)]

st.title("⭐ 즐겨찾기 목록")

# 필터 입력
with st.container():
    st.markdown("### 🔍 검색 및 필터")
    row1_col1, row1_col2 = st.columns([3, 3])
    with row1_col1:
        search = st.text_input("게임 이름 검색", placeholder="예: 젤다")
    with row1_col2:
        sort_option = st.selectbox("정렬 기준", ["기본", "할인율 높은 순", "할인가 낮은 순"])

    row2_col1, row2_col2 = st.columns([3, 3])
    with row2_col1:
        genre_options = sorted(df["장르"].dropna().unique())
        selected_genre = st.multiselect("장르 선택", options=genre_options)
    with row2_col2:
        maker_options = sorted(df["메이커"].dropna().unique())
        selected_maker = st.multiselect("제작사 선택", options=maker_options)

# 필터 적용
results = df.copy()
if search:
    results = results[results["게임이름"].str.contains(search, case=False, na=False)]
if selected_genre:
    results = results[results["장르"].isin(selected_genre)]
if selected_maker:
    results = results[results["메이커"].isin(selected_maker)]
if sort_option == "할인율 높은 순":
    results = results.sort_values("할인율", ascending=False)
elif sort_option == "할인가 낮은 순":
    results = results.sort_values("할인가")

# 게임 목록 출력 (3열 카드 배열)
st.markdown("### 🎯 즐겨찾기 결과")
rows = [results.iloc[i:i+3] for i in range(0, len(results), 3)]
for row_group in rows:
    cols = st.columns(3)
    for idx, (_, row) in enumerate(row_group.iterrows()):
        with cols[idx]:
            st.image(row["이미지"], width=180)
            st.write(f"**{row['게임이름']}**")
            st.write(f"💰 {row['할인가']}원 / {row['정가']}원")
            st.write(f"🔥 할인율: {row['할인율']}%")
            # 상세 보기 버튼
            if st.button("📄 상세 보기", key=f"detail_{row['게임이름']}_bookmark"):
                st.session_state.selected_game = row["게임이름"]
                st.switch_page("pages/1_details.py")