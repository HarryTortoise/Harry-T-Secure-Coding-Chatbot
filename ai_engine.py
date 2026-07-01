import os
import json
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
is_configured = False

if api_key and api_key != "your_actual_api_key_here":
    genai.configure(api_key=api_key)
    is_configured = True

def check_api_status() -> Dict[str, Any]:
    """Returns status check of the Gemini API configuration."""
    return {
        "configured": is_configured,
        "message": "Connected to Gemini API" if is_configured else "Gemini API key missing. Please paste your key in the .env file."
    }

def ask_tutor(message: str, history: List[Dict[str, str]], level: str, language: str, current_lesson: str) -> str:
    """Handles chat with the AI Tutor, providing tailored advice based on user profile."""
    if not is_configured:
        return "⚠️ Gemini API key is not configured. Please paste your key in the `.env` file and restart."

    try:
        system_instruction = (
            f"You are a friendly, encouraging, and highly knowledgeable Secure-Coding Tutor.\n"
            f"Your job is to teach the student about secure coding concepts, explain vulnerabilities, and guide them in coding.\n"
            f"Always adapt your tone, depth, and vocabulary to the user's details:\n"
            f"- Coder Skill Level: {level.upper()}\n"
            f"- Preferred Language: {language}\n"
            f"- Current Lesson Topic: {current_lesson}\n\n"
            f"Explain complex attacks with simple real-world analogies. Use side-by-side vulnerable vs secure "
            f"code comparisons to show changes. Keep explanations concise, clear, and focused on security."
        )

        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )

        # Reconstruct history in Gemini format
        formatted_history = []
        for msg in history[:-1]:  # Skip the last query which goes into send_message
            formatted_history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })

        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"Error communicating with AI Tutor: {str(e)}"

