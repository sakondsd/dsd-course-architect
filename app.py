import streamlit as st
import os
from src.ui.admin_page import render_admin_page
from src.ui.user_page import render_user_page

# ===================================================
# 1. ตั้งค่าหน้าจอ (PAGE CONFIG) - ต้องอยู่บรรทัดแรกสุด
# ===================================================
st.set_page_config(
    page_title="DSD Course Architect", 
    layout="wide",
    page_icon="https://www.dsd.go.th/img/symbol/logo_dsd.png"
)

# สร้างโฟลเดอร์เก็บไฟล์ถ้ายังไม่มี
if not os.path.exists("knowledge_base"):
    os.makedirs("knowledge_base")

# ===================================================
# 2. 🎨 CSS STYLING (ปรับแต่งความสวยงาม)
# ===================================================
st.markdown("""
<style>
    /* นำเข้าฟอนต์ Prompt */
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    /* บังคับใช้ฟอนต์ทั้งเว็บ */
    html, body, [class*="css"]  { 
        font-family: 'Prompt', sans-serif; 
    }

    /* 🟣 ปรับแต่ง Header ด้านบน */
    .header-container {
        display: flex;
        align-items: center;
        background-color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-bottom: 5px solid #5A2D81; /* สีม่วงกรมฯ */
    }
    
    .header-title {
        color: #5A2D81;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        padding-left: 20px;
    }
    
    .header-subtitle {
        color: #666;
        font-size: 16px;
        font-weight: 300;
        margin: 0;
        padding-left: 20px;
    }

    /* 🟣 ปรับแต่ง Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #ddd;
    }

    /* 🟣 Footer ด้านล่าง (Fixed Bottom) */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #5A2D81; /* สีม่วง */
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        z-index: 999;
    }
    
    /* เว้นระยะด้านล่างไม่ให้เนื้อหาโดน Footer บัง */
    .block-container {
        padding-bottom: 80px;
    }
    
    /* ปรับปุ่ม Primary ให้เป็นสีม่วง */
    .stButton>button[kind="primary"] { 
        background: linear-gradient(135deg, #5A2D81 0%, #7B4397 100%); 
        border: none; 
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================
# 3. HEADER SECTION (โลโก้ + ชื่อ อยู่ข้างบน)
# ===================================================

# ใช้ Columns แบ่งพื้นที่: ซ้าย(โลโก้) ขวา(ชื่อระบบ)
col1, col2 = st.columns([1, 6])

with col1:
    # เช็คว่ามีไฟล์โลโก้ไหม ถ้าไม่มีใช้รูป Placeholder
    if os.path.exists("dsd_logo.png"):
        st.image("dsd_logo.png", width=100)
    else:
        st.image("https://www.dsd.go.th/img/symbol/logo_dsd.png", width=100)

with col2:
    st.markdown("""
    <div style="padding-top: 10px;">
        <h1 style='margin:0; color:#5A2D81; font-size: 32px;'>DSD Course Architect</h1>
        <p style='margin:0; color:#555; font-size: 18px;'>ระบบอัจฉริยะช่วยออกแบบหลักสูตรฝึกอบรมฝีมือแรงงาน</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---") # เส้นคั่นสวยๆ

# ===================================================
# 4. SIDEBAR NAVIGATION (เมนูเลือกหน้า)
# ===================================================
with st.sidebar:
    st.header("📌 เมนูหลัก")
    
    # ใช้ radio button หรือ selectbox ก็ได้
    page = st.radio(
        "เลือกฟังก์ชันการทำงาน:",
        ["🎓 ออกแบบหลักสูตร (User)", "🛠️ จัดการระบบ (Admin)"],
        index=0
    )
    
    st.markdown("---")
    st.info("""
    **คำแนะนำ:**
    เลือกเมนู "ออกแบบหลักสูตร" เพื่อเริ่มสร้างโครงการฝึกอบรมใหม่
    """)

# ===================================================
# 5. ROUTER (ส่วนแสดงผลเนื้อหา)
# ===================================================

if "User" in page:
    render_user_page()
else:
    render_admin_page()

# ===================================================
# 6. FOOTER SECTION (ส่วนท้ายเว็บ)
# ===================================================
st.markdown("""
<div class="footer">
    © 2026 กรมพัฒนาฝีมือแรงงาน (Department of Skill Development) | 
    พัฒนาโดยทีม DSD Architect AI | 
    <a href="https://www.dsd.go.th" target="_blank" style="color: #FFD700; text-decoration: none;">www.dsd.go.th</a>
</div>
""", unsafe_allow_html=True)