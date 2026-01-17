import streamlit as st
import os
import PyPDF2
from src.logic.ai_engine import extract_rules_from_pdf_text as extract_rules_from_text
from src.logic.data_manager import rebuild_knowledge_base

KB_FOLDER = "knowledge_base"
ADMIN_PASSWORD = "12345"  # 🔑 กำหนดรหัสผ่านตรงนี้ (เปลี่ยนได้ตามใจชอบ)

def render_admin_page():
    st.header("🛠️ Admin Panel: จัดการกฎระเบียบ")

    # =========================================
    # 🔐 ส่วนตรวจสอบรหัสผ่าน (Password Check)
    # =========================================
    # 1. เช็คว่ามีตัวแปรเก็บสถานะการ Login หรือยัง
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    # 2. ถ้ายังไม่ Login -> แสดงช่องกรอกรหัส
    if not st.session_state.admin_logged_in:
        st.info("🔒 หน้านี้จำกัดสิทธิ์เฉพาะผู้ดูแลระบบ")
        password_input = st.text_input("กรุณาใส่รหัสผ่าน (Password):", type="password")
        
        if st.button("เข้าสู่ระบบ (Login)"):
            if password_input == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("เข้าสู่ระบบสำเร็จ!")
                st.rerun() # รีโหลดหน้าเพื่อแสดงเนื้อหา
            else:
                st.error("❌ รหัสผ่านไม่ถูกต้อง")
        
        # หยุดการทำงานฟังก์ชันไว้แค่นี้ ถ้ายังไม่ Login ไม่ต้องโชว์ข้างล่าง
        return 

    # =========================================
    # ✅ ส่วนเนื้อหา Admin (จะโชว์เฉพาะตอน Login แล้ว)
    # =========================================
    
    # ปุ่ม Logout (เผื่ออยากออก)
    if st.button("ออกจากระบบ (Logout)", type="secondary"):
        st.session_state.admin_logged_in = False
        st.rerun()

    st.divider()

    # =========================================
    # ส่วนที่ 1: AI Rule Extractor (สร้างกฎใหม่)
    # =========================================
    st.markdown("### 1. AI Rule Extractor (สร้างกฎใหม่)")
    st.info("อัปโหลดไฟล์ (PDF หรือ TXT) เพื่อให้ AI ช่วยสรุปเป็นกฎแบบมีตัวคั่น")
    
    uploaded_file = st.file_uploader("เลือกไฟล์ต้นฉบับ", type=["pdf", "txt"], key="rule_extractor")
    
    if uploaded_file:
        # เช็คขนาดไฟล์ก่อนเลย
        if uploaded_file.size == 0:
            st.error("⚠️ ไฟล์นี้ว่างเปล่า (0 Bytes) กรุณาตรวจสอบไฟล์ต้นฉบับ")
        else:
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if st.button(f"✨ แปลงไฟล์ {file_type.upper()} เป็นกฎ"):
                with st.spinner("AI กำลังอ่านและแกะกฎ..."):
                    raw_text = ""
                    try:
                        # กรณี PDF
                        if file_type == 'pdf':
                            reader = PyPDF2.PdfReader(uploaded_file)
                            raw_text = "".join([p.extract_text() for p in reader.pages])
                        
                        # กรณี TXT (เพิ่มระบบรองรับภาษาไทย Windows)
                        elif file_type == 'txt':
                            bytes_data = uploaded_file.getvalue()
                            try:
                                # ลองอ่านแบบ UTF-8 ก่อน (มาตรฐานสากล)
                                raw_text = bytes_data.decode("utf-8")
                            except UnicodeDecodeError:
                                try:
                                    # ถ้าไม่ได้ ให้ลองอ่านแบบ Windows Thai (CP874)
                                    raw_text = bytes_data.decode("cp874")
                                except:
                                    st.error("❌ อ่านไฟล์ภาษาไทยไม่ได้ กรุณา Save ไฟล์เป็น UTF-8")
                                    return

                        # ส่งข้อความดิบไปให้ AI สรุป
                        if raw_text and len(raw_text.strip()) > 0:
                            rules = extract_rules_from_text(raw_text)
                            st.session_state["draft_rules"] = rules
                            st.session_state["draft_filename"] = f"กฎ_{uploaded_file.name}"
                            st.success("✅ อ่านไฟล์สำเร็จ! กำลังประมวลผล...")
                        else:
                            st.error("⚠️ อ่านไฟล์ได้ แต่ไม่พบข้อความข้างใน (Text is empty)")
                            
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
    
    # ส่วนแสดงผลลัพธ์และบันทึก
    if "draft_rules" in st.session_state:
        st.markdown("#### 📝 ตรวจสอบผลลัพธ์")
        edited_rules = st.text_area("แก้ไขกฎก่อนบันทึก:", st.session_state["draft_rules"], height=300)
        
        suggested_name = st.session_state.get("draft_filename", "rules_extracted.txt")
        save_name = st.text_input("ชื่อไฟล์ที่จะบันทึก:", value=suggested_name)

        if st.button("💾 บันทึกลงระบบ"):
            if not save_name.endswith('.txt'): save_name += ".txt"
            
            # บันทึกไฟล์ลง folder
            save_path = os.path.join(KB_FOLDER, save_name)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(edited_rules)
            
            st.success(f"บันทึกไฟล์ {save_path} เรียบร้อย!")
            
            # ล้างค่า session
            del st.session_state["draft_rules"]
            if "draft_filename" in st.session_state: del st.session_state["draft_filename"]
            st.rerun()

    st.markdown("---")
    # =========================================
    # ส่วนที่ 2: อัปเดตสมอง AI
    # =========================================
    st.markdown("### 2. อัปเดตสมอง AI")
    st.caption("กดปุ่มนี้ทุกครั้งที่มีการเพิ่มไฟล์กฎใหม่ลงในโฟลเดอร์ knowledge_base")
    if st.button("🔄 Re-index Knowledge Base", type="primary"):
        with st.spinner("กำลังสร้างฐานข้อมูลใหม่..."):
            msg = rebuild_knowledge_base()
            st.success(msg)