def generate_quiz(lesson_title: str, level: str, language: str, failed_topics: Optional[str] = None) -> Dict[str, Any]:
    """Generates a dynamic 5-question quiz for a lesson topic."""
    if not is_configured:
        return {"error": "Gemini API not configured"}

    try:
        # Define video context constraints to make quiz test concepts covered in the Computerphile lectures
        video_context = ""
        if "SQL" in lesson_title:
            video_context = "Integrate material from Computerphile's SQL Injection video (how single quotes break SQL strings, how comment characters -- negate parts of query logic, and prepared statements compilation)."
        elif "Cross Site" in lesson_title or "XSS" in lesson_title:
            video_context = "Integrate material from Computerphile's Cross-Site Scripting (XSS) video (how script execution tags steal session token cookies, reflected inputs vs database-stored injections, and output escaping rules)."
        elif "Authentication" in lesson_title or "Auth" in lesson_title:
            video_context = "Integrate material from Computerphile's salts/hashing video (using cryptographically secure random salts to prevent pre-calculated rainbow table matching, SHA/MD5 weakness, and bcrypt algorithms)."
        elif "Password" in lesson_title:
            video_context = "Integrate material from Computerphile's Password Security video (evaluating character length vs complex character set entropy, dictionary attack lists, brute force cracking speeds, and rate limits)."
        elif "Passkey" in lesson_title:
            video_context = "Integrate material from Computerphile's Passkeys video (how public/private key cryptographic challenge handshakes replace passwords, biometrics/PIN bindings, and domain validation protection)."

        prompt = (
            f"Create a 5-question multiple-choice quiz about '{lesson_title}' in {language} for a {level} coder.\n"
            f"Every question must test a secure coding concept, vulnerability signature, or proper defense.\n"
            f"{video_context}\n"
        )
        if failed_topics:
            prompt += (
                f"The user struggled with these topics previously: '{failed_topics}'. "
                f"Generate a FRESH set of 5 new questions specifically emphasizing these areas to test their understanding.\n"
            )

        prompt += (
            "Return the output STRICTLY as a JSON object matching this schema (do not wrap in markdown):\n"
            "{\n"
            "  \"questions\": [\n"
            "    {\n"
            "      \"question\": \"Question text here\",\n"
            "      \"code\": \"Optional code block illustrating the security issue, or empty string if not needed\",\n"
            "      \"options\": [\n"
            "        \"A) Option description\",\n"
            "        \"B) Option description\",\n"
            "        \"C) Option description\",\n"
            "        \"D) Option description\"\n"
            "      ],\n"
            "      \"correct_answer\": 0, // 0-based integer index of correct answer\n"
            "      \"explanation\": \"Detailed explanation of why the correct option is secure and why the others are vulnerable.\"\n"
            "    }\n"
            "  ]\n"
            "}"
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return {"error": f"Failed to generate quiz: {str(e)}"}

def evaluate_quiz_performance(lesson_title: str, level: str, language: str, score: float, quiz_data: List[Dict[str, Any]], user_answers: Dict[int, int]) -> str:
    """Evaluates user mistakes, explains corrections, and provides remedial study notes if score < 60%."""
    if not is_configured:
        return "⚠️ Gemini API key is not configured."

    try:
        wrong_count = 0
        mistakes_details = ""
        for i, q in enumerate(quiz_data):
            u_ans = user_answers.get(i)
            c_ans = q["correct_answer"]
            if u_ans != c_ans:
                wrong_count += 1
                mistakes_details += (
                    f"Question: {q['question']}\n"
                    f"Code: {q.get('code', 'None')}\n"
                    f"User's Choice: {q['options'][u_ans] if u_ans is not None else 'None'}\n"
                    f"Correct Choice: {q['options'][c_ans]}\n"
                    f"Correct Explanation: {q['explanation']}\n\n"
                )

        if wrong_count == 0:
            prompt = (
                f"The student scored 100% on a secure coding quiz about '{lesson_title}' ({level} level, {language}). "
                f"Write a short, motivating congratulatory note."
            )
        elif score >= 60.0:
            prompt = (
                f"The student scored {score}% (Passed, threshold is 60%) on a secure coding quiz about "
                f"'{lesson_title}' ({level} level, {language}).\n"
                f"Review the question(s) they got wrong and write a brief, helpful explanation explaining the "
                f"mistake and how it relates to secure coding:\n\n{mistakes_details}"
            )
        else:
            prompt = (
                f"The student scored {score}% (Failed, threshold is 60%) on a secure coding quiz about "
                f"'{lesson_title}' ({level} level, {language}). They need to review and retake a new quiz.\n"
                f"Analyze their mistakes:\n\n{mistakes_details}\n"
                f"Provide:\n"
                f"1. A friendly note letting them know they will try again.\n"
                f"2. A brief 1-paragraph Remedial Study Guide summarizing the exact rules they missed (e.g. escaping vs parameterization, least privilege, safe hashes) so they are prepared for the retake."
            )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during quiz evaluation: {str(e)}"

def check_code_security(code: str, language: str) -> str:
    """Analyzes a block of pasted code and returns secure coding grades, flaws, and safe rewrites."""
    if not is_configured:
        return "⚠️ Gemini API key is not configured. Please paste your key in the `.env` file."

    try:
        prompt = (
            f"Analyze the following {language} code snippet for security vulnerabilities (like OWASP Top 10, injections, leaks, flaws):\n\n"
            f"```\n{code}\n```\n\n"
            f"Provide a comprehensive analysis in Markdown. Include:\n"
            f"1. **Security Grade**: A single letter grade (A to F) based on safety, with a brief sentence rationale.\n"
            f"2. **Identified Flaws**: Bullet points explaining any weaknesses, risk severity, and how they could be exploited.\n"
            f"3. **Secure Refactored Code**: Write a fully secured rewrite of the code demonstrating best practices.\n"
            f"4. **Fix Explanations**: A summary of changes made and why they resolve the issues."
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error scanning code: {str(e)}"

def check_password_security(password: str) -> str:
    """Analyzes password strength, evaluates entropy, vulnerability to dictionaries, and provides feedback."""
    if not is_configured:
        return "⚠️ Gemini API key is not configured. Please paste your key in the `.env` file."

    try:
        prompt = (
            f"Analyze the security strength of the following password: '{password}'.\n"
            f"Perform a professional cybersecurity review. Output your response in Markdown, including:\n"
            f"1. **Security Level Rating**: A rating (Weak, Moderate, Strong, or Very Strong) with a quick summary of why.\n"
            f"2. **Analysis Details**: Address length, character complexity (upper/lower/numbers/symbols), predictability, dictionary words, and entropy.\n"
            f"3. **Attack Vulnerability**: Evaluate how this password would hold up against brute-force attacks, dictionary attacks, and credential stuffing.\n"
            f"4. **Suggestions**: Provide actionable improvements to make this password (or their general passphrase strategies) more secure."
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error checking password security: {str(e)}"
