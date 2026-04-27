from groq import Groq

# ============================== API CLIENT ==============================
GROQ_API_KEY = "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"

client = None

try:
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
except:
    client = None


# ============================== FALLBACK ANSWER ==============================
def local_fallback_answer(question, missing_skills):

    context = ", ".join(missing_skills[:5]) if missing_skills else "general resume optimization"

    return f"""
Based on the current resume screening, the profile can be improved around {context}.

Recommended next actions:
1. Add stronger measurable achievements in previous roles/projects.
2. Improve ATS keywords exactly matching recruiter job descriptions.
3. Highlight certifications, tools, and deployment exposure.
4. Add more quantified business impact and technical accomplishments.
5. Prepare interview examples around your strongest technical skills.

You can also ask about interview preparation, resume rewriting, or career roadmap.
"""


# ============================== MAIN AI COACH ==============================
def ai_resume_coach(question, missing_skills, history=None):

    if history is None:
        history = []

    if client is None:
        return local_fallback_answer(question, missing_skills)

    context_skills = ", ".join(missing_skills[:10]) if missing_skills else "No major missing skills detected"

    system_prompt = f"""
You are ResumeIQ1 AI Career Coach, an advanced recruiter-grade resume consultant and hiring mentor.

Your responsibilities:
- improve ATS resume quality
- suggest recruiter friendly resume optimization
- provide interview preparation help
- provide upskilling roadmap
- answer career guidance professionally
- provide practical and detailed hiring advice

Current missing skills detected in candidate resume: {context_skills}

Always answer in:
- professional recruiter tone
- practical actionable style
- 5 to 10 lines
- clear bullet points when needed
"""

    messages = [{"role": "system", "content": system_prompt}]

    for sender, msg in history[-8:]:
        if sender == "user":
            messages.append({"role": "user", "content": msg})
        else:
            messages.append({"role": "assistant", "content": msg})

    messages.append({"role": "user", "content": question})

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5
        )

        return chat_completion.choices[0].message.content

    except:
        return local_fallback_answer(question, missing_skills)
