import streamlit as st
import datetime
import json
import os
import pandas as pd
import altair as alt
from textblob import TextBlob

# --- Page Configuration ---
st.set_page_config(
    page_title="Reflective Journal",
    page_icon="🌱",
    layout="centered"
)

# --- Styling ---
st.markdown("""
    <style>
    .reportview-container .main .block-container{
        padding: 2rem;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 0.5rem;
        padding: 0.75rem;
    }
    .stButton>button {
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- JSON File Path ---
JSON_FILE = "journal_entries.json"

# --- Mood Options & Prompts ---
MOOD_OPTIONS = {
    "😊 Happy": "What brought you the most joy today?",
    "😐 Neutral": "What kept you grounded today?",
    "😔 Sad": "What was difficult for you today?",
    "😡 Frustrated": "What triggered your frustration, and how did you handle it?",
    "😴 Tired": "What drained your energy, and how can you recharge?"
}

MOOD_COLORS = {
    "😊 Happy": "#90EE90",
    "😐 Neutral": "#D3D3D3",
    "😔 Sad": "#ADD8E6",
    "😡 Frustrated": "#FFB6C1",
    "😴 Tired": "#FFD580"
}

# --- Load Entries ---
if 'journal_entries' not in st.session_state:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            st.session_state.journal_entries = json.load(f)
    else:
        st.session_state.journal_entries = {}

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.date.today()

# --- Functions ---
def save_entry(date, mood, entry_text):
    st.session_state.journal_entries[date.isoformat()] = {
        "mood": mood,
        "text": entry_text
    }
    with open(JSON_FILE, "w") as f:
        json.dump(st.session_state.journal_entries, f, indent=4)
    st.success(f"Entry for {date.strftime('%Y-%m-%d')} saved!")

def get_entry(date):
    return st.session_state.journal_entries.get(date.isoformat(), {"mood": None, "text": ""})

def calculate_streak():
    dates = sorted([datetime.date.fromisoformat(d) for d in st.session_state.journal_entries.keys()])
    streak = 0
    today = datetime.date.today()
    for d in reversed(dates):
        if (today - d).days == streak:
            streak += 1
        else:
            break
    return streak

def sentiment_score(text):
    return TextBlob(text).sentiment.polarity

# --- Header ---
st.title("🌱 Reflective Journal")
st.markdown("---")

# --- Sidebar ---
st.sidebar.header("Select a Date")
selected_date = st.sidebar.date_input(
    "Choose a date to view or write an entry:",
    value=st.session_state.selected_date,
    max_value=datetime.date.today(),
    key="date_selector"
)
st.session_state.selected_date = selected_date

# --- Search Entries ---
st.sidebar.header("Search Entries")
search_query = st.sidebar.text_input("Keyword search:")
filtered_entries = {}
for date_str, data in st.session_state.journal_entries.items():
    if search_query.lower() in data.get("text", "").lower():
        filtered_entries[date_str] = data

# --- Main Content ---
st.subheader(f"Journal Entry for {selected_date.strftime('%A, %B %d, %Y')}")
entry_data = get_entry(selected_date)
current_mood = entry_data.get("mood", None)
current_text = entry_data.get("text", "")

# Mood selection
mood = st.selectbox(
    "How are you feeling today?", 
    options=list(MOOD_OPTIONS.keys()), 
    index=list(MOOD_OPTIONS.keys()).index(current_mood) if current_mood else 0
)

# Mood-based prompt
st.info(MOOD_OPTIONS[mood])

# Text area
entry_text = st.text_area(
    "Write your reflection here:",
    value=current_text,
    height=300,
    key=f"journal_editor_{selected_date}"
)

# Save entry
if st.button("Save Entry", key=f"save_button_{selected_date}"):
    save_entry(selected_date, mood, entry_text)

# Sentiment Analysis
if entry_text.strip():
    score = sentiment_score(entry_text)
    st.markdown(f"**Sentiment Score:** {score:.2f} (Negative ⬅️ 0 ➡️ Positive)")

st.markdown("---")

# --- Mood Tracker & Streak ---
st.sidebar.header("Mood Tracker")
if st.session_state.journal_entries:
    for date_str, data in sorted(st.session_state.journal_entries.items(), reverse=True):
        color = MOOD_COLORS.get(data.get("mood", ""), "#FFFFFF")
        st.sidebar.markdown(
            f"<div style='background-color:{color}; padding:5px; border-radius:5px; margin-bottom:5px;'>"
            f"<b>{date_str}</b> - {data['mood']}</div>",
            unsafe_allow_html=True
        )
    streak = calculate_streak()
    st.sidebar.success(f"🔥 Current streak: {streak} day(s) of journaling")
else:
    st.sidebar.info("No entries yet.")

# --- Mood Trend Chart ---
if st.session_state.journal_entries:
    df = pd.DataFrame([
        {"date": datetime.date.fromisoformat(date), "mood": data["mood"]}
        for date, data in st.session_state.journal_entries.items()
    ])
    mood_order = list(MOOD_OPTIONS.keys())
    df['mood_code'] = df['mood'].apply(lambda x: mood_order.index(x))
    chart = alt.Chart(df).mark_line(point=True).encode(
        x='date:T',
        y='mood_code:Q',
        tooltip=['date', 'mood'],
        color=alt.Color('mood:N', scale=alt.Scale(domain=mood_order, range=list(MOOD_COLORS.values())))
    ).properties(height=200)
    st.subheader("📈 Mood Trend")
    st.altair_chart(chart, use_container_width=True)

# --- Filtered Search Results ---
if search_query.strip():
    st.subheader(f"Search Results for '{search_query}':")
    if filtered_entries:
        for date_str, data in sorted(filtered_entries.items(), reverse=True):
            st.markdown(f"**{date_str}** - {data['mood']}")
            st.write(data['text'])
            st.markdown("---")
    else:
        st.info("No matching entries found.")