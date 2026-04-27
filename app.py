import streamlit as st
import pandas as pd
import plotly.express as px

from auth import login
from utils import (
    extract_text, clean_text, get_similarity_advanced,
    get_skill_analysis, generate_suggestions,
    weighted_score, init_db, save_result,
    get_history, generate_pdf_report,
    build_candidate_profile
)
from chatbot import ai_resume_coach

st.set_page_config(page_title="ResumeIQ1", layout="wide", initial_sidebar_state="collapsed")

init_db()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "all_results" not in st.session_state:
    st.session_state.all_results = []

# ================= LOGIN =================
if not st.session_state.logged_in:
    login()
    st.stop()

# ================= DASHBOARD CSS =================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}

.stApp{
    background:#edf2f7;
}

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:1400px;
}

.main-header{
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
    padding:25px;
    border-radius:20px;
    margin-bottom:20px;
}

.header-title{
    font-size:34px;
    font-weight:800;
}

.header-sub{
    font-size:14px;
    color:#cbd5e1;
}

.user-box{
    text-align:right;
    color:white;
    font-weight:600;
    margin-top:10px;
}

.kpi-card{
    background:linear-gradient(135deg,#111827,#1e293b);
    color:white;
    padding:22px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 4px 14px rgba(0,0,0,0.10);
    min-height:130px;
}

.top-card{
    background:linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
    padding:24px;
    border-radius:18px;
    margin-top:20px;
    margin-bottom:25px;
}

.section-box{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
    margin-bottom:20px;
}

.profile-card{
    background:white;
    padding:20px;
    border-radius:18px;
    box-shadow:0 2px 10px rgba(0,0,0,0.05);
    margin-bottom:15px;
}

.rank-card{
    background:white;
    padding:18px;
    border-radius:16px;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
    margin-bottom:12px;
}

.chat-user{
    background:#dbeafe;
    padding:12px;
    border-radius:12px;
    margin-bottom:10px;
}

.chat-ai{
    background:#111827;
    color:white;
    padding:12px;
    border-radius:12px;
    margin-bottom:10px;
}

.stButton>button{
    background:#0f172a;
    color:white;
    border:none;
    border-radius:12px;
    padding:10px 24px;
    font-weight:700;
}

.stTextInput>div>div>input,
.stTextArea textarea{
    border-radius:12px;
    border:1px solid #dbe2ea;
}

section[data-testid="stFileUploader"]{
    background:white;
    padding:15px;
    border-radius:16px;
    border:1px solid #dbe2ea;
}

div[role="radiogroup"]{
    display:flex;
    justify-content:center;
    gap:30px;
    background:white;
    padding:14px;
    border-radius:16px;
    margin-bottom:25px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER WITH LOGOUT =================
h1, h2 = st.columns([6,1])

with h1:
    st.markdown(f"""
    <div class='main-header'>
        <div class='header-title'>ResumeIQ1</div>
        <div class='header-sub'>Enterprise AI Resume Screening • Recruiter Hiring Dashboard • AI Career Coach</div>
        <div class='user-box'>Logged in as: {st.session_state.user}</div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.write("")
    st.write("")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.session_state.chat_history = []
        st.session_state.all_results = []
        st.rerun()

# ================= MENU =================
page = st.radio("", ["🏠 ATS Dashboard", "📚 Screening Logs", "🤖 AI Career Coach"], horizontal=True)

# ================= DASHBOARD =================
if page == "🏠 ATS Dashboard":

    st.markdown("<div class='section-box'><h3>📄 Candidate Resume Screening Workspace</h3></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        resumes = st.file_uploader("Upload Candidate Resumes", type=["pdf", "docx"], accept_multiple_files=True)

    with c2:
        job_desc = st.text_area("Paste Recruiter Job Description", height=220)

    if st.button("🚀 Run Enterprise ATS Screening"):

        if resumes and job_desc:

            st.session_state.all_results = []
            prog = st.progress(0)

            for idx, file in enumerate(resumes):

                raw_text = extract_text(file)
                cleaned_resume = clean_text(raw_text)
                cleaned_jd = clean_text(job_desc)

                profile = build_candidate_profile(raw_text)
                base_score = get_similarity_advanced(cleaned_resume, cleaned_jd)
                matched, missing = get_skill_analysis(cleaned_resume, cleaned_jd)
                final_score = weighted_score(base_score, matched.keys(), cleaned_resume)

                save_result(profile["name"], final_score)
                st.session_state.all_results.append((profile, final_score, matched, missing))

                prog.progress(int(((idx+1)/len(resumes))*100))

            st.success("ATS Screening Completed Successfully")

    if st.session_state.all_results:

        ranked = sorted(st.session_state.all_results, key=lambda x: x[1], reverse=True)

        total = len(ranked)
        avg_score = round(sum([x[1] for x in ranked]) / total, 2)
        top_candidate = ranked[0][0]["name"]
        top_score = ranked[0][1]
        shortlist = len([x for x in ranked if x[1] >= 70])

        st.markdown("## 📌 Recruiter Decision Overview")

        k1,k2,k3,k4 = st.columns(4)

        with k1:
            st.markdown(f"<div class='kpi-card'><h4>Total Candidates</h4><h2>{total}</h2></div>", unsafe_allow_html=True)
        with k2:
            st.markdown(f"<div class='kpi-card'><h4>Average ATS</h4><h2>{avg_score}%</h2></div>", unsafe_allow_html=True)
        with k3:
            st.markdown(f"<div class='kpi-card'><h4>Top Candidate</h4><h2>{top_score}%</h2></div>", unsafe_allow_html=True)
        with k4:
            st.markdown(f"<div class='kpi-card'><h4>Shortlisted</h4><h2>{shortlist}/{total}</h2></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class='top-card'>
            <h2>🏆 Recommended Hire: {top_candidate}</h2>
            <h3>ATS Intelligence Score: {top_score}%</h3>
            <p>Recruiter Confidence Index: {min(top_score+5,100)}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## 📊 Detailed Candidate Intelligence")

        for item in ranked:
            profile, score, matched, missing = item

            st.markdown(f"""
            <div class='profile-card'>
                <h3>👤 {profile['name']}</h3>
                <p><b>Email:</b> {profile['email']} | <b>Phone:</b> {profile['phone']}</p>
                <p><b>Experience:</b> {profile['experience']} Years</p>
                <p><b>Education:</b> {profile['education']}</p>
                <p><b>Certifications:</b> {profile['certifications']}</p>
                <p><b>Top Skills:</b> {profile['top_skills']}</p>
                <p><b>Profile Strength:</b> {profile['strength']}</p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(score))
            st.write(f"### ATS Match Score: {score}%")

            a, b = st.columns(2)

            with a:
                st.subheader("Matched Recruiter Skills")
                st.write(", ".join(list(matched.keys())[:10]) if matched else "No strong skill alignment")

                st.subheader("AI Improvement Suggestions")
                for s in generate_suggestions(list(missing.keys())):
                    st.write("•", s)

            with b:
                st.subheader("Missing Recruiter Skills")
                st.write(", ".join(list(missing.keys())[:10]) if missing else "No major missing skills")

            st.markdown("---")

        st.markdown("## 🏆 Final Candidate Ranking")

        for idx, item in enumerate(ranked, start=1):
            profile, score, _, _ = item

            if score >= 85:
                status = "Highly Recommended"
                icon = "🟢"
            elif score >= 70:
                status = "Good Match"
                icon = "🟡"
            else:
                status = "Needs Improvement"
                icon = "🔴"

            medal = "🥇" if idx==1 else "🥈" if idx==2 else "🥉" if idx==3 else f"#{idx}"

            st.markdown(f"""
            <div class='rank-card'>
                <h3>{medal} {profile['name']}</h3>
                <p><b>ATS Score:</b> {score}%</p>
                <p><b>Hiring Decision:</b> {icon} {status}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("## 📈 Recruiter Analytics")
        df = pd.DataFrame({
            "Candidate":[x[0]["name"] for x in ranked],
            "Score":[x[1] for x in ranked]
        })
        fig = px.bar(df, x="Candidate", y="Score", text="Score")
        st.plotly_chart(fig, use_container_width=True)

        pdf_file = generate_pdf_report(ranked)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Executive ATS Report", f, file_name="ResumeIQ1_Executive_Report.pdf")

# ================= HISTORY =================
elif page == "📚 Screening Logs":

    st.markdown("<div class='section-box'><h3>📚 Previous Screening History</h3></div>", unsafe_allow_html=True)

    history = get_history()

    if history:
        df = pd.DataFrame(history, columns=["Candidate", "Score", "Date"])
        df.index = range(1, len(df)+1)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No previous logs available.")

# ================= CHATBOT =================
elif page == "🤖 AI Career Coach":

    st.markdown("<div class='section-box'><h3>🤖 ResumeIQ1 AI Career Coach</h3></div>", unsafe_allow_html=True)

    for sender, msg in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f"<div class='chat-user'>🧑 {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 {msg}</div>", unsafe_allow_html=True)

    st.markdown("---")

    question = st.text_input("Ask Resume / Career / Interview / ATS Question")

    c1, c2 = st.columns(2)
    with c1:
        ask = st.button("Send")
    with c2:
        clear = st.button("Reset Chat")

    if ask and question:
        missing_context = []
        if st.session_state.all_results:
            missing_context = list(st.session_state.all_results[0][3].keys())

        answer = ai_resume_coach(question, missing_context, st.session_state.chat_history)
        st.session_state.chat_history.append(("user", question))
        st.session_state.chat_history.append(("assistant", answer))
        st.rerun()

    if clear:
        st.session_state.chat_history = []
        st.rerun()

st.markdown("<hr><center>ResumeIQ1 © 2026 • Enterprise Resume Intelligence SaaS</center>", unsafe_allow_html=True)
