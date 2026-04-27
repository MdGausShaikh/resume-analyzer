# 🧠 ResumeIQ1 – AI-Powered Resume Screening & ATS Intelligence System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![AI](https://img.shields.io/badge/AI-Powered-green)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 🚀 Overview

**ResumeIQ1** is an AI-powered recruitment intelligence system that automates resume screening, analyzes candidate profiles, and generates ATS-based rankings.

It helps recruiters make faster and smarter hiring decisions using **Machine Learning + NLP + AI Chatbot assistance**.

---

## 🎯 Key Features

### 📄 Resume Processing
- Upload multiple resumes (PDF / DOCX)
- Automatic text extraction
- Data cleaning and preprocessing

### 🧠 ATS Scoring Engine
- TF-IDF + Cosine Similarity model
- Weighted scoring based on:
  - Skills match
  - Experience
  - Certifications
  - Projects

### 🧩 Skill Intelligence System
- 60+ technical & soft skills database
- Detects:
  - Matched skills
  - Missing skills
- Job description comparison

### 👤 Candidate Profiling
Automatically extracts:
- Name
- Email
- Phone
- Experience
- Education
- Certifications
- Projects
- LinkedIn / GitHub presence

### 🏆 Ranking System
- Automated candidate ranking
- Hiring decisions:
  - 🟢 Strong Hire
  - 🟡 Interview Recommended
  - 🟠 Backup Candidate
  - 🔴 Low Priority

### 📊 Analytics Dashboard
- Recruiter KPI insights
- Candidate score visualization
- Interactive Plotly charts

### 🤖 AI Career Coach
- Powered by Groq LLM (Llama 3)
- Resume improvement suggestions
- Interview preparation guidance
- Career roadmap recommendations

### 📚 History Tracking
- Stores past screening results using SQLite
- Last 20 evaluations available

### 📑 PDF Report Generation
- Professional recruiter-ready reports
- Candidate-wise analysis
- Skill gap insights

---

## 🏗️ System Architecture
Resume Upload
↓
Text Extraction (PDF / DOCX)
↓
Data Cleaning & Preprocessing
↓
Skill Matching Engine
↓
TF-IDF + Cosine Similarity
↓
Weighted ATS Scoring
↓
Candidate Ranking
↓
Dashboard + PDF Report


---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | Streamlit |
| Backend | Python |
| ML/NLP | Scikit-learn, TF-IDF |
| Data Handling | Pandas |
| Visualization | Plotly |
| Database | SQLite |
| File Parsing | PyPDF2, python-docx |
| Reporting | ReportLab |
| AI Chatbot | Groq LLM |

---

## 📂 Project Structure
ResumeIQ1/
│
├── app.py # Main Streamlit app
├── auth.py # Login system
├── utils.py # ATS engine & ML logic
├── chatbot.py # AI Career Coach
├── requirements.txt # Dependencies
├── history.db # SQLite database
└── README.md # Documentation
