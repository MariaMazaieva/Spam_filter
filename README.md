#  Spam Filter System

This project is a Python-based Spam Filter designed to detect and classify spam emails using a custom-built corpus and rule-based filtering.

---

##  Features

-  Extracts and parses email content
-  Preprocesses email bodies and subjects
-  Builds and improves a keyword-based spam corpus
-  Detects spam based on rules and keyword matches
-  Outputs email classifications for analysis

---

##  Project Structure

| File | Description |
|------|-------------|
| `getemail.py` | Retrieves and parses emails |
| `emailanalysis.py` | Analyzes email content using rule-based logic |
| `filter.py` | Filters emails based on keywords and classification |
| `trainingcorpus.py` | Contains the original training data and keywords |
| `improved_corpus.py` | Enhanced and extended spam keyword corpus |

---

##  How It Works

1. **Training corpus** is built from manually defined spam keywords.
2. **Email content** is extracted and cleaned.
3. Each email is **analyzed** using rule-based logic.
4. The result is marked as `spam` or `not spam`.
