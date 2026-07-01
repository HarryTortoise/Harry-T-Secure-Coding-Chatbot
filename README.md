# 🛡️ Interactive Secure-Coding Learning Platform

An interactive cybersecurity learning platform built in Python with **Streamlit** and powered by **Gemini 2.5 AI**. Learn, test, scan, and review secure-coding principles on SQL Injection, Cross-Site Scripting (XSS), Weak Authentication, Password Strength, and Passkeys.

## 🚀 Key Features

* **📚 Interactive Lessons**: Structured courses on 5 core security topics (SQLi, XSS, Weak Auth, Password Security, Passkeys).
* **🎯 Dynamic Language-Specific Tabs**: Select your programming language (Python, JavaScript, Java, C++) and see all code defenses dynamically update.
* **📺 Video Lectures**: Built-in YouTube tutorial embeds from Computerphile for structured study.
* **⏱️ Dynamic Locked Quizzes**: Lockout systems that enforce reading the study materials before taking quizzes.
* **🔑 Presentation Bypass**: Input a secret passcode (`1701`) in the sidebar to bypass lesson locks during live presentations.
* **🤖 AI Secure-Coding Tutor**: Renamable chatbot sessions with memory context to ask questions and discuss lessons.
* **🔍 Code Security Scanner**: Scan your codes for OWASP vulnerabilities and receive grade ratings and safe refactoring rewrites.
* **🔑 Password Security Reviewer**: Test entropy strength, dictionary predictability, and crack-time metrics.
* **☀️ Light & Dark Themes**: Toggle between Dark Mode 🌙 and Light Mode ☀️ with glowing blurred aurora backdrops.

---

## 🛠️ Setup Instructions

### 1. Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### 2. Install Dependencies
Clone this repository (or copy the files) into your folder, open your terminal, and run:
```cmd
pip install -r requirements.txt
```

### 3. Setup API Key
Create a `.env` file in the root directory and add your Google AI Studio API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> **Note**: The `.env` file is excluded from git commits by `.gitignore` to prevent leaking your private key.

### 4. Run the Application
Start the Streamlit server using:
```cmd
python -m streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.
