import streamlit as st
from datetime import datetime, timedelta
from core.dictionary_api import DictionaryAPI
from core.learning_service import LearningService

service = LearningService()

st.set_page_config(page_title="Language Learning Progress Tracker", layout="centered")
st.title("📚 Language Learning Progress Tracker")

# Sidebar: เลือกผู้ใช้
st.sidebar.header("User")
username = st.sidebar.text_input("Your name", value=st.session_state.get("username", ""))
if st.sidebar.button("Set user", use_container_width=True):
    st.session_state["username"] = username.strip()
    if st.session_state["username"]:
        service.set_user(st.session_state["username"])
        st.sidebar.success(f"Using personal DB")
        st.rerun()
    else:
        st.sidebar.warning("Please enter your name.")

# ถ้าตั้งชื่อแล้ว ให้สลับ DB ทุกครั้งที่รัน
if st.session_state.get("username"):
    service.set_user(st.session_state["username"])
else:
    st.info("ใส่ชื่อใน Sidebar เพื่อแยกข้อมูลเป็นรายบุคคล")

if "lookup_info" not in st.session_state:
    st.session_state["lookup_info"] = None

tab1, tab2, tab3 = st.tabs(["Add Word", "Review", "Statistics"])

# Tab 1: Add Word
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

# Tab 2: Review
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

# Tab 3: Statistics
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
        st.table([dict(zip(headers, r)) for r in full_rows])
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
