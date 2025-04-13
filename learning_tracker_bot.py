import streamlit as st
import datetime
import json
import os

# ----- Set up ----- #
st.set_page_config(page_title="SkillTrack Bot")
st.title("🤖 SkillTrack Bot")
st.caption("Your chatbot assistant to track ML & Web Dev progress.")

# ----- Data Persistence ----- #
DATA_FILE = "progress_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"logs": [], "completed_topics": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Load data
user_data = load_data()

# ----- Topic Roadmaps ----- #
ml_roadmap = [
    "Supervised Learning", "Unsupervised Learning", "Regression", "Classification", "Decision Trees",
    "Random Forests", "XGBoost", "Model Evaluation", "Overfitting", "Underfitting", "Feature Engineering"
]

web_roadmap = [
    "HTML", "CSS", "Flexbox", "Grid", "JavaScript", "React", "Node.js", "APIs", "Express.js", "MongoDB",
    "Frontend Deployment", "Backend Deployment"
]

# Combine for detection
all_topics = {topic.lower(): topic for topic in ml_roadmap + web_roadmap}

# ----- Chat Input ----- #
st.subheader("💬 Chat with SkillTrack Bot")
user_input = st.text_input("You:", placeholder="I learned Decision Trees and Flexbox today.")

if st.button("Send") and user_input:
    log_entry = {
        'date': datetime.date.today().isoformat(),
        'entry': user_input
    }
    user_data["logs"].append(log_entry)

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
ml_done = [t for t in ml_roadmap if t in user_data["completed_topics"]]
web_done = [t for t in web_roadmap if t in user_data["completed_topics"]]

# ----- Chatbot Response ----- #
if user_input:
    st.markdown("---")
    st.markdown("**🤖 SkillTrack Bot says:**")
    if ml_done or web_done:
        st.write("Nice! I’ve updated your progress.")
    else:
        st.write("Got it! Keep pushing forward.")

    next_ml = [t for t in ml_roadmap if t not in user_data["completed_topics"]][:1]
    next_web = [t for t in web_roadmap if t not in user_data["completed_topics"]][:1]

    if next_ml:
        st.info(f"Next ML topic to learn: **{next_ml[0]}**")
    else:
        st.success("🎉 You've completed all ML topics!")

    if next_web:
        st.info(f"Next Web Dev topic to learn: **{next_web[0]}**")
    else:
        st.success("🎉 You've completed all Web Dev topics!")

# ----- Visual Progress ----- #
st.subheader("📊 Your Learning Progress")
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Machine Learning**")
    st.progress(len(ml_done) / len(ml_roadmap))
    st.write(f"{len(ml_done)} / {len(ml_roadmap)} topics completed")

with col2:
    st.markdown("**Web Development**")
    st.progress(len(web_done) / len(web_roadmap))
    st.write(f"{len(web_done)} / {len(web_roadmap)} topics completed")

# ----- Log History ----- #
st.subheader("🗒️ Your Learning Log")
if user_data["logs"]:
    for log in reversed(user_data["logs"]):
        st.write(f"[{log['date']}] {log['entry']}")
else:
    st.write("No logs yet. Start learning and log your first entry!")
