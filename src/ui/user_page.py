import streamlit as st
from src.logic.data_manager import search_rules
from src.logic.ai_engine import generate_course_design

def render_user_page():
    st.header("🎓 AI Course Architect: ออกแบบหลักสูตร")
    
    col1, col2 = st.columns(2)
    with col1:
        job = st.text_input("1. ตำแหน่งงาน (Target)", placeholder="เช่น พนักงานบัญชี")
        problem = st.text_area("3. ปัญหาที่อยากแก้", placeholder="เช่น ทำงานช้า, คำนวณผิด")
    with col2:
        time = st.text_input("2. ระยะเวลา", placeholder="เช่น 6 ชั่วโมง")
        context = st.text_area("4. ข้อมูลเพิ่มเติม", placeholder="เช่น เน้นปฏิบัติ")

    if st.button("✨ ออกแบบหลักสูตร", type="primary"):
        if job and time and problem:
            with st.spinner("1/2 🔍 AI กำลังตรวจสอบกฎระเบียบ..."):
                # ค้นหากฎที่เกี่ยวกับตำแหน่งงานนั้นๆ
                rules = search_rules(f"ข้อห้าม เงื่อนไข หลักสูตร {job} {problem}")
            
            with st.spinner("2/2 🏗️ AI กำลังออกแบบโครงสร้าง..."):
                result = generate_course_design(job, time, problem, context, rules)
                
            st.markdown("### ✅ ผลลัพธ์การออกแบบ")
            st.markdown(result)
            
            with st.expander("ดูข้อมูลกฎที่ AI ใช้ตรวจสอบ"):
                st.text(rules if rules else "ไม่พบกฎเฉพาะเจาะจง (ใช้เกณฑ์ทั่วไป)")
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบ 3 ข้อแรก")