import PyPDF2
import docx
import re
import sqlite3
from collections import Counter
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# ================= UNIVERSAL SKILL LIBRARY =================
SKILL_LIBRARY = [
    "python","java","c++","sql","mysql","postgresql","mongodb","oracle",
    "machine learning","deep learning","tensorflow","keras","pytorch",
    "nlp","data science","data analysis","power bi","tableau","excel",
    "aws","azure","gcp","cloud","docker","kubernetes","linux",
    "git","github","rest api","flask","django","fastapi","streamlit",
    "html","css","javascript","react","node","angular",
    "testing","automation","selenium","devops","ci cd",
    "project management","agile","scrum","communication",
    "leadership","problem solving","statistics","scikit learn",
    "pandas","numpy","matplotlib","opencv","computer vision",
    "api","microservices","big data","hadoop","spark"
]


# ================= TEXT EXTRACTION =================
def extract_text(file):
    text = ""

    if file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "

    return text


# ================= CLEAN TEXT =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ================= ADVANCED SEMANTIC SIMILARITY =================
def get_similarity_advanced(resume, job_desc):
    tfidf = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
    vectors = tfidf.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(float(score[0][0]) * 100, 2)


# ================= SMART SKILL ANALYSIS =================
def get_skill_analysis(resume, job_desc):

    resume_lower = resume.lower()
    jd_lower = job_desc.lower()

    matched = {}
    missing = {}

    for skill in SKILL_LIBRARY:
        in_resume = skill in resume_lower
        in_jd = skill in jd_lower

        if in_jd and in_resume:
            matched[skill] = 1
        elif in_jd and not in_resume:
            missing[skill] = 1

    jd_words = set(jd_lower.split())
    resume_words = set(resume_lower.split())

    for word in jd_words:
        if len(word) > 4:
            if word in resume_words:
                matched[word] = 1
            else:
                missing[word] = 1

    return matched, missing


# ================= IMPROVEMENT SUGGESTIONS =================
def generate_suggestions(missing_skills):

    sug = []

    for skill in missing_skills[:6]:
        sug.append(f"Add practical project exposure or certification related to {skill}")

    if not sug:
        sug.append("Profile already shows strong recruiter alignment")

    return sug


# ================= CANDIDATE PROFILE PARSER =================
def build_candidate_profile(text):

    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.findall(r'\+?\d[\d -]{8,15}\d', text)

    lines = [x.strip() for x in text.split("\n") if x.strip()]
    name = lines[0][:35] if lines else "Unknown Candidate"

    exp_match = re.findall(r'(\d+)\+?\s+years', text.lower())
    experience = exp_match[0] if exp_match else "0"

    cert_keywords = ["certified", "certificate", "certification", "aws certified", "google certified"]
    cert_count = sum(1 for k in cert_keywords if k in text.lower())

    project_count = len(re.findall(r'project', text.lower()))

    education = "Not Found"
    edu_keys = ["b.tech", "b.e", "m.tech", "mba", "bsc", "msc", "bachelor", "master", "engineering"]
    for e in edu_keys:
        if e in text.lower():
            education = e.upper()
            break

    found_skills = []
    for skill in SKILL_LIBRARY:
        if skill in text.lower():
            found_skills.append(skill)

    linkedin = "Yes" if "linkedin" in text.lower() else "No"
    github = "Yes" if "github" in text.lower() else "No"

    strength = "Strong" if len(found_skills) >= 8 else "Moderate" if len(found_skills) >= 4 else "Basic"

    return {
        "name": name,
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found",
        "experience": experience,
        "education": education,
        "certifications": cert_count,
        "projects": project_count,
        "top_skills": ", ".join(found_skills[:8]) if found_skills else "No major skills detected",
        "linkedin": linkedin,
        "github": github,
        "strength": strength
    }


