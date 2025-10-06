import requests

class DictionaryAPI:
    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    @classmethod
    def lookup(cls, word: str):
        """Fetch word definition + part of speech from Free Dictionary API."""
        try:
            w = word.strip().lower()
            if not w:
                return {"word": word, "meaning": "Empty word.", "phonetic": "", "pos": ""}

            r = requests.get(cls.BASE_URL + w, timeout=8)
            if r.status_code == 200:
                data = r.json()[0]
                meaning = data["meanings"][0]["definitions"][0]["definition"]
                phonetic = data.get("phonetic", "")
                pos = data["meanings"][0].get("partOfSpeech", "")
                return {"word": word, "meaning": meaning, "phonetic": phonetic, "pos": pos}

            return {"word": word, "meaning": "No definition found.", "phonetic": "", "pos": ""}
        except Exception:
            return {"word": word, "meaning": "Error fetching definition.", "phonetic": "", "pos": ""}
