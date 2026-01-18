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
    
    /* ✅ แก้ไข 1: เจาะจง Element แทนการเหมาเข่ง (เอา div, span ออก) เพื่อไม่ให้ Icon พัง */
    /* นี่คือจุดที่ต่างจากโค้ดเดิมครับ เราจะไม่ใช้ [class*="css"] แล้ว */
    html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, a, button, input, label, textarea { 
        font-family: 'Prompt', sans-serif !important; 
        color: #000000 !important;  /* ดำสนิท */
        font-weight: 400 !important; /* หนาขึ้น */
    }

    /* ซ่อน Decoration Bar ด้านบน */
    header {visibility: hidden;}
    
    /* --- 🔠 Typography --- */
    h1 { font-size: 26px !important; font-weight: 700 !important; color: #5A2D81 !important; margin-bottom: 20px !important; line-height: 1.4 !important; }
    h2 { font-size: 22px !important; font-weight: 600 !important; color: #333333 !important; margin-top: 30px !important; margin-bottom: 15px !important; border-left: 5px solid #5A2D81; padding-left: 10px; }
    h3 { font-size: 18px !important; font-weight: 600 !important; color: #444444 !important; margin-top: 15px !important; }

    /* --- 🟣 Button Fix (ปุ่มปกติ) --- */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button[kind="primary"] * { color: #FFFFFF !important; font-weight: 500 !important; }

    /* --- 🟣 Download Button Fix (ปุ่มดาวน์โหลด) --- */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    [data-testid="stDownloadButton"] button * { color: #FFFFFF !important; font-weight: 500 !important; }

    /* --- 📊 Table Fix (ตาราง) --- */
    th {
        background-color: #f0f2f6;
        color: #5A2D81 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        text-align: left !important;
    }
    td {
        font-size: 15px !important;
        color: #000000 !important;
        font-weight: 400 !important;
        vertical-align: top !important;
    }
    /* ช่องเวลา */
    th:first-child, td:first-child {
        min-width: 130px !important;
        white-space: nowrap !important;
        font-weight: 600 !important;
        color: #5A2D81 !important;
    }

    /* --- Header/Footer/Tabs --- */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: transparent; padding-bottom: 10px; border-bottom: 1px solid #ddd; margin-top: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px; color: #666; font-size: 16px; font-weight: 500; }
    .stTabs [aria-selected="true"] { background-color: #f0f2f6; color: #5A2D81; border-bottom: 3px solid #5A2D81; font-weight: 700; }

    .top-nav-container { display: flex; justify-content: flex-start; align-items: center; padding: 20px 30px; margin-bottom: 10px; background: linear-gradient(135deg, #5A2D81 0%, #4a236e 100%); border-radius: 12px; box-shadow: 0 4px 15px rgba(90, 45, 129, 0.2); color: white; }
    .logo-img { height: 65px; width: auto; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); background-color: white; padding: 5px; border-radius: 50%; margin-right: 20px; }
    .app-title { font-size: 28px; font-weight: 700; color: white !important; margin: 0; line-height: 1.2; }
    .app-subtitle { font-size: 16px; color: #e0e0e0 !important; font-weight: 300; margin: 0; opacity: 0.9; }
    
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #333; color: #ccc; text-align: center; padding: 10px; font-size: 12px; z-index: 100; }
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
    
    /* ✅ แก้ไข 2: เพิ่มการรองรับ Expander ให้แสดงผลถูกต้อง */
    [data-testid="stExpander"] details summary p {
        font-weight: 600 !important;
        color: #5A2D81 !important;
    }
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