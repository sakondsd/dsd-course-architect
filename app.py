import streamlit as st
import os
import base64
from src.ui.admin_page import render_admin_page
from src.ui.user_page import render_user_page

# ===================================================
# 1. SETUP & CONFIGURATION
# ===================================================
st.set_page_config(
    page_title="DSD Course Architect", 
    layout="wide",
    page_icon="logo_dsd.png" if os.path.exists("logo_dsd.png") else "https://www.dsd.go.th/img/symbol/logo_dsd.png",
    initial_sidebar_state="collapsed"
)

# สร้างโฟลเดอร์เก็บข้อมูลถ้ายังไม่มี
if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

def get_image_base64(image_path):
    """แปลงไฟล์รูปภาพเป็น Base64 สำหรับแสดงผลใน HTML"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        ext = image_path.split('.')[-1].lower()
        mime_type = "jpeg" if ext in ['jpg', 'jpeg'] else "png"
        return f"data:image/{mime_type};base64,{encoded}"
    else:
        # รูปสำรองถ้าหาไฟล์ไม่เจอ
        return "https://www.dsd.go.th/img/symbol/logo_dsd.png"

# ===================================================
# 2. GLOBAL CSS STYLING
# ===================================================
st.markdown("""
<style>
    /* นำเข้าฟอนต์ Prompt */
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    /* บังคับใช้ฟอนต์ Prompt ทั้งหมด */
    html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, a, button, input, label, textarea { 
        font-family: 'Prompt', sans-serif !important; 
        color: #000000 !important;
        font-weight: 400 !important;
    }

    /* ซ่อน Header มาตรฐานของ Streamlit */
    header {visibility: hidden;}
    
    /* --- HEADER STYLE --- */
    .top-nav-container { 
        display: flex; 
        justify-content: flex-start; 
        align-items: center; 
        padding: 20px 30px; 
        margin-bottom: 20px; 
        background: linear-gradient(135deg, #5A2D81 0%, #4a236e 100%); /* สีม่วง DSD */
        border-radius: 12px; 
        box-shadow: 0 4px 15px rgba(90, 45, 129, 0.2); 
        color: white; 
    }
    .logo-img { 
        height: 65px; 
        width: auto; 
        background-color: white; 
        padding: 5px; 
        border-radius: 50%; 
        margin-right: 20px; 
    }
    .app-title { 
        font-size: 28px; 
        font-weight: 700; 
        color: white !important; 
        margin: 0; 
        line-height: 1.2; 
    }
    .app-subtitle { 
        font-size: 16px; 
        color: #e0e0e0 !important; 
        font-weight: 300; 
        margin: 0; 
        opacity: 0.9; 
    }
    
    /* --- FOOTER STYLE --- */
    .custom-footer {
        background: linear-gradient(to right, #2c1342, #1E2A45, #2c1342); 
        color: #ffffff;
        padding: 20px 30px; 
        border-top: 3px solid #FFD700; /* เส้นสีทอง */
        margin-top: 50px;
        box-shadow: 0 -5px 15px rgba(0,0,0,0.2);
        display: flex; 
        align-items: center; 
        justify-content: flex-start; 
        text-align: left;
    }
    .profile-img {
        width: 65px !important; 
        height: 65px !important; 
        object-fit: cover !important;
        border-radius: 50% !important; 
        border: 2px solid #FFD700 !important;
        margin-right: 20px !important; 
        background-color: white; 
        display: inline-block !important;
    }
    .footer-text-group { 
        display: flex; 
        flex-direction: column; 
    }
    .footer-header { 
        color: #FFD700 !important; /* สีทอง */
        font-size: 14px !important; 
        font-weight: 700 !important; 
        text-transform: uppercase; 
        margin-bottom: 5px;
    }
    .footer-text { 
        color: #E0E0E0 !important; 
        font-size: 12px !important; 
        font-weight: 300 !important; 
        margin: 0;
    }
    .footer-link { 
        color: #FFD700 !important; 
        text-decoration: none; 
        font-weight: 600 !important; 
    }
    .copyright {
        margin-top: 5px;
        font-size: 11px !important;
        opacity: 0.7;
        color: #aaa !important;
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
# 4. MAIN CONTENT (TABS)
# ===================================================
tab1, tab2 = st.tabs(["🎓 ออกแบบหลักสูตร (User)", "🛠️ จัดการระบบ (Admin)"])

with tab1:
    # เรียกใช้ User Page (รวม Chat และ ปุ่มเลือกตัวอย่างไว้ข้างในแล้ว)
    render_user_page()

with tab2:
    st.markdown("### ⚙️ ส่วนจัดการระบบ")
    render_admin_page()

# ===================================================
# 5. FOOTER SECTION
# ===================================================
# หารูป profile.png (ถ้ามี) หรือใช้ logo แทน
profile_src = get_image_base64("profile.jpg" if os.path.exists("profile.jpg") else "logo_dsd.png")

st.markdown(f"""
<div class="custom-footer">
    <img src="{profile_src}" class="profile-img">
    <div class="footer-text-group">
        <div class="footer-header">ทีมงานผู้พัฒนา</div>
        <div class="footer-text">พบปัญหาการใช้งาน ติดต่อ นายเทอดศิลป์ โสมูล (อาร์ท)</div>
        <div class="footer-text">e-mail : <a href="mailto:toedsin.so@dsd.go.th" class="footer-link">toedsin.so@dsd.go.th</a></div>
        <div class="copyright">© 2026 DSD Course Architect by SAKON-DSD. All rights reserved.</div>
    </div>
</div>
""", unsafe_allow_html=True)