# ================= RECRUITER WEIGHTED FINAL SCORE =================
def weighted_score(base_score, matched_skills, resume_text):

    score = base_score

    score += min(len(matched_skills) * 1.8, 18)

    exp_match = re.findall(r'(\d+)\+?\s+years', resume_text.lower())
    if exp_match:
        score += min(int(exp_match[0]) * 2, 10)

    cert_bonus = len(re.findall(r'certified|certificate|certification', resume_text.lower()))
    score += min(cert_bonus * 2, 8)

    project_bonus = len(re.findall(r'project', resume_text.lower()))
    score += min(project_bonus, 6)

    if "@" in resume_text:
        score += 2
    if re.search(r'\d{10}', resume_text):
        score += 2
            return round(min(score, 100), 2)


# ================= AI HIRING DECISION =================
def hiring_decision(score):

    if score >= 85:
        return "Strong Hire", "Excellent recruiter alignment with high interview conversion potential"

    elif score >= 70:
        return "Interview Recommended", "Good technical fit with moderate recruiter confidence"

    elif score >= 55:
        return "Backup Candidate", "Some recruiter expectations are met but profile needs strengthening"

    else:
        return "Low Priority", "Low recruiter-job alignment detected"


# ================= RECRUITER INSIGHTS =================
def recruiter_global_insights(all_results):

    if not all_results:
        return {}

    most_exp = max(all_results, key=lambda x: int(x[0]["experience"]) if str(x[0]["experience"]).isdigit() else 0)
    best_cert = max(all_results, key=lambda x: x[0]["certifications"])
    best_project = max(all_results, key=lambda x: x[0]["projects"])

    all_missing = []
    for item in all_results:
        all_missing.extend(list(item[3].keys()))

    common_gap = Counter(all_missing).most_common(1)
    common_gap = common_gap[0][0] if common_gap else "No major gap"

    return {
        "most_experienced": most_exp[0]["name"],
        "best_certified": best_cert[0]["name"],
        "best_project_profile": best_project[0]["name"],
        "common_gap": common_gap
    }


# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_name TEXT,
            score REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_result(resume_name, score):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (resume_name, score, date) VALUES (?, ?, ?)",
        (resume_name, float(score), str(datetime.now()))
    )
    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT resume_name, score, date FROM history ORDER BY id DESC LIMIT 20")
    data = c.fetchall()
    conn.close()
    return data


# ================= EXECUTIVE PDF REPORT =================
def generate_pdf_report(all_results):

    file_path = "resume_report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("ResumeIQ1 Executive ATS Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 20))

    for idx, item in enumerate(all_results, start=1):

        profile, score, matched, missing = item
        decision, reason = hiring_decision(score)

        content.append(Paragraph(f"Candidate {idx}: {profile['name']}", styles["Heading2"]))
        content.append(Paragraph(f"Final ATS Recruiter Score: {score}%", styles["Heading3"]))
        content.append(Paragraph(f"Hiring Decision: {decision}", styles["Heading3"]))
        content.append(Paragraph(reason, styles["BodyText"]))
        content.append(Spacer(1, 12))

        table_data = [
            ["Email", profile["email"]],
            ["Phone", profile["phone"]],
            ["Experience", str(profile["experience"]) + " Years"],
            ["Education", profile["education"]],
            ["Certifications", str(profile["certifications"])],
            ["Projects", str(profile["projects"])],
            ["Matched Skills", ", ".join(list(matched.keys())[:8])],
            ["Missing Skills", ", ".join(list(missing.keys())[:8])]
        ]

        table = Table(table_data, colWidths=[130, 330])
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 1, colors.black),
            ("VALIGN", (0,0), (-1,-1), "TOP")
        ]))

        content.append(table)
        content.append(Spacer(1, 18))

        content.append(Paragraph("Recruiter Suggestions:", styles["Heading4"]))
        for s in generate_suggestions(list(missing.keys())):
            content.append(Paragraph("• " + s, styles["BodyText"]))

        content.append(PageBreak())

    doc.build(content)
    return file_path
