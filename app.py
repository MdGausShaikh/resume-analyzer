import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    extract_text,
    clean_text,
    get_similarity_advanced,
    get_skill_analysis,
    generate_suggestions,
    detect_sections,
    weighted_score,
    init_db,
    save_result,
    get_history,
    generate_pdf_report
)

# ================= CONFIG =================
st.set_page_config(page_title="AI Resume Analyzer PRO", layout="wide")
init_db()

# ================= STYLE =================
st.markdown("""
<style>
.block {
    padding: 10px;
    border-radius: 10px;
    background-color: #f8f9fa;
    margin-bottom: 10px;
}
.badge-green {
    background:#2ecc71;
    padding:5px 10px;
    border-radius:6px;
    color:white;
    margin:3px;
}
.badge-red {
    background:#e74c3c;
    padding:5px 10px;
    border-radius:6px;
    color:white;
    margin:3px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
col_logo, col_title = st.columns([1,5])
with col_logo:
    try:
        st.image("logo.png", width=150)
    except:
        st.write("🚀")
with col_title:
    st.title("AI Resume Analyzer PRO")

st.divider()

# ================= TABS =================
tab1, tab2 = st.tabs(["📊 Analyze", "📜 History"])

# ================= ANALYZE =================
with tab1:

    # INPUT SECTION
    col1, col2 = st.columns(2)

    with col1:
        uploaded_files = st.file_uploader("Upload Resume(s)", type=["pdf", "docx"], accept_multiple_files=True)

    with col2:
        job_desc = st.text_area("Paste Job Description")

    if st.button("🚀 Analyze"):

        if not uploaded_files or not job_desc:
            st.warning("Please upload resume and job description")
        else:
            results = []

            for file in uploaded_files:
                text = extract_text(file)
                resume_clean = clean_text(text)
                job_clean = clean_text(job_desc)

                score = get_similarity_advanced(resume_clean, job_clean)
                matched, missing = get_skill_analysis(resume_clean, job_clean)
                score = weighted_score(score, matched.keys())

                results.append((file.name, score, matched, missing))

            results.sort(key=lambda x: x[1], reverse=True)

            # ================= TOP SECTION =================
            col1, col2 = st.columns([2,1])

            with col1:
                st.subheader("🏆 Ranking")
                for name, score, _, _ in results:
                    st.write(f"{name} → {score}%")

            # TOP RESUME SUMMARY
            name, score, matched, missing = results[0]
            save_result(score)

            with col2:
                st.subheader("📊 Score")
                st.metric("Match %", f"{score}%")
                st.progress(float(score)/100)

            st.divider()

            # ================= MAIN DASHBOARD =================
            col1, col2 = st.columns(2)

            # LEFT SIDE
            with col1:
                st.subheader("✅ Matched Skills")
                for s in list(matched.keys())[:12]:
                    st.markdown(f"<span class='badge-green'>{s}</span>", unsafe_allow_html=True)

                st.markdown("---")

                st.subheader("💡 Suggestions")
                for s in generate_suggestions(list(missing.keys())):
                    st.write("•", s)

            # RIGHT SIDE
            with col2:
                st.subheader("❌ Missing Skills")
                for s in list(missing.keys())[:12]:
                    st.markdown(f"<span class='badge-red'>{s}</span>", unsafe_allow_html=True)

                st.markdown("---")

                st.subheader("📑 Sections")
                st.json(detect_sections(" ".join(matched.keys())))

            st.divider()

            # ================= CHART + DOWNLOAD =================
            col1, col2 = st.columns(2)

            with col1:
                chart_df = pd.DataFrame({
                    "Type": ["Matched", "Missing"],
                    "Count": [len(matched), len(missing)]
                })

                fig = px.pie(chart_df, names="Type", values="Count")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📄 Download Report")
                pdf_path = generate_pdf_report(score, matched, missing)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        f,
                        "resume_report.pdf",
                        "application/pdf"
                    )

# ================= HISTORY =================
with tab2:

    st.subheader("📜 Recent Analysis")

    history = get_history()

    if history:
        for score, date in history:
            st.write(f"{date} → {round(float(score),2)}%")
    else:
        st.info("No history yet")
