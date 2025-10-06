import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("data", "words.db")

class WordRepository:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.create_table()

    def create_table(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE,
            meaning TEXT,
            phonetic TEXT,
            last_reviewed TEXT,
            review_count INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    def add_word(self, word, meaning, phonetic=""):
        cur = self.conn.cursor()
        cur.execute("""
        INSERT OR IGNORE INTO words (word, meaning, phonetic, last_reviewed, review_count)
        VALUES (?, ?, ?, ?, 0)
        """, (word, meaning, phonetic, datetime.now().strftime("%Y-%m-%d")))
        self.conn.commit()

    def get_all_words(self):
        cur = self.conn.cursor()
        cur.execute("SELECT word, meaning, review_count, last_reviewed FROM words")
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
