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
        "custom_daily_duration": 1,
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

# Initial prompt based on goal or roadmap
if not user_data["goals"]:
    question = "What do you want to learn? (e.g., Machine Learning, Web Development, etc.)"
else:
    question = f"What did you work on today in {', '.join(user_data['goals'])}?"

user_input = st.text_input("💬 You:", key="chat")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    response = ""

    if not user_data["goals"]:
        user_data["goals"].append(user_input)
        user_data["learning_paths"][user_input] = []
        user_data["roadmaps"][user_input] = ROADMAPS.get(user_input, [])
        user_data["progress"][user_input] = {topic: False for topic in ROADMAPS.get(user_input, [])}
        response = f"Great! I've added {user_input} to your learning goals and built a roadmap for it."
    else:
        today = str(datetime.date.today())
        user_data["logs"].append({"date": today, "goal": user_data["goals"], "entry": user_input})
        response = "Nice progress! I've logged this entry for today."

    st.session_state.chat_history.append(("Bot", response))
    save_data(user_data)

# Show current progress and goals
if user_data["goals"]:
    st.sidebar.subheader("📈 Your Progress")
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
