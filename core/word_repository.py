import sqlite3
import os
import re
from datetime import datetime

DATA_DIR = "data"
DEFAULT_DB = os.path.join(DATA_DIR, "words.db")

def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", (name or "").lower()).strip("_")
    return slug or "default"

class WordRepository:
    def __init__(self, db_path: str = DEFAULT_DB):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.db_path = db_path
        self.create_table()

    # ----- multi-user: สลับไฟล์ DB ตามชื่อผู้ใช้ -----
    def _reconnect(self, db_path: str):
        try:
            self.conn.close()
        except Exception:
            pass
        self.conn = sqlite3.connect(db_path)
        self.db_path = db_path
        self.create_table()

    def use_db_for_user(self, username: str):
        slug = _slugify(username)
        path = os.path.join(DATA_DIR, f"words_{slug}.db")
        self._reconnect(path)

    # ----- schema & migration (รองรับคอลัมน์ pos) -----
    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            meaning TEXT,
            phonetic TEXT,
            pos TEXT,
            last_reviewed TEXT,
            review_count INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()
        # เผื่อเป็น DB เก่าที่ยังไม่มีคอลัมน์ pos
        cur.execute("PRAGMA table_info(words)")
        cols = [c[1] for c in cur.fetchall()]
        if "pos" not in cols:
            cur.execute("ALTER TABLE words ADD COLUMN pos TEXT")
            self.conn.commit()

    # ----- CRUD -----
    def add_word(self, word, meaning, phonetic="", pos=""):
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO words (word, meaning, phonetic, pos, last_reviewed, review_count)
        VALUES (?, ?, ?, ?, ?, 0)
        """, (word, meaning, phonetic, pos, datetime.now().strftime("%Y-%m-%d")))
        self.conn.commit()

    # ใช้ใน logic เดิม (ไม่มี pos)
    def get_all_words(self):
        cur = self.conn.cursor()
        cur.execute("SELECT word, meaning, review_count, last_reviewed FROM words ORDER BY id DESC")
        return cur.fetchall()

    # ใช้แสดงสถิติเต็ม (มี pos)
    def get_all_words_full(self):
        cur = self.conn.cursor()
        cur.execute("SELECT word, meaning, pos, review_count, last_reviewed FROM words ORDER BY id DESC")
        return cur.fetchall()

    def review_word(self, word):
        cur = self.conn.cursor()
        cur.execute("""
        UPDATE words
        SET review_count = review_count + 1,
            last_reviewed = ?
        WHERE word = ?
        """, (datetime.now().strftime("%Y-%m-%d"), word))
        self.conn.commit()

    def set_last_reviewed(self, word, ymd_str):
        cur = self.conn.cursor()
        cur.execute("UPDATE words SET last_reviewed=? WHERE word=?", (ymd_str, word))
        self.conn.commit()

    # ล้างข้อมูลเฉพาะ DB ปัจจุบัน (ผู้ใช้ที่เลือก)
    def clear_all(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM words")
        self.conn.commit()
