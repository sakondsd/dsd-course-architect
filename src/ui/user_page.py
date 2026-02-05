import streamlit as st
from src.logic.doc_generator import create_word_docx 
from src.logic.ai_engine import generate_course_design
from src.logic.data_manager import search_rules
from src.logic.chat_consultant import consult_and_fill
from langchain_core.messages import HumanMessage, AIMessage

def render_user_page():
    # --- 1. Initialize Session ---
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            AIMessage(content="สวัสดีครับ! ผมคือ AI ผู้ช่วยออกแบบหลักสูตร\nมีไอเดียอยากจัดอบรมเรื่องอะไร บอกผมได้เลย หรือเลือกตัวอย่างทางขวามือก็ได้ครับ")
        ]
    
    # --- 2. CSS & STYLING (ฉบับแก้ไข: จัดระเบียบปุ่ม + บังคับสีพื้นหลัง) ---
    st.markdown("""
    <style>
        /* ----------------------------------------------------
           1. บังคับสีพื้นหลังกล่อง Chat (สีเทา)
           ---------------------------------------------------- */
        /* เจาะจงไปที่กล่องที่มีข้อความ Chat อยู่ข้างใน */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.stChatMessage) {
            background-color: #F0F2F6 !important; /* สีเทา */
            border: 2px solid #E0E0E0 !important;
        }
        /* บังคับทุก Layer ข้างในให้เป็นสีเทาด้วย (แก้ปัญหาพื้นหลังขาวซ้อน) */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.stChatMessage) > div,
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.stChatMessage) > div > div {
            background-color: #F0F2F6 !important;
        }

        /* ----------------------------------------------------
           2. ปรับแต่ง Bubble ข้อความ
           ---------------------------------------------------- */
        /* User (เรา) - สีม่วง */
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) {
            flex-direction: row-reverse;
            text-align: right;
        }
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) div[data-testid="stMarkdownContainer"] {
            background-color: #5A2D81;
            color: #FFFFFF !important;
            padding: 10px 18px;
            border-radius: 20px 20px 5px 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) p { color: #FFFFFF !important; }

        /* AI (บอท) - สีขาว */
        [data-testid="stChatMessage"]:has(div[aria-label="assistant"]) {
            flex-direction: row;
            text-align: left;
        }
        [data-testid="stChatMessage"]:has(div[aria-label="assistant"]) div[data-testid="stMarkdownContainer"] {
            background-color: #FFFFFF;
            color: #333333 !important;
            padding: 10px 18px;
            border-radius: 20px 20px 20px 5px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
            border: 1px solid #E5E7EB;
        }
        .stChatMessageAvatarImage { display: none; }

        /* ----------------------------------------------------
           3. ปรับแต่งช่องพิมพ์และปุ่มส่ง (Layout ใหม่)
           ---------------------------------------------------- */
        /* ปรับช่องพิมพ์ให้มนขึ้น */
        .stTextInput input {
            border-radius: 30px !important;
            border: 1px solid #D1D5DB;
            padding-left: 15px;
        }
        
        /* ปรับปุ่มส่ง (จรวด) ให้เป็นวงกลมสวยๆ หรือสี่เหลี่ยมมน */
        div[data-testid="stFormSubmitButton"] > button {
            border-radius: 50% !important; /* ทำเป็นปุ่มกลม */
            height: 45px;
            width: 45px;
            padding: 0 !important;
            border: none;
            background-color: #5A2D81;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            float: right; /* ชิดขวา */
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #4a236e;
            color: #FFD700;
        }
        
        /* จัดตำแหน่งปุ่มให้ตรงกับช่องพิมพ์ */
        [data-testid="stForm"] [data-testid="column"]:nth-child(2) {
            display: flex;
            align-items: flex-end; /* ดันปุ่มลงมาข้างล่างให้เสมอช่องพิมพ์ */
            justify-content: center;
        }

        /* ----------------------------------------------------
           4. ปุ่ม Quick Start (ขวามือ)
           ---------------------------------------------------- */
        div.stButton > button {
            width: 100%;
            border-radius: 12px;
            height: 3.5em;
            border: 1px solid #5A2D81;
            color: #5A2D81;
            background-color: white;
            font-weight: 500;
        }
        div.stButton > button:hover {
            background-color: #F3E5F5;
            border-color: #5A2D81;
        }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 🖥️ LAYOUT: แบ่ง 2 คอลัมน์ (ซ้าย 65% | ขวา 35%)
    # ==========================================
    col_chat, col_examples = st.columns([0.65, 0.35], gap="large")

    # 🔴 ส่วนซ้าย: Chat + Input (รวมอยู่ในคอลัมน์นี้ตามภาพวาด)
    with col_chat:
        st.markdown("##### 🤖 คุยกับ AI เพื่อร่างหลักสูตร")
        
        # 1. Chat Box (Container)
        chat_container = st.container(height=480, border=True)
        
        with chat_container:
            for msg in st.session_state["chat_history"]:
                if isinstance(msg, HumanMessage):
                    with st.chat_message("user"):
                        st.markdown(msg.content)
                elif isinstance(msg, AIMessage):
                    with st.chat_message("assistant"):
                        st.markdown(msg.content)

        # 2. Input Area (Form) - วางไว้ใต้ Chat Box ทันที
        with st.form(key="chat_form", clear_on_submit=True):
            # แบ่งคอลัมน์สำหรับ "ช่องพิมพ์" (85%) และ "ปุ่มส่ง" (15%)
            c_input, c_btn = st.columns([0.85, 0.15])
            
            with c_input:
                user_input = st.text_input(
                    "พิมพ์ข้อความ...", 
                    label_visibility="collapsed", 
                    placeholder="พิมพ์ไอเดียที่นี่... (กด Enter เพื่อส่ง)"
                )
            
            with c_btn:
                # ปุ่มส่งรูปจรวด
                submitted = st.form_submit_button("🚀")

            if submitted and user_input:
                # 2.1 แสดงข้อความ User
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(user_input)
                st.session_state["chat_history"].append(HumanMessage(content=user_input))
                
                # 2.2 AI ตอบกลับ
                with chat_container:
                    with st.chat_message("assistant"):
                        with st.spinner("..."):
                            response_text, extracted_data = consult_and_fill(st.session_state["chat_history"], user_input)
                            st.markdown(response_text)
                st.session_state["chat_history"].append(AIMessage(content=response_text))
                
                # 2.3 Auto Fill
                if extracted_data:
                    st.session_state["job_title"] = extracted_data.get("job_title", "")
                    st.session_state["duration"] = extracted_data.get("duration", "")
                    st.session_state["objectives"] = extracted_data.get("objectives", "")
                    st.session_state["context"] = extracted_data.get("context", "")
                    
                    final_msg = "✅ **ผมเติมข้อมูลลงในแบบฟอร์มด้านล่างให้เรียบร้อยแล้วครับ!**"
                    st.session_state["chat_history"].append(AIMessage(content=final_msg))
                    st.rerun()

    # 🟠 ส่วนขวา: Quick Start (แยกออกมาอยู่อีกคอลัมน์)
    with col_examples:
        st.markdown("##### 💡 เลือกตัวอย่าง (Quick Start)")
        st.caption("คลิกเพื่อเติมข้อมูลอัตโนมัติ")
        
        with st.container(border=True):
            if st.button("⚡ ช่างไฟฟ้าภายในอาคาร"):
                st.session_state["job_title"] = "ช่างไฟฟ้าภายในอาคาร ระดับ 1"
                st.session_state["duration"] = "30 ชั่วโมง (5 วัน)"
                st.session_state["objectives"] = "เดินสายไฟไม่สวยงาม, ต่อวงจรผิดพลาดบ่อย"
                st.session_state["context"] = "เน้นปฏิบัติ 80%, เตรียมทดสอบมาตรฐาน"
                st.toast("✅ โหลดข้อมูลเรียบร้อย!")
                st.rerun()

            if st.button("🏥 ผู้ดูแลผู้สูงอายุ"):
                st.session_state["job_title"] = "พนักงานดูแลผู้สูงอายุ (Caregiver)"
                st.session_state["duration"] = "18 ชั่วโมง (3 วัน)"
                st.session_state["objectives"] = "ขาดทักษะปฐมพยาบาล, เคลื่อนย้ายผู้ป่วยผิดวิธี"
                st.session_state["context"] = "เน้นฝึกกับหุ่นจำลอง"
                st.toast("✅ โหลดข้อมูลเรียบร้อย!")
                st.rerun()

            if st.button("📱 นักการตลาดออนไลน์"):
                st.session_state["job_title"] = "นักการตลาดออนไลน์"
                st.session_state["duration"] = "12 ชั่วโมง (2 วัน)"
                st.session_state["objectives"] = "เขียนแคปชั่นไม่ดึงดูด, ยิงโฆษณาไม่ตรงกลุ่ม"
                st.session_state["context"] = "เน้นใช้ Smartphone และ AI ช่วยทำงาน"
                st.toast("✅ โหลดข้อมูลเรียบร้อย!")
                st.rerun()
                
            if st.button("📊 Power BI หัวหน้างาน"):
                st.session_state["job_title"] = "หัวหน้างาน/ผู้จัดการ"
                st.session_state["duration"] = "12 ชั่วโมง (2 วัน)"
                st.session_state["objectives"] = "วิเคราะห์ข้อมูลช้า, ทำ Dashboard ไม่เป็น"
                st.session_state["context"] = "ผู้เรียนพอมีพื้นฐาน Excel มาบ้าง"
                st.toast("✅ โหลดข้อมูลเรียบร้อย!")
                st.rerun()

    st.markdown("---")

    # ==========================================
    # 📝 Form Section (ส่วนตรวจสอบข้อมูล)
    # ==========================================
    with st.expander("📝 ตรวจสอบและแก้ไขข้อมูล (คลิกเพื่อเปิด)", expanded=True):
        st.markdown("##### รายละเอียดโครงการ")
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("1. ตำแหน่งงาน/กลุ่มเป้าหมาย", key="job_title")
            problem = st.text_area("3. ปัญหา/สิ่งที่ต้องการพัฒนา", height=150, key="objectives")
        with col2:
            duration = st.text_input("2. ระยะเวลาฝึกอบรม", key="duration")
            context = st.text_area("4. บริบทเพิ่มเติม", height=150, key="context")

        generate_btn = st.button("✨ สร้างหลักสูตร (Generate Course)", type="primary", use_container_width=True)

    # ==========================================
    # 🚀 Process
    # ==========================================
    if generate_btn:
        if not job_title or not duration:
            st.warning("⚠️ กรุณากรอกข้อมูลให้ครบถ้วน")
            return

        with st.spinner("🤖 AI กำลังค้นหากฎระเบียบและออกแบบหลักสูตร..."):
            rules = search_rules(f"{job_title} {problem}")
            if not rules: rules = "ไม่พบกฎระเบียบที่เจาะจง"
            
            result = generate_course_design(job_title, duration, problem, context, rules)
            
            st.session_state["generated_course"] = result
            st.session_state["course_title"] = f"หลักสูตร_{job_title}"

    if "generated_course" in st.session_state:
        st.divider()
        st.subheader("✅ ผลลัพธ์การออกแบบ")
        with st.container(border=True):
            st.markdown(st.session_state["generated_course"])
        
        docx_file = create_word_docx(st.session_state["generated_course"])
        st.download_button(
            label="📄 ดาวน์โหลดไฟล์ Word",
            data=docx_file,
            file_name=f"{st.session_state.get('course_title', 'Course')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary"
        )