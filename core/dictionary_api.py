import requests

class DictionaryAPI:
    BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

    @classmethod
    def lookup(cls, word: str):
        """ดึงข้อมูลคำศัพท์จาก Free Dictionary API"""
        try:
            response = requests.get(cls.BASE_URL + word.strip().lower(), timeout=5)
            if response.status_code == 200:
                data = response.json()[0]
                meaning = data["meanings"][0]["definitions"][0]["definition"]
                phonetic = data.get("phonetic", "")
                return {"word": word, "meaning": meaning, "phonetic": phonetic}
            else:
                return {"word": word, "meaning": "No definition found."}
        except Exception:
            return {"word": word, "meaning": "Error fetching definition."}
