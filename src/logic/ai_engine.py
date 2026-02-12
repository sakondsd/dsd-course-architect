import os
import re
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# ===================================================
# 1. CONFIG & SETUP
# ===================================================
def get_api_key():
    key = os.getenv("GOOGLE_API_KEY")
    if not key and "GOOGLE_API_KEY" in st.secrets:
        key = st.secrets["GOOGLE_API_KEY"]
    return key

def get_llm():
    api_key = get_api_key()
    if not api_key:
        raise ValueError("❌ ไม่พบ Google API Key! กรุณาตั้งค่าใน .env หรือ Secrets")
    
    # ใช้ 1.5 flash เพื่อความเสถียรและโควต้าเยอะ (หรือเปลี่ยนเป็น 2.0-flash ถ้าต้องการ)
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash", 
        google_api_key=api_key,
        temperature=0.3
    )

# ===================================================
# 2. HELPER: คำนวณงบประมาณ (Python Calculation)
# ===================================================
def calculate_estimated_budget(duration_str):
    """
    ฟังก์ชันช่วยคำนวณงบประมาณเบื้องต้นจากข้อความระยะเวลา
    """
    try:
        # สมมติฐานตัวเลข (แก้ไขได้ตามจริง)
        people = 20
        food_rate = 250
        speaker_rate = 1200
        
        # พยายามเดาจำนวนวันจากข้อความ
        days = 1
        hours = 6
        
        # หาตัวเลขหน้าคำว่า "วัน"
        day_match = re.search(r"(\d+)\s*วัน", duration_str)
        if day_match:
            days = int(day_match.group(1))
            hours = days * 6
        else:
            # ถ้าไม่มีวัน หาชั่วโมง
            hour_match = re.search(r"(\d+)\s*ชั่วโมง", duration_str)
            if hour_match:
                hours = int(hour_match.group(1))
                days = max(1, hours // 6)

        total_food = people * food_rate * days
        total_speaker = hours * speaker_rate
        grand_total = total_food + total_speaker
        
        return f"""
        * **สมมติฐาน:** ผู้เข้าอบรม {people} คน, อาหาร {food_rate} บ./วัน, วิทยากร {speaker_rate} บ./ชม. ({hours} ชม.)
        * **ค่าอาหารและเครื่องดื่ม:** {total_food:,.2f} บาท
        * **ค่าตอบแทนวิทยากร:** {total_speaker:,.2f} บาท
        * **รวมงบประมาณทั้งสิ้น:** {grand_total:,.2f} บาท
        """
    except:
        return "ไม่สามารถคำนวณงบประมาณได้ (ระบุระยะเวลาไม่ชัดเจน)"

# ===================================================
# 3. LOGIC: Extract Rules
# ===================================================
def extract_rules_from_pdf_text(raw_text):
    try:
        llm = get_llm()
        prompt_template = """
        คุณคือผู้เชี่ยวชาญด้านกฎหมายแรงงานและมาตรฐานฝีมือแรงงาน
        หน้าที่ของคุณคือสรุป "ข้อกำหนด" และ "ระเบียบ" จากเอกสารให้อยู่ในรูปแบบที่นำไปอ้างอิงได้ง่าย
        
        คำสั่ง:
        1. อ่านข้อความต้นฉบับ
        2. สกัดเงื่อนไขที่เป็น "ข้อบังคับ", "มาตรฐาน", หรือ "สิ่งที่ต้องทำ"
        3. ตัดข้อความน้ำท่วมทุ่งทิ้ง เอาแต่เนื้อหากฎเน้นๆ
        4. คั่นระหว่างข้อด้วย "--------------------" เสมอ
        
        ข้อความต้นฉบับ:
        {text}
        
        ผลลัพธ์ (Format: กฎข้อที่ 1 ... \n--------------------\n กฎข้อที่ 2 ...):
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = prompt | llm
        return chain.invoke({"text": raw_text}).content
    except Exception as e:
        return f"Error extracting rules: {e}"

# ===================================================
# 4. LOGIC: Main Course Generator
# ===================================================
def generate_course_design(job_title, duration, objectives, context, retrieved_rules):
    try:
        llm = get_llm()
        
        # 1. คำนวณงบประมาณเตรียมไว้
        budget_info = calculate_estimated_budget(duration)
        
        # 2. Prompt (ใช้ Version ละเอียดจาก Backup + ใส่ Budget เข้าไป)
        design_prompt = """
        คุณคือ "DSD Course Architect" นักออกแบบหลักสูตรกรมพัฒนาฝีมือแรงงานที่ทันสมัยและแม่นยำ
        
        ข้อมูลโจทย์:
        - หลักสูตรสำหรับ: {job_title}
        - ระยะเวลา: {duration}
        - วัตถุประสงค์หลัก: {objectives}
        - ข้อมูลเพิ่มเติม: {context}
        - งบประมาณเบื้องต้น: {budget_info}
        
        📂 ฐานข้อมูลกฎระเบียบ/ข้อกำหนดของคุณ (Internal Rules):
        "{rules}"
        
        🧠 คำสั่งการทำงานแบบผสมผสาน (Hybrid Logic):
        1. **แกนหลัก (Core):** ให้ยึด "ฐานข้อมูลกฎระเบียบ" (ข้างบน) เป็นโครงสร้างหลักและข้อบังคับที่ห้ามละเมิด
        2. **ส่วนเสริม (Modernization):** ให้ใช้ความรู้ของคุณเกี่ยวกับเทคโนโลยีล่าสุด, มาตรฐานสากล (ISO, IEEE, ฯลฯ), และเครื่องมือดิจิทัลยุคใหม่ มาออกแบบ "เนื้อหา" และ "กิจกรรม" ให้ทันสมัย
        3. **ความสัมพันธ์ (Relation):** เนื้อหาที่ทันสมัยที่นำมาใส่ **ต้องสอดคล้อง** หรือ **ช่วยสนับสนุน** ข้อกำหนดที่มีอยู่ ห้ามขัดแย้งกัน
        
        ⏰ โครงสร้างเวลาบังคับ (Time Structure):
           - 09:00 - 10:30 (1.5 ชม.)
           - 10:30 - 10:45 (พักเบรกเช้า 15 นาที)
           - 10:45 - 12:15 (1.5 ชม.)
           - 12:15 - 13:15 (พักรับประทานอาหารกลางวัน 1 ชั่วโมง)
           - 13:15 - 14:45 (1.5 ชม.)
           - 14:45 - 15:00 (พักเบรกบ่าย 15 นาที)
           - 15:00 - 16:30 (1.5 ชม.)
           *รวมเวลาฝึก 6 ชั่วโมงต่อวัน*
        
        รูปแบบการตอบ (Markdown Only):
        
        # หลักสูตร: [ชื่อหลักสูตรภาษาไทยที่เป็นทางการ]

        ## 1. หลักการและเหตุผล
        [เขียนบรรยายโดยเชื่อมโยงปัญหากับเทคโนโลยีสมัยใหม่ และสอดคล้องกับนโยบายกรมฯ]

        ## 2. วัตถุประสงค์ (Outcome Based)
        * [ข้อ 1 - เน้นผลลัพธ์ที่วัดได้]
        * [ข้อ 2 - เน้นการนำไปใช้จริง]

        ## 3. กลุ่มเป้าหมาย
        * {job_title}

        ## 4. กำหนดการฝึกอบรม (Schedule)
        
        | เวลา | หัวข้อวิชา (ระบุ ทฤษฎี/ปฏิบัติ) | กิจกรรม/วิธีการฝึก (เน้น Modern Tech) | มาตรฐาน/กฎที่เกี่ยวข้อง |
        | :--- | :--- | :--- | :--- |
        | 09:00 - 10:30 | **[ทฤษฎี]** [ชื่อวิชา] | [ระบุกิจกรรม เช่น ใช้ AI, Case Study ใหม่ๆ] | ✅ [อ้างอิงกฎจาก Database หรือ มาตรฐานสากลที่เกี่ยวข้อง] |
        | 10:30 - 10:45 | **พักรับประทานอาหารว่าง** | - | - |
        | 10:45 - 12:15 | **[ปฏิบัติ]** [ชื่อวิชา] | [ระบุกิจกรรม Workshop ทันสมัย] | ✅ [อ้างอิงกฎจาก Database หรือ มาตรฐานสากลที่เกี่ยวข้อง] |
        | 12:15 - 13:15 | **พักรับประทานอาหารกลางวัน** | - | - |
        | 13:15 - 14:45 | **[ปฏิบัติ]** [ชื่อวิชา] | [ระบุกิจกรรม เน้นลงมือทำ] | ✅ [อ้างอิงกฎจาก Database หรือ มาตรฐานสากลที่เกี่ยวข้อง] |
        | 14:45 - 15:00 | **พักรับประทานอาหารว่าง** | - | - |
        | 15:00 - 16:30 | **[ปฏิบัติ]** [ชื่อวิชา] | [ระบุกิจกรรม และสรุปผล] | ✅ [อ้างอิงกฎจาก Database หรือ มาตรฐานสากลที่เกี่ยวข้อง] |
        *(หากหลักสูตรมีมากกว่า 1 วัน ให้ทำซ้ำตารางตามจำนวนวัน)*
        
        ## 5. ผลลัพธ์ที่คาดว่าจะได้รับ (Impact)
        * [ระบุสิ่งที่วัดผลได้ เช่น งานเร็วขึ้น, ลดข้อผิดพลาด]

        ## 6. การประเมินผล
        * [ระบุวิธีวัดผล เช่น ชิ้นงาน, แบบทดสอบ]

        ## 7. งบประมาณโครงการ (โดยประมาณ)
        {budget_info}
        """
        
        prompt = PromptTemplate(
            template=design_prompt, 
            input_variables=["job_title", "duration", "objectives", "context", "rules", "budget_info"]
        )
        
        chain = prompt | llm
        
        return chain.invoke({
            "job_title": job_title, 
            "duration": duration, 
            "objectives": objectives, 
            "context": context, 
            "rules": retrieved_rules,
            "budget_info": budget_info
        }).content

    except Exception as e:
        return f"Error designing course: {e}"