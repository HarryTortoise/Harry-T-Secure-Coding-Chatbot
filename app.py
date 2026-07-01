import streamlit as st
import time
import json
import os
import hashlib
import ai_engine as ai

# Set page config
st.set_page_config(
    page_title="Learn Secure-Coding Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load lessons database
lessons_file = os.path.join(os.path.dirname(__file__), "lessons.json")
try:
    with open(lessons_file, "r", encoding="utf-8") as f:
        lessons_data = json.load(f)
except Exception:
    lessons_data = []

# Helper function for dynamic password hashing
def hash_password(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

# User Account Database (Stored securely using SHA-256 Hashes)
USER_DB = {
    "Ryan Farber": "7e9539d1ff6e5e9ea14b101157a2bae67e4da7b2049f7aecc47a7ff7db4f0caf",
    "Harry Torres": "aeb2f12af743187f42d47c09eb0a832f066081373119e0fc366f1054cb9eef97",
    "Guest1": "01148711a694a7c9b6ed60e9bf2da2a8699db5895f73bcfc58ada7dd3ad1f3ab",
    "Guest2": "efeddc3a2c36da6355a5b655845bba8cfe82932091e08116236796ac7168d16d",
    "Guest3": "8e4574329a83a862910a51a12e4e14193a45c76488e44749ac08ff50fb03891a",
    "Guest4": "4b902f78357164244725b3e8b0db946d8fc1d452edc8394c8700fb12c40bb1e4",
    "Guest5": "5dd3d8454fc33a8d77696b45cae3f1980648e7f1c1aa139ec2343dcb9244ccd5",
    "Guest6": "e1bf4f7fcec5d14ea837fdbcb764d86b936fe5bb074ecbd79de654e58dc120c7",
    "Guest7": "4904e6ad8f36d4c82744d10813c66ba40c6128775f9162e8ee7bd343803a3a8d",
    "Guest8": "3a74d67db9d3643aa67912ea26f8c02dfb2d1168ae348e8c765fe3e74f26c915"
}

# --- Canva Glowing Purple/Blue Styling Overlay ---
def inject_spotify_css():
    theme = st.session_state.get("theme", "Dark Mode 🌙")
    if theme == "Light Mode ☀️":
        st.markdown("""
        <style>
        /* Light Theme Base Colors */
        .stApp {
            background-color: transparent !important;
            color: #121212;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            overflow-x: hidden;
        }
        
        /* Blurry Neon Aurora Spheres (Light Mode: Softer Pastels) */
        .aurora-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -2;
            overflow: hidden;
            pointer-events: none;
            background-color: #F5F4FA; /* Solid light base bg */
        }
        .glow-sphere {
            position: absolute;
            border-radius: 50%;
            filter: blur(120px);
            opacity: 0.6;
        }
        .sphere-1 {
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, #E1BEE7, #B39DDB);
            top: -100px;
            left: -100px;
        }
        .sphere-2 {
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, #C5CAE9, #9FA8DA);
            bottom: -150px;
            right: -100px;
        }
        
        /* Sidebar Navigation Styles */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid #E2E8F0;
            padding-top: 20px;
        }
        
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
            color: #8E2DE2 !important;
            font-weight: bold;
        }
        
        /* Custom Glowing Purple Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #8E2DE2, #4A00E0) !important;
            color: #FFFFFF !important;
            border-radius: 500px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(142, 45, 226, 0.3) !important;
        }
        
        div.stButton > button:first-child:hover {
            transform: scale(1.04) !important;
            box-shadow: 0 6px 20px rgba(142, 45, 226, 0.5) !important;
        }
        
        /* card styling for main panels */
        .spotify-card {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 8px;
            border: 1px solid #E8E7F5;
            margin-bottom: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        
        .spotify-card:hover {
            background-color: #FDFDFF;
        }
        
        /* Glowing vulnerable vs secure code blocks */
        .vulnerable-header {
            color: #FF5555;
            font-weight: bold;
            border-left: 4px solid #FF5555;
            padding-left: 8px;
            margin-top: 10px;
        }
        
        .secure-header {
            color: #8E2DE2;
            font-weight: bold;
            border-left: 4px solid #8E2DE2;
            padding-left: 8px;
            margin-top: 10px;
        }
        
        /* Timer styling */
        .timer-container {
            font-size: 24px;
            font-weight: bold;
            color: #8E2DE2;
            text-align: center;
            background-color: #FFFFFF;
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #8E2DE2;
            margin-bottom: 20px;
        }
        .timer-paused {
            color: #FF5555 !important;
            border-color: #FF5555 !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        /* Dark Theme Base Colors with purple radial glowing background simulation */
        .stApp {
            background-color: transparent !important;
            color: #FFFFFF;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            overflow-x: hidden;
        }
        
        /* Blurry Neon Aurora Spheres (Dark Mode: Cyberpunk Vibe) */
        .aurora-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -2;
            overflow: hidden;
            pointer-events: none;
            background-color: #080710; /* Solid dark base bg */
        }
        .glow-sphere {
            position: absolute;
            border-radius: 50%;
            filter: blur(130px);
            opacity: 0.55;
        }
        .sphere-1 {
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(142, 45, 226, 0.8), rgba(74, 0, 224, 0));
            top: -100px;
            left: -100px;
        }
        .sphere-2 {
            width: 550px;
            height: 550px;
            background: radial-gradient(circle, rgba(74, 0, 224, 0.85), rgba(142, 45, 226, 0));
            bottom: -150px;
            right: -100px;
        }
        
        /* Sidebar Navigation Styles */
        section[data-testid="stSidebar"] {
            background-color: #040308 !important;
            border-right: 1px solid #1c1535;
            padding-top: 20px;
        }
        
        section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
            color: #8E2DE2 !important;
            font-weight: bold;
        }
        
        /* Custom Glowing Purple Buttons */
        div.stButton > button:first-child {
            background: linear-gradient(135deg, #8E2DE2, #4A00E0) !important;
            color: #FFFFFF !important;
            border-radius: 500px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease !important;
            box-shadow: 0 4px 15px rgba(142, 45, 226, 0.4) !important;
        }
        
        div.stButton > button:first-child:hover {
            transform: scale(1.04) !important;
            box-shadow: 0 6px 22px rgba(142, 45, 226, 0.6) !important;
        }
        
        /* Glassmorphic card styling for main panels */
        .spotify-card {
            background-color: #12101f;
            padding: 24px;
            border-radius: 8px;
            border: 1px solid #231c42;
            margin-bottom: 20px;
            transition: background-color 0.3s ease;
        }
        
        .spotify-card:hover {
            background-color: #1a172e;
        }
        
        /* Tabs customization */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }
    
        .stTabs [data-baseweb="tab"] {
            background-color: #12101f !important;
            color: #b3b3c6 !important;
            border: 1px solid #231c42 !important;
            border-radius: 500px !important;
            padding: 6px 16px !important;
            font-weight: bold !important;
        }
    
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #8E2DE2, #4A00E0) !important;
            color: #FFFFFF !important;
            border-color: #8E2DE2 !important;
        }
        
        /* Glowing vulnerable vs secure code blocks */
        .vulnerable-header {
            color: #FF5555;
            font-weight: bold;
            border-left: 4px solid #FF5555;
            padding-left: 8px;
            margin-top: 10px;
        }
        
        .secure-header {
            color: #8E2DE2;
            font-weight: bold;
            border-left: 4px solid #8E2DE2;
            padding-left: 8px;
            margin-top: 10px;
        }
        
        /* Timer styling */
        .timer-container {
            font-size: 24px;
            font-weight: bold;
            color: #8E2DE2;
            text-align: center;
            background-color: #12101f;
            padding: 12px;
            border-radius: 8px;
            border: 2px solid #8E2DE2;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(142, 45, 226, 0.3);
        }
        .timer-paused {
            color: #FF5555 !important;
            border-color: #FF5555 !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Initialize Session States
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"
if "language" not in st.session_state:
    st.session_state["language"] = "Python"
if "level" not in st.session_state:
    st.session_state["level"] = "beginner"
if "completed_lessons" not in st.session_state:
    st.session_state["completed_lessons"] = []
if "quiz_states" not in st.session_state:
    st.session_state["quiz_states"] = {}

# Theme mode state
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark Mode 🌙"

# Visited tabs trackers
if "visited_tabs" not in st.session_state:
    st.session_state["visited_tabs"] = {}
if "current_tabs" not in st.session_state:
    st.session_state["current_tabs"] = {}

# Chat history state
if "chat_sessions" not in st.session_state:
    st.session_state["chat_sessions"] = {
        "Default Session": []
    }
if "active_session_name" not in st.session_state:
    st.session_state["active_session_name"] = "Default Session"

# Timer states
if "quiz_active" not in st.session_state:
    st.session_state["quiz_active"] = False
if "quiz_type" not in st.session_state:
    st.session_state["quiz_type"] = "" # "unit" or "final"
if "quiz_lesson_id" not in st.session_state:
    st.session_state["quiz_lesson_id"] = 0
if "quiz_time_limit" not in st.session_state:
    st.session_state["quiz_time_limit"] = 0
if "quiz_start_time" not in st.session_state:
    st.session_state["quiz_start_time"] = 0.0
if "quiz_paused" not in st.session_state:
    st.session_state["quiz_paused"] = False
if "quiz_paused_time_left" not in st.session_state:
    st.session_state["quiz_paused_time_left"] = 0.0
if "quiz_questions" not in st.session_state:
    st.session_state["quiz_questions"] = []
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = {}
if "quiz_eval_result" not in st.session_state:
    st.session_state["quiz_eval_result"] = None

# Inject CSS and render glowing blurry neon auroras globally
inject_spotify_css()
st.markdown("""
<div class="aurora-container">
    <div class="glow-sphere sphere-1"></div>
    <div class="glow-sphere sphere-2"></div>
</div>
""", unsafe_allow_html=True)

# --- Timer Mechanics Helper ---
def update_timer() -> Optional[float]:
    """Calculates remaining seconds, handles automatic timeouts, and returns seconds left."""
    if not st.session_state["quiz_active"]:
        return None
        
    if st.session_state["quiz_paused"]:
        return st.session_state["quiz_paused_time_left"]
        
    elapsed = time.time() - st.session_state["quiz_start_time"]
    left = st.session_state["quiz_time_limit"] - elapsed
    
    if left <= 0:
        # Time expired! Force submit quiz
        st.session_state["quiz_active"] = False
        st.session_state["quiz_paused"] = False
        submit_quiz(timeout=True)
        st.rerun()
        
    return left

def submit_quiz(timeout=False):
    """Submits answers and calls AI evaluation API."""
    st.session_state["quiz_active"] = False
    
    questions = st.session_state["quiz_questions"]
    user_answers = st.session_state["quiz_answers"]
    
    correct_count = 0
    evaluated_answers = []
    
    for i, q in enumerate(questions):
        u_ans = user_answers.get(i)
        c_ans = q["correct_answer"]
        is_correct = (u_ans == c_ans)
        if is_correct:
            correct_count += 1
            
        evaluated_answers.append({
            "question": q["question"],
            "code": q.get("code", ""),
            "user_answer": q["options"][u_ans] if u_ans is not None else "No Answer",
            "correct_answer": q["options"][c_ans],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })
        
    score = (correct_count / len(questions)) * 100.0
    
    # Generate AI feedback
    title = f"Lesson {st.session_state['quiz_lesson_id']}" if st.session_state["quiz_type"] == "unit" else "Final Exam"
    with st.spinner("AI is grading your responses and generating personalized study reviews..."):
        ai_review = ai.evaluate_quiz_performance(
            lesson_title=title,
            level=st.session_state["level"],
            language=st.session_state["language"],
            score=score,
            quiz_data=questions,
            user_answers=user_answers
        )
        
    # Save results
    result_data = {
        "score": score,
        "review": ai_review,
        "answers": evaluated_answers,
        "timeout": timeout
    }
    
    if st.session_state["quiz_type"] == "unit":
        st.session_state["quiz_states"][st.session_state["quiz_lesson_id"]] = result_data
        if score >= 60.0:
            if st.session_state["quiz_lesson_id"] not in st.session_state["completed_lessons"]:
                st.session_state["completed_lessons"].append(st.session_state["quiz_lesson_id"])
    else:
        st.session_state["final_exam_state"] = result_data

# --- LOGIN SCREEN ---
# --- CANVA STYLE LOGIN SCREEN ---
if not st.session_state["logged_in"]:
    # Run CSS Injection first to get correct backdrop colors
    inject_spotify_css()
    
    # Custom CSS for Login Page layout
    st.markdown("""
    <style>
    .login-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 40px;
        position: relative;
    }
    .login-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        font-family: 'Helvetica Neue', Helvetica, sans-serif;
    }
    .brand-triangle {
        color: #8E2DE2;
        font-size: 24px;
        font-weight: 900;
    }
    .brand-text {
        color: inherit;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .theme-selector-container {
        width: 150px;
    }
    .login-container {
        text-align: center;
        margin-top: 50px;
    }
    .welcome-text {
        font-size: 80px;
        font-weight: 900;
        color: inherit;
        text-shadow: 0 0 30px rgba(142, 45, 226, 0.5);
        margin-bottom: 5px;
        letter-spacing: -1.5px;
    }
    .login-sub {
        font-size: 22px;
        color: #B3B3C6;
        margin-bottom: 30px;
        font-weight: 400;
    }
    /* Style form boxes */
    div[data-testid="stForm"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(142, 45, 226, 0.25) !important;
        border-radius: 12px !important;
        padding: 30px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render Logo on Left and Theme Toggle on Right side of the top header
    col_brand, col_theme = st.columns([3, 1])
    with col_brand:
        st.markdown("""
        <div class="login-brand">
            <span class="brand-triangle">▲</span>
            <span class="brand-text">Learn Secure Coding</span>
        </div>
        """, unsafe_allow_html=True)
    with col_theme:
        st.session_state["theme"] = st.selectbox(
            "Theme Mode", 
            ["Dark Mode 🌙", "Light Mode ☀️"], 
            key="login_theme_selector",
            index=["Dark Mode 🌙", "Light Mode ☀️"].index(st.session_state.get("theme", "Dark Mode 🌙"))
        )
        # Rerun to switch backdrop colors immediately if changed
        if st.session_state.get("theme") != st.session_state.get("prev_theme", ""):
            st.session_state["prev_theme"] = st.session_state["theme"]
            st.rerun()
    
    # Welcome & Login Headings in the Center
    st.markdown("""
    <div class="login-container">
        <h1 class="welcome-text">Welcome</h1>
        <div class="login-sub">Login</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Username")
            password = st.text_input("Password", type="password", placeholder="Password")
            submitted = st.form_submit_button("Log In")
            
            if submitted:
                if username in USER_DB and USER_DB[username] == hash_password(password):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.success("Successfully logged in!")
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
    st.stop()

# --- SIDEBAR & NAVIGATION ---
with st.sidebar:
    # Theme Mode Selector
    st.session_state["theme"] = st.selectbox(
        "Theme Mode", 
        ["Dark Mode 🌙", "Light Mode ☀️"], 
        index=["Dark Mode 🌙", "Light Mode ☀️"].index(st.session_state.get("theme", "Dark Mode 🌙"))
    )
    
    st.markdown(f"### Welcome, {st.session_state['username']}")
    st.write(f"Lang: `{st.session_state['language']}`")
    
    # Secret Bypass
    bypass_input = st.text_input("Unlock Bypass (Key)", type="password")
    if bypass_input == "1701":
        st.session_state["bypass_active"] = True
    else:
        st.session_state["bypass_active"] = False
        
    st.markdown("---")
    
    # Active quiz indicator
    if st.session_state["quiz_active"]:
        st.markdown("<div style='background-color:#FF5555; padding:8px; border-radius:4px; text-align:center; font-weight:bold; color:white;'>⚠️ EXAM IN PROGRESS</div>", unsafe_allow_html=True)
        st.write("Navigation options are locked until the test is completed or paused.")
        st.markdown("---")
        
    # Navigation choices
    nav_options = ["Home", "📚 Lessons", "🤖 AI Tutor", "🔍 Coding Checker", "🔑 Password Checker"]
    
    # Enable Lockout on AI Tutor during quiz
    selected_page = st.session_state["selected_page"]
    
    for opt in nav_options:
        disabled = False
        if st.session_state["quiz_active"] and opt == "🤖 AI Tutor":
            disabled = True
            btn_label = f"🤖 AI Tutor (🔒 Locked)"
        else:
            btn_label = opt
            
        if st.sidebar.button(btn_label, disabled=disabled, use_container_width=True):
            st.session_state["selected_page"] = opt
            st.rerun()
            
    st.markdown("---")
    if st.button("Log Out", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- SCREEN CONTROLLERS ---

# 1. HOME SCREEN
if st.session_state["selected_page"] == "Home":
    st.markdown("<h1 style='color: #8E2DE2;'>Welcome to the Learn Secure-Coding Platform</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='spotify-card'>
        <h3>Get Ready to Learn Secure Coding</h3>
        <p>This interactive platform uses <b>Gemini AI</b> to guide you through security vulnerabilities and teach you secure coding practices. Here's what you can do:</p>
        <ul>
            <li><b>📚 Lessons</b>: Complete 5 core units on SQLi, XSS, Weak Auth, Password Security, and Passkeys.</li>
            <li><b>🤖 AI Tutor</b>: Ask questions and get customized explanations for any topic.</li>
            <li><b>🔍 Coding Checker</b>: Paste your code to scan for security weaknesses and refactor safely.</li>
            <li><b>🔑 Password Checker</b>: Test password strengths and learn mitigation tactics.</li>
        </ul>
        <p>Before you start, customize your settings below:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["language"] = st.selectbox(
            "Target Programming Language",
            ["Python", "JavaScript", "Java", "C++"],
            index=["Python", "JavaScript", "Java", "C++"].index(st.session_state["language"])
        )
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Lessons 🚀"):
        st.session_state["selected_page"] = "📚 Lessons"
        st.rerun()

# 2. LESSONS DIRECTORY & VIEWER
elif st.session_state["selected_page"] == "📚 Lessons":
    st.markdown("<h1 style='color: #8E2DE2;'>📚 Course Lessons</h1>", unsafe_allow_html=True)
    
    # Check if a quiz is currently running
    if st.session_state["quiz_active"]:
        st.warning("You are currently taking a quiz. Finish or pause the quiz to view the lesson content.")
        
        # RENDER QUIZ BLOCK HERE
        left_time = update_timer()
        if left_time is not None:
            timer_class = "timer-container timer-paused" if st.session_state["quiz_paused"] else "timer-container"
            mins = int(left_time // 60)
            secs = int(left_time % 60)
            st.markdown(f"<div class='{timer_class}'>⏱️ Time Remaining: {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)
            
            col_p, col_r = st.columns(2)
            with col_p:
                if st.session_state["quiz_paused"]:
                    if st.button("Resume Exam", use_container_width=True):
                        st.session_state["quiz_paused"] = False
                        st.session_state["quiz_start_time"] = time.time()
                        st.session_state["quiz_time_limit"] = st.session_state["quiz_paused_time_left"]
                        st.rerun()
                else:
                    if st.button("Pause Exam", use_container_width=True):
                        st.session_state["quiz_paused"] = True
                        st.session_state["quiz_paused_time_left"] = left_time
                        st.rerun()
            
            if st.session_state["quiz_paused"]:
                st.info("Quiz is paused. Question input has been locked.")
            else:
                # Render active quiz questions
                with st.form("quiz_questions_form"):
                    for idx, q in enumerate(st.session_state["quiz_questions"]):
                        st.write(f"**Question {idx+1}:** {q['question']}")
                        if q.get("code"):
                            st.code(q["code"], language=st.session_state["language"].lower())
                        
                        st.session_state["quiz_answers"][idx] = st.radio(
                            "Select your answer:",
                            q["options"],
                            key=f"q_{idx}",
                            index=None
                        )
                        st.write("---")
                    
                    if st.form_submit_button("Submit Exam"):
                        submit_quiz()
                        st.rerun()
        st.stop()
        
    # Check if a quiz was just submitted and we need to display results
    if "quiz_lesson_id" in st.session_state and st.session_state["quiz_lesson_id"] in st.session_state["quiz_states"]:
        result = st.session_state["quiz_states"][st.session_state["quiz_lesson_id"]]
        
        st.markdown(f"<div class='spotify-card'>", unsafe_allow_html=True)
        score = result["score"]
        if score >= 60.0:
            st.success(f"🎉 PASSED! You scored {score}%")
        else:
            st.error(f"❌ TRY AGAIN! You scored {score}% (Passing score is 60%)")
            
        st.markdown("### AI Review & Remedial Study Guide")
        st.markdown(result["review"])
        
        st.markdown("### Question Breakdown")
        for idx, ans in enumerate(result["answers"]):
            is_correct = ans["is_correct"]
            st.markdown(f"**Question {idx+1}:** {ans['question']}")
            if ans.get("code"):
                st.code(ans["code"])
            st.write(f"Your Answer: {'🟢' if is_correct else '🔴'} {ans['user_answer']}")
            if not is_correct:
                st.write(f"Correct Answer: 🟢 {ans['correct_answer']}")
            st.info(f"Explanation: {ans['explanation']}")
            st.write("---")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        col_c, col_r = st.columns(2)
        with col_c:
            if st.button("Close Review"):
                # Reset quiz history view state
                del st.session_state["quiz_lesson_id"]
                st.rerun()
        with col_r:
            if score < 60.0:
                if st.button("Retake Quiz 🔄"):
                    # Generate a fresh quiz
                    lesson_id = st.session_state["quiz_lesson_id"]
                    lesson_title = next(l["title"] for l in lessons_data if l["id"] == lesson_id)
                    with st.spinner("AI is generating a fresh quiz with new questions..."):
                        quiz_data = ai.generate_quiz(
                            lesson_title=lesson_title,
                            level=st.session_state["level"],
                            language=st.session_state["language"],
                            failed_topics="Prior failed concepts"
                        )
                    if "error" not in quiz_data:
                        st.session_state["quiz_active"] = True
                        st.session_state["quiz_type"] = "unit"
                        st.session_state["quiz_time_limit"] = 40 * 60  # 40 mins
                        st.session_state["quiz_start_time"] = time.time()
                        st.session_state["quiz_paused"] = False
                        st.session_state["quiz_questions"] = quiz_data["questions"]
                        st.session_state["quiz_answers"] = {}
                        st.rerun()
        st.stop()
        
    # Main lessons directory list
    if not lessons_data:
        st.info("Lessons database is currently empty.")
    else:
        # Side-by-side lessons view
        lesson_names = [f"{l['id']}. {l['title']}" for l in lessons_data]
        selected_lesson_name = st.selectbox("Choose a Lesson:", lesson_names)
        
        selected_id = int(selected_lesson_name.split(".")[0])
        lesson = next(l for l in lessons_data if l["id"] == selected_id)
        
        st.markdown(f"## {lesson['title']}")
        st.caption(f"Category: {lesson['category']} | Status: {'🟢 Completed' if selected_id in st.session_state['completed_lessons'] else '🟡 Unstarted'}")
        
        # Dynamic button tabs to track visited history
        tabs = list(lesson["tabs"].keys())
        if "video_url" in lesson:
            tabs.append("📺 Video Lecture")
            
        lang = st.session_state["language"]
        lang_tab_title = f"🎯 {lang} Examples"
        if "language_examples" in lesson and lang in lesson["language_examples"]:
            tabs.append(lang_tab_title)
        
        if lesson["id"] not in st.session_state["visited_tabs"]:
            st.session_state["visited_tabs"][lesson["id"]] = set()
        if lesson["id"] not in st.session_state["current_tabs"]:
            st.session_state["current_tabs"][lesson["id"]] = tabs[0]
            
        col_tabs = st.columns(len(tabs))
        for idx, tab_name in enumerate(tabs):
            is_active = (tab_name == st.session_state["current_tabs"][lesson["id"]])
            
            # Label prefix shows if tab was visited
            was_visited = tab_name in st.session_state["visited_tabs"][lesson["id"]]
            label = f"🟢 {tab_name}" if was_visited else tab_name
            
            # Select active tab and mark visited
            if col_tabs[idx].button(label, key=f"btn_tab_{lesson['id']}_{tab_name}", use_container_width=True):
                st.session_state["current_tabs"][lesson["id"]] = tab_name
                st.session_state["visited_tabs"][lesson["id"]].add(tab_name)
                st.rerun()
                
        # Mark active tab as visited on first load too
        st.session_state["visited_tabs"][lesson["id"]].add(st.session_state["current_tabs"][lesson["id"]])
        
        # Render Active Tab
        active_tab = st.session_state["current_tabs"][lesson["id"]]
        st.markdown("<div class='spotify-card'>", unsafe_allow_html=True)
        if active_tab == "📺 Video Lecture" and "video_url" in lesson:
            st.markdown("### 📺 Video Lecture")
            st.write("Watch this video tutorial from Computerphile to learn more about the concepts covered in this lesson:")
            st.video(lesson["video_url"])
        elif active_tab == lang_tab_title:
            st.markdown(lesson["language_examples"][lang])
        else:
            st.markdown(lesson["tabs"][active_tab])
            
            # Dynamically inject code defense comparison blocks based on active language
            if active_tab == "Code Defense" and "code_defense" in lesson:
                st.markdown("<h4 class='secure-header'>Code Comparison Details</h4>", unsafe_allow_html=True)
                st.markdown(lesson["code_defense"][lang])
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enforce Reading or 1701 bypass
        is_unlocked = (len(st.session_state["visited_tabs"][lesson["id"]]) == len(tabs)) or st.session_state.get("bypass_active", False)
        
        if not is_unlocked:
            st.warning(f"🔒 Read all sections of the lesson tabs above to unlock the quiz (Progress: {len(st.session_state['visited_tabs'][lesson['id']])}/{len(tabs)})")
        else:
            st.success("🔓 Lesson completed! The quiz is unlocked.")
            
            # Experience-level selection right before the quiz
            exp_choice = st.selectbox(
                f"How experienced are you with {lesson['title']} before taking the quiz?",
                [
                    "I've never learned this before",
                    "I've seen it before, but don't know it well",
                    "I've seen it and done it before, but not that good at it",
                    "I am experienced with it"
                ]
            )
            
            # Map choice to difficulty levels
            level_map = {
                "I've never learned this before": "beginner",
                "I've seen it before, but don't know it well": "intermediate",
                "I've seen it and done it before, but not that good at it": "intermediate",
                "I am experienced with it": "advanced"
            }
            
            # Take Quiz Action Button
            if st.button("Start Timer & Quiz 📝"):
                selected_level = level_map[exp_choice]
                st.session_state["level"] = selected_level
                
                with st.spinner("AI is generating your secure-coding quiz..."):
                    quiz_data = ai.generate_quiz(
                        lesson_title=lesson["title"],
                        level=selected_level,
                        language=st.session_state["language"]
                    )
                if "questions" in quiz_data:
                    st.session_state["quiz_active"] = True
                    st.session_state["quiz_type"] = "unit"
                    st.session_state["quiz_lesson_id"] = selected_id
                    st.session_state["quiz_time_limit"] = 40 * 60  # 40 mins
                    st.session_state["quiz_start_time"] = time.time()
                    st.session_state["quiz_paused"] = False
                    st.session_state["quiz_questions"] = quiz_data["questions"]
                    st.session_state["quiz_answers"] = {}
                    st.rerun()
                else:
                    st.error("Failed to generate quiz. Check your API configuration status.")

# 3. AI TUTOR CHATBOT
elif st.session_state["selected_page"] == "🤖 AI Tutor":
    st.markdown("<h1 style='color: #8E2DE2;'>🤖 AI Secure-Coding Tutor</h1>", unsafe_allow_html=True)
    
    # Check if API configured
    api_status = ai.check_api_status()
    if not api_status["configured"]:
        st.warning(api_status["message"])
        st.stop()
        
    # Ensure session dict is initialized
    if "chat_sessions" not in st.session_state:
        st.session_state["chat_sessions"] = {"Default Session": []}
    if "active_session_name" not in st.session_state:
        st.session_state["active_session_name"] = "Default Session"
        
    col_sessions, col_chat = st.columns([1, 3])
    
    with col_sessions:
        st.markdown("### 🗃️ Chat Memory")
        
        # New Chat / Clear Screen Button
        if st.button("➕ New Chat / Clear", use_container_width=True):
            new_session_id = len(st.session_state["chat_sessions"]) + 1
            new_session_name = f"Session {new_session_id}"
            st.session_state["chat_sessions"][new_session_name] = []
            st.session_state["active_session_name"] = new_session_name
            st.rerun()
            
        st.markdown("---")
        
        # List and select existing sessions
        for session_name in list(st.session_state["chat_sessions"].keys()):
            is_active = (session_name == st.session_state["active_session_name"])
            
            col_btn, col_del = st.columns([4, 1])
            with col_btn:
                # Custom label for active chat session
                label = f"🟢 {session_name}" if is_active else f"💬 {session_name}"
                if st.button(label, key=f"session_btn_{session_name}", use_container_width=True):
                    st.session_state["active_session_name"] = session_name
                    st.rerun()
            with col_del:
                if st.button("🗑️", key=f"del_session_{session_name}", use_container_width=True):
                    if len(st.session_state["chat_sessions"]) > 1:
                        del st.session_state["chat_sessions"][session_name]
                        if is_active:
                            st.session_state["active_session_name"] = list(st.session_state["chat_sessions"].keys())[0]
                        st.rerun()
                    else:
                        st.warning("Keep at least one active chat session.")
                        
    with col_chat:
        active_session = st.session_state["active_session_name"]
        
        # Rename Chat Session
        new_name = st.text_input("💬 Active Session Name (Click to Edit):", value=active_session, key=f"rename_tutor_{active_session}")
        if new_name != active_session and new_name.strip() != "":
            if new_name in st.session_state["chat_sessions"]:
                st.error("Session name already exists!")
            else:
                st.session_state["chat_sessions"][new_name] = st.session_state["chat_sessions"].pop(active_session)
                st.session_state["active_session_name"] = new_name
                st.rerun()
                
        st.write("Ask your tutor secure-coding questions. All messages in this session are remembered.")
        
        history = st.session_state["chat_sessions"][active_session]
        
        # Render active session chat messages
        for msg in history:
            role = "Student" if msg["role"] == "user" else "Tutor"
            style = "background-color: #1a172e;" if msg["role"] == "user" else "background-color: #0b0914; border: 1px solid #8E2DE2;"
            st.markdown(f"""
            <div style='padding: 12px; border-radius: 8px; margin-bottom: 8px; {style}'>
                <b>{role}:</b><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True)
            
        # Chat input form
        with st.form("chat_form", clear_on_submit=True):
            chat_msg = st.text_input("Ask a question:")
            submitted = st.form_submit_button("Send")
            
            if submitted and chat_msg.strip():
                # Append user query
                st.session_state["chat_sessions"][active_session].append({"role": "user", "content": chat_msg})
                
                # Fetch AI response using active session's history
                with st.spinner("Tutor is thinking..."):
                    current_topic = f"Lesson {st.session_state['quiz_lesson_id']}" if st.session_state.get("quiz_lesson_id") else "General Security"
                    response = ai.ask_tutor(
                        message=chat_msg,
                        history=st.session_state["chat_sessions"][active_session],
                        level=st.session_state["level"],
                        language=st.session_state["language"],
                        current_lesson=current_topic
                    )
                st.session_state["chat_sessions"][active_session].append({"role": "model", "content": response})
                st.rerun()

# 4. CODING CHECKER
elif st.session_state["selected_page"] == "🔍 Coding Checker":
    st.markdown("<h1 style='color: #8E2DE2;'>🔍 Code Security Scanner</h1>", unsafe_allow_html=True)
    
    api_status = ai.check_api_status()
    if not api_status["configured"]:
        st.warning(api_status["message"])
        st.stop()
        
    # Ensure variables initialized
    if "code_sessions" not in st.session_state:
        st.session_state["code_sessions"] = {"Scan 1": {"code": "", "lang": "Python", "result": ""}}
    if "active_code_session" not in st.session_state:
        st.session_state["active_code_session"] = "Scan 1"
        
    col_sessions, col_main = st.columns([1, 3])
    
    with col_sessions:
        st.markdown("### 🗃️ Scan Memory")
        if st.button("➕ New Scan / Clear", key="new_code_scan", use_container_width=True):
            new_id = len(st.session_state["code_sessions"]) + 1
            new_name = f"Scan {new_id}"
            st.session_state["code_sessions"][new_name] = {"code": "", "lang": "Python", "result": ""}
            st.session_state["active_code_session"] = new_name
            st.rerun()
            
        st.markdown("---")
        
        for s_name in list(st.session_state["code_sessions"].keys()):
            is_active = (s_name == st.session_state["active_code_session"])
            
            c_btn, c_del = st.columns([4, 1])
            with c_btn:
                label = f"🟢 {s_name}" if is_active else f"🔍 {s_name}"
                if st.button(label, key=f"code_btn_{s_name}", use_container_width=True):
                    st.session_state["active_code_session"] = s_name
                    st.rerun()
            with c_del:
                if st.button("🗑️", key=f"del_code_{s_name}", use_container_width=True):
                    if len(st.session_state["code_sessions"]) > 1:
                        del st.session_state["code_sessions"][s_name]
                        if is_active:
                            st.session_state["active_code_session"] = list(st.session_state["code_sessions"].keys())[0]
                        st.rerun()
                    else:
                        st.warning("Keep at least one active scan.")
                        
    with col_main:
        active_scan = st.session_state["active_code_session"]
        scan_data = st.session_state["code_sessions"][active_scan]
        
        # Rename Scan Session
        new_scan_name = st.text_input("🔍 Active Scan Name (Click to Edit):", value=active_scan, key=f"rename_code_{active_scan}")
        if new_scan_name != active_scan and new_scan_name.strip() != "":
            if new_scan_name in st.session_state["code_sessions"]:
                st.error("Scan name already exists!")
            else:
                st.session_state["code_sessions"][new_scan_name] = st.session_state["code_sessions"].pop(active_scan)
                st.session_state["active_code_session"] = new_scan_name
                st.rerun()
        st.write("Paste your code snippet below. Gemini AI will scan it for flaws, grade the security, and write a secured refactored version.")
        
        code_input = st.text_area("Paste your code here:", value=scan_data["code"], height=200, placeholder="# Write or paste code to scan...")
        
        langs = ["Python", "JavaScript", "Java", "C++"]
        lang_idx = langs.index(scan_data["lang"]) if scan_data["lang"] in langs else 0
        scan_lang = st.selectbox("Select Language:", langs, index=lang_idx)
        
        if st.button("Scan Code 🔍", key="scan_btn_trigger"):
            if code_input.strip() == "":
                st.warning("Please paste some code to check.")
            else:
                # Update input cache
                st.session_state["code_sessions"][active_scan]["code"] = code_input
                st.session_state["code_sessions"][active_scan]["lang"] = scan_lang
                
                with st.spinner("AI is analyzing code patterns for vulnerabilities..."):
                    analysis = ai.check_code_security(code_input, scan_lang)
                    
                st.session_state["code_sessions"][active_scan]["result"] = analysis
                st.rerun()
                
        # Render scan result if exists
        if scan_data["result"]:
            st.markdown("### AI Code Security Analysis")
            st.markdown(scan_data["result"])

# 5. PASSWORD CHECKER
elif st.session_state["selected_page"] == "🔑 Password Checker":
    st.markdown("<h1 style='color: #8E2DE2;'>🔑 Password Security Reviewer</h1>", unsafe_allow_html=True)
    
    api_status = ai.check_api_status()
    if not api_status["configured"]:
        st.warning(api_status["message"])
        st.stop()
        
    # Ensure variables initialized
    if "password_sessions" not in st.session_state:
        st.session_state["password_sessions"] = {"Check 1": {"password": "", "result": ""}}
    if "active_password_session" not in st.session_state:
        st.session_state["active_password_session"] = "Check 1"
        
    col_sessions, col_main = st.columns([1, 3])
    
    with col_sessions:
        st.markdown("### 🗃️ Check Memory")
        if st.button("➕ New Check / Clear", key="new_password_check", use_container_width=True):
            new_id = len(st.session_state["password_sessions"]) + 1
            new_name = f"Check {new_id}"
            st.session_state["password_sessions"][new_name] = {"password": "", "result": ""}
            st.session_state["active_password_session"] = new_name
            st.rerun()
            
        st.markdown("---")
        
        for s_name in list(st.session_state["password_sessions"].keys()):
            is_active = (s_name == st.session_state["active_password_session"])
            
            c_btn, c_del = st.columns([4, 1])
            with c_btn:
                label = f"🟢 {s_name}" if is_active else f"🔑 {s_name}"
                if st.button(label, key=f"pass_btn_{s_name}", use_container_width=True):
                    st.session_state["active_password_session"] = s_name
                    st.rerun()
            with c_del:
                if st.button("🗑️", key=f"del_pass_{s_name}", use_container_width=True):
                    if len(st.session_state["password_sessions"]) > 1:
                        del st.session_state["password_sessions"][s_name]
                        if is_active:
                            st.session_state["active_password_session"] = list(st.session_state["password_sessions"].keys())[0]
                        st.rerun()
                    else:
                        st.warning("Keep at least one active check.")
                        
    with col_main:
        active_check = st.session_state["active_password_session"]
        check_data = st.session_state["password_sessions"][active_check]
        
        # Rename Check Session
        new_check_name = st.text_input("🔑 Active Check Name (Click to Edit):", value=active_check, key=f"rename_pass_{active_check}")
        if new_check_name != active_check and new_check_name.strip() != "":
            if new_check_name in st.session_state["password_sessions"]:
                st.error("Check name already exists!")
            else:
                st.session_state["password_sessions"][new_check_name] = st.session_state["password_sessions"].pop(active_check)
                st.session_state["active_password_session"] = new_check_name
                st.rerun()
        st.write("Enter a password below to test its strength. Gemini AI will evaluate it against dictionary attacks, cracking times, and details entropy.")
        
        pass_input = st.text_input("Enter Password to Test:", value=check_data["password"], type="password")
        
        if st.button("Evaluate Password 🔑", key="eval_btn_trigger"):
            if pass_input.strip() == "":
                st.warning("Please enter a password to evaluate.")
            else:
                # Update input cache
                st.session_state["password_sessions"][active_check]["password"] = pass_input
                
                with st.spinner("AI is evaluating password complexity and entropy rules..."):
                    analysis = ai.check_password_security(pass_input)
                    
                st.session_state["password_sessions"][active_check]["result"] = analysis
                st.rerun()
                
        # Render check result if exists
        if check_data["result"]:
            st.markdown("### Password Security Report")
            st.markdown(check_data["result"])
