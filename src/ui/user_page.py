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
            AIMessage(content="สวัสดีครับ! ผมคือ AI ผู้ช่วยออกแบบหลักสูตร\nมีไอเดียอยากจัดอบรมเรื่องอะไร บอกผมได้เลยครับ เดี๋ยวผมช่วยร่างโครงสร้างให้")
        ]
    
    # ==========================================
    # 🎨 CSS: High Contrast Chat (DSD Theme)
    # ==========================================
    st.markdown("""
    <style>
        /* ปรับพื้นหลัง Container หลัก */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff;
        }
        
        /* 🟢 User Bubble (ฝั่งขวา - เรา) */
        /* เปลี่ยนเป็นสีม่วงเข้ม เพื่อให้ตัดกับพื้นหลังชัดเจน */
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) {
            flex-direction: row-reverse;
            text-align: right;
        }
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) div[data-testid="stMarkdownContainer"] {
            background-color: #5A2D81; /* สีม่วง DSD */
            color: #FFFFFF !important; /* ตัวหนังสือสีขาว */
            padding: 12px 20px;
            border-radius: 20px 20px 5px 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2); /* เงาเข้มขึ้น */
            text-align: left;
            display: inline-block;
        }
        /* บังคับสีตัวอักษรใน User Bubble ให้ขาวเสมอ */
        [data-testid="stChatMessage"]:has(div[aria-label="user"]) p {
            color: #FFFFFF !important;
        }

        /* 🤖 AI Bubble (ฝั่งซ้าย - บอท) */
        /* ใส่พื้นหลังสีเทาอ่อนและขอบ เพื่อให้ดูเป็นกล่องชัดเจน */
        [data-testid="stChatMessage"]:has(div[aria-label="assistant"]) {
            flex-direction: row;
            text-align: left;
        }
        [data-testid="stChatMessage"]:has(div[aria-label="assistant"]) div[data-testid="stMarkdownContainer"] {
            background-color: #F8F9FA; /* สีเทาอ่อนมาก */
            border: 1px solid #E0E0E0; /* เส้นขอบบางๆ */
            color: #333333 !important; /* ตัวหนังสือสีเทาเข้ม */
            padding: 12px 20px;
            border-radius: 20px 20px 20px 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: inline-block;
            margin-top: 5px;
        }
        
        /* ปรับ Avatar ให้ดูดีขึ้น */
        .stChatMessageAvatarImage {
            background-color: #FFFFFF;
            border: 1px solid #eee;
        }
        
        /* ดัน Input bar ขึ้นมานิดนึง */
        .stChatInputContainer {
            padding-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- 3. Chat Interface ---
    st.markdown("### 🤖 คุยกับ AI เพื่อร่างหลักสูตร (AI Consultant)")
    
    # Chat Box (Scrollable)
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        for msg in st.session_state["chat_history"]:
            if isinstance(msg, HumanMessage):
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(msg.content)
            elif isinstance(msg, AIMessage):
                with st.chat_message("assistant", avatar="✨"):
                    st.markdown(msg.content)

    # Input Bar (ลอยอยู่ล่างสุด)
    if prompt := st.chat_input("พิมพ์ไอเดียหลักสูตรที่นี่... (เช่น อยากจัดอบรม Excel ให้ฝ่ายขาย)"):
        
        with chat_container:
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(prompt)
        st.session_state["chat_history"].append(HumanMessage(content=prompt))
        
        with chat_container:
            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("กำลังวิเคราะห์ข้อมูล..."):
                    response_text, extracted_data = consult_and_fill(st.session_state["chat_history"], prompt)
                    st.markdown(response_text)
        
        st.session_state["chat_history"].append(AIMessage(content=response_text))
        
        # Auto Fill Logic
        if extracted_data:
            st.session_state["job_title"] = extracted_data.get("job_title", "")
            st.session_state["duration"] = extracted_data.get("duration", "")
            st.session_state["objectives"] = extracted_data.get("objectives", "")
            st.session_state["context"] = extracted_data.get("context", "")
            
            # แจ้งเตือนปิดท้าย
            final_msg = "✅ **ผมเติมข้อมูลลงในแบบฟอร์มด้านล่างให้เรียบร้อยแล้วครับ!** \n\nคุณสามารถตรวจสอบความถูกต้อง หรือเลื่อนลงไปกดปุ่ม **'✨ สร้างหลักสูตร'** ได้เลยครับ"
            st.session_state["chat_history"].append(AIMessage(content=final_msg))
            st.rerun()

    st.markdown("---")

    # --- 4. Form Section ---
    with st.expander("📝 ตรวจสอบและแก้ไขข้อมูลก่อนสร้างเอกสาร", expanded=True):
        st.markdown("##### รายละเอียดโครงการ")
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("1. ตำแหน่งงาน/กลุ่มเป้าหมาย", key="job_title")
            problem = st.text_area("3. ปัญหา/สิ่งที่ต้องการพัฒนา", height=150, key="objectives")
        with col2:
            duration = st.text_input("2. ระยะเวลาฝึกอบรม", key="duration")
            context = st.text_area("4. บริบทเพิ่มเติม", height=150, key="context")

        generate_btn = st.button("✨ สร้างหลักสูตร (Generate Course)", type="primary", use_container_width=True)

    # --- 5. Generate Logic ---
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