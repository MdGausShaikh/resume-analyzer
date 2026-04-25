import PyPDF2
import docx
import re
from collections import Counter
import sqlite3
from datetime import datetime

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')


# ================= TEXT EXTRACTION =================
def extract_text(file):
    text = ""

    if file.name.endswith('.pdf'):
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()

    elif file.name.endswith('.docx'):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text + " "

    return text


# ================= CLEAN TEXT =================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# ================= AI SIMILARITY =================
def get_similarity_advanced(resume, job_desc):
    embeddings = model.encode([resume, job_desc])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])
    return round(float(score[0][0]) * 100, 2)


# ================= SKILL ANALYSIS =================
def get_skill_analysis(resume, job_desc):
    resume_words = resume.split()
    job_words = job_desc.split()

    resume_count = Counter(resume_words)
    job_count = Counter(job_words)

    matched = {}
    missing = {}

    for word in job_count:
        if len(word) > 3:
            if word in resume_count:
                matched[word] = job_count[word]
            else:
                missing[word] = job_count[word]

    return matched, missing


def generate_suggestions(missing_skills):
    return [f"Consider adding experience with {skill}" for skill in missing_skills[:5]]


# ================= SECTION DETECTION =================
def detect_sections(text):
    sections = {"Skills": "No", "Experience": "No", "Education": "No"}

    text = text.lower()

    if "skills" in text:
        sections["Skills"] = "Yes"
    if "experience" in text:
        sections["Experience"] = "Yes"
    if "education" in text:
        sections["Education"] = "Yes"

    return sections


# ================= SCORE WEIGHTING =================
def weighted_score(base_score, matched_skills):
    important = ["python", "machine", "learning", "sql"]
    bonus = sum(1 for skill in matched_skills if skill in important)
    return min(base_score + bonus, 100)


# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score REAL,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_result(score):
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (score, date) VALUES (?, ?)",
        (float(score), str(datetime.now()))
    )
    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("SELECT score, date FROM history ORDER BY id DESC LIMIT 5")
    data = c.fetchall()
    conn.close()
    return data


# ================= PDF REPORT =================
def generate_pdf_report(score, matched, missing):
    file_path = "report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Resume Analysis Report", styles["Title"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Match Score: {round(float(score), 2)}%", styles["Heading2"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Matched Skills:", styles["Heading3"]))
    content.append(Paragraph(", ".join(matched.keys()), styles["BodyText"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Missing Skills:", styles["Heading3"]))
    content.append(Paragraph(", ".join(missing.keys()), styles["BodyText"]))
    content.append(Spacer(1, 10))

    doc.build(content)

    return file_path
