import streamlit as st
import datetime
import json
import os

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
    return {"logs": [], "completed_topics": [], "learning_path": [], "goal": None, "last_log_date": None}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

user_data = load_data()

# ----- Learning Goal Selection ----- #
if not user_data["goal"]:
    st.sidebar.subheader("🎯 Choose Your Learning Goal")
    goal = st.sidebar.selectbox("What do you want to learn?", ["Machine Learning", "Web Development", "Data Science", "App Development", "Other"])
    if st.sidebar.button("Set Goal"):
        user_data["goal"] = goal
        if goal == "Machine Learning":
            user_data["learning_path"] = [
                "Supervised Learning", "Unsupervised Learning", "Regression", "Classification", "Decision Trees",
                "Random Forests", "XGBoost", "Model Evaluation", "Overfitting", "Underfitting", "Feature Engineering"
            ]
        elif goal == "Web Development":
            user_data["learning_path"] = [
                "HTML", "CSS", "Flexbox", "Grid", "JavaScript", "React", "Node.js", "APIs", "Express.js", "MongoDB",
                "Frontend Deployment", "Backend Deployment"
            ]
        elif goal == "Data Science":
            user_data["learning_path"] = [
                "Python Basics", "Numpy", "Pandas", "Data Visualization", "EDA", "Data Cleaning",
                "Statistical Analysis", "Machine Learning Basics", "Model Evaluation"
            ]
        elif goal == "App Development":
            user_data["learning_path"] = [
                "Flutter Basics", "Widgets", "Navigation", "State Management", "Firebase Integration",
                "API Calls", "Authentication", "Deployment"
            ]
        else:
            user_data["learning_path"] = []

        save_data(user_data)
        st.experimental_rerun()

if not user_data["goal"]:
    st.stop()

st.sidebar.success(f"Current Goal: {user_data['goal']}")

# ----- Daily Reminder to Log Progress ----- #
today = datetime.date.today().isoformat()
if user_data.get("last_log_date") != today:
    st.warning("👋 Don't forget to log your progress today!")

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

    # Match topics
    for word in user_input.lower().split():
        word_clean = word.strip(",.()")
        if word_clean in all_topics:
            topic = all_topics[word_clean]
            if topic not in user_data["completed_topics"]:
                user_data["completed_topics"].append(topic)

    save_data(user_data)
    st.success("✅ Logged your progress!")

# ----- Progress Calculation ----- #
completed = [t for t in user_data["learning_path"] if t in user_data["completed_topics"]]
remaining = [t for t in user_data["learning_path"] if t not in completed]

# ----- Chatbot Response ----- #
if user_input:
    st.markdown("---")
    st.markdown("**🤖 SkillTrack Bot says:**")
    if completed:
        st.write("Nice! I’ve updated your progress.")
    else:
        st.write("Got it! Keep pushing forward.")

    if remaining:
        st.info(f"Next topic to learn: **{remaining[0]}**")
    else:
        st.success("🎉 You've completed your learning path for this goal!")

# ----- Visual Progress ----- #
st.subheader("📊 Your Learning Progress")
st.progress(len(completed) / len(user_data["learning_path"]))
st.write(f"{len(completed)} / {len(user_data['learning_path'])} topics completed")

# ----- Personalized Learning Path Generator ----- #
st.subheader("🎯 Your Personalized Learning Path")
st.markdown("Based on your current progress, here's what we suggest next:")

if remaining:
    for i, topic in enumerate(remaining[:5], start=1):
        st.write(f"{i}. {topic}")
else:
    st.success("You've completed your custom learning path! 🎉")

# ----- Learning Roadmap (Daily, Weekly, Monthly) ----- #
st.subheader("🗺️ Suggested Roadmap")
with st.expander("📅 Daily Goals"):
    st.markdown("- Learn 1 small topic")
    st.markdown("- Practice 1 problem / mini project")
    st.markdown("- Log your learning in SkillTrack Bot")

with st.expander("📆 Weekly Goals"):
    st.markdown("- Complete 3–5 topics")
    st.markdown("- Build a mini-project using what you learned")
    st.markdown("- Revise previous week’s concepts")

with st.expander("🗓️ Monthly Goals"):
    st.markdown("- Complete a full module")
    st.markdown("- Create a capstone project and upload to GitHub")
    st.markdown("- Share progress on your portfolio or blog")

# ----- Leaderboard ----- #
st.subheader("🏆 Leaderboard")
leaderboard = []

for filename in os.listdir(DATA_DIR):
    if filename.endswith("_progress.json"):
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            if data.get("learning_path"):
                score = len(data.get("completed_topics", [])) / len(data["learning_path"])
                name = filename.replace("_progress.json", "")
                leaderboard.append((name, round(score * 100, 1)))

leaderboard.sort(key=lambda x: x[1], reverse=True)

for rank, (name, progress) in enumerate(leaderboard[:10], start=1):
    st.write(f"{rank}. **{name}** - {progress}% completed")

# ----- Log History ----- #
st.subheader("🗒️ Your Learning Log")
if user_data["logs"]:
    for log in reversed(user_data["logs"]):
        st.write(f"[{log['date']}] {log['entry']}")
else:
    st.write("No logs yet. Start learning and log your first entry!")


