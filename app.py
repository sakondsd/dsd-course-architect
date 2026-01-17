import streamlit as st
import os
# สังเกตว่าเรา Import แค่หน้าจอ ไม่ Import Logic โดยตรง
from src.ui.admin_page import render_admin_page
from src.ui.user_page import render_user_page

# 1. ตั้งค่าหน้าจอ
st.set_page_config(
    page_title="DSD Course Architect", 
    layout="wide",
    page_icon="https://www.dsd.go.th/img/symbol/logo_dsd.png"
)

# 2. สร้างโฟลเดอร์เก็บไฟล์ถ้ายังไม่มี
if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

# ===================================================
# 🎨 3. DSD THEME
# ===================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Prompt', sans-serif; }
    h1, h2, h3, h4 { color: #5A2D81 !important; }
    .stButton>button[kind="primary"] { background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%); border: none; }
    .dsd-header-bar { background: linear-gradient(90deg, #5A2D81 0%, #7B4397 100%); height: 4px; width: 100%; margin-bottom: 20px; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ===================================================
# 4. Application Logic
# ===================================================

# Sidebar เมนู
with st.sidebar:
    if os.path.exists("dsd_logo.png"):
        st.image("dsd_logo.png", use_container_width=True) 
    
    st.title("🏗️ DSD Architect")
    st.caption("ระบบออกแบบหลักสูตรพัฒนาฝีมือแรงงาน")
    st.markdown("---")
    page = st.radio("เมนูหลัก", ["ออกแบบหลักสูตร (User)", "จัดการระบบ (Admin)"])

# Router เลือกหน้าจอ
if page == "ออกแบบหลักสูตร (User)":
    st.markdown('<div class="dsd-header-bar"></div>', unsafe_allow_html=True)
    render_user_page()
else:
    render_admin_page()