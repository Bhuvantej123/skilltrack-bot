import streamlit as st
import datetime
import json
import os
import calendar

# ----- Set up ----- #
st.set_page_config(page_title="SkillTrack Bot")
st.title("🤖 SkillTrack Bot")
st.caption("Your chatbot assistant to track any learning journey.")

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

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "logs": [], "completed_topics": [], "learning_path": [], "goal": None,
        "last_log_date": None, "custom_daily_duration": 1, "daily_topic_targets_met": {}
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

user_data = load_data()

# ----- Learning Goal Selection ----- #
if not user_data["goal"]:
    st.sidebar.subheader("🌟 Choose Your Learning Goal")
    goal = st.sidebar.selectbox("What do you want to learn?", ["Machine Learning", "Web Development", "Data Science", "App Development", "Other"])
    if st.sidebar.button("Set Goal"):
        user_data["goal"] = goal
        if goal == "Machine Learning":
            user_data["learning_path"] = [
                "Supervised Learning", "Unsupervised Learning", "Regression", "Classification", "Decision Trees",
                "Random Forests", "XGBoost", "Model Evaluation", "Overfitting", "Underfitting", "Feature Engineering"
            ]
            user_data["roadmap"] = {
                "Week 1": ["Supervised Learning", "Unsupervised Learning"],
                "Week 2": ["Regression", "Classification"],
                "Week 3": ["Decision Trees", "Random Forests"],
                "Week 4": ["XGBoost", "Model Evaluation", "Overfitting", "Underfitting", "Feature Engineering"]
            }
        elif goal == "Web Development":
            user_data["learning_path"] = [
                "HTML", "CSS", "Flexbox", "Grid", "JavaScript", "React", "Node.js", "APIs", "Express.js", "MongoDB",
                "Frontend Deployment", "Backend Deployment"
            ]
            user_data["roadmap"] = {
                "Week 1": ["HTML", "CSS"],
                "Week 2": ["Flexbox", "Grid", "JavaScript"],
                "Week 3": ["React", "Node.js"],
                "Week 4": ["APIs", "Express.js", "MongoDB"],
                "Week 5": ["Frontend Deployment", "Backend Deployment"]
            }
        elif goal == "Data Science":
            user_data["learning_path"] = [
                "Python Basics", "Numpy", "Pandas", "Data Visualization", "EDA", "Data Cleaning",
                "Statistical Analysis", "Machine Learning Basics", "Model Evaluation"
            ]
            user_data["roadmap"] = {
                "Week 1": ["Python Basics", "Numpy"],
                "Week 2": ["Pandas", "Data Visualization"],
                "Week 3": ["EDA", "Data Cleaning"],
                "Week 4": ["Statistical Analysis", "Machine Learning Basics", "Model Evaluation"]
            }
        elif goal == "App Development":
            user_data["learning_path"] = [
                "Flutter Basics", "Widgets", "Navigation", "State Management", "Firebase Integration",
                "API Calls", "Authentication", "Deployment"
            ]
            user_data["roadmap"] = {
                "Week 1": ["Flutter Basics", "Widgets"],
                "Week 2": ["Navigation", "State Management"],
                "Week 3": ["Firebase Integration", "API Calls"],
                "Week 4": ["Authentication", "Deployment"]
            }
        else:
            user_data["learning_path"] = []
            user_data["roadmap"] = {}

        save_data(user_data)
        st.experimental_rerun()

if not user_data["goal"]:
    st.stop()

st.sidebar.success(f"Current Goal: {user_data['goal']}")

# ----- Daily Reminder to Log Progress ----- #
today = datetime.date.today().isoformat()
if user_data.get("last_log_date") != today:
    st.warning("👋 Don't forget to log your progress today!")

# ----- Daily Study Duration Setting ----- #
st.sidebar.subheader("⏱️ Custom Daily Learning Duration")
daily_duration = st.sidebar.slider("How many hours per day do you plan to study?", 0.5, 12.0, float(user_data.get("custom_daily_duration", 1)), 0.5)
user_data["custom_daily_duration"] = daily_duration
save_data(user_data)

# ----- Combine topics for detection ----- #
all_topics = {topic.lower(): topic for topic in user_data["learning_path"]}

# ----- Chat Input ----- #
st.subheader("💬 Chat with SkillTrack Bot")
user_input = st.text_input("You:", placeholder="I learned Decision Trees and Flexbox today.")

if st.button("Send") and user_input:
    log_entry = {
        'date': today,
        'entry': user_input
    }
    user_data["logs"].append(log_entry)
    user_data["last_log_date"] = today

    topics_learned_today = []

    for word in user_input.lower().split():
        word_clean = word.strip(",.()")
        if word_clean in all_topics:
            topic = all_topics[word_clean]
            if topic not in user_data["completed_topics"]:
                user_data["completed_topics"].append(topic)
                topics_learned_today.append(topic)

    expected_topics_today = int(user_data["custom_daily_duration"])
    actual_topics = len(topics_learned_today)
    met_target = actual_topics >= expected_topics_today
    user_data["daily_topic_targets_met"][today] = met_target

    save_data(user_data)
    st.success("✅ Logged your progress!")

    st.markdown("---")
    st.markdown("**🤖 SkillTrack Bot says:**")
    if topics_learned_today:
        st.write(f"Awesome! I logged the topics: {', '.join(topics_learned_today)}")
    else:
        st.write("Got it! I didn't detect specific topics, but your log was saved.")

    if met_target:
        st.success(f"🎯 You met your target of {expected_topics_today} topic(s) today!")
    else:
        st.warning(f"⚠️ You learned {actual_topics} topic(s) today. Target was {expected_topics_today}.")

completed = [t for t in user_data["learning_path"] if t in user_data["completed_topics"]]
remaining = [t for t in user_data["learning_path"] if t not in completed]

if user_input:
    if remaining:
        st.info(f"Next topic to learn: **{remaining[0]}**")
    else:
        st.success("🎉 You've completed your learning path for this goal!")



