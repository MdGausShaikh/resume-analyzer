import streamlit as st
import pandas as pd
from utils import extract_text, clean_text, get_similarity, get_missing_skills

# Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# Title
st.title("📄 AI Resume Analyzer")
st.markdown("### Upload your resume and compare it with a job description")

# File upload
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

# Job description input
job_desc = st.text_area("Paste Job Description")

if uploaded_file and job_desc:

    # Extract text
    resume_text = extract_text(uploaded_file)

    if not resume_text.strip():
        st.error("Could not extract text from resume. Try another file.")
    else:
        # Clean text
        resume_clean = clean_text(resume_text)
        job_clean = clean_text(job_desc)

        # Similarity score
        score = get_similarity(resume_clean, job_clean)

        # Show score
        st.subheader("📊 Match Score")

        if score > 70:
            st.success(f"{score}% - Strong Match ✅")
        elif score > 40:
            st.warning(f"{score}% - Average Match ⚠️")
        else:
            st.error(f"{score}% - Needs Improvement ❌")

        # Missing skills
        missing_skills = get_missing_skills(resume_clean, job_clean)

        st.subheader("❌ Missing Keywords / Skills")

        if missing_skills:
            st.write(", ".join(missing_skills))
        else:
            st.success("No major missing skills detected 🎉")

        # Download report
        st.subheader("📥 Download Report")

        data = {
            "Match Score (%)": [score],
            "Missing Skills": [", ".join(missing_skills)]
        }

        df = pd.DataFrame(data)

        st.download_button(
            label="Download CSV Report",
            data=df.to_csv(index=False),
            file_name="resume_analysis_report.csv",
            mime="text/csv"
        )