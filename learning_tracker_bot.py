import streamlit as st
import datetime
import json
import os
import calendar
import random
from datetime import timedelta

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
        "notifications_enabled": True,
        "planner": {}
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

# ----- Smart Notification Reminder ----- #
today_str = str(datetime.date.today())
last_log_date = user_data.get("last_log_date")

today_logged = any(log["date"] == today_str for log in user_data["logs"])
if user_data.get("notifications_enabled", True) and not today_logged:
    st.warning("⏰ Reminder: You haven't logged your progress today! Don't forget to update your tracker.")

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
                user_data["planner"][goal_input] = {
                    "weekly_goal": ROADMAPS[goal_input][:3],
                    "daily_tasks": ROADMAPS[goal_input][:1],
                    "priority": "medium"
                }
        st.success("Goals added successfully!")

        # Side-by-side roadmap display
        cols = st.columns(len(selected_goals))
        for idx, goal_input in enumerate(selected_goals):
            with cols[idx]:
                st.info(f"### {goal_input} Roadmap")
                for i, topic in enumerate(user_data["roadmaps"][goal_input], 1):
                    st.markdown(f"{i}. {topic}")
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
            user_data["planner"].pop(goal, None)
            save_data(user_data)
            st.rerun()

        for topic in user_data["roadmaps"].get(goal, []):
            is_done = user_data["progress"][goal].get(topic, False)
            checkbox_key = f"{username}_{goal}_{topic}"
            checkbox = st.checkbox(label=topic, value=is_done, key=checkbox_key)
            user_data["progress"][goal][topic] = checkbox
        save_data(user_data)

    user_input = st.text_input("💬 What did you work on today?", key="chat")
    if user_input:
        st.session_state.chat_history.append(("You", user_input))
        today = str(datetime.date.today())
        user_data["logs"].append({"date": today, "goal": user_data["goals"], "entry": user_input})
        user_data["last_log_date"] = today
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

# Display logs and calendar view
tabs = st.tabs(["📔 Logs", "🗕 Calendar View"])

with tabs[0]:
    if user_data["logs"]:
        for log in reversed(user_data["logs"]):
            st.write(f"🗓 {log['date']} — {log['goal']}\n📜 {log['entry']}")
    else:
        st.info("No logs yet. Start tracking your progress!")

with tabs[1]:
    st.markdown("### Calendar Logs")
    selected_date = st.date_input("Pick a date to view logs")
    selected_date_str = str(selected_date)
    logs_for_date = [log for log in user_data["logs"] if log["date"] == selected_date_str]
    if logs_for_date:
        for log in logs_for_date:
            st.write(f"🗓 {log['date']} — {log['goal']}\n📜 {log['entry']}")
    else:
        st.info("No entries found for this date.")

# ----- Weekly Progress Analysis & Feedback ----- #
st.subheader("📈 Weekly Progress Analysis")

one_week_ago = datetime.date.today() - timedelta(days=7)
logs_past_week = [
    log for log in user_data["logs"]
    if datetime.date.fromisoformat(log["date"]) >= one_week_ago
]

topics_completed_this_week = {
    goal: sum(
        1 for topic, done in user_data["progress"][goal].items()
        if done and any(
            goal in log["goal"] and topic.lower() in log["entry"].lower()
            for log in logs_past_week
        )
    )
    for goal in user_data["goals"]
}

for goal in user_data["goals"]:
    total = len(user_data["progress"][goal])
    completed = topics_completed_this_week[goal]
    st.markdown(f"**{goal}**: You completed **{completed}** out of **{total}** topics this week.")

    if completed == 0:
        st.warning("Try to get at least one topic done this week. You got this! 💪")
    elif completed < 3:
        st.info("Nice start! Aim to complete 3 or more topics weekly for good momentum. 🚀")
    else:
        st.success("Great job! You're making solid weekly progress. Keep it up! 🌟")

# Display chat history
st.divider()
for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
