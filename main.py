import streamlit as st
st.title('나의 첫 웹앱!')
st.write('우앙 신기하다 코딩!')
import streamlit as st
import random
from datetime import datetime, timedelta

# -------------------------
# 기본 설정
# -------------------------
st.set_page_config(
    page_title="MBTI 맞춤 공부법 🎯",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -------------------------
# 스타일 (간단한 애니메이션 & 카드 느낌)
# -------------------------
CUSTOM_CSS = """
<style>
@keyframes floaty { 0% { transform: translateY(0px);} 50% { transform: translateY(-6px);} 100% { transform: translateY(0px);} }
@keyframes glow { from { text-shadow: 0 0 6px rgba(255,255,255,.45);} to { text-shadow: 0 0 14px rgba(255,255,255,.85);} }

h1.title-hero {
  font-size: 2.1rem; line-height: 1.25; text-align:center; margin-top: .2rem;
  animation: glow 2s ease-in-out infinite alternate;
}
.subtitle { text-align:center; opacity:.9; }
.card { border-radius: 16px; padding: 18px 18px 10px; margin: 8px 0 14px; border: 1px solid rgba(200,200,200,.35); background: linear-gradient(180deg, rgba(255,255,255,.75), rgba(255,255,255,.55)); box-shadow: 0 4px 16px rgba(0,0,0,.06); }
.badge { display:inline-block; padding: 6px 10px; border-radius: 999px; font-size:.85rem; background: #eef2ff; border:1px solid #c7d2fe; }
.small { font-size:.92rem; opacity:.9; }
.footer { text-align:center; opacity:.7; font-size:.9rem; margin-top: 18px; }
.sparkle { display:inline-block; animation: floaty 3s ease-in-out infinite; }
hr.sep { border: none; border-top: 1px dashed rgba(0,0,0,.15); margin: 16px 0; }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------
# 데이터: MBTI별 추천
# -------------------------
MBTI_TIPS = {
    "INTJ": {
        "title": "전략가형 🧠🧭",
        "strategy": [
            "장기 목표를 역산(Backward)하여 주간·일간 체크포인트 설정",
            "깊은 몰입 시간(📵 방해 금지 60~90분) + 짧은 복습 루프",
            "개념지도를 직접 그리고, 증명/원리부터 이해"
        ],
        "focus": [
            "깊게 파고들다 과투입⚠️ → 80/20로 우선순위 컷",
            "완벽주의 대신 *First pass*→*Refine* 두 번에 나눠 처리"
        ],
        "tools": ["Notion 로드맵", "Anki 간격반복", "Obsidian ZK"],
        "avoid": ["계획만 세우고 착수 지연", "세부 최적화로 본질 지연"],
        "slogan": "원리를 붙잡고, 실행은 가볍게."
    },
    "INFJ": {
        "title": "통찰형 상담가 🌿🔮",
        "strategy": [
            "의미 연결 노트: 배운 개념을 삶/가치와 연결해 서술",
            "한 번에 길게보다 `45분 집중 + 10분 회고 저널`",
            "개념을 가르치듯 설명하는 *Teach-back* 활용"
        ],
        "focus": ["감정 피로 시 라이트 테마 → 자연광/식물 옆 자리 🌱", "마감 24시간 전 ‘핵심 3가지’만 남기고 가지치기"],
        "tools": ["GoodNotes 개념 스케치", "Notion 회고 템플릿", "Forest 타이머"],
        "avoid": ["완벽한 가치 정합성 찾다 착수 지연", "과도한 공감 소모"],
        "slogan": "의미를 심고, 루틴으로 물 주기."
    },
    "ISTJ": {
        "title": "현실주의 관리자 📚🧱",
        "strategy": ["체크리스트 기반 *규격 루틴*", "과목별 ‘표준 절차서’ 만들기", "오답노트에 ‘원인→대응 규칙’ 작성"],
        "focus": ["같은 시간, 같은 자리, 같은 순서 ✨ 습관화", "주 1회 진도 점검 & 보상 시스템"],
        "tools": ["Excel/스프레드시트 진도표", "TickTick 반복할 일", "Pomofocus"],
        "avoid": ["계획 과다, 유연성 부족"],
        "slogan": "꾸준함은 최고의 치트키." 
    },
    "ISFJ": {
        "title": "수호자형 🧺💗",
        "strategy": ["소단원 나누기 → ‘작은 승리’ 스탬프", "요점정리 카드+친절한 설명 붙이기", "스터디 짝과 상호 점검"],
        "focus": ["타인 부탁에 시간 잠식 주의 → ‘나의 공부 시간’ 배지 달기 🎖️", "휴식 알람 필수"],
        "tools": ["Quizlet 카드", "Google Calendar 시간 블록", "Toggl 트래킹"],
        "avoid": ["양심 공부(양만 채우기)", "타인 우선으로 자기 시간 손실"],
        "slogan": "나를 챙겨야, 모두를 챙긴다."
    },
    "INTP": {
        "title": "사색가 🧩🔍",
        "strategy": ["개념 간 링크드노트(그래프 보기)로 구조화", "왜?를 3번 묻고 가설-검증 메모", "공식 유도 과정을 직접 써보기"],
        "focus": ["주의 산만 방지: 전자기기 미니멀 세팅", "마감 48시간 전 ‘발표/설명’ 리허설"],
        "tools": ["Obsidian 그래프", "Anki Cloze", "VS Code + Markdown"],
        "avoid": ["이론 수집만 하고 연습 문제 회피"],
        "slogan": "이해→연습→설명, 세 단계 루프." 
    },
    "INFP": {
        "title": "중재자 🎨🕊️",
        "strategy": ["감성 앵커 만들기(플레이리스트, 스티커)로 동기 부스터", "스토리텔링 요약카드", "‘오늘의 의미 2줄’ 데일리 로그"],
        "focus": ["기분 따라 흔들림 방지: 25분 타이머 + 체크박스 ✅", "시작 허들을 2분으로 낮추기(딱 2분만)"],
        "tools": ["Notion 캘린더 + 갤러리", "Daylio 무드 트래커", "Forest"],
        "avoid": ["완벽한 영감 기다리기", "과한 미학화로 시간 소모"],
        "slogan": "작게 시작하면, 열정이 따라온다."
    },
    "ISTP": {
        "title": "장인형 🛠️🧊",
        "strategy": ["문제 먼저 풀고 필요 개념 역추적", "실험/사례 중심 Hands-on", "타이핑보다 손필기 혼합"],
        "focus": ["짧고 강한 스프린트(30–40분) + 움직이는 휴식 🧎", "체크리스트는 간결하게"],
        "tools": ["Excel 시뮬레이션", "YouTube 실습 영상 북마크", "Whiteboard"],
        "avoid": ["지루한 장문 이론만 보기"],
        "slogan": "손으로 배우면 오래간다." 
    },
    "ISFP": {
        "title": "모험가형 🐾🌈",
        "strategy": ["시각 요소 풍부한 마인드맵", "컬러코딩 노트(테마 색🎨)", "학습 장소 스위칭(카페/도서관 교차)"],
        "focus": ["루틴이 무너지지 않게 ‘코어 루틴 3개’만 고정", "보상은 경험형(산책, 맛있는 간식)"],
        "tools": ["GoodNotes 스티커", "Canva 한 페이지 요약", "Google Keep"],
        "avoid": ["기분 따라 전면 중단"],
        "slogan": "감각을 즐기며, 핵심은 고정."
    },
    "ENTJ": {
        "title": "지도자형 🏁🦾",
        "strategy": ["OKR 스타일 목표-핵심지표 설정", "모의고사→오답 KPI 추적", "주간 리뷰로 전략 피봇"],
        "focus": ["과제 위임할 수 없으니 ‘자동화’와 ‘템플릿’으로 대체", "과몰입 시 수면 우선"],
        "tools": ["Notion 프로젝트", "Excel 대시보드", "Toggl/Kanban"],
        "avoid": ["달성치만 보고 학습의 질 놓치기"],
        "slogan": "성과는 시스템에서 나온다." 
    },
    "ENFJ": {
        "title": "언변능숙형 🎤🤝",
        "strategy": ["스터디 리더 역할로 Teach-back", "발표 데드라인을 먼저 박아두기", "피드백 루프(동료 체크)"],
        "focus": ["타인 일정에 휩쓸리지 않게 ‘개인 블록’ 고정", "과도한 대인 피로 시 소셜 미디어 단식"],
        "tools": ["Google Calendar 공유", "Miro 보드", "Slides 리허설"],
        "avoid": ["사람 챙기다 자기 학습 도둑 맞기"],
        "slogan": "가르치며, 스스로 성장하기." 
    },
    "ENTP": {
        "title": "변론가 🧨🧪",
        "strategy": ["프로젝트형 과제로 흥미 점화", "아이디어→실험→피드백의 빠른 반복", "논쟁·퀴즈로 개념 고정"],
        "focus": ["시작 난이도 낮추고 ‘마감 공개’로 동력 확보", "산만함은 토픽 타이머로 격리"],
        "tools": ["Trello 실험 보드", "Kahoot 퀴즈", "Notion 아이디어 인박스"],
        "avoid": ["새로운 주제만 찾아다니기"],
        "slogan": "실험하고, 우선순위로 정복하라."
    },
    "ENFP": {
        "title": "활동가형 ✨🚀",
        "strategy": ["테마 스터디(흥미 중심) + ‘핵심 3개’만 성과 관리", "비주얼 라이브러리(예시·사례) 축적", "파트너와 체크인"],
        "focus": ["루틴 파편화 방지: 아침 앵커 루틴 20분", "마감 24h 전 집중 공간으로 이동"],
        "tools": ["Notion 보드", "Pinterest/Canva 영감", "Habitify 습관"],
        "avoid": ["새 프로젝트 과다 착수"],
        "slogan": "흥미를 엔진으로, 구조로 조향."
    },
    "ESTJ": {
        "title": "경영자형 🧾📈",
        "strategy": ["학습 SOP 문서화", "시간 블록 + 버퍼", "모의-리뷰-표준화 사이클"],
        "focus": ["지표가 아닌 ‘이해도 인터뷰’도 병행", "과도한 규칙은 최소 핵심 규칙만"],
        "tools": ["Sheets KPI", "Calendar 블록", "Anki"],
        "avoid": ["유연성 부족, 창의적 접근 저해"],
        "slogan": "시스템이 실력을 만든다."
    },
    "ESFJ": {
        "title": "집정관형 🎀🏠",
        "strategy": ["친구/가족에 목표 선포 → 책임감 스위치", "스터디 파트너와 상호 채점", "요약 슬라이드 만들어 공유"],
        "focus": ["과도한 부탁 수락 금지(‘학습 보호 구역’ 선포) 🛡️", "작은 보상과 칭찬 적극 활용"],
        "tools": ["Slides 요약", "Google Form 퀴즈", "Shared Calendar"],
        "avoid": ["타인 일정 최우선"],
        "slogan": "함께해서 더 멀리, 그래도 나를 먼저."
    },
    "ESTP": {
        "title": "사업가형 🏎️💥",
        "strategy": ["타임어택 문제풀이로 게임화", "실전 중심 스터디(과감한 시도)", "경쟁/랭킹 요소로 동기 부여"],
        "focus": ["짧고 강한 라운드(20–30분) + 몸을 쓰는 휴식", "기초 개념은 속도 늦추고 정확도 우선"],
        "tools": ["Quizizz/Kahoot", "스톱워치", "화이트보드"],
        "avoid": ["속도만 추구하다 정확도 저하"],
        "slogan": "스피드에 정확도를 더하라."
    },
    "ESFP": {
        "title": "연예인형 🎉📸",
        "strategy": ["브이로그/스냅샷으로 공부 기록 → 재미 부스팅", "친구와 퀴즈 배틀", "시각·소리 자극 활용"],
        "focus": ["학습은 ‘쇼타임’ 전에 먼저! (핵심 40분)", "소셜 보상은 집중 블록 후"],
        "tools": ["TikTok/Shorts 기록(비공개)", "Kahoot", "Color sticky notes"],
        "avoid": ["공부 기록만 하고 학습량 부족"],
        "slogan": "재미를 리듬으로, 핵심을 먼저."
    },
    "ENTP": {
        "title": "변론가 🧨🧪",
        "strategy": ["프로젝트형 과제로 흥미 점화", "아이디어→실험→피드백의 빠른 반복", "논쟁·퀴즈로 개념 고정"],
        "focus": ["시작 난이도 낮추고 ‘마감 공개’로 동력 확보", "산만함은 토픽 타이머로 격리"],
        "tools": ["Trello 실험 보드", "Kahoot 퀴즈", "Notion 아이디어 인박스"],
        "avoid": ["새로운 주제만 찾아다니기"],
        "slogan": "실험하고, 우선순위로 정복하라."
    },
    "ESTP": {
        "title": "사업가형 🏎️💥",
        "strategy": ["타임어택 문제풀이로 게임화", "실전 중심 스터디(과감한 시도)", "경쟁/랭킹 요소로 동기 부여"],
        "focus": ["짧고 강한 라운드(20–30분) + 몸을 쓰는 휴식", "기초 개념은 속도 늦추고 정확도 우선"],
        "tools": ["Quizizz/Kahoot", "스톱워치", "화이트보드"],
        "avoid": ["속도만 추구하다 정확도 저하"],
        "slogan": "스피드에 정확도를 더하라."
    },
    "ENTJ": {
        "title": "지도자형 🏁🦾",
        "strategy": ["OKR 스타일 목표-핵심지표 설정", "모의고사→오답 KPI 추적", "주간 리뷰로 전략 피봇"],
        "focus": ["과제 위임할 수 없으니 ‘자동화’와 ‘템플릿’으로 대체", "과몰입 시 수면 우선"],
        "tools": ["Notion 프로젝트", "Excel 대시보드", "Toggl/Kanban"],
        "avoid": ["달성치만 보고 학습의 질 놓치기"],
        "slogan": "성과는 시스템에서 나온다." 
    }
}

# 누락 타입 보완 (중복 제거 및 빠진 유형 채우기)
MISSING = {
    "ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"
}
# 위 사전에 없는 키는 INTP 템플릿을 기본으로 사용
for t in list(MISSING):
    if t not in MBTI_TIPS:
        MBTI_TIPS[t] = MBTI_TIPS["INTP"]

ALL_TYPES = [
    "ISTJ","ISFJ","INFJ","INTJ","ISTP","ISFP","INFP","INTP",
    "ESTP","ESFP","ENFP","ENTP","ESTJ","ESFJ","ENFJ","ENTJ"
]

# -------------------------
# 헤더
# -------------------------
st.markdown('<h1 class="title-hero">MBTI 맞춤 공부법 추천 🌟</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">당신의 성향에 딱 맞는 공부 전략을 처방합니다! <span class="sparkle">✨</span></p>', unsafe_allow_html=True)

# -------------------------
# 사이드바: 사용법 & 미니 플래너
# -------------------------
st.sidebar.header("🔧 사용법")
st.sidebar.write("1) MBTI를 선택하고, 2) 추천 받기 버튼을 누르세요. 3) 아래 미션으로 오늘 공부 시작! 💪")

st.sidebar.subheader("⏱️ 미니 플래너")
total_min = st.sidebar.slider("오늘 공부 시간(분)", 20, 240, 80, step=10)
slot = 25
sessions = max(1, total_min // slot)
st.sidebar.caption(f"권장 포모도로 세션: **{sessions}회** (25분 집중 + 5분 휴식)")

if st.sidebar.button("✅ 오늘의 미션 생성"):
    tasks_pool = [
        "핵심 개념 3가지 요약하기 ✍️",
        "오답노트 원인-대응 규칙 쓰기 🛠️",
        "문제 10개 타임어택 🏁",
        "배운 내용을 2분 설명하기 🎤",
        "마인드맵 1장 만들기 🗺️",
        "Anki 카드 15장 생성/복습 🃏",
        "실전 사례 한 개 찾아 연결하기 🔗",
    ]
    today_tasks = random.sample(tasks_pool, k=min(3, len(tasks_pool)))
    with st.sidebar:
        st.success("오늘의 추천 미션 💡")
        for i, t in enumerate(today_tasks, 1):
            st.checkbox(f"{i}. {t}")
        st.balloons()

# -------------------------
# 본문: 선택 & 결과
# -------------------------
col1, col2 = st.columns([1,1])
with col1:
    selected = st.selectbox("🔎 MBTI 유형을 선택하세요", ALL_TYPES, index=ALL_TYPES.index("ENFP"))
with col2:
    mood = st.select_slider("오늘의 기분", options=["🥱", "🙂", "🔥"], value="🙂")

if st.button("🎯 맞춤 공부법 추천 받기"):
    tips = MBTI_TIPS.get(selected, MBTI_TIPS["INTP"])  # fallback

    # 효과: 기분에 따라 눈/풍선
    if mood == "🔥":
        st.balloons()
    else:
        try:
            st.snow()
        except Exception:
            pass

    st.markdown(f"<div class='badge'>추천 유형</div>", unsafe_allow_html=True)
    st.markdown(f"### {selected} · {tips['title']}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### 📌 공부 전략")
        for s in tips["strategy"]:
            st.markdown(f"- {s}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### 🧰 추천 도구/앱")
        st.markdown(", ".join([f"`{x}`" for x in tips["tools"]]))
        st.markdown("<hr class='sep'>", unsafe_allow_html=True)
        st.markdown("#### 🚫 피하면 좋은 것")
        for a in tips["avoid"]:
            st.markdown(f"- {a}")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("#### 🎯 집중 팁")
        for f in tips["focus"]:
            st.markdown(f"- {f}")
        st.markdown("<hr class='sep'>", unsafe_allow_html=True)
        st.markdown("#### 🪄 한 줄 슬로건")
        st.markdown(f"**{tips['slogan']}** ✨")
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("🧪 보너스: 60분 퀵 루틴 제안 보기"):
        now = datetime.now()
        routine = [
            ("집중", 25, "핵심 개념 3개 요약 ✍️"),
            ("휴식", 5, "물 마시고 스트레칭 🧘"),
            ("집중", 25, "연습문제 10개 & 오답 표시 ✅"),
            ("정리", 5, "오늘 배운 것 2줄 회고 🧾"),
        ]
        for phase, mins, todo in routine:
            end = now + timedelta(minutes=mins)
            st.markdown(f"- **{phase} {mins}분** → *{todo}*  (예상 종료 {end.strftime('%H:%M')})")

# 하단 푸터
st.markdown('<div class="footer">Made with Streamlit ❤️ · 공부엔 꾸준함이 최고! 📚</div>', unsafe_allow_html=True)
