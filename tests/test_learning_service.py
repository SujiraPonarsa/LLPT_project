from core.learning_service import LearningService
import core.word_repository as repo_mod
def test_add_word_and_stats(tmp_path, monkeypatch):
    monkeypatch.setattr(repo_mod, "DB_PATH", str(tmp_path / "test.db"))
    s = LearningService()

    s.add_new_word({"word": "apple", "meaning": "A fruit", "phonetic": ""})
    stats = s.get_statistics()
    assert stats["total"] == 1
    assert stats["reviewed"] == 0

    from datetime import datetime, timedelta
    ymd = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    s.repo.set_last_reviewed("apple", ymd)

    due = s.get_words_for_review()
    assert ("apple", "A fruit") in due

    s.repo.review_word("apple")
    stats2 = s.get_statistics()
    assert stats2["reviewed"] == 1
