import streamlit as st
import pdfplumber

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="ResumeIQ", page_icon="📄")

# -------------------------
# Header
# -------------------------
st.title("📄 ResumeIQ")
st.markdown("### AI-Powered Resume Analyzer")
st.markdown("---")

# -------------------------
# Role Selection
# -------------------------
role = st.selectbox("Select Job Role", ["QA", "Developer"])

# -------------------------
# File Upload
# -------------------------
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="resume_upload")

# -------------------------
# Extract Text Function
# -------------------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# -------------------------
# ATS Score Function
# -------------------------
def calculate_ats_score(text, keywords):
    score = 0
    text = text.lower()

    for word in keywords:
        if word in text:
            score += 1

    return int((score / len(keywords)) * 100)

# -------------------------
# Suggestions Function
# -------------------------
def generate_suggestions(text, score):
    tips = []
    text_lower = text.lower()

    if "project" not in text_lower:
        tips.append("📌 Add a Projects section to showcase your work.")

    if "skills" not in text_lower:
        tips.append("📌 Include a Skills section with relevant technologies.")

    if "experience" not in text_lower:
        tips.append("📌 Add Experience section (internship/freelance counts too).")

    if len(text) < 1000:
        tips.append("📌 Resume content is too short. Add more details.")

    if score < 50:
        tips.append("⚠️ Low ATS score – add more relevant keywords.")
    elif score < 75:
        tips.append("👍 Good, but can improve by adding more role-specific keywords.")
    else:
        tips.append("🔥 Strong resume! Minor improvements can make it perfect.")

    return tips

# -------------------------
# Keywords
# -------------------------
qa_keywords = [
    "testing", "selenium", "automation", "jira",
    "test cases", "manual testing", "bug"
]

dev_keywords = [
    "python", "java", "api", "database",
    "sql", "backend", "frontend"
]

# -------------------------
# Main Logic
# -------------------------
if file is not None:
    with st.container():
        st.success("✅ Resume uploaded successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.write("📂 Filename:", file.name)

        with col2:
            st.write("📦 Size:", file.size, "bytes")

    # Extract text
    text = extract_text(file)

    st.subheader("📄 Extracted Resume Text")
    st.text_area("Resume Content", text, height=250)

    # Select keywords
    keywords = qa_keywords if role == "QA" else dev_keywords

    # Calculate ATS score
    score = calculate_ats_score(text, keywords)

    st.subheader("📊 ATS Score")
    st.metric(label="Your Score", value=f"{score}%")
    st.progress(score / 100)

    # Suggestions
    tips = generate_suggestions(text, score)

    st.subheader("💡 Suggestions to Improve")
    for tip in tips:
        st.markdown(f"- {tip}")

    st.markdown("---")
    st.markdown("### 🚀 Improve your resume to increase your chances!")