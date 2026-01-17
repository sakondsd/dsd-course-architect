import streamlit as st
import os
from src.ui.admin_page import render_admin_page
from src.ui.user_page import render_user_page

# 1. ตั้งค่าหน้าจอ basic
st.set_page_config(
    page_title="DSD Course Architect", 
    layout="wide",
    page_icon="https://www.dsd.go.th/img/symbol/logo_dsd.png"
)

# 2. สร้างโฟลเดอร์เก็บไฟล์ถ้ายังไม่มี
if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

# ===================================================
# 🎨 3. DSD THEME (Light Mode: White/Purple/Yellow)
# ===================================================
st.markdown("""
<style>
    /* Import Font: Prompt */
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

    /* Global Settings - พื้นหลังขาว ตัวหนังสือเข้ม */
    html, body, [class*="css"]  {
        font-family: 'Prompt', sans-serif;
        color: #333333; /* สีเทาเข้มเกือบดำ */
        background-color: #FFFFFF; /* สีขาว */
    }

    /* Headers - สีม่วงกรมฯ */
    h1, h2, h3, h4 {
        color: #5A2D81 !important; /* DSD Purple */
        font-weight: 600 !important;
    }
    
    /* Sidebar - สีพื้นหลังเทาอมม่วงอ่อนๆ */
    section[data-testid="stSidebar"] {
        background-color: #F9F7FC;
        border-right: 1px solid #E5D9F2;
    }
    
    /* Buttons (Primary) - ไล่สีม่วง */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
    }
    /* Buttons (Secondary) - ขอบม่วง พื้นขาว */
    .stButton>button[kind="secondary"] {
        color: #5A2D81;
        border: 1px solid #5A2D81;
        background-color: white;
        border-radius: 8px;
    }

    /* Input Fields - ขอบเรียบ พื้นขาว */
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF;
        border: 1px solid #D0D0D0;
        border-radius: 8px;
        color: #333333;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #5A2D81;
        box-shadow: 0 0 0 1px #5A2D81;
    }
    
    /* Accent Highlights (เช่น เส้นคั่น, info box) - ใช้สีเหลือง/ทอง DSD */
    hr {
        border-color: #F2A900; /* DSD Yellow/Gold */
        opacity: 0.3;
    }
    .stAlert[data-baseweb="notification"] {
        border-left-color: #F2A900 !important;
    }
    
    /* Custom Header Bar (แถบสีม่วงคาดบน) */
    .dsd-header-bar {
        background: linear-gradient(90deg, #5A2D81 0%, #7B4397 100%);
        height: 4px;
        width: 100%;
        margin-bottom: 20px;
        border-radius: 2px;
    }
    
    /* Result Card (การ์ดแสดงผลลัพธ์) */
    .result-card {
        background-color: #FDFDFD;
        border: 1px solid #EEEEEE;
        border-top: 4px solid #F2A900; /* หัวสีเหลือง */
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

</style>
""", unsafe_allow_html=True)

# ===================================================
# 4. Application Logic
# ===================================================

# Sidebar เมนู
with st.sidebar:
    # ✅ 1. ใส่โค้ดแสดงโลโก้ตรงนี้ (บรรทัดบนสุดของ sidebar)
    # ตรวจสอบว่ามีไฟล์อยู่จริงไหม เพื่อป้องกัน Error
    if os.path.exists("logo.png"):
        # use_container_width=True จะทำให้รูปขยายเต็มความกว้าง sidebar สวยงาม
        st.image("logo.png", use_container_width=True) 
    else:
        # ถ้าหาไฟล์ไม่เจอ ให้แสดงข้อความเตือนบางๆ
        st.caption("⚠️ ไม่พบไฟล์ logo.png")

    st.markdown("---") # เส้นคั่นเล็กน้อยเพื่อความสวยงาม

    # (โค้ดเดิมของคุณต่อจากนี้)
    st.title("🏗️ DSD Architect")
    st.caption("ระบบออกแบบหลักสูตรพัฒนาฝีมือแรงงาน")
    st.markdown("---")
    page = st.radio("เมนูหลัก", ["ออกแบบหลักสูตร (User)", "จัดการระบบ (Admin)"])

# Router เลือกหน้าจอ
if page == "ออกแบบหลักสูตร (User)":
    # เพิ่มแถบสีด้านบนในหน้า User
    st.markdown('<div class="dsd-header-bar"></div>', unsafe_allow_html=True)
    render_user_page()
else:
    render_admin_page()