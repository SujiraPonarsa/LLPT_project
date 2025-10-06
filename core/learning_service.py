from datetime import datetime, timedelta
from core.word_repository import WordRepository

class LearningService:
    def __init__(self):
        self.repo = WordRepository()

    # เลือก/สลับผู้ใช้ → ใช้ไฟล์ DB ของคนนั้น
    def set_user(self, username: str):
        self.repo.use_db_for_user(username)

    def add_new_word(self, word_info: dict):
        self.repo.add_word(
            word_info["word"],
            word_info["meaning"],
            word_info.get("phonetic", ""),
            word_info.get("pos", "")
        )

    def get_words_for_review(self):
        words = self.repo.get_all_words()
        today = datetime.now().date()
        due = []
        for word, meaning, count, last in words:
            try:
                last_date = datetime.strptime(last, "%Y-%m-%d").date()
            except Exception:
                due.append((word, meaning))
                continue
            next_due = last_date + timedelta(days=2 ** max(0, int(count)))
            if today >= next_due:
                due.append((word, meaning))
        return due

    def get_statistics(self):
        all_words = self.repo.get_all_words()
        total = len(all_words)
        reviewed = sum(1 for w in all_words if (w[2] or 0) > 0)
        return {"total": total, "reviewed": reviewed}
