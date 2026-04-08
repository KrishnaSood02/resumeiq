import streamlit as st
import pdfplumber

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")

# -------------------------
# PREMIUM CSS (Glass + Animations)
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Headings */
h1, h2, h3 {
    color: #00ffd5;
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    animation: fadeInUp 0.6s ease;
}

/* Hover effect */
.card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 8px 20px rgba(0,255,213,0.2);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00ffd5, #00c6ff);
    color: black;
    border-radius: 10px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 10px #00ffd5;
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #00ffd5, #00c6ff);
}

/* Animation */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

section {
    animation: fadeInUp 0.8s ease;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.title("📄 ResumeIQ")
st.markdown("### 🚀 AI Resume Analyzer")
st.markdown("---")

# -------------------------
# Job Roles
# -------------------------
role = st.selectbox("Select Job Role", [
    "QA",
    "Developer",
    "Data Analyst",
    "Data Scientist",
    "DevOps Engineer",
    "Web Developer"
])

# -------------------------
# Upload Resume
# -------------------------
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# -------------------------
# Extract Text
# -------------------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text()
    return text.lower()

# -------------------------
# Keywords
# -------------------------
keywords_dict = {
    "QA": ["testing", "selenium", "automation", "jira", "bug"],
    "Developer": ["python", "java", "api", "sql", "backend"],
    "Data Analyst": ["excel", "sql", "tableau", "power bi", "analysis"],
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "model"],
    "DevOps Engineer": ["docker", "kubernetes", "aws", "ci/cd", "linux"],
    "Web Developer": ["html", "css", "javascript", "react", "frontend"]
}

# -------------------------
# Score
# -------------------------
def calculate_score(text, keywords):
    match = sum(1 for k in keywords if k in text)
    return int((match / len(keywords)) * 100)

# -------------------------
# Missing Keywords
# -------------------------
def find_missing(text, keywords):
    return [k for k in keywords if k not in text]

# -------------------------
# Suggestions
# -------------------------
def suggestions(score):
    if score < 50:
        return "Add more relevant skills and keywords."
    elif score < 75:
        return "Good resume, but can improve."
    else:
        return "Excellent resume!"

# -------------------------
# MAIN LOGIC
# -------------------------
if file:
    st.success("✅ Resume uploaded successfully!")

    text = extract_text(file)
    keywords = keywords_dict[role]

    score = calculate_score(text, keywords)
    missing = find_missing(text, keywords)

    # Dashboard
    st.markdown("## 📊 Resume Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("ATS Score", f"{score}%")
        st.progress(score / 100)

    with col2:
        st.markdown("### 📌 Feedback")
        if score < 50:
            st.error("Needs Improvement ❌")
        elif score < 75:
            st.warning("Good ⚠️")
        else:
            st.success("Excellent ✅")

    # Suggestions
    st.markdown("## 💡 Suggestions")
    st.markdown(f"<div class='card'>{suggestions(score)}</div>", unsafe_allow_html=True)

    # Missing Keywords
    st.markdown("## ❌ Missing Keywords")

    if missing:
        for word in missing:
            st.markdown(f"<div class='card'>🔴 {word}</div>", unsafe_allow_html=True)
    else:
        st.success("No missing keywords!")

    # Resume Preview
    st.markdown("## 📄 Resume Content")
    st.text_area("", text, height=200)

    st.markdown("---")
    st.markdown("### ✅ Analysis Complete")
