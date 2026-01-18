import streamlit as st
import os
import base64
from src.ui.admin_page import render_admin_page
from src.ui.user_page import render_user_page

# ===================================================
# 1. SETUP & CONFIG
# ===================================================
st.set_page_config(
    page_title="DSD Course Architect", 
    layout="wide",
    page_icon="logo_dsd.png" if os.path.exists("logo_dsd.png") else "https://www.dsd.go.th/img/symbol/logo_dsd.png",
    initial_sidebar_state="collapsed"
)

if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

# ===================================================
# 📍 ฟังก์ชันแปลงรูปภาพ
# ===================================================
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    else:
        return "https://www.dsd.go.th/img/symbol/logo_dsd.png"

# ===================================================
# 2. PROFESSIONAL CSS (Updated Fixes ✅)
# ===================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stMarkdown { 
        font-family: 'Prompt', sans-serif; 
        color: #333;
    }

    header {visibility: hidden;}
    
    /* --- 🔠 ปรับขนาดตัวอักษร (Typography) --- */
    h1 { font-size: 26px !important; font-weight: 700 !important; color: #5A2D81 !important; margin-bottom: 20px !important; line-height: 1.4 !important; }
    h2 { font-size: 22px !important; font-weight: 600 !important; color: #444 !important; margin-top: 30px !important; margin-bottom: 15px !important; border-left: 5px solid #5A2D81; padding-left: 10px; }
    h3 { font-size: 18px !important; font-weight: 600 !important; color: #555 !important; margin-top: 15px !important; }
    p, li, div { font-size: 16px !important; line-height: 1.7 !important; color: #333 !important; font-weight: 300 !important; }

    /* --- 🟣 1. แก้ไขปุ่มกด (Button Fix) --- */
    /* บังคับให้ปุ่ม Primary เป็นสีม่วง และตัวหนังสือสีขาวเสมอ */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%) !important;
        border: none !important;
        color: #FFFFFF !important; /* ✅ บังคับตัวหนังสือสีขาว */
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    /* แก้ไขกรณี Streamlit ซ้อน Element ภายในปุ่ม */
    .stButton > button[kind="primary"] p {
        color: #FFFFFF !important; /* ✅ บังคับสีขาวในระดับ p tag */
    }           

    /* --- 🟣 แก้ไขปุ่มดาวน์โหลด (Download Button Fix) --- */
    /* เจาะจงไปที่ปุ่ม Download โดยเฉพาะ */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%) !important;
        color: #FFFFFF !important; /* ✅ บังคับตัวหนังสือสีขาว */
        border: none !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* บังคับทุกข้อความในปุ่มให้เป็นสีขาว */
    [data-testid="stDownloadButton"] button * {
        color: #FFFFFF !important;
    }

    /* ตอนเอาเมาส์ชี้ (Hover) */
    [data-testid="stDownloadButton"] button:hover {
        background: linear-gradient(135deg, #7B4397 0%, #5A2D81 100%) !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    /* --- 📊 2. แก้ไขตาราง (Table Fix) --- */
    th {
        background-color: #f0f2f6;
        color: #5A2D81 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-align: left !important;
    }
    
    /* ✅ จัดการช่องแรก (เวลา) ให้กว้างและไม่ตัดคำ */
    th:first-child, td:first-child {
        min-width: 130px !important;   /* กำหนดความกว้างขั้นต่ำ */
        white-space: nowrap !important; /* ห้ามตัดบรรทัด (เช่น 09:00 - 10:30 จะอยู่บรรทัดเดียว) */
        font-weight: 600 !important;
        color: #5A2D81 !important;     /* ให้เวลาเป็นสีม่วงสวยๆ */
        vertical-align: top !important; /* ให้ตัวหนังสือชิดบนเสมอ */
    }

    /* --- (ส่วน Header & Footer เดิม) --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px; background-color: transparent;
        padding-bottom: 10px; border-bottom: 1px solid #ddd; margin-top: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: transparent;
        border-radius: 4px; color: #666; font-size: 16px; font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f0f2f6; color: #5A2D81;
        border-bottom: 3px solid #5A2D81; font-weight: 700;
    }

    .top-nav-container {
        display: flex; justify-content: flex-start; align-items: center;
        padding: 20px 30px; margin-bottom: 10px;
        background: linear-gradient(135deg, #5A2D81 0%, #4a236e 100%);
        border-radius: 12px; box-shadow: 0 4px 15px rgba(90, 45, 129, 0.2);
        color: white;
    }
    .logo-img {
        height: 65px; width: auto;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); 
        background-color: white; padding: 5px; border-radius: 50%;
        margin-right: 20px;
    }
    .app-title { font-size: 28px; font-weight: 700; color: white !important; margin: 0; line-height: 1.2; }
    .app-subtitle { font-size: 16px; color: #e0e0e0 !important; font-weight: 300; margin: 0; opacity: 0.9; }
    
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #333; color: #ccc;
        text-align: center; padding: 10px; font-size: 12px; z-index: 100;
    }
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
</style>
""", unsafe_allow_html=True)

# ===================================================
# 3. HEADER SECTION
# ===================================================

logo_src = get_image_base64("logo_dsd.png")

st.markdown(f"""
<div class="top-nav-container">
    <img src="{logo_src}" class="logo-img">
    <div>
        <div class="app-title">DSD Course Architect</div>
        <div class="app-subtitle">ระบบอัจฉริยะช่วยออกแบบหลักสูตรฝึกอบรมฝีมือแรงงาน</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 4. NAVIGATION TABS
# ===================================================

tab1, tab2 = st.tabs(["🎓 ออกแบบหลักสูตร (User)", "🛠️ จัดการระบบ (Admin)"])

with tab1:
    st.markdown("###")
    render_user_page()

with tab2:
    st.markdown("###")
    render_admin_page()

# ===================================================
# 5. FOOTER
# ===================================================
st.markdown("""
<div class="footer">
    © 2026 กรมพัฒนาฝีมือแรงงาน (Department of Skill Development) | Powered by DSD AI Team
</div>
""", unsafe_allow_html=True)