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
        ext = image_path.split('.')[-1].lower()
        mime_type = "jpeg" if ext in ['jpg', 'jpeg'] else "png"
        return f"data:image/{mime_type};base64,{encoded}"
    else:
        return "https://www.dsd.go.th/img/symbol/logo_dsd.png"

# ===================================================
# 2. PROFESSIONAL CSS
# ===================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    /* Global Font Settings */
    html, body, .stMarkdown, p, h1, h2, h3, h4, h5, h6, li, a, button, input, label, textarea { 
        font-family: 'Prompt', sans-serif !important; 
        color: #000000 !important;
        font-weight: 400 !important;
    }

    header {visibility: hidden;}
    
    /* Typography */
    h1 { font-size: 26px !important; font-weight: 700 !important; color: #5A2D81 !important; margin-bottom: 20px !important; line-height: 1.4 !important; }
    h2 { font-size: 22px !important; font-weight: 600 !important; color: #333333 !important; margin-top: 30px !important; margin-bottom: 15px !important; border-left: 5px solid #5A2D81; padding-left: 10px; }
    h3 { font-size: 18px !important; font-weight: 600 !important; color: #444444 !important; margin-top: 15px !important; }

    /* Button Fixes */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button[kind="primary"] * { color: #FFFFFF !important; font-weight: 500 !important; }

    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
    }
    [data-testid="stDownloadButton"] button * { color: #FFFFFF !important; font-weight: 500 !important; }

    /* Table Fixes */
    th { background-color: #f0f2f6; color: #5A2D81 !important; font-weight: 600 !important; font-size: 16px !important; text-align: left !important; }
    td { font-size: 15px !important; color: #000000 !important; font-weight: 400 !important; vertical-align: top !important; }
    th:first-child, td:first-child { min-width: 130px !important; white-space: nowrap !important; font-weight: 600 !important; color: #5A2D81 !important; }

    /* Header & Navigation */
    .top-nav-container { 
        display: flex; justify-content: flex-start; align-items: center; 
        padding: 20px 30px; margin-bottom: 10px; 
        background: linear-gradient(135deg, #5A2D81 0%, #4a236e 100%); 
        border-radius: 12px; box-shadow: 0 4px 15px rgba(90, 45, 129, 0.2); 
        color: white; 
    }
    .logo-img { height: 65px; width: auto; background-color: white; padding: 5px; border-radius: 50%; margin-right: 20px; }
    .app-title { font-size: 28px; font-weight: 700; color: white !important; margin: 0; line-height: 1.2; }
    .app-subtitle { font-size: 16px; color: #e0e0e0 !important; font-weight: 300; margin: 0; opacity: 0.9; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: transparent; padding-bottom: 10px; border-bottom: 1px solid #ddd; margin-top: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px; color: #666; font-size: 16px; font-weight: 500; }
    .stTabs [aria-selected="true"] { background-color: #f0f2f6; color: #5A2D81; border-bottom: 3px solid #5A2D81; font-weight: 700; }

    /* --- ✨ COMPACT & LEFT ALIGNED FOOTER ✨ --- */
    .custom-footer {
        background: linear-gradient(to right, #2c1342, #1E2A45, #2c1342); 
        color: #ffffff;
        padding: 15px 30px; 
        border-top: 3px solid #FFD700; 
        margin-top: 40px;
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
        margin-bottom: 0 !important;
        margin-right: 20px !important;
        box-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
        background-color: white;
        display: inline-block !important;
    }
    
    .footer-text-group { display: flex; flex-direction: column; }
    .footer-header { color: #FFD700; font-size: 14px !important; font-weight: 700 !important; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.5px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }
    .footer-text { color: #E0E0E0 !important; font-size: 12px !important; margin-bottom: 2px; font-weight: 300 !important; }
    .footer-link { color: #FFD700 !important; text-decoration: none; font-weight: 600 !important; transition: all 0.3s ease; }
    .footer-link:hover { text-decoration: underline; color: #ffffff !important; text-shadow: 0 0 5px #FFD700; }
    .copyright { margin-top: 5px; font-size: 10px !important; color: #aaaac0 !important; }

    /* Expander Fix */
    [data-testid="stExpander"] details summary p { font-weight: 600 !important; color: #5A2D81 !important; }

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
        <div class="app-subtitle">ระบบอัจฉริยะช่วยออกแบบหลักสูตรฝึกอบรมฝีมือแรงงาน โดย สำนักงานพัฒนาฝีมือแรงงานสกลนคร</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================================
# 4. NAVIGATION TABS
# ===================================================
tab1, tab2 = st.tabs(["🎓 ออกแบบหลักสูตร (User)", "🛠️ จัดการระบบ (Admin)"])

with tab1:
    # --- ✨ ส่วนปุ่มตัวอย่าง (Quick Start) ✨ ---
    st.markdown("### 💡 เลือกตัวอย่างหลักสูตร (คลิกเพื่อเติมข้อมูลอัตโนมัติ)")
    
    # แบ่งเป็น 3 คอลัมน์
    col_ex1, col_ex2, col_ex3 = st.columns(3)

    # 1. ปุ่มช่างไฟฟ้า
    with col_ex1:
        if st.button("⚡ ช่างไฟฟ้าภายในอาคาร", use_container_width=True):
            st.session_state["job_title"] = "ช่างไฟฟ้าภายในอาคาร ระดับ 1"
            st.session_state["duration"] = "30 ชั่วโมง (5 วัน)"
            st.session_state["objectives"] = "1. เดินสายไฟไม่สวยงามและไม่ปลอดภัย\n2. ต่อวงจรไฟฟ้าพื้นฐานผิดพลาดบ่อย\n3. ขาดความรู้เรื่องมาตรฐานความปลอดภัย"
            st.session_state["context"] = "ต้องการติวเข้มเพื่อเตรียมทดสอบมาตรฐานฝีมือแรงงานแห่งชาติ เน้นปฏิบัติ 80%"

    # 2. ปุ่มพยาบาล/ดูแลผู้สูงอายุ (ตามคำขอ)
    with col_ex2:
        if st.button("🏥 ผู้ดูแลผู้สูงอายุ/พยาบาล", use_container_width=True):
            st.session_state["job_title"] = "พนักงานดูแลผู้สูงอายุ (Caregiver)"
            st.session_state["duration"] = "18 ชั่วโมง (3 วัน)"
            st.session_state["objectives"] = "1. ขาดทักษะการปฐมพยาบาลเบื้องต้น (CPR)\n2. เคลื่อนย้ายผู้ป่วยติดเตียงผิดวิธี\n3. การวัดสัญญาณชีพและการดูแลสุขอนามัยยังไม่ถูกต้อง"
            st.session_state["context"] = "ผู้เข้าอบรมเป็นประชาชนทั่วไป เน้นฝึกปฏิบัติกับหุ่นจำลอง และการใช้เครื่องมือแพทย์เบื้องต้น"

    # 3. ปุ่มนักการตลาดออนไลน์
    with col_ex3:
        if st.button("📱 นักการตลาดออนไลน์", use_container_width=True):
            st.session_state["job_title"] = "นักการตลาดออนไลน์ (Digital Marketing)"
            st.session_state["duration"] = "12 ชั่วโมง (2 วัน)"
            st.session_state["objectives"] = "1. ถ่ายรูปสินค้าไม่สวย\n2. เขียนแคปชั่นขายของไม่ดึงดูด\n3. ยิงโฆษณาไม่ตรงกลุ่มเป้าหมาย"
            st.session_state["context"] = "เน้นการใช้ Smartphone เครื่องเดียวในการทำงาน และใช้ AI ช่วยเขียนคอนเทนต์"

    st.markdown("---") # เส้นคั่นสวยๆ
    
    # เรียกหน้า User Page ปกติ (ซึ่งจะดึงค่าจาก session_state ไปแสดง)
    render_user_page()

with tab2:
    st.markdown("###")
    render_admin_page()

# ===================================================
# 5. FOOTER
# ===================================================

# หารูปโปรไฟล์
profile_img = "logo_dsd.png"
if os.path.exists("profile.png"):
    profile_img = "profile.png"
elif os.path.exists("profile.jpg"):
    profile_img = "profile.jpg"
elif os.path.exists("image_f7b6be.jpg"):
    profile_img = "image_f7b6be.jpg"
    
profile_src = get_image_base64(profile_img)

st.markdown(f"""
<div class="custom-footer">
    <img src="{profile_src}" class="profile-img">
    <div class="footer-text-group">
        <div class="footer-header">ทีมงานผู้พัฒนา</div>
        <div class="footer-text">พบปัญหาการใช้งาน ติดต่อ นายเทอดศิลป์ โสมูล (อาร์ท)</div>
        <div class="footer-text">
            e-mail : <a href="mailto:toedsin.so@dsd.go.th" class="footer-link">toedsin.so@dsd.go.th</a>
        </div>
        <div class="copyright">
            © 2026 DSD Course Architect by SAKON-DSD
        </div>
    </div>
</div>
""", unsafe_allow_html=True)