import streamlit as st
from groq import Groq

# ============================== SECURE API CLIENT ==============================
client = None

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    client = None


# ============================== SMART FALLBACK ANSWER ==============================
def local_fallback_answer(question, missing_skills):

    question_lower = question.lower()
    context = ", ".join(missing_skills[:5]) if missing_skills else "general recruiter optimization"

    if "interview" in question_lower:
        return f"""
Interview readiness can be improved by focusing on your strongest resume areas and preparing quantified project explanations.

Recommended:
1. Prepare STAR format answers for projects and achievements.
2. Revise core technical concepts mentioned in your resume.
3. Practice recruiter HR questions plus role-specific scenarios.
4. Build confidence around problem-solving communication.
5. Keep examples ready for {context}.
"""

    elif "career" in question_lower or "roadmap" in question_lower:
        return f"""
For stronger career growth, focus on closing the current recruiter gap around {context}.

Recommended roadmap:
1. Add one advanced industry certification.
2. Build 2 to 3 measurable practical projects.
3. Improve LinkedIn and recruiter visibility.
4. Strengthen domain tools matching hiring demand.
5. Target roles aligned with your current strongest skills.
"""

    elif "ats" in question_lower or "score" in question_lower or "resume" in question_lower:
        return f"""
Your resume can be improved significantly around {context}.

Recommended ATS actions:
1. Add exact recruiter keywords from target job descriptions.
2. Include quantified achievements in each role.
3. Strengthen technical stack visibility.
4. Add certifications, deployments, and business impact.
5. Improve section formatting for ATS parsers.
"""

    else:
        return f"""
Based on the current recruiter analysis, profile strengthening is recommended around {context}.

Focus on:
1. stronger measurable achievements,
2. deeper technical keyword coverage,
3. recruiter visible certifications,
4. interview storytelling,
5. role aligned project presentation.
"""


# ============================== MAIN AI COACH ==============================
def ai_resume_coach(question, missing_skills=None, history=None):

    if missing_skills is None:
        missing_skills = []

    if history is None:
        history = []

    if client is None:
        return local_fallback_answer(question, missing_skills)

    context_skills = ", ".join(missing_skills[:10]) if missing_skills else "No major recruiter skill gap detected"

    system_prompt = f"""
You are ResumeIQ1 AI Career Coach, an enterprise recruiter consultant, ATS strategist, interview mentor, and career advisor.

Behavior rules:
1. Always answer specifically to the user's latest question.
2. Never repeat the same generic response.
3. If asked about resume -> provide resume optimization.
4. If asked about ATS score -> provide ATS improvement strategy.
5. If asked about interview -> provide interview preparation guidance.
6. If asked about career -> provide roadmap guidance.
7. If asked about technical growth -> provide upskilling advice.
8. Give practical recruiter-grade intelligent suggestions.
9. Keep responses concise but meaningful.

Current recruiter detected missing skills from screened resumes: {context_skills}

Answer in 5 to 10 professional lines.
"""

    messages = [{"role": "system", "content": system_prompt}]

    recent_history = history[-6:] if len(history) > 6 else history

    for sender, msg in recent_history:
        if sender == "user":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})

    messages.append({"role": "user", "content": question})

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.8
        )

        return chat_completion.choices[0].message.content

    except Exception:
        return local_fallback_answer(question, missing_skills)
