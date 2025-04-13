import streamlit as st
import datetime
import json
import os
import calendar
import random

# ----- Set up ----- #
st.set_page_config(page_title="SkillTrack App")
st.title("📚 SkillTrack")
st.caption("Your ultimate learning progress tracker")

# ----- Multi-user Key Input ----- #
st.sidebar.header("👤 User Login")
username = st.sidebar.text_input("Enter your name or username")

if not username:
    st.warning("Please enter your name in the sidebar to continue.")
    st.stop()

# ----- Data Persistence ----- #
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)
DATA_FILE = os.path.join(DATA_DIR, f"{username}_progress.json")

# ----- Daily Motivational Quotes ----- #
QUOTES = [
    "Keep pushing forward, even small progress is progress!",
    "Every expert was once a beginner.",
    "You're doing great — keep it up!",
    "Learning never exhausts the mind.",
    "A little progress each day adds up to big results.",
    "The future depends on what you do today."
]

def get_daily_quote():
    today_index = datetime.date.today().toordinal() % len(QUOTES)
    return QUOTES[today_index]

# ----- Load/Save Data ----- #
def make_json_serializable(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    else:
        return obj

def load_data():
    default_data = {
        "logs": [],
        "completed_topics": [],
        "learning_paths": {},
        "goals": [],
        "last_log_date": None,
        "custom_daily_duration": 1,
        "daily_topic_targets_met": {},
        "roadmaps": {}
    }
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        for key, value in default_data.items():
            if key not in data:
                data[key] = value
        return data
    return default_data

def save_data(data):
    serializable_data = make_json_serializable(data)
    with open(DATA_FILE, 'w') as f:
        json.dump(serializable_data, f, indent=2)

user_data = load_data()

# ----- Predefined Learning Roadmaps with Subtopics ----- #
ROADMAPS = {
    "Machine Learning": [
        "Python Basics", "Numpy & Pandas", "Data Visualization", "Statistics & Probability",
        "Linear Regression", "Logistic Regression", "Decision Trees", "SVM",
        "Ensemble Methods", "Clustering", "Dimensionality Reduction", "Model Evaluation",
        "Neural Networks", "Deep Learning Basics", "Projects"
    ],
    "Web Development": [
        "HTML & CSS", "JavaScript Basics", "DOM Manipulation", "Responsive Design",
        "Version Control (Git)", "Frontend Frameworks (React)", "Backend Basics",
        "APIs & REST", "Databases", "Authentication & Security", "Deployment", "Full Stack Project"
    ],
    "Data Science": [
        "Python for Data Science", "Pandas & Numpy", "Matplotlib & Seaborn", "EDA",
        "Data Cleaning", "Feature Engineering", "ML Algorithms", "Model Deployment"
    ]
}

user_data["roadmaps"] = ROADMAPS

# ----- Save ----- #
save_data(user_data)
