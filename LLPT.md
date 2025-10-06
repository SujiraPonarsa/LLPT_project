# 🧠 Language Learning Progress Tracker
## 🎯 หน้าที่หลัก

# 📚 Language Learning Progress Tracker

> แอปช่วยเรียนรู้คำศัพท์ภาษาอังกฤษแบบมีระบบทบทวน (Spaced Repetition System - SRS)  
> พัฒนาโดยใช้ **Python + Streamlit + SQLite**  
> แบ่งโครงสร้างเป็น 3 ชั้นหลัก: **UI / Service / Repository**

---

## 🖥️ 1) ชั้น UI — `streamlit_app.py` (Streamlit)

**หน้าที่หลัก**
- ตั้งค่าเพจ และสร้าง 3 แท็บ: **Add Word**, **Review**, **Statistics**
- เก็บสถานะใน `st.session_state` (เช่น `lookup_info`, `username`)
- ผูกปุ่มและอินพุตกับ service เพื่อให้ทำงานจริง

**ขั้นตอน/ฟังก์ชันสำคัญ**
- `st.set_page_config(...)` → ตั้งชื่อหน้า + layout  
- ส่วน “เลือกผู้ใช้” → รับ `username` แล้วเรียก `service.set_user(username)`  
  → สลับไปใช้ฐานข้อมูลของคนนั้น `data/words_<username>.db`

### 🔹 Tab: Add Word
- พิมพ์คำ → `st.text_input("Enter a word")`
- ปุ่ม **Search Definition** → เรียก `DictionaryAPI.lookup(word)`
- แสดงผล: **Meaning**, **Phonetic**, **POS**
- ปุ่ม **Save to Database** → `service.add_new_word(info)`
- ถ้าเลือก “Mark as due now” → เซ็ต `last_reviewed = เมื่อวาน` เพื่อให้คำนี้อยู่ใน Review วันนี้

### 🔹 Tab: Review
- ดึงคำที่ถึงกำหนดทบทวนด้วย `service.get_words_for_review()`
- แสดงผลเป็น expander แต่ละคำ พร้อมปุ่ม “Mark as reviewed”
  → เรียก `repo.review_word(word)` เพื่อเพิ่ม `review_count` และอัปเดตวันที่ล่าสุด

### 🔹 Tab: Statistics
- ใช้ `service.get_statistics()` เพื่อแสดง
  - Metric: **Total Words**, **Reviewed Words**
  - ตารางคำทั้งหมดจาก `repo.get_all_words()`

**เหตุผลด้าน UX**
- ใช้ `st.session_state` เพื่อคงผลลัพธ์ระหว่างการคลิก
- ใช้ `st.rerun()` เพื่อรีเฟรชหลังบันทึก/ทบทวนแบบเรียลไทม์

---

## ⚙️ 2) ชั้นบริการ / ตรรกะ — `core/learning_service.py`

**บทบาท:** เป็น “ตัวกลาง” ระหว่าง **UI** และ **ฐานข้อมูล**, กำหนดสูตร **SRS**

### เมธอดหลัก
- `__init__`: สร้าง `self.repo = WordRepository()`
- `set_user(username: str)`: เปลี่ยนไฟล์ DB ตามชื่อผู้ใช้ (`words_<username>.db`)
- `add_new_word(word_info: dict)`: ส่งต่อข้อมูลคำไปเก็บในฐานข้อมูล
- `get_words_for_review()`:  
  - ดึงคำทั้งหมดจากฐานข้อมูล  
  - คำนวณว่าถึงเวลารีวิวหรือยัง ด้วยสูตร  
    ```
    next_due = last_reviewed + 2 ** max(0, review_count) วัน
    ```
    | รอบ | review_count | ระยะห่าง (วัน) |
    |-----:|--------------:|----------------:|
    | 1 | 0 | 1 |
    | 2 | 1 | 2 |
    | 3 | 2 | 4 |
  - ถ้า `today >= next_due` → ใส่ในรายการ `due`
- `get_statistics()`:  
  - `total` = จำนวนคำทั้งหมด  
  - `reviewed` = จำนวนคำที่เคยรีวิว (`review_count > 0`)

**ภาพรวมข้อมูลที่ไหลผ่าน**

