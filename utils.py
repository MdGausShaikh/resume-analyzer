import PyPDF2
import docx
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Extract text from PDF or DOCX
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


# Clean text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# Calculate similarity score
def get_similarity(resume, job_desc):
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0], vectors[1])
    return round(score[0][0] * 100, 2)


# Find missing skills/keywords
def get_missing_skills(resume, job_desc):
    resume_words = set(resume.split())
    job_words = set(job_desc.split())

    missing = job_words - resume_words

    # remove very small/common words
    filtered = [word for word in missing if len(word) > 3]

    return filtered[:20]