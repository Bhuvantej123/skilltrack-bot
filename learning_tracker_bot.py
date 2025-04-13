import streamlit as st
import datetime
import json
import os
import calendar
import random

# ----- Set up ----- #
st.set_page_config(page_title="SkillTrack App")
st.title("🤖 SkillTrack Chatbot")

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
    "App Development": [
        "Java/Kotlin or Swift Basics", "Mobile UI/UX Principles", "Navigation & Routing",
        "State Management", "Local Storage", "APIs & Networking", "Authentication",
        "Push Notifications", "Publishing to Play Store/App Store"
    ],
    "Data Science": [
        "Python for Data Science", "Data Wrangling with Pandas", "Exploratory Data Analysis",
        "Data Visualization with Matplotlib/Seaborn", "Statistics & Probability",
        "Machine Learning Introduction", "Data Storytelling", "Capstone Project"
    ]
}

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
        "custom_daily_duration": None,
        "daily_topic_targets_met": {},
        "roadmaps": {},
        "progress": {},
        "notifications_enabled": True
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

# ----- Display Chatbot UI ----- #
st.subheader("👋 Hello, " + username + "!")
st.success(get_daily_quote())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Learning path setup first
if not user_data["goals"]:
    st.markdown("### 🌟 Let's set your learning path(s)")
    multiple = st.radio("Would you like to select multiple learning paths?", ["Yes", "No"])

    if multiple == "Yes":
        selected_goals = st.multiselect("Select what you want to learn:", list(ROADMAPS.keys()))
    else:
        selected_goal = st.selectbox("Select what you want to learn:", list(ROADMAPS.keys()))
        selected_goals = [selected_goal]

    if selected_goals:
        for goal_input in selected_goals:
            if goal_input not in user_data["goals"]:
                user_data["goals"].append(goal_input)
                user_data["learning_paths"][goal_input] = []
                user_data["roadmaps"][goal_input] = ROADMAPS.get(goal_input, [])
                user_data["progress"][goal_input] = {topic: False for topic in ROADMAPS.get(goal_input, [])}
        st.success("Goals added successfully!")
        for goal_input in selected_goals:
            st.info(f"### Roadmap for {goal_input}")
            for idx, topic in enumerate(user_data["roadmaps"][goal_input], 1):
                st.markdown(f"- {idx}. {topic}")
        save_data(user_data)
        st.stop()
elif user_data["custom_daily_duration"] is None:
    duration = st.slider("⏱️ Set your custom learning time per day (hours):", 1, 8, 1)
    if duration:
        user_data["custom_daily_duration"] = duration
        st.success(f"Awesome! You'll spend {duration} hour(s) per day learning.")
        save_data(user_data)
        st.rerun()
else:
    st.markdown("### 📋 Your Learning Roadmap")
    for goal in user_data["goals"]:
        st.markdown(f"#### {goal}")
        if st.button(f"Delete {goal}", key=f"delete_{goal}"):
            user_data["goals"].remove(goal)
            user_data["learning_paths"].pop(goal, None)
            user_data["roadmaps"].pop(goal, None)
            user_data["progress"].pop(goal, None)
            save_data(user_data)
            st.rerun()
        for topic in user_data["roadmaps"].get(goal, []):
            is_done = user_data["progress"][goal].get(topic, False)
            checkbox = st.checkbox(label=topic, value=is_done, key=f"{goal}_{topic}")
            user_data["progress"][goal][topic] = checkbox
        save_data(user_data)

    user_input = st.text_input("💬 What did you work on today?", key="chat")
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        today = str(datetime.date.today())
        user_data["logs"].append({"date": today, "goal": user_data["goals"], "entry": user_input})
        response = "Great job! Your progress has been logged."
        st.session_state.chat_history.append(("Bot", response))
        save_data(user_data)

# Show current progress and goals
if user_data["goals"]:
    st.sidebar.subheader("📊 Your Progress")
    for goal in user_data["goals"]:
        completed = sum(user_data["progress"].get(goal, {}).values())
        total = len(user_data["progress"].get(goal, {}))
        percent = int((completed / total) * 100) if total > 0 else 0
        st.sidebar.write(f"**{goal}**: {percent}% complete")
        st.sidebar.progress(percent)

# Display chat history
st.divider()
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
