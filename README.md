# 🌱 Reflective Journal

A simple, private daily journaling app built with Streamlit. Pick a date, choose your mood, answer a mood-based reflection prompt, and track how you're feeling over time.

![Reflective Journal screenshot](screenshot.png)

## Features

- **Daily entries**: write or revisit a journal entry for any past date
- **Mood-based prompts**: the reflection prompt changes with your mood (Happy, Neutral, Sad, Frustrated, Tired)
- **Sentiment analysis**: a live polarity score for each entry, powered by TextBlob
- **Mood tracker**: color-coded history of your moods in the sidebar
- **Streak counter**: see how many consecutive days you've journaled
- **Mood trend chart**: an Altair line chart of your mood over time
- **Keyword search**: find past entries by keyword
- **Local storage**: entries are saved to a local `journal_entries.json` file

## Tech Stack

Python, Streamlit, pandas, Altair, TextBlob

## Getting Started

### Prerequisites

- Python 3.9+

### Installation

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# optional: create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Project Structure

```
.
├── app.py                  # Streamlit app
├── requirements.txt        # Python dependencies
├── screenshot.png          # README screenshot
└── journal_entries.json    # Created on first save (git-ignored)
```

## Data & Privacy

All entries stay on your machine in `journal_entries.json`. This file is listed in `.gitignore` so your personal journal is never committed to the repository.

## Notes

- Sentiment scoring uses TextBlob's built-in lexicon, so no extra NLTK corpora downloads are required.
- If you're on macOS and `python` isn't found, use `python3`.

## Future Ideas

- Edit/delete confirmation for entries
- Export entries to PDF or Markdown
- Weekly and monthly mood summaries
- Optional password protection

## License

MIT
