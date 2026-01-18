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
# 2. PROFESSIONAL CSS
# ===================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  { font-family: 'Prompt', sans-serif; }
    header {visibility: hidden;}
    
    /* Tabs styling */
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

    /* Dark Header */
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

    .app-title {
        font-size: 28px; font-weight: 700; color: white !important;
        margin: 0; line-height: 1.2;
    }
    .app-subtitle {
        font-size: 16px; color: #e0e0e0 !important; font-weight: 300; margin: 0; opacity: 0.9;
    }
    
    /* Footer */
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #333; color: #ccc;
        text-align: center; padding: 10px; font-size: 12px; z-index: 100;
    }
    
    .block-container { padding-top: 1rem; padding-bottom: 5rem; }
</style>
""", unsafe_allow_html=True)

# ===================================================
# 3. HEADER SECTION (Clean Version)
# ===================================================

logo_src = get_image_base64("logo_dsd.png")

# ไม่แบ่งคอลัมน์แล้ว ใช้พื้นที่เต็มเลยให้ดูสง่า
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