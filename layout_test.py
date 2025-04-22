# ✅ popular_games_ui.py (Streamlit 카드 스타일 예시)
import streamlit as st

# 타이틀 및 설명
st.title("🔥 인기 게임 할인 목록")
st.markdown("최고 인기 게임의 현재 할인 정보를 확인하세요!")

# 카드 데이터를 수동 예시로 정의
popular_games = [
    {
        "이름": "Hades",
        "국기": "🇧🇷",
        "가격": "R$32,36",
        "할인": "-65%",
        "이미지": "https://cdn.cloudflare.steamstatic.com/steam/apps/1145360/header.jpg"
    },
    {
        "이름": "Hogwarts Legacy",
        "국기": "🇰🇷",
        "가격": "₩19,950",
        "할인": "-75%",
        "이미지": "https://cdn.cloudflare.steamstatic.com/steam/apps/990080/header.jpg"
    },
    {
        "이름": "DAVE THE DIVER",
        "국기": "🇰🇷",
        "가격": "₩15,600",
        "할인": "-35%",
        "이미지": "https://cdn.cloudflare.steamstatic.com/steam/apps/1868140/header.jpg"
    },
    {
        "이름": "Animal Crossing",
        "국기": "🇺🇸",
        "가격": "$53.30",
        "할인": "-33%",
        "이미지": "https://upload.wikimedia.org/wikipedia/en/0/0d/Animal_Crossing_New_Horizons.jpg"
    },
    {
        "이름": "Monster Hunter Rise",
        "국기": "🇳🇴",
        "가격": "kr 99.00",
        "할인": "-75%",
        "이미지": "https://cdn.cloudflare.steamstatic.com/steam/apps/1446780/header.jpg"
    }
]

# 2단 구성 (왼쪽: 인기 게임 / 오른쪽: 베스트 세일 예시)
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🎯 인기 게임")
    for game in popular_games[:3]:
        with st.container():
            cols = st.columns([1, 5])
            with cols[0]:
                st.image(game["이미지"], width=80)
            with cols[1]:
                st.markdown(f"**{game['이름']}**")
                st.markdown(f"{game['국기']} {game['가격']} &nbsp;&nbsp;&nbsp; 🔥 {game['할인']}", unsafe_allow_html=True)
        st.markdown("---")

with right_col:
    st.subheader("🏆 베스트 세일")
    for game in popular_games[3:]:
        with st.container():
            cols = st.columns([1, 5])
            with cols[0]:
                st.image(game["이미지"], width=80)
            with cols[1]:
                st.markdown(f"**{game['이름']}**")
                st.markdown(f"{game['국기']} {game['가격']} &nbsp;&nbsp;&nbsp; 🔥 {game['할인']}", unsafe_allow_html=True)
        st.markdown("---")
