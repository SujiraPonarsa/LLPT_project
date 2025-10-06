import streamlit as st
from datetime import datetime, timedelta
from core.dictionary_api import DictionaryAPI
from core.learning_service import LearningService
import pandas as pd

service = LearningService()

st.set_page_config(page_title="Language Learning Progress Tracker", layout="centered")

# CSS
st.markdown("""
<style>
/* ---- Global Layout ---- */
.stApp, .block-container, body { background: #ffece4 !important; }
html, body, [class^="css"] {
  color: #2b2b2b !important;
  font-family: 'Sarabun', 'Noto Sans Thai', system-ui, -apple-system, sans-serif !important;
}

/* ---- Font Garuda (heading only) ---- */
@font-face {
  font-family: 'Garuda';
  src: url('assets/fonts/Garuda.ttf') format('truetype');
  font-weight: normal; font-style: normal; font-display: swap;
}

/* ---- Heading ---- */
.garuda-title{
  font-family:'Garuda','Sarabun','Noto Sans Thai',sans-serif !important;
  font-weight:700; color:#f23f0a !important;
  font-size:2.6rem !important; line-height:1.1;
  margin:0 auto .8rem auto !important; text-align:center !important;
  white-space:nowrap !important; /* ไม่ตกบรรทัด */
  display:inline-flex; gap:.6rem; align-items:center;
}
.garuda-title .emoji{ filter: drop-shadow(0 2px 6px rgba(242,63,10,.25)); }

/* ---- Center the Tabs ---- */
div[role="tablist"]{
  display:flex !important; justify-content:center !important;
  gap:2rem !important; margin-bottom:1rem !important;
  border-bottom:1.5px solid rgba(242,63,10,.25) !important; padding-bottom:.3rem !important;
}
div[role="tablist"] button[role="tab"]{
  white-space:nowrap !important; font-weight:600 !important; font-size:1.05rem !important;
  color:#a63a14 !important; background:transparent !important;
}
div[role="tablist"] button[role="tab"][aria-selected="true"]{
  color:#f23f0a !important; border-bottom:3px solid #f23f0a !important; border-radius:0 !important;
}

/* ---- Buttons ---- */
.stButton>button{
  background:#f23f0a !important; color:#fff !important;
  border:none !important; border-radius:10px !important;
  padding:.55rem 1.1rem !important; font-weight:600 !important;
  box-shadow:0 6px 14px rgba(242,63,10,.25) !important;
}
.stButton>button:hover{ filter:brightness(1.12); transform:translateY(-1px); }

/* ---- Sidebar ---- */
section[data-testid="stSidebar"]{
  background:#ffece4 !important; border-right:1px solid rgba(242,63,10,.2) !important;
}
section[data-testid="stSidebar"] *{ color:#c22700 !important; }

/* ---- Inputs ---- */
label, .stTextInput label, .stCheckbox label{ color:#c22700 !important; }
input, textarea, select, .stTextInput input{
  background:#fff !important; color:#2b2b2b !important;
  border:1px solid rgba(242,63,10,.25) !important; border-radius:10px !important;
}

/* ---- Alerts ---- */
.stAlert{
  background:#fff3ed !important; border:1px solid rgba(242,63,10,.25) !important; color:#c22700 !important;
}

/* ---- Frosted info box ---- */
.frost-info{
  background:rgba(255,255,255,.9); color:#f23f0a;
  border:1px solid rgba(242,63,10,.3); border-radius:12px; padding:12px 14px;
  font-weight:500; text-align:center; margin-top:10px;
  box-shadow:0 4px 14px rgba(242,63,10,.08), inset 0 0 0 1px rgba(255,255,255,.4);
}

/* ---- Tables (when st.table is used) ---- */
div[data-testid="stTable"] thead th{ white-space:nowrap !important; }
div[data-testid="stTable"] tbody td{ white-space:nowrap !important; }
div[data-testid="stTable"] tbody td:nth-child(2){ white-space:normal !important; } 
div[data-testid="stTable"] table{ table-layout:auto !important; }

/* ---- Metric boxes ---- */
div[data-testid="stMetric"]{
  background:#fffaf8 !important; border:1px solid rgba(242,63,10,.25) !important;
  border-radius:12px !important; padding:10px 12px !important;
}
div[data-testid="stMetric"] label{ color:#c22700 !important; }
div[data-testid="stMetric"] div{ color:#f23f0a !important; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown(
    '<h1 class="garuda-title"></span>Language Learning Progress Tracker</h1>',
    unsafe_allow_html=True
)

# SIDEBAR: USER
st.sidebar.header("User")
username = st.sidebar.text_input("Your name", value=st.session_state.get("username", ""))
if st.sidebar.button("Set user", use_container_width=True):
    st.session_state["username"] = username.strip()
    if st.session_state["username"]:
        service.set_user(st.session_state["username"])
        st.sidebar.success("Using personal DB")
        st.rerun()
    else:
        st.sidebar.warning("Please enter your name.")

# 
if st.session_state.get("username"):
    service.set_user(st.session_state["username"])
else:
    st.markdown('<div class="frost-info">ใส่ชื่อใน Sidebar เพื่อแยกข้อมูลเป็นรายบุคคล</div>', unsafe_allow_html=True)

# 
if "lookup_info" not in st.session_state:
    st.session_state["lookup_info"] = None

tab1, tab2, tab3 = st.tabs(["Add Word", "Review", "Statistics"])

# ---------- Tab 1: Add Word ----------
with tab1:
    st.subheader("Add New Word")
    new_word = st.text_input("Enter a word:")

    c1, c2 = st.columns([1, 1])
    with c1:
        do_lookup = st.button("Search Definition", use_container_width=True)
    with c2:
        due_now = st.checkbox("Mark as due now (show in Review today)")

    if do_lookup and new_word:
        st.session_state["lookup_info"] = DictionaryAPI.lookup(new_word)

    info = st.session_state["lookup_info"]
    if info:
        st.write(f"**Meaning:** {info['meaning']}")
        st.write(f"**Phonetic:** {info.get('phonetic', '')}")
        if info.get("pos"):
            st.write(f"**Part of Speech:** {info['pos']}")

        if st.button("Save to Database", type="primary"):
            service.add_new_word(info)
            if due_now:
                y = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                service.repo.set_last_reviewed(info["word"], y)
            st.success(f"Saved '{info['word']}' ✅")
            st.session_state["lookup_info"] = None
            st.rerun()
    else:
        st.info("Type a word and press **Search Definition** to fetch meaning.")

# ---------- Tab 2: Review ----------
with tab2:
    st.subheader("Flashcard Review")
    due_words = service.get_words_for_review()
    if due_words:
        for word, meaning in due_words:
            with st.expander(f"🔹 {word}", expanded=False):
                st.write(meaning)
                if st.button(f"Mark '{word}' as reviewed", key=f"rv-{word}"):
                    service.repo.review_word(word)
                    st.success(f"Reviewed '{word}' ✅")
                    st.rerun()
    else:
        st.info("No words to review today.")

# ---------- Tab 3: Statistics ----------
with tab3:
    st.subheader("Learning Statistics")
    stats = service.get_statistics()
    c1, c2 = st.columns(2)
    c1.metric("Total Words", stats["total"])
    c2.metric("Reviewed Words", stats["reviewed"])

    st.subheader("All Saved Words (per user)")
    full_rows = service.repo.get_all_words_full()
    if full_rows:
        headers = ["word", "meaning", "pos", "review_count", "last_reviewed"]
        df = pd.DataFrame([dict(zip(headers, r)) for r in full_rows])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No words saved yet.")

    st.divider()
    st.warning("Clear my data")
    colx, coly = st.columns(2)
    confirm = colx.checkbox("I understand, delete all my words")
    if coly.button("Clear my data", disabled=not confirm):
        service.repo.clear_all()
        st.success("Cleared all your words.")
        st.rerun()
