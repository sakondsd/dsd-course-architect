import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

# สร้างตัวแปร llm กลาง
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

def extract_rules_from_pdf_text(raw_text):
    """
    หน้าที่: แปลงข้อความดิบจาก PDF ให้กลายเป็นกฎที่คั่นด้วย Separator
    """
    try:
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
    """
    หน้าที่: ออกแบบหลักสูตรโดยอ้างอิงกฎที่ค้นเจอ (Output เป็นตาราง)
    """
    try:
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
        จงออกแบบหลักสูตรฝึกอบรม 1 หลักสูตร ให้ถูกต้องตามกฎระเบียบ โดยมีโครงสร้างการตอบดังนี้:
        
        รูปแบบการตอบ (Response Format):
        
        ## ชื่อหลักสูตร: [ตั้งชื่อให้กระชับและเป็นทางการ]

        **หลักการและเหตุผล:**
        [อธิบายสั้นๆ ว่าทำไมถึงจัดหลักสูตรนี้ และแก้ปัญหาตามโจทย์ได้อย่างไร]

        **วัตถุประสงค์:** (ระบุเป็นข้อๆ)
        1. เพื่อให้ผู้เข้ารับการฝึกอบรมสามารถ...
        2. เพื่อแก้ไขปัญหา...
        3. ...

        **ตารางโครงสร้างหลักสูตร (Agenda):**
        | เวลา (นาที/ชม.) | หัวข้อวิชา | รายละเอียด/วิธีการฝึก | ความสอดคล้องกับกฎ |
        |---|---|---|---|
        | [ระบุเวลา] | [ชื่อหัวข้อ] | [อธิบายเนื้อหาโดยสังเขป] | [ระบุว่าทำไมหัวข้อนี้ถึงสอนได้ (ไม่ขัดกฎข้อไหน)] |
        | ... | ... | ... | ... |
        *(แบ่งเวลาให้ครบตาม {duration} พอดี)*

        **สรุปการตรวจสอบกฎ:**
        [ยืนยันว่าหลักสูตรนี้สอดคล้องกับกฎระเบียบ และไม่มีหัวข้อต้องห้ามสำหรับตำแหน่งงานนี้]
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