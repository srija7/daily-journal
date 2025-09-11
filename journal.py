import streamlit as st
import datetime
import json
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Daily Journal",
    page_icon="✍️",
    layout="centered"
)

# --- Styling (Optional) ---
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

# --- Load Entries from JSON ---
if 'journal_entries' not in st.session_state:
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            st.session_state.journal_entries = json.load(f)
    else:
        st.session_state.journal_entries = {}  # Key: date (str), Value: entry_text (str)

# --- Session State Initialization ---
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.date.today()

# --- Functions ---
def save_entry(date, entry_text):
    st.session_state.journal_entries[date.isoformat()] = entry_text
    # Save to JSON file
    with open(JSON_FILE, "w") as f:
        json.dump(st.session_state.journal_entries, f, indent=4)
    st.success(f"Entry for {date.strftime('%Y-%m-%d')} saved!")

def get_entry(date):
    return st.session_state.journal_entries.get(date.isoformat(), "")

# --- Header ---
st.title("✍️ Daily Journal")
st.markdown("---")

# --- Date Selection ---
st.sidebar.header("Select a Date")
selected_date = st.sidebar.date_input(
    "Choose a date to view or write an entry:",
    value=st.session_state.selected_date,
    max_value=datetime.date.today(),
    key="date_selector"
)
st.session_state.selected_date = selected_date

# --- Main Content Area ---
st.subheader(f"Journal Entry for {selected_date.strftime('%A, %B %d, %Y')}")

# Load existing entry for the selected date
current_entry_text = get_entry(selected_date)

# Text area for writing/editing the entry
entry_text = st.text_area(
    "What's on your mind today?",
    value=current_entry_text,
    height=300,
    key=f"journal_editor_{selected_date}"
)

# Save button
if st.button("Save Entry", key=f"save_button_{selected_date}"):
    save_entry(selected_date, entry_text)

st.markdown("---")

# --- View All Entries ---
st.sidebar.header("All Entries")
if st.session_state.journal_entries:
    sorted_dates = sorted(st.session_state.journal_entries.keys(), reverse=True)
    for date_str in sorted_dates:
        if st.sidebar.button(date_str, key=f"view_date_{date_str}"):
            # Set the selected date to view this entry
            st.session_state.selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            st.experimental_rerun()
else:
    st.sidebar.info("No entries saved yet.")

st.sidebar.markdown("---")
st.sidebar.info(f"Your entries are saved in `{JSON_FILE}` and will persist between sessions.")
