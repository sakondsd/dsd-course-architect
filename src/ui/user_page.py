import streamlit as st
import base64
import os
import streamlit.components.v1 as components # ✅ เพิ่ม import นี้เพื่อใช้รัน JavaScript
from src.logic.doc_generator import create_word_docx 
from src.logic.ai_engine import generate_course_design
from src.logic.data_manager import search_rules
from src.logic.chat_consultant import consult_and_fill
from langchain_core.messages import HumanMessage, AIMessage

# ==========================================
# 🔧 HELPER: แปลงรูปเป็น Base64 (เหมือนเดิม)
# ==========================================
def get_img_as_base64(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# ==========================================
# 🎨 CSS & ASSETS (เหมือนเดิม)
# ==========================================
def load_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700&display=swap');
        
        /* 1. HEADER SECTION */
        .header-container {
            background-image: linear-gradient(to right, rgba(75, 44, 104, 0.9), rgba(46, 20, 64, 0.9)), 
                              url('https://images.unsplash.com/photo-1534972195531-d756b9bfa9f2?q=80&w=2070&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            border-radius: 15px;
            padding: 20px 30px;
            color: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            display: flex; 
            align-items: center;
            gap: 25px;
        }
        .header-text-block { display: flex; flex-direction: column; justify-content: center; }
        .header-title { font-family: 'Prompt', sans-serif; font-size: 2rem; font-weight: 700; margin: 0; color: #ffffff; text-shadow: 2px 2px 4px rgba(0,0,0,0.6); }
        .header-subtitle { font-family: 'Prompt', sans-serif; font-size: 1rem; margin-top: 5px; opacity: 0.9; font-weight: 300; }
        .header-logo-img { height: 75px; width: auto; object-fit: contain; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.3)); }

        /* 2. FOOTER SECTION */
        .footer-container { margin-top: 50px; padding-top: 25px; border-top: 1px solid #444; display: flex; justify-content: center; align-items: center; gap: 20px; }
        .footer-text { color: #aaa; font-size: 0.95rem; margin: 0; line-height: 1.5; }
        .footer-profile-img { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; border: 3px solid #8e44ad; }

        /* 3. QUICK START AREA */
        .quickstart-img-container { margin-bottom: 15px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
        .quickstart-img { width: 100%; height: 120px; object-fit: cover; display: block; }

        div.stButton > button { width: 100%; border-radius: 10px; text-align: left; border: 1px solid #3e405b; background-color: #2b2d42; color: #e0e0e0; transition: all 0.2s; margin-bottom: 8px; padding: 12px 15px; }
        div.stButton > button:hover { border-color: #8e44ad; background-color: #383a54; color: white; transform: translateX(5px); }
        
        /* 4. FORM STYLING */
        div[data-testid="stForm"] { background-color: #1a1c24; padding: 30px; border-radius: 15px; border: 1px solid #333; }
        ::placeholder { color: #666 !important; opacity: 1; }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# 💡 PART 0: ONBOARDING POPUP (ส่วนเพิ่มใหม่)
# ==========================================
@st.dialog("ยินดีต้อนรับสู่ DSD Course Architect! 🚀")
def show_onboarding():
    st.markdown("""
    ระบบนี้ช่วยคุณออกแบบหลักสูตรฝึกอบรมได้ง่ายๆ ใน 3 ขั้นตอน:
    
    **1️⃣ บอกความต้องการ**
    * พิมพ์บอก **AI Consultant** 🤖 ทางซ้าย (เช่น "อยากสอน Excel ให้ฝ่ายบัญชี")
    * หรือเลือก **Quick Start** 💡 ทางขวา เพื่อใช้แม่แบบยอดนิยม
    
    **2️⃣ ตรวจสอบข้อมูล**
    * ระบบจะสรุปข้อมูลลงใน **แบบฟอร์มด้านล่าง** 📝
    * คุณสามารถแก้ไขรายละเอียดเพิ่มเติมได้ตามต้องการ
    
    **3️⃣ สร้างและดาวน์โหลด**
    * กดปุ่ม **"✨ สร้างหลักสูตร"** แล้วรอ AI เนรมิตหลักสูตรให้
    * ดาวน์โหลดเป็นไฟล์ **Word (.docx)** 📄 ไปใช้งานต่อได้เลย!
    """)
    
    if st.button("เริ่มใช้งานเลย! 🚀", type="primary", use_container_width=True):
        st.session_state["has_seen_guide"] = True
        st.rerun()

# ==========================================
# 🧩 PART 1: HEADER (เหมือนเดิม)
# ==========================================
def render_header():
    logo_path = "static/logo_dsd.png"
    img_b64 = get_img_as_base64(logo_path)
    img_tag = f'<img src="data:image/png;base64,{img_b64}" class="header-logo-img">' if img_b64 else ''

    st.markdown(f"""
        <div class="header-container">
            {img_tag}
            <div class="header-text-block">
                <p class="header-title">DSD Course Architect</p>
                <p class="header-subtitle">ระบบออกแบบหลักสูตรพัฒนาฝีมือแรงงานอัจฉริยะ ด้วย AI</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 🧩 PART 2: CHAT & QUICK START (เหมือนเดิม)
# ==========================================
def render_chat_and_ideas():
    st.markdown("###")
    col_chat, col_ideas = st.columns([0.6, 0.4], gap="large")

    with col_ideas:
        st.subheader("💡 Quick Start Ideas")
        st.markdown("""
            <div class="quickstart-img-container">
                <img src="https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=2070&auto=format&fit=crop" class="quickstart-img" alt="Ideas">
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ ช่างไฟฟ้าภายในอาคาร (30 ชม.)"):
            return { "job_title": "ช่างไฟฟ้าภายในอาคาร ระดับ 1", "duration": "30 ชั่วโมง (5 วัน)", "problem": "การติดตั้งเดินสายไฟไม่ได้มาตรฐาน ความปลอดภัยต่ำ", "context": "เน้นปฏิบัติ 80% เตรียมทดสอบมาตรฐานฝีมือแรงงาน" }
        if st.button("🏥 ผู้ดูแลผู้สูงอายุ (18 ชม.)"):
             return { "job_title": "ผู้ดูแลผู้สูงอายุ (Caregiver)", "duration": "18 ชั่วโมง (3 วัน)", "problem": "ขาดทักษะการปฐมพยาบาลและการเคลื่อนย้ายผู้ป่วยที่ถูกวิธี", "context": "ฝึกกับหุ่นจำลองสถานการณ์จริง มีอุปกรณ์ครบครัน" }
        if st.button("📊 Data Analysis for Manager (12 ชม.)"):
             return { "job_title": "หัวหน้างาน/ผู้จัดการฝ่ายผลิต", "duration": "12 ชั่วโมง (2 วัน)", "problem": "ใช้เวลานานในการสรุปข้อมูลการผลิตรายวันเพื่อนำเสนอผู้บริหาร", "context": "ผู้เรียนมีพื้นฐาน Excel ต้องการต่อยอดใช้ Power BI เบื้องต้น" }
        if st.button("📱 การตลาดออนไลน์สำหรับ SMEs (6 ชม.)"):
             return { "job_title": "ผู้ประกอบการ SMEs / พ่อค้าแม่ค้าออนไลน์", "duration": "6 ชั่วโมง (1 วัน)", "problem": "ยิงแอดโฆษณาแล้วไม่ตรงกลุ่มเป้าหมาย ต้นทุนสูงแต่ยอดขายน้อย", "context": "เน้นการใช้ Facebook Ads Manager และ TikTok Ads เบื้องต้น" }
        if st.button("🦺 ความปลอดภัยในการทำงาน (จป.) (6 ชม.)"):
             return { "job_title": "พนักงานทั่วไปในโรงงานอุตสาหกรรม", "duration": "6 ชั่วโมง (1 วัน)", "problem": "พนักงานขาดความตระหนักเรื่องความปลอดภัยในการทำงานกับเครื่องจักร", "context": "หลักสูตรตามกฎหมายกำหนด เน้นกรณีศึกษาอุบัติเหตุจริง" }

    with col_chat:
        st.subheader("🤖 AI Consultant")
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = [AIMessage(content="สวัสดีครับ! ต้องการจัดอบรมเรื่องอะไร บอกผมได้เลยครับ")]

        chat_box = st.container(height=550) 
        with chat_box:
            for msg in st.session_state["chat_history"]:
                if isinstance(msg, HumanMessage): st.chat_message("user", avatar="👤").write(msg.content)
                elif isinstance(msg, AIMessage): st.chat_message("assistant", avatar="🤖").write(msg.content)

        user_input = st.chat_input("พิมพ์โจทย์ที่ต้องการ...")
        if user_input:
            st.session_state["chat_history"].append(HumanMessage(content=user_input))
            with chat_box:
                st.chat_message("user", avatar="👤").write(user_input)
                with st.chat_message("assistant", avatar="🤖"):
                    with st.spinner("Thinking..."):
                        response, data = consult_and_fill(st.session_state["chat_history"], user_input)
                        st.write(response)
            st.session_state["chat_history"].append(AIMessage(content=response))
            if data: return data 

    return None

# ==========================================
# 🧩 PART 3: FORM (แก้ไขแก้ Error ไอคอน)
# ==========================================
def render_form(prefill_data):
    # 1. ฝัง Anchor ไว้ตรงนี้เพื่อให้ JS วิ่งมาหา
    st.markdown('<div id="form_anchor"></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📝 ตรวจสอบและสร้างหลักสูตร")

    if prefill_data:
        st.session_state.update(prefill_data)
        # ✅ แก้ไขจุดที่ Error: เปลี่ยน icon="magic" เป็น "✨" (ต้องเป็น Emoji เท่านั้น)
        st.toast("✅ โหลดข้อมูลเรียบร้อย!", icon="✨")
        
        # 2. ยิง JavaScript เพื่อสั่ง Scroll หน้าจอลงมาที่ #form_anchor
        js = """
        <script>
            setTimeout(function() {
                var element = window.parent.document.getElementById('form_anchor');
                if (element) {
                    element.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            }, 500);
        </script>
        """
        components.html(js, height=0)

    with st.form("course_gen_form"):
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            st.text_input("1. กลุ่มเป้าหมาย", key="job_title", placeholder="เช่น หัวหน้างาน ฝ่ายผลิต, วิศวกรจบใหม่")
            st.text_area("3. ปัญหา/สิ่งที่ต้องการพัฒนา", key="problem", height=120, placeholder="เช่น ทำงานล่าช้า, ขาดทักษะการใช้เครื่องมือพิเศษ")
        with c2:
            st.text_input("2. ระยะเวลา", key="duration", placeholder="เช่น 6 ชั่วโมง (1 วัน), 30 ชั่วโมง (5 วัน)")
            st.text_area("4. บริบทเพิ่มเติม", key="context", height=120, placeholder="เช่น เน้นปฏิบัติ 80%, ต้องเตรียมเครื่องจักรเฉพาะ")

        st.markdown("###")
        submitted = st.form_submit_button("✨ สร้างหลักสูตร (Generate Course)", type="primary", use_container_width=True)
        return submitted

# ==========================================
# 🧩 PART 4 & 5: RESULT & FOOTER (เหมือนเดิม)
# ==========================================
def render_result():
    if st.session_state.get("generated_course"):
        st.divider()
        st.subheader("✅ ผลลัพธ์การออกแบบ")
        with st.container(border=True):
            st.markdown(st.session_state["generated_course"])
        docx = create_word_docx(st.session_state["generated_course"])
        st.download_button("📄 ดาวน์โหลดไฟล์ Word (.docx)", docx, "Course_Design.docx", 
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document", type="primary")

def render_footer():
    profile_path = "static/profile.jpg"
    img_b64 = get_img_as_base64(profile_path)
    img_tag = f'<img src="data:image/jpg;base64,{img_b64}" class="footer-profile-img">' if img_b64 else ''

    st.markdown(f"""
        <div class="footer-container">
            {img_tag}
            <div class="footer-text">
                <strong>DSD Course Architect © 2026</strong><br>
                <span style="opacity: 0.8;">พัฒนาโดย สำนักงานพัฒนาฝีมือแรงงานสกลนคร | Power by artist_auto</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 🚀 MAIN FUNCTION
# ==========================================
def render_user_page():
    load_custom_css()

    # ---------------------------------------
    # 1. ส่วนควบคุม Popup (Auto + Manual)
    # ---------------------------------------
    # ถ้ายังไม่เคยดู ให้เด้ง Auto
    if "has_seen_guide" not in st.session_state:
        show_onboarding()

    # ปุ่ม Manual สำหรับกดดูซ้ำ (วางมุมขวาบนสุด)
    col_empty, col_btn = st.columns([0.92, 0.08]) 
    with col_btn:
        if st.button("❓", help="แนะนำวิธีการใช้งาน"):
            show_onboarding()
    # ---------------------------------------

    render_header()
    selected_data = render_chat_and_ideas()
    is_submitted = render_form(selected_data)
    
    if is_submitted:
        job = st.session_state.get("job_title")
        dur = st.session_state.get("duration")
        prob = st.session_state.get("problem")
        ctx = st.session_state.get("context")
        
        if job and dur:
            with st.spinner("🤖 AI กำลังออกแบบหลักสูตร..."):
                rules = search_rules(f"{job} {prob}")
                res = generate_course_design(job, dur, prob, ctx, rules)
                st.session_state["generated_course"] = res
                st.rerun()
        else:
            st.warning("กรุณากรอกข้อมูลให้ครบถ้วน")

    render_result()
    render_footer()