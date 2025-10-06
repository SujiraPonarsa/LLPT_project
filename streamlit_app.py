import streamlit as st
from core.dictionary_api import DictionaryAPI
from core.learning_service import LearningService

# สร้าง instance ของ service (ใช้เชื่อมฐานข้อมูล + คำนวณ)
service = LearningService()

# ตั้งค่าหน้าหลักของเว็บ
st.set_page_config(page_title="Language Learning Progress Tracker", layout="centered")
st.title("📚 Language Learning Progress Tracker")

# สร้าง 3 แท็บหลัก
tab1, tab2, tab3 = st.tabs(["Add Word", "Review", "Statistics"])

# --- Tab 1: เพิ่มคำศัพท์ใหม่ ---
with tab1:
    st.subheader("Add New Word")
    new_word = st.text_input("Enter a word:")
    if st.button("Search Definition"):
        if new_word:
            info = DictionaryAPI.lookup(new_word)
            st.write(f"**Meaning:** {info['meaning']}")
            st.write(f"**Phonetic:** {info.get('phonetic', '')}")
            if st.button("Save to Database"):
                service.add_new_word(info)
                st.success(f"Saved '{new_word}' to database!")
        else:
            st.warning("Please enter a word!")

# --- Tab 2: ทบทวนคำศัพท์ ---
with tab2:
    st.subheader("Flashcard Review")
    due_words = service.get_words_for_review()
    if due_words:
        for word, meaning in due_words:
            with st.expander(f"🔹 {word}"):
                st.write(meaning)
                if st.button(f"Mark '{word}' as reviewed"):
                    service.repo.review_word(word)
                    st.success(f"Reviewed '{word}' ✅")
    else:
        st.info("No words to review today. 🎉")

# --- Tab 3: สถิติการเรียน ---
with tab3:
    st.subheader("Learning Statistics")
    stats = service.get_statistics()
    st.metric("Total Words", stats["total"])
    st.metric("Reviewed Words", stats["reviewed"])
