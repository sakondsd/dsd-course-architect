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
    
    # --- 2. CSS & STYLING (ฉบับจัดระเบียบ + แก้สีปุ่ม) ---
    st.markdown("""
    <style>
        /* ================= 1. CARDS & CONTAINERS ================= */
        /* บังคับให้ st.container(border=True) ทุกตัวเป็น Card สีขาวลอยขึ้นมา */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E5E7EB !important;
            border-radius: 16px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
            padding: 20px !important;
        }
        
        /* ถมสีขาวลงไปข้างใน Card */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            background-color: #FFFFFF !important;
        }

        /* ================= 2. CHAT BUBBLES ================= */
        /* User (เรา) - สีม่วง */
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) div[data-testid="stMarkdownContainer"] {
            background-color: #5A2D81 !important;
            color: #FFFFFF !important;
            padding: 12px 18px;
            border-radius: 18px 18px 4px 18px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) p { color: #FFFFFF !important; }

        /* AI (บอท) - สีเทาอ่อน */
        [data-testid="stChatMessage"]:has(div[aria-label="assistant"]) div[data-testid="stMarkdownContainer"] {
            background-color: #F3F4F6 !important;
            color: #1F2937 !important;
            padding: 12px 18px;
            border-radius: 18px 18px 18px 4px;
        }
        .stChatMessageAvatarImage { display: none; }

        /* ================= 3. INPUT & BUTTONS ALIGNMENT (แก้จุดที่ 1) ================= */
        /* ช่องพิมพ์ข้อความ */
        .stTextArea textarea {
            border-radius: 25px !important; /* มนเหมือนแคปซูล */
            border: 1px solid #D1D5DB !important;
            background-color: #F0F2F6 !important; /* พื้นเทาอ่อนให้เห็นชัด */
            height: 50px !important; /* กำหนดความสูงแน่นอน */
            resize: none;
            padding: 12px 20px;
        }
        .stTextArea textarea:focus {
            border-color: #5A2D81 !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 0 0 1px #5A2D81 !important;
        }
        .stTextArea label { display: none; }

        /* ปุ่มส่ง (วงกลม) */
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #5A2D81 !important;
            color: #FFFFFF !important;
            border-radius: 50% !important;
            height: 50px !important; /* สูงเท่าช่องพิมพ์เป๊ะๆ */
            width: 50px !important;  /* กว้างเท่ากันให้เป็นวงกลม */
            border: none !important;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 2px 5px rgba(90, 45, 129, 0.2) !important;
            margin: 0 !important; /* ลบ margin ที่อาจทำให้เบี้ยว */
        }
        /* ไอคอนในปุ่มส่ง */
        div[data-testid="stFormSubmitButton"] > button p {
            font-size: 20px !important;
            margin: 0 !important;
            padding-bottom: 2px !important; /* ดันไอคอนขึ้นนิดนึงให้ดู center จริงๆ */
            color: #FFFFFF !important;
        }
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: scale(1.05);
            background-color: #4a236e !important;
        }
        
        /* จัดให้ช่องพิมพ์และปุ่มอยู่ในระนาบเดียวกัน (Align Bottom/Center) */
        [data-testid="stForm"] [data-testid="column"] {
             display: flex;
             align-items: flex-end; /* จัดให้ก้นเสมอกัน */
        }

        /* ================= 4. QUICK START BUTTONS ================= */
        button[kind="secondary"] {
            background-color: #FFFFFF !important;
            color: #4B5563 !important;
            border: 1px solid #E5E7EB !important;
            border-left: 5px solid #5A2D81 !important;
            border-radius: 8px !important;
            height: auto !important;
            padding: 15px !important;
            font-weight: 500 !important;
            justify-content: flex-start !important;
            text-align: left !important;
            transition: all 0.2s;
        }
        button[kind="secondary"]:hover {
            border-color: #5A2D81 !important;
            background-color: #F9FAFB !important;
            color: #5A2D81 !important;
            transform: translateX(4px) !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        }
        
        /* ================= 5. GENERATE BUTTON COLOR (แก้จุดที่ 2) ================= */
        /* ปุ่มสร้างหลักสูตร (Primary Button) */
        button[kind="primary"] {
            background-color: #5A2D81 !important;
            color: #FFFFFF !important; /* บังคับสีขาว */
            border: none !important;
            border-radius: 10px !important;
            height: 3.5em;
            font-weight: 600 !important;
            box-shadow: 0 4px 10px rgba(90, 45, 129, 0.3) !important;
        }
        /* บังคับตัวอักษรข้างในให้ขาวด้วย */
        button[kind="primary"] p {
            color: #FFFFFF !important;
        }
        button[kind="primary"]:hover {
            background-color: #432063 !important;
            box-shadow: 0 6px 12px rgba(90, 45, 129, 0.4) !important;
            color: #FFFFFF !important;
        }
        button[kind="primary"]:hover p {
            color: #FFFFFF !important;
        }

    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 🖥️ LAYOUT STRUCTURE
    # ==========================================
    
    col_chat, col_quick = st.columns([0.65, 0.35], gap="medium")

    # 🟢 LEFT COLUMN: CHAT INTERFACE
    with col_chat:
        st.markdown("##### 🤖 DSD Course Assistant")
        
        # กล่อง Card สีขาว (Container)
        with st.container(border=True):
            
            # 1. Chat History Area (Scrollable)
            chat_box = st.container(height=420, border=False)
            with chat_box:
                for msg in st.session_state["chat_history"]:
                    if isinstance(msg, HumanMessage):
                        with st.chat_message("user"):
                            st.markdown(msg.content)
                    elif isinstance(msg, AIMessage):
                        with st.chat_message("assistant"):
                            st.markdown(msg.content)

            # 2. Input Area
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            
            with st.form(key="chat_form", clear_on_submit=True):
                # ปรับสัดส่วนคอลัมน์เล็กน้อยเพื่อให้ปุ่มกลมพอดี
                c_input, c_btn = st.columns([0.88, 0.12], gap="small")
                
                with c_input:
                    user_input = st.text_area(
                        "Message",
                        placeholder="พิมพ์ไอเดียที่นี่... (เช่น 'อบรม Excel ให้ฝ่ายบัญชี')",
                        height=50 # ความสูงต้องตรงกับ CSS
                    )
                
                with c_btn:
                    # ปุ่มส่ง
                    submitted = st.form_submit_button("➤")

                if submitted and user_input:
                    with chat_box:
                        with st.chat_message("user"):
                            st.markdown(user_input)
                    st.session_state["chat_history"].append(HumanMessage(content=user_input))
                    
                    with chat_box:
                        with st.chat_message("assistant"):
                            with st.spinner("กำลังคิด..."):
                                response_text, extracted_data = consult_and_fill(st.session_state["chat_history"], user_input)
                                st.markdown(response_text)
                    st.session_state["chat_history"].append(AIMessage(content=response_text))
                    
                    if extracted_data:
                        st.session_state.update(extracted_data)
                        st.rerun()

    # 🟠 RIGHT COLUMN: QUICK START
    with col_quick:
        st.markdown("##### 💡 Quick Start")
        st.caption("เลือกตัวอย่างเพื่อเริ่มทันที")
        
        # ปุ่มเหล่านี้ Streamlit จะให้เป็น kind="secondary" โดยอัตโนมัติ (เข้ากับ CSS ข้างบน)
        if st.button("⚡ ช่างไฟฟ้าภายในอาคาร\n(หลักสูตรมาตรฐาน 30 ชม.)"):
            st.session_state.update({
                "job_title": "ช่างไฟฟ้าภายในอาคาร ระดับ 1",
                "duration": "30 ชั่วโมง (5 วัน)",
                "objectives": "เดินสายไฟไม่สวยงาม, ต่อวงจรผิดพลาดบ่อย",
                "context": "เน้นปฏิบัติ 80%, เตรียมทดสอบมาตรฐาน"
            })
            st.toast("โหลดข้อมูลแล้ว!", icon="⚡")
            st.rerun()

        if st.button("🏥 ผู้ดูแลผู้สูงอายุ\n(เน้นปฏิบัติจริง 18 ชม.)"):
            st.session_state.update({
                "job_title": "พนักงานดูแลผู้สูงอายุ (Caregiver)",
                "duration": "18 ชั่วโมง (3 วัน)",
                "objectives": "ขาดทักษะปฐมพยาบาล, เคลื่อนย้ายผู้ป่วยผิดวิธี",
                "context": "เน้นฝึกกับหุ่นจำลอง"
            })
            st.toast("โหลดข้อมูลแล้ว!", icon="🏥")
            st.rerun()

        if st.button("📱 นักการตลาดออนไลน์\n(Upskill AI & Content)"):
            st.session_state.update({
                "job_title": "นักการตลาดออนไลน์",
                "duration": "12 ชั่วโมง (2 วัน)",
                "objectives": "เขียนแคปชั่นไม่ดึงดูด, ยิงโฆษณาไม่ตรงกลุ่ม",
                "context": "เน้นใช้ Smartphone และ AI ช่วยทำงาน"
            })
            st.toast("โหลดข้อมูลแล้ว!", icon="📱")
            st.rerun()
            
        if st.button("📊 Power BI หัวหน้างาน\n(Data Analysis for Manager)"):
            st.session_state.update({
                "job_title": "หัวหน้างาน/ผู้จัดการ",
                "duration": "12 ชั่วโมง (2 วัน)",
                "objectives": "วิเคราะห์ข้อมูลช้า, ทำ Dashboard ไม่เป็น",
                "context": "ผู้เรียนพอมีพื้นฐาน Excel มาบ้าง"
            })
            st.toast("โหลดข้อมูลแล้ว!", icon="📊")
            st.rerun()

    st.markdown("---")

    # ==========================================
    # 📝 FORM SECTION
    # ==========================================
    st.subheader("📝 ตรวจสอบและสร้างหลักสูตร")
    
    with st.container(border=True): # Card สีขาว
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("1. กลุ่มเป้าหมาย", key="job_title", placeholder="เช่น ช่างไฟฟ้า, พนักงานบัญชี")
            problem = st.text_area("3. ปัญหา/สิ่งที่ต้องการพัฒนา", height=120, key="objectives")
        with col2:
            duration = st.text_input("2. ระยะเวลา", key="duration", placeholder="เช่น 6 ชั่วโมง, 2 วัน")
            context = st.text_area("4. บริบทเพิ่มเติม", height=120, key="context")

        st.markdown("###") 
        # ใช้ type="primary" เพื่อให้ CSS จับ button[kind="primary"] ได้
        generate_btn = st.button("✨ สร้างหลักสูตร (Generate Course)", type="primary", use_container_width=True)

    # Process Logic
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