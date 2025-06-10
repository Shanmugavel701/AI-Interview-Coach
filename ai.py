# ai_interview_coach.py
import streamlit as st
import time
import google.generativeai as genai

# -------------------------------
# CONFIGURATION
# -------------------------------
# Setup Gemini API
genai.configure(api_key="AIzaSyD-q5-mcoLn6Horgx-tPD_q4V5N_GV7uQE")
model = genai.GenerativeModel("gemini-2.0-flash")  # Use correct model name

# -------------------------------
# UTILITY FUNCTION
# -------------------------------
def call_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        return ""

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="AI Interview Coach", layout="wide")
st.title("🤖 AI Interview Coach")

with st.sidebar:
    st.header("Interview Configuration")
    job_role = st.text_input("Enter Your Role", "Software Engineer")
    experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=1)
    skills_input = st.text_area("Enter Your Skills (comma separated)", "Python, SQL, Communication")
    skills = [skill.strip() for skill in skills_input.split(",") if skill.strip()]
    start_button = st.button("Start Interview 🎤")

if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []

if start_button:
    st.session_state.questions.clear()
    st.session_state.answers.clear()
    st.success("Interview Started! Generating first question...")
    time.sleep(1)

    # Generate first question
    prompt = f"Act as an interviewer for a {job_role} position with {experience} years of experience. Ask a technical interview question based on skills: {', '.join(skills)}."
    question = call_gemini(prompt)
    st.session_state.questions.append(question)

if st.session_state.questions:
    st.subheader("🧠 Interview Simulation")
    current_question = st.session_state.questions[-1]
    st.markdown(f"**Q: {current_question}**")

    user_answer = st.text_area("Your Answer", height=200)
    submit_answer = st.button("Submit Answer")

    if submit_answer and user_answer:
        st.session_state.answers.append(user_answer)

        # Get feedback
        feedback_prompt = f"""Analyze this interview response:
Question: {current_question}
Answer: {user_answer}

Provide:
- Confidence Score (0-100)
- Tone Analysis (Professional, Confident, etc)
- Keyword Match % based on skills: {', '.join(skills)}
- Constructive Feedback
- Suggested Improvements"""
        feedback = call_gemini(feedback_prompt)

        st.markdown("---")
        st.subheader("📊 Feedback & Analysis")
        st.markdown(feedback)

        # Next Question
        next_question_prompt = f"Ask a follow-up interview question for a {job_role} with {experience} years of experience, based on skills: {', '.join(skills)}."
        next_question = call_gemini(next_question_prompt)
        st.session_state.questions.append(next_question)

# -------------------------------
# END
# -------------------------------
