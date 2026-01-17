import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# โหลด environment (สำหรับเครื่องตัวเอง)
load_dotenv()

# ฟังก์ชันดึง API Key แบบปลอดภัย (รองรับทั้ง Local และ Cloud)
def get_api_key():
    # 1. ลองหาจาก .env ก่อน
    key = os.getenv("GOOGLE_API_KEY")
    # 2. ถ้าไม่เจอ ให้ลองหาจาก Streamlit Secrets (บน Cloud)
    if not key and "GOOGLE_API_KEY" in st.secrets:
        key = st.secrets["GOOGLE_API_KEY"]
    return key

# ---------------------------------------------------------
# ⚠️ เปลี่ยน: ไม่สร้าง llm ทิ้งไว้ข้างนอก (Global)
# เพราะถ้าไม่มี Key โปรแกรมจะพังทันทีตอน Import
# เราจะสร้างในฟังก์ชันแทน
# ---------------------------------------------------------

def get_llm():
    api_key = get_api_key()
    if not api_key:
        raise ValueError("❌ ไม่พบ Google API Key! กรุณาตั้งค่าใน .env หรือ Secrets")
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=api_key,
        temperature=0.3
    )

def extract_rules_from_pdf_text(raw_text):
    try:
        llm = get_llm() # ✅ เรียกใช้ LLM ตรงนี้แทน
        prompt_template = """
        คุณคือผู้เชี่ยวชาญด้านกฎหมายแรงงาน หน้าที่ของคุณคือแปลงเอกสารเป็นกฎระเบียบสำหรับระบบ AI
        
        คำสั่ง:
        1. อ่านข้อความต้นฉบับ
        2. สกัดเงื่อนไขที่เป็น "ข้อห้าม" หรือ "ข้อกำหนด" (Do's & Don'ts)
        3. ตัดน้ำท่วมทุ่งทิ้ง เอาแต่เนื้อๆ
        4. สำคัญมาก: ต้องคั่นระหว่างข้อด้วย "--------------------" (ขีดกลาง 20 ที) เสมอ
        
        ข้อความต้นฉบับ:
        {text}
        
        ผลลัพธ์ (Format: กฎข้อที่ 1 ... \n--------------------\n กฎข้อที่ 2 ...):
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = prompt | llm
        return chain.invoke({"text": raw_text}).content
    except Exception as e:
        return f"Error extracting rules: {e}"

def generate_course_design(job_title, duration, objectives, context, retrieved_rules):
    try:
        llm = get_llm()
        
        design_prompt = """
        คุณคือ "DSD Course Architect" นักออกแบบหลักสูตรมืออาชีพของกรมพัฒนาฝีมือแรงงาน
        
        ข้อมูลโจทย์:
        - หลักสูตรสำหรับ: {job_title}
        - ระยะเวลา: {duration}
        - วัตถุประสงค์หลัก: {objectives}
        - ข้อมูลเพิ่มเติม: {context}
        
        กฎระเบียบที่เกี่ยวข้อง (Strict Rules):
        {rules}
        
        คำสั่ง:
        จงออกแบบหลักสูตรฝึกอบรม โดยให้ผลลัพธ์อยู่ในรูปแบบ "เอกสารโครงการฝึกอบรม" ที่พร้อมใช้งานจริง
        
        รูปแบบการตอบ (Response Format) - ใช้ Markdown เท่านั้น:
        
        # [ชื่อหลักสูตรที่ดึงดูดใจและเป็นทางการ]

        ## 1. หลักการและเหตุผล
        [เขียนบรรยาย 1 ย่อหน้า ถึงความสำคัญและที่มาของหลักสูตร]

        ## 2. วัตถุประสงค์
        * เพื่อ...
        * เพื่อ...
        * (ระบุอย่างน้อย 3 ข้อ)

        ## 3. กลุ่มเป้าหมาย
        * {job_title} จำนวนผู้เข้าอบรม ... คน

        ## 4. กำหนดการฝึกอบรม (Schedule)
        | เวลา | หัวข้อวิชา | กิจกรรม/วิธีการฝึก | มาตรฐาน/กฎที่เกี่ยวข้อง |
        | :--- | :--- | :--- | :--- |
        | 09:00 - 10:30 | [ชื่อหัวข้อ] | [รายละเอียดกิจกรรม] | ✅ [อ้างอิงกฎ] |
        | 10:30 - 10:45 | *พักรับประทานอาหารว่าง* | - | - |
        | 10:45 - 12:00 | [ชื่อหัวข้อ] | [รายละเอียดกิจกรรม] | ✅ [อ้างอิงกฎ] |
        | 12:00 - 13:00 | *พักรับประทานอาหารกลางวัน* | - | - |
        | 13:00 - ... | [ใส่เนื้อหาต่อให้ครบตามเวลา {duration}] | ... | ... |
        
        ## 5. การประเมินผล
        * [ระบุวิธีการวัดผล เช่น การทดสอบภาคทฤษฎี/ปฏิบัติ]

        ## 6. สรุปความสอดคล้องกับกฎระเบียบ
        * [อธิบายสั้นๆ ว่าหลักสูตรนี้ไม่ขัดต่อกฎหมายและระเบียบกรมฯ อย่างไร]
        """
        
        prompt = PromptTemplate(template=design_prompt, input_variables=["job_title", "duration", "objectives", "context", "rules"])
        chain = prompt | llm
        return chain.invoke({
            "job_title": job_title, 
            "duration": duration, 
            "objectives": objectives, 
            "context": context, 
            "rules": retrieved_rules
        }).content
    except Exception as e:
        return f"Error designing course: {e}"