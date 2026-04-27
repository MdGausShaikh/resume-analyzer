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


# ================= SIMILARITY =================
def get_similarity_advanced(resume, job_desc):
    tfidf = TfidfVectorizer(ngram_range=(1,2), stop_words="english")
    vectors = tfidf.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(float(score[0][0]) * 100, 2)


# ================= SKILL ANALYSIS =================
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

    return matched, missing


# ================= SUGGESTIONS =================
def generate_suggestions(missing_skills):

    sug = []

    for skill in missing_skills[:6]:
        sug.append(f"Add practical project or certification in {skill}")

    if not sug:
        sug.append("Strong profile alignment with job description")

    return sug


# ================= PROFILE BUILDER =================
def build_candidate_profile(text):

    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.findall(r'\+?\d[\d -]{8,15}\d', text)

    lines = [x.strip() for x in text.split("\n") if x.strip()]
    name = lines[0][:35] if lines else "Unknown"

    exp_match = re.findall(r'(\d+)\+?\s+years', text.lower())
    experience = exp_match[0] if exp_match else "0"

    cert_keywords = ["certified", "certificate", "certification"]
    cert_count = sum(1 for k in cert_keywords if k in text.lower())

    project_count = len(re.findall(r'project', text.lower()))

    edu_keys = ["b.tech", "b.e", "m.tech", "mba", "bsc", "msc"]
    education = "Not Found"
    for e in edu_keys:
        if e in text.lower():
            education = e.upper()
            break

    found_skills = [s for s in SKILL_LIBRARY if s in text.lower()]

    strength = "Strong" if len(found_skills) >= 8 else "Moderate" if len(found_skills) >= 4 else "Basic"

    return {
        "name": name,
        "email": email[0] if email else "Not Found",
        "phone": phone[0] if phone else "Not Found",
        "experience": experience,
        "education": education,
        "certifications": cert_count,
        "projects": project_count,
        "top_skills": ", ".join(found_skills[:8]) if found_skills else "No skills detected",
        "strength": strength
    }


# ================= FIXED WEIGHTED SCORE =================
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


# ================= HISTORY DB =================
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


# ================= PDF REPORT =================
def generate_pdf_report(all_results):

    file_path = "resume_report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("ResumeIQ1 ATS Report", styles["Title"]))
    content.append(Spacer(1, 20))

    for idx, item in enumerate(all_results, start=1):

        profile, score, matched, missing = item

        content.append(Paragraph(f"Candidate {idx}: {profile['name']}", styles["Heading2"]))
        content.append(Paragraph(f"Score: {score}%", styles["BodyText"]))
        content.append(Spacer(1, 10))

        table_data = [
            ["Email", profile["email"]],
            ["Phone", profile["phone"]],
            ["Experience", str(profile["experience"])],
            ["Education", profile["education"]],
            ["Skills", profile["top_skills"]],
        ]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.black)
        ]))

        content.append(table)
        content.append(PageBreak())

    doc.build(content)
    return file_path
