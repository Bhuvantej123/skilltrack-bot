import streamlit as st
import datetime
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import calplot
import base64

st.set_page_config(page_title="✨ SkillTrack Bot ✨", layout="wide")

# ------------------ SESSION STATE ------------------ #
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "📊 Dashboard"

# if st.session_state.get("jump_to_logs"):
#     st.session_state.current_tab = "📒 Logs"
#     st.session_state.jump_to_logs = False
#     st.rerun()

# ------------------ GLOWING DARK SPARKLE BACKGROUND ------------------ #
st.markdown("""
<style>
body { background-color: #1e1e2f; }
.stApp {
    background: radial-gradient(circle, #2c3e50, #1e1e2f);
    color: #f5f6fa;
    font-family: 'Segoe UI', sans-serif;
}
.stButton>button {
    background: linear-gradient(90deg, #8e44ad, #3498db);
    color: white;
    border-radius: 12px;
    font-weight: bold;
}
.stProgress>div>div>div {
    background: linear-gradient(to right, #f39c12, #f1c40f);
}
#sparkles {
    position: fixed;
    width: 100%;
    height: 100%;
    pointer-events: none;
    top: 0; left: 0; z-index: 0;
}
.sparkle {
    width: 8px; height: 8px;
    background: rgba(255,255,255,0.7);
    border-radius: 50%;
    position: absolute;
    animation: float 10s infinite ease-in-out;
}
@keyframes float {
    0% { transform: translateY(0) translateX(0); opacity: 1;}
    100% { transform: translateY(-100vh) translateX(100px); opacity: 0;}
}
</style>
<div id="sparkles"></div>
<script>
for (let i = 0; i < 40; i++) {
    let s = document.createElement("div");
    s.className = "sparkle";
    s.style.left = Math.random() * 100 + "vw";
    s.style.top = Math.random() * 100 + "vh";
    s.style.animationDuration = (Math.random() * 10 + 5) + "s";
    document.getElementById("sparkles").appendChild(s);
}
</script>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR USER LOGIN ------------------ #
st.sidebar.header("👤 User Login")
username = st.sidebar.text_input("Enter your name")
# profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
DATA_DIR = "user_data"
os.makedirs(DATA_DIR, exist_ok=True)

if not username:
    st.warning("Please enter a name to continue.")
    st.stop()

# profile_pic_path = os.path.join(DATA_DIR, f"{username}_pic.jpg")
# if profile_pic:
#     with open(profile_pic_path, "wb") as f:
#         f.write(profile_pic.read())

data_path = os.path.join(DATA_DIR, f"{username}_data.json")
if os.path.exists(data_path):
    with open(data_path, "r") as f:
        user_data = json.load(f)
else:
    user_data = {"logs": {}, "completed": [], "achievements": []}

# ------------------ SIDEBAR NAVIGATION ------------------ #
tabs = ["📊 Dashboard", "🗺️ Roadmaps", "📒 Logs", "🎯 Motivation", "📆 Calendar"]
if st.session_state.current_tab not in tabs:
    st.session_state.current_tab = tabs[0]

current_tab = st.sidebar.radio("📁 Navigate", tabs, index=tabs.index(st.session_state.current_tab))
st.session_state.current_tab = current_tab

# ------------------ DASHBOARD ------------------ #

        
 # Ensure this is at the top

# ------------------ DASHBOARD ------------------ #
if current_tab == "📊 Dashboard":
    st.subheader("👤 Your Profile")
    profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    profile_col, info_col = st.columns([1, 5])
    profile_pic_path = os.path.join(DATA_DIR, f"{username}_pic.jpg")
    with profile_col:
        # Show profile picture
        if os.path.exists(profile_pic_path):
            with open(profile_pic_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode()
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <img src='data:image/png;base64,{encoded}' width='120'
                    style='border-radius: 50%; border: 2px solid #8e44ad; box-shadow: 0 0 10px #8e44ad;'>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.image("https://avatars.githubusercontent.com/u/9919?s=280&v=4", width=100)

        # Show upload option only if not just uploaded
        if "pic_uploaded" not in st.session_state:
            st.markdown("### 🖼️ Update Profile Picture", unsafe_allow_html=True)
            new_pic = st.file_uploader("Upload new image", type=["jpg", "jpeg", "png"])
            if new_pic and st.button("✨ Update Picture"):
                with open(profile_pic_path, "wb") as f:
                    f.write(new_pic.read())
                st.session_state.pic_uploaded = True
                st.success("Profile picture updated! 🎉")
                st.rerun()

    with info_col:
        st.markdown(f"<h2>Welcome back, {username} 🌟</h2>", unsafe_allow_html=True)
        with st.expander("⚙️ Profile Settings"):
            st.markdown("### 🖊️ Change Username")
            new_username = st.text_input("Enter new username", value=username, key="username_editor")
            if st.button("✅ Update Username"):
                if new_username and new_username != username:
                    new_data_path = os.path.join(DATA_DIR, f"{new_username}_data.json")
                    if os.path.exists(new_data_path):
                        st.error("This username already exists. Please choose another.")
                    else:
                        os.rename(data_path, new_data_path)

                        old_pic = os.path.join(DATA_DIR, f"{username}_pic.jpg")
                        new_pic = os.path.join(DATA_DIR, f"{new_username}_pic.jpg")
                        if os.path.exists(old_pic):
                            os.rename(old_pic, new_pic)

                        st.success("Username updated. Please log in again.")
                        st.session_state.clear()
                        st.rerun()
                else:
                    st.info("No change detected.")

            st.markdown("### 🖼️ Update Profile Picture")
            new_pic = st.file_uploader("Upload new profile image", type=["jpg", "jpeg", "png"], key="new_profile_pic")
            if new_pic and st.button("📸 Upload New Picture"):
                with open(os.path.join(DATA_DIR, f"{username}_pic.jpg"), "wb") as f:
                    f.write(new_pic.read())
                st.success("Profile picture updated! 🎉")
                st.rerun()

            st.markdown("### 🔒 Logout")
            if st.button("🚪 Log Out"):
                st.session_state.clear()
                st.rerun()



        # XP + Level system
        xp_per_topic = 20
        completed = user_data.get("completed", [])
        xp = len(completed) * xp_per_topic
        level = xp // 100
        next_level_xp = 100 - (xp % 100)

        st.markdown(f"**🧠 XP:** `{xp}`  &nbsp;|&nbsp; **📈 Level:** `{level}`")
        st.progress((xp % 100) / 100)
        st.caption(f"{next_level_xp} XP to next level")

        # Achievements
        achievements = user_data.get("achievements", [])
        if len(completed) >= 5 and "Starter" not in achievements:
            achievements.append("Starter")
        if len(completed) >= 10 and "Achiever" not in achievements:
            achievements.append("Achiever")
        if len(user_data.get("logs", {})) >= 7 and "Logger Pro" not in achievements:
            achievements.append("Logger Pro")
        if level >= 3 and "Level 3+" not in achievements:
            achievements.append("Level 3+")

        user_data["achievements"] = achievements
        with open(data_path, "w") as f:
            json.dump(user_data, f, indent=2)

        if achievements:
            st.subheader("🏅 Achievements")
            for badge in achievements:
                st.success(f"🏆 {badge}")


    

    

# ------------------ ROADMAPS ------------------ #
elif current_tab == "🗺️ Roadmaps":
    st.header("🗺️ Personalized Learning Roadmaps")

    all_paths = {
        "Machine Learning": [
            "Python Basics", "Numpy & Pandas", "Data Visualization", "Linear Regression", "Classification",
            "Decision Trees", "Random Forest", "Unsupervised Learning", "Clustering", "Model Evaluation"
        ],
        "Web Development": [
            "HTML", "CSS", "JavaScript", "Flexbox & Grid", "DOM Manipulation",
            "React Basics", "React Router", "Node.js", "Express", "MongoDB"
        ],
        "Data Science": [
            "Python for Data Science", "Data Wrangling", "EDA", "Matplotlib & Seaborn", "Statistical Analysis",
            "Hypothesis Testing", "Machine Learning Overview", "Model Selection", "Regression & Classification"
        ],
        "App Development": [
            "Flutter Basics", "Widgets & Layouts", "State Management", "Firebase Setup", "Authentication",
            "API Integration", "Data Storage", "Navigation", "Deployment"
        ]
    }

    if "goal_paths" not in user_data:
        st.subheader("✨ Choose Your Career Path")
        selected = st.multiselect("Select paths:", list(all_paths.keys()))
        if st.button("🚀 Generate Roadmaps") and selected:
            user_data["goal_paths"] = selected
            user_data["roadmaps"] = {}
            for path in selected:
                topics = all_paths[path]
                roadmap = {}
                for i in range(0, len(topics), 3):
                    week = f"Week {(i // 3) + 1}"
                    roadmap[week] = topics[i:i + 3]
                user_data["roadmaps"][path] = roadmap
            with open(data_path, "w") as f:
                json.dump(user_data, f, indent=2)
            st.rerun()

    elif "roadmaps" in user_data:
        updated = False
        completed_paths = []

        for path, roadmap in user_data["roadmaps"].items():
            st.subheader(f"📘 {path}")

            all_path_topics = [topic for topics in roadmap.values() for topic in topics]
            completed = user_data.get("completed", [])

            # Progress calculation
            done = sum(1 for topic in all_path_topics if topic in completed)
            total = len(all_path_topics)
            percent = int((done / total) * 100) if total else 0
            progress = percent / 100

            st.markdown(f"**Progress:** `{done}/{total}` topics completed — **{percent}%**")
            st.progress(progress)

            if percent == 100:
                st.success("🎉 You've completed this learning path!")
                completed_paths.append(path)

            # Topics checklist
            for week, topics in roadmap.items():
                with st.expander(week, expanded=True):
                    for topic in topics:
                        key = f"{path}_{week}_{topic}"
                        checked = topic in completed
                        new_checked = st.checkbox(topic, value=checked, key=key)
                        if new_checked != checked:
                            updated = True
                            if new_checked:
                                user_data["completed"].append(topic)
                            else:
                                user_data["completed"].remove(topic)

        # Save if user interacted
        if updated:
            with open(data_path, "w") as f:
                json.dump(user_data, f, indent=2)

        # Suggest new path if any was completed
        all_selected = set(user_data.get("goal_paths", []))
        all_available = set(all_paths.keys())
        remaining_paths = sorted(list(all_available - all_selected))

        if completed_paths and remaining_paths:
            st.subheader("🚀 Choose your next learning path")
            new_choices = st.multiselect("Available paths:", remaining_paths)
            if st.button("➕ Add Selected Paths") and new_choices:
                user_data["goal_paths"].extend(new_choices)
                for path in new_choices:
                    topics = all_paths[path]
                    roadmap = {}
                    for i in range(0, len(topics), 3):
                        week = f"Week {(i // 3) + 1}"
                        roadmap[week] = topics[i:i + 3]
                    user_data["roadmaps"][path] = roadmap
                with open(data_path, "w") as f:
                    json.dump(user_data, f, indent=2)
                st.success("New roadmap(s) added!")
                st.rerun()

        elif completed_paths and not remaining_paths:
            st.success("🏆 You've completed all available learning paths! You're a legend!")




# ------------------ LOGS ------------------ #
elif current_tab == "📒 Logs":
    st.header("📒 Your Logs")
    today = datetime.date.today().isoformat()
    entry = st.text_area("What did you learn today?", user_data["logs"].get(today, ""))
    if st.button("💾 Save Log"):
        user_data["logs"][today] = entry
        with open(data_path, "w") as f:
            json.dump(user_data, f, indent=2)
        st.success("Log saved!")
    for date in sorted(user_data["logs"].keys(), reverse=True):
        with st.expander(date):
            st.write(user_data["logs"][date])

# ------------------ MOTIVATION ------------------ #
elif current_tab == "🎯 Motivation":
    st.header("🎯 Your Motivation")
    st.success("🏅 You're doing amazing!")
    st.info("✅ Each small step gets you closer to your goal.")
    st.warning("💪 Stay consistent. Greatness builds daily.")

# ------------------ CALENDAR ------------------ #
elif current_tab == "📆 Calendar":
    st.header("📆 Calendar")
    if user_data["logs"]:
        df = pd.DataFrame({"date": list(user_data["logs"].keys()), "value": 1})
        df["date"] = pd.to_datetime(df["date"])
        df = df.groupby("date").sum()
        calplot.calplot(df["value"])
        st.pyplot(plt.gcf())
    else:
        st.info("Start logging to view your progress heatmap.")

# ------------------ CHATBOT ------------------ #
