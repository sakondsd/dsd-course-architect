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
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        ext = image_path.split('.')[-1].lower()
        mime_type = "jpeg" if ext in ['jpg', 'jpeg'] else "png"
        return f"data:image/{mime_type};base64,{encoded}"
    else:
        return "https://www.dsd.go.th/img/symbol/logo_dsd.png"

# ===================================================
# 2. GLOBAL CSS STYLING
# ===================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, a, button, input, label, textarea { 
        font-family: 'Prompt', sans-serif !important; 
        color: #333333 !important; /* ปรับสีตัวอักษรหลักเป็นเทาเข้ม */
        font-weight: 400 !important;
    }

    header {visibility: hidden;}
    
    /* --- HEADER STYLE --- */
    .top-nav-container { 
        display: flex; 
        justify-content: flex-start; 
        align-items: center; 
        padding: 20px 30px; 
        margin-bottom: 20px; 
        background: linear-gradient(135deg, #5A2D81 0%, #4a236e 100%); 
        border-radius: 16px; /* มนขึ้นนิดนึง */
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
    
    /* --- FOOTER STYLE (Light Theme) --- */
    .custom-footer {
        background: #FFFFFF; /* เปลี่ยนเป็นพื้นขาว */
        color: #333333;
        padding: 20px 30px; 
        border-top: 1px solid #E5E7EB; /* เส้นขอบบางๆ */
        margin-top: 50px;
        display: flex; 
        align-items: center; 
        justify-content: flex-start; 
        text-align: left;
        border-radius: 16px;
    }
    .profile-img {
        width: 60px !important; 
        height: 60px !important; 
        object-fit: cover !important;
        border-radius: 50% !important; 
        border: 2px solid #5A2D81 !important;
        margin-right: 20px !important; 
        background-color: white; 
        display: inline-block !important;
    }
    .footer-text-group { 
        display: flex; 
        flex-direction: column; 
    }
    .footer-header { 
        color: #5A2D81 !important; /* หัวข้อสีม่วง */
        font-size: 14px !important; 
        font-weight: 700 !important; 
        text-transform: uppercase; 
        margin-bottom: 5px;
    }
    .footer-text { 
        color: #6B7280 !important; /* เทา */
        font-size: 12px !important; 
        font-weight: 300 !important; 
        margin: 0;
    }
    .footer-link { 
        color: #5A2D81 !important; 
        text-decoration: none; 
        font-weight: 600 !important; 
    }
    .copyright {
        margin-top: 5px;
        font-size: 11px !important;
        opacity: 0.7;
        color: #9CA3AF !important;
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
# 4. MAIN CONTENT
# ===================================================
tab1, tab2 = st.tabs(["🎓 ออกแบบหลักสูตร (User)", "🛠️ จัดการระบบ (Admin)"])

with tab1:
    render_user_page()

with tab2:
    st.markdown("### ⚙️ ส่วนจัดการระบบ")
    render_admin_page()

# ===================================================
# 5. FOOTER SECTION
# ===================================================
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