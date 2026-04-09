import streamlit as st
import pdfplumber
import plotly.graph_objects as go

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="ResumeIQ", page_icon="📄", layout="wide")

# -------------------------
# ULTRA PREMIUM CSS
# -------------------------
st.markdown("""
<style>

/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Orbitron:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #1c2b3a, #2c5364);
    color: white;
}

/* Glow Title */
@keyframes glow {
    from { text-shadow: 0 0 10px #00ffd5; }
    to { text-shadow: 0 0 25px #00c6ff, 0 0 40px #0072ff; }
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}

/* Hover effect */
.card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 10px 25px rgba(0,255,213,0.2);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00ffd5, #00c6ff);
    color: black;
    border-radius: 10px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* Smooth fade */
section {
    animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HERO HEADER
# -------------------------
st.markdown("""
<div style='text-align:center; padding:40px 0;'>

<h1 style="
font-family:Orbitron;
font-size:3.2rem;
background:linear-gradient(90deg,#00ffd5,#00c6ff,#0072ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
animation:glow 2s infinite alternate;
">
ResumeIQ
</h1>

<p style="font-size:1.2rem;color:#cbd5e1;">
🚀 Smart Resume Analyzer Dashboard
</p>

<p style="color:#94a3b8;">
Analyze • Improve • Get Hired
</p>

</div>
<hr style="border:1px solid #00ffd5;opacity:0.3;">
""", unsafe_allow_html=True)

# -------------------------
# Role Selection
# -------------------------
role = st.selectbox("Select Job Role", [
    "QA","Developer","Data Analyst","Data Scientist","DevOps Engineer","Web Developer"
])

# -------------------------
# Upload
# -------------------------
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# -------------------------
# Extract Text
# -------------------------
def extract_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for p in pdf.pages:
            if p.extract_text():
                text += p.extract_text()
    return text.lower()

# -------------------------
# Keywords
# -------------------------
keywords = {
    "QA":["testing","selenium","automation","jira","bug"],
    "Developer":["python","java","api","sql","backend"],
    "Data Analyst":["excel","sql","tableau","power bi","analysis"],
    "Data Scientist":["python","machine learning","pandas","numpy","model"],
    "DevOps Engineer":["docker","kubernetes","aws","ci/cd","linux"],
    "Web Developer":["html","css","javascript","react","frontend"]
}

# -------------------------
# Logic
# -------------------------
def score_calc(text, keys):
    return int(sum(1 for k in keys if k in text)/len(keys)*100)

def missing_keys(text, keys):
    return [k for k in keys if k not in text]

# -------------------------
# MAIN
# -------------------------
if file:
    st.success("✅ Resume uploaded")

    text = extract_text(file)
    keys = keywords[role]

    score = score_calc(text, keys)
    missing = missing_keys(text, keys)

    matched = len(keys) - len(missing)

    # Metrics
    st.markdown("## 📊 Dashboard")
    c1,c2,c3 = st.columns(3)
    c1.metric("ATS Score",f"{score}%")
    c2.metric("Matched",matched)
    c3.metric("Missing",len(missing))

    st.progress(score/100)

    # Charts
    st.markdown("## 📈 Analysis")

    col1,col2 = st.columns(2)

    with col1:
        fig = go.Figure(data=[go.Bar(x=["Matched","Missing"], y=[matched,len(missing)])])
        fig.update_layout(template="plotly_dark", height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        pie = go.Figure(data=[go.Pie(labels=["Matched","Missing"], values=[matched,len(missing)], hole=0.4)])
        pie.update_layout(template="plotly_dark", height=280)
        st.plotly_chart(pie, use_container_width=True)

    # Feedback
    st.markdown("## 🎯 Feedback")
    if score<50:
        st.error("Needs improvement")
    elif score<75:
        st.warning("Good, improve more")
    else:
        st.success("Excellent")

    # Missing Skills
    st.markdown("## ❌ Missing Skills")
    if missing:
        cols = st.columns(3)
        for i,w in enumerate(missing):
            with cols[i%3]:
                st.markdown(f"<div class='card'>🔴 {w}</div>", unsafe_allow_html=True)
    else:
        st.success("No missing skills")

    # Resume text
    st.markdown("## 📄 Resume")
    st.text_area("", text, height=200)

    st.markdown("---")
    st.markdown("### ✅ Analysis Complete")
