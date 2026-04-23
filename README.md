# 📄 AI Resume Analyzer

An AI-powered Resume Analyzer that compares a candidate's resume with a job description and provides a **match score**, **missing skills**, and a **downloadable report**.

---

## 🚀 Live Demo

🔗 https://your-app-name.streamlit.app

---

## 📌 Features

* 📄 Upload Resume (PDF / DOCX)
* 📝 Paste Job Description
* 📊 Match Score using NLP (TF-IDF)
* ❌ Identify Missing Skills / Keywords
* 📥 Download Analysis Report (CSV)
* 🌐 Simple Web UI using Streamlit

---

## 🧠 How It Works

1. Extracts text from resume (PDF/DOCX)
2. Cleans and preprocesses text
3. Converts text into numerical vectors using TF-IDF
4. Calculates similarity score using cosine similarity
5. Displays:

   * Match Percentage
   * Missing Skills

---

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:**

  * pandas
  * scikit-learn
  * PyPDF2
  * python-docx
  * nltk / spaCy
  * streamlit

---

## 📂 Project Structure

```
resume-analyzer/
│── app.py
│── utils.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run Application

```
python -m streamlit run app.py
```

---

## 📊 Example Output

* ✅ Match Score: 82% (Strong Match)
* ⚠️ Missing Skills: Docker, Kubernetes, AWS

---

## 🔥 Advantages

* 100% Free & Open Source
* Real-world AI use case
* Easy to use interface
* Helps improve resume quality

---

## ⚠️ Limitations

* Based on keyword matching (TF-IDF)
* Limited contextual understanding
* Accuracy can be improved with advanced AI models

---

## 🚀 Future Enhancements

* AI-based resume suggestions
* Skill gap analysis
* Integration with job portals
* Advanced NLP using Transformers

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo and improve it.

---

## 📧 Contact

For any queries or collaboration:
📩 [your-email@example.com](mailto:your-email@example.com)

---

## ⭐ Acknowledgment

If you like this project, give it a ⭐ on GitHub!
