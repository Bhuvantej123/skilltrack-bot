import streamlit as st
import datetime
from datetime import timedelta
import json
import os

# ----- Load or Initialize User Data ----- #
def load_user_data():
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as f:
            return json.load(f)
    else:
        return {
            "goals": [],
            "progress": {},
            "logs": [],
            "duration": {},
        }

def save_user_data(data):
    with open("user_data.json", "w") as f:
        json.dump(data, f, indent=4)

user_data = load_user_data()

st.title("📚 SkillTrack Learning Assistant")

# ----- Add Learning Paths ----- #
if st.sidebar.button("➕ Add Learning Path"):
    new_goal = st.sidebar.text_input("Enter learning path name:")
    if new_goal:
        user_data["goals"].append(new_goal)
        user_data["progress"][new_goal] = {}
        user_data["duration"][new_goal] = 1  # default 1 hour/day
        save_user_data(user_data)
        st.experimental_rerun()

# ----- Display Goals and Allow Selection ----- #
if user_data["goals"]:
    selected_goals = st.sidebar.multiselect("Your Learning Paths:", user_data["goals"], default=user_data["goals"])

    for goal in selected_goals:
        st.header(f"📘 {goal} Roadmap")

        # Duration input
        duration = st.number_input(f"Set daily learning time for {goal} (in hours):", min_value=1, max_value=10, value=user_data["duration"].get(goal, 1))
        user_data["duration"][goal] = duration

        # Sample Subtopics (Can be expanded dynamically based on learning path)
        if not user_data["progress"][goal]:
            subtopics = ["Introduction", "Core Concepts", "Project 1", "Advanced Topics"]
            user_data["progress"][goal] = {topic: False for topic in subtopics}

        # Display and update topic progress
        for topic in user_data["progress"][goal]:
            completed = st.checkbox(f"✅ {topic}", value=user_data["progress"][goal][topic], key=f"{goal}_{topic}")
            user_data["progress"][goal][topic] = completed

        # Option to delete learning path
        if st.button(f"🗑️ Delete {goal}"):
            user_data["goals"].remove(goal)
            user_data["progress"].pop(goal, None)
            user_data["duration"].pop(goal, None)
            save_user_data(user_data)
            st.experimental_rerun()

# ----- Daily Log Entry ----- #
st.subheader("📝 Daily Progress Log")
log_text = st.text_area("What did you learn today?")
selected_goal_for_log = st.selectbox("Which learning path does this log belong to?", user_data["goals"] if user_data["goals"] else ["None"])

if st.button("📥 Save Log") and log_text:
    user_data["logs"].append({
        "date": str(datetime.date.today()),
        "goal": selected_goal_for_log,
        "entry": log_text
    })
    save_user_data(user_data)
    st.success("Log saved successfully!")

# ----- Logs Tab ----- #
st.subheader("📜 Logs")
if user_data["logs"]:
    for log in reversed(user_data["logs"]):
        st.markdown(f"**{log['date']} - {log['goal']}**: {log['entry']}")
else:
    st.info("No logs yet. Start by writing what you learned today!")

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

feedback_messages = {
    0: "Let's jumpstart this week! Even one step counts. You've got this! 💡",
    1: "Solid step! Try hitting 2-3 topics next week. Slow progress is still progress. 🚀",
    2: "Great job tackling two topics! You’re getting warmed up. Keep going! 🏃",
    3: "Nice! Three topics completed — you’re right on track. Stay consistent! 📆",
    4: "You're crushing it! Four topics down this week — fantastic hustle! 🎉",
    5: "Wow! Five topics? That’s top-tier dedication! 🏆 Keep slaying those goals!",
    '5+': "Legend mode activated! You're blazing through your goals like a pro. 🚀🌟"
}

for goal in user_data["goals"]:
    total = len(user_data["progress"][goal])
    completed = topics_completed_this_week[goal]
    st.markdown(f"**{goal}**: You completed **{completed}** out of **{total}** topics this week.")

    if completed >= 6:
        st.success(feedback_messages['5+'])
    else:
        feedback = feedback_messages.get(completed, "Keep learning, you're on the path to mastery!")
        if completed == 0:
            st.warning(feedback)
        elif completed < 3:
            st.info(feedback)
        else:
            st.success(feedback)

save_user_data(user_data)
