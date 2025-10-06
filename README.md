# 📚 Language Learning Progress Tracker (LLPT)

A Streamlit-based application that helps users learn and review new vocabulary using spaced repetition techniques.
It integrates a dictionary API for instant meaning lookup and stores learning progress in a local SQLite database.

---

## 🚀 Features

* 🔍 **Dictionary Lookup:** Search for word definitions and phonetics using the Free Dictionary API
* 🧠 **Spaced Repetition:** Review due flashcards and grade your recall quality
* 💾 **Local Database:** Automatically saves vocabulary data to `data/words.db`
* 📊 **Statistics:** View total words, reviewed words, and upcoming reviews
* ✅ **Lightweight CI Check:** Run linting and tests via `simulate_ci.ps1`

---

## 🧬 Project Structure

```
LLPT_project/
│
├── streamlit_app.py          # Main Streamlit frontend
├── core/
│   ├── learning_service.py   # Handles database + spaced repetition
│   ├── dictionary_api.py     # Fetches meaning from API
│   └── word_repo.py          # (optional future module)
│
├── data/
│   └── words.db              # SQLite database (auto-created)
│
├── tests/
│   └── test_app.py           # Unit tests
│
├── requirements.txt          # Dependencies
├── simulate_ci.ps1           # Mock CI for linting and testing
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/SujiraPonarsa/LLPT_project.git
cd LLPT_project
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run streamlit_app.py
```

Once it runs, open your browser at:
🔗 [http://localhost:8501](http://localhost:8501)

---

## 🧪 Testing

To verify CI locally:

```bash
# Run flake8 for style checks
flake8 .

# Run unit tests
pytest -q

# Or run all with mock CI
./simulate_ci.ps1   # (PowerShell)
```

---

## 🧠 How It Works

1. **Add Word** — Lookup definitions via API and save to the database
2. **Review** — Shows due flashcards using spaced repetition logic
3. **Stats** — Displays learning progress metrics

---

## 📦 Tech Stack

* [Streamlit](https://streamlit.io/)
* [SQLite3](https://www.sqlite.org/)
* [Requests](https://pypi.org/project/requests/)
* [Free Dictionary API](https://dictionaryapi.dev/)
* [pytest](https://pytest.org/)
* [flake8](https://flake8.pycqa.org/)

---

---

## ✨ Future Improvements

* 📊 Progress visualization graphs
* 🌍 Multi-language dictionary integration
* 🧩 User login and cloud sync
* 🗕 Daily reminder system
* 📱 PWA mobile-friendly version

---

**Developed with ❤️ by Team LLPT**

> A learning companion to make language study consistent and fun.
