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
        llm = get_llm() # ✅ เรียกใช้ LLM ตรงนี้แทน
        
        design_prompt = """
        คุณคือ "DSD Course Architect" (นักออกแบบหลักสูตรกรมพัฒนาฝีมือแรงงาน)
        
        ข้อมูลโจทย์:
        - ตำแหน่งงาน: {job_title}
        - เวลา: {duration}
        - ปัญหาที่ต้องการแก้: {objectives}
        - บริบทเพิ่มเติม: {context}
        
        กฎระเบียบที่ต้องปฏิบัติตาม (Strict Rules):
        {rules}
        
        คำสั่ง:
        จงออกแบบหลักสูตรฝึกอบรม 1 หลักสูตร ให้ถูกต้องตามกฎระเบียบ... (ใช้ Prompt เดิมของคุณต่อตรงนี้)
        """
        # (ส่วน Prompt ยาวๆ คงเดิมไว้ได้เลยครับ ผมตัดย่อให้ดูเป็นตัวอย่าง)
        
        # ... ใส่ Prompt เต็มๆ ของคุณตรงนี้ ...
        
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