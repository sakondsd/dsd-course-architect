import streamlit as st
from src.ui.user_page import render_user_page
from src.ui.admin_page import render_admin_page

# 1. Page Config: ตั้งค่าให้รองรับมือถือและจอ Wide
st.set_page_config(
    page_title="DSD Course Architect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Global CSS: ปรับแต่ง Scrollbar และ Font หลัก
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Prompt', sans-serif;
    }

    /* ปรับแต่ง Scrollbar ให้ดูโมเดิร์น */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1e1e1e; 
    }
    ::-webkit-scrollbar-thumb {
        background: #8e44ad; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #9b59b6; 
    }
</style>
""", unsafe_allow_html=True)

# 3. Main Navigation
# ซ่อน Tab Bar เดิมของ Streamlit แล้วใช้ Logic เลือกหน้าแทน หรือใช้ Tab แบบเดิมก็ได้
# ในที่นี้ใช้ Tab แบบเดิมแต่ปรับแต่งให้สวยงามใน user_page.py
tab1, tab2 = st.tabs(["🎓 ออกแบบหลักสูตร", "⚙️ จัดการระบบ"])

with tab1:
    render_user_page()

with tab2:
    render_admin_page()

# Footer Global (ถ้าต้องการให้ติดทุกหน้า)
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        © 2026 DSD Course Architect | Powered by Department of Skill Development
    </div>
    """, 
    unsafe_allow_html=True
)