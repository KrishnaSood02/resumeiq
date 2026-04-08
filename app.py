import streamlit as st
import pdfplumber
import plotly.graph_objects as go

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")

# -------------------------
# PREMIUM CSS
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

h1, h2, h3 {
    color: #00ffd5;
}

.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
}

/* Glow animation */
@keyframes glow {
    from { text-shadow: 0 0 10px #00ffd5; }
    to { text-shadow: 0 0 20px #00c6ff, 0 0 30px #0072ff; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO HEADER
# -------------------------
st.markdown("""
<div style='text-align: center; padding: 30px 0;'>

<h1 style="
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00ffd5, #00c6ff, #0072ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glow 2s ease-in-out infinite alternate;
">
ResumeIQ
</h1>

<p style='font-size: 1.3rem; color: #cbd5e1;'>
🚀 Smart Resume Analyzer Dashboard
</p>

<p style='font-size: 1rem; color: #94a3b8;'>
Analyze • Improve • Get Hired
</p>

</div>

<hr style="border: 1px solid #00ffd5; opacity: 0.3;">
""", unsafe_allow_html=True)

# -------------------------
# Job Role
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
# Score Logic
# -------------------------
def calculate_score(text, keywords):
    match = sum(1 for k in keywords if k in text)
    return int((match / len(keywords)) * 100)

def find_missing(text, keywords):
    return [k for k in keywords if k not in text]

# -------------------------
# MAIN LOGIC
# -------------------------
if file:
    st.success("✅ Resume uploaded successfully!")

    text = extract_text(file)
    keywords = keywords_dict[role]

    score = calculate_score(text, keywords)
    missing = find_missing(text, keywords)

    matched_count = len(keywords) - len(missing)
    missing_count = len(missing)

    # -------------------------
    # METRICS
    # -------------------------
    st.markdown("## 📊 Resume Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("ATS Score", f"{score}%")
    col2.metric("Matched Skills", matched_count)
    col3.metric("Missing Skills", missing_count)

    st.progress(score / 100)

    # -------------------------
    # CHARTS SIDE-BY-SIDE 🔥
    # -------------------------
    st.markdown("## 📈 Skill Analysis")

    col1, col2 = st.columns(2)

    # Bar Chart
    with col1:
        fig = go.Figure(data=[
            go.Bar(
                x=["Matched", "Missing"],
                y=[matched_count, missing_count]
            )
        ])

        fig.update_layout(
            title="Match vs Missing",
            template="plotly_dark",
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

    # Pie Chart (Donut)
    with col2:
        pie = go.Figure(data=[go.Pie(
            labels=["Matched", "Missing"],
            values=[matched_count, missing_count],
            hole=0.4
        )])

        pie.update_layout(
            title="Distribution",
            template="plotly_dark",
            height=300
        )

        st.plotly_chart(pie, use_container_width=True)

    # -------------------------
    # FEEDBACK
    # -------------------------
    st.markdown("## 🎯 Feedback")

    if score < 50:
        st.error("Your resume needs improvement.")
    elif score < 75:
        st.warning("Good, but can improve.")
    else:
        st.success("Excellent resume!")

    # -------------------------
    # MISSING SKILLS GRID
    # -------------------------
    st.markdown("## ❌ Missing Skills")

    if missing:
        cols = st.columns(3)
        for i, word in enumerate(missing):
            with cols[i % 3]:
                st.markdown(f"<div class='card'>🔴 {word}</div>", unsafe_allow_html=True)
    else:
        st.success("No missing skills!")

    # -------------------------
    # RESUME TEXT
    # -------------------------
    st.markdown("## 📄 Resume Content")
    st.text_area("", text, height=200)

    st.markdown("---")
    st.markdown("### ✅ Analysis Complete")
