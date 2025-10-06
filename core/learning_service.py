from datetime import datetime, timedelta
from core.word_repository import WordRepository

class LearningService:
    def __init__(self):
        self.repo = WordRepository()

    def add_new_word(self, word_info: dict):
        self.repo.add_word(word_info["word"], word_info["meaning"], word_info.get("phonetic", ""))

    def get_words_for_review(self):
        words = self.repo.get_all_words()
        today = datetime.now().date()
        due = []
        for word, meaning, count, last in words:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            next_due = last_date + timedelta(days=2**count)
            if today >= next_due:
                due.append((word, meaning))
        return due

    def get_statistics(self):
        all_words = self.repo.get_all_words()
        total = len(all_words)
        reviewed = sum(1 for w in all_words if w[2] > 0)
        return {"total": total, "reviewed": reviewed}