---

## 💾 3) ชั้นจัดเก็บข้อมูล — `core/word_repository.py` (SQLite)

**บทบาท:** ติดต่อฐานข้อมูล SQLite และทำ CRUD

### 
- แยก DB ต่อผู้ใช้: `use_db_for_user(username)` → `data/words_<username>.db`
- สร้างตารางอัตโนมัติ:

### เมธอดหลัก
- `use_db_for_user(username)` → เปิด DB ใหม่, เพิ่มคอลัมน์ `pos` หากยังไม่มี  
- `add_word(...)` → เพิ่มคำใหม่ (`review_count=0`, `last_reviewed=วันนี้`)
- `get_all_words()` → ดึงรายการคำทั้งหมด (เรียงใหม่สุดก่อน)
- `review_word(word)` → เพิ่ม `review_count +1`, อัปเดต `last_reviewed=วันนี้`
- `set_last_reviewed(word, ymd_str)` → ใช้ในกรณี mark “due now”
- `clear_all()` → ล้างข้อมูลทั้งหมดในตาราง

**เหตุผลเชิงออกแบบ**
- SQLite ใช้งานง่าย, พกพาได้, ไม่ต้องมี server  
- รองรับการ “auto-migrate” เพิ่มคอลัมน์ใหม่โดยไม่ลบข้อมูลเก่า

---

## 🌐 4) เรียก API — `core/dictionary_api.py`

**บทบาท:** ดึงคำจำกัดความจาก Free Dictionary API  
**ลิงก์:** [https://api.dictionaryapi.dev](https://api.dictionaryapi.dev)

### ลอจิก
```python
BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
```
## 🧪 5) การทดสอบ — `tests/test_learning_service.py`

**วัตถุประสงค์:**  
ทดสอบการทำงานของชั้น `service` โดยไม่แตะฐานข้อมูลจริงของผู้ใช้

**เทคนิคที่ใช้:**  
ใช้ `monkeypatch` เปลี่ยน path ของฐานข้อมูลชั่วคราว (เช่น `test.db` ใน temp directory)  
เพื่อจำลองสถานการณ์การใช้งานจริง โดยไม่กระทบข้อมูลเดิม

### 🧾 เคสทดสอบหลัก
1. ✅ `add_new_word()` → ตรวจว่า  
   - `total = 1`  
   - `reviewed = 0`
2. 🔄 เปลี่ยน `last_reviewed` เป็น “เมื่อวาน” →  
   - คำต้องอยู่ในลิสต์ `due` จาก `get_words_for_review()`
3. 📈 เรียก `repo.review_word("apple")` →  
   - `reviewed` ต้องกลายเป็น `1`

**ประโยชน์ที่ได้**
- ยืนยันความถูกต้องของสูตร SRS  
- ตรวจสอบความถูกต้องของการเก็บสถิติ  
- ทดสอบการเชื่อมโยงระหว่าง service ↔ repository  
- ลดโอกาสเกิด bug เวลาขยายฟีเจอร์ในอนาคต

---

## 🗂️ 6) ข้อมูลตัวอย่าง — โฟลเดอร์ `data/`

| ไฟล์ | คำอธิบาย |
|------|-----------|
| `words.db` | ฐานข้อมูลค่าเริ่มต้น |
| `words_bee.db`, `words_suji.db` | ฐานข้อมูลเฉพาะของผู้ใช้แต่ละคน |

**ข้อดี:**  
รองรับการใช้งานหลายผู้ใช้ในเครื่องเดียว โดยข้อมูลไม่ปะปนกัน  
ทำให้สามารถทดสอบแยกผู้ใช้ (multi-profile) ได้สะดวก

---

## 🔄 7) ลำดับการทำงาน (Flow Summary)

- 1️⃣ ผู้ใช้กรอกชื่อ → service.set_user(name)
- 2️⃣ Add Word → DictionaryAPI.lookup → service.add_new_word → repo.insert
- 3️⃣ Mark “due now” → repo.set_last_reviewed(word, yesterday)
- 4️⃣ Review → service.get_words_for_review() → repo.review_word()
- 5️⃣ Statistics → service.get_statistics() → แสดงใน UI
