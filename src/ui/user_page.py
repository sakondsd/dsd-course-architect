import streamlit as st
# เพิ่ม import ตัวสร้าง Word
from src.logic.doc_generator import create_word_docx 
from src.logic.ai_engine import generate_course_design
from src.logic.data_manager import search_rules

def render_user_page():
    st.header("🎓 AI Course Architect: ออกแบบหลักสูตร")
    
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("ตำแหน่งงาน (Target)", placeholder="เช่น ช่างไฟฟ้า, พนักงานบัญชี")
        problem = st.text_area("ปัญหาที่อยากแก้", placeholder="เช่น ทำงานช้า, เกิดอุบัติเหตุบ่อย")
    with col2:
        duration = st.text_input("ระยะเวลา", placeholder="เช่น 6 ชั่วโมง, 2 วัน")
        context = st.text_area("ข้อมูลเพิ่มเติม", placeholder="เช่น เน้นปฏิบัติ, มีเครื่องจักรเฉพาะ")

    if st.button("✨ ออกแบบหลักสูตร", type="primary"):
        if not job_title or not duration:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")
            return

        with st.spinner("🤖 AI กำลังค้นหากฎระเบียบและออกแบบหลักสูตร..."):
            # 1. ค้นหากฎ
            rules = search_rules(f"{job_title} {problem}")
            if not rules: rules = "ไม่พบกฎระเบียบที่เจาะจง (ใช้วิจารณญาณทั่วไป)"
            
            # 2. ให้ AI ออกแบบ
            result = generate_course_design(job_title, duration, problem, context, rules)
            
            # เก็บผลลัพธ์ลง Session เพื่อไม่ให้หายเวลาปุ่มอื่นถูกกด
            st.session_state["generated_course"] = result
            st.session_state["course_title"] = f"หลักสูตร_{job_title}"

    # --- ส่วนแสดงผลและปุ่มดาวน์โหลด ---
    if "generated_course" in st.session_state:
        st.markdown("---")
        st.subheader("✅ ผลลัพธ์การออกแบบ")
        st.markdown(st.session_state["generated_course"])
        
        st.markdown("---")
        st.markdown("### 📥 ดาวน์โหลดเอกสาร")
        
        # สร้างไฟล์ Word จากข้อความ
        docx_file = create_word_docx(st.session_state["generated_course"])
        
        st.download_button(
            label="📄 ดาวน์โหลดเป็นไฟล์ Word (.docx)",
            data=docx_file,
            file_name=f"{st.session_state['course_title']}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )