import os
import json
import re
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

def get_chat_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key and "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash", 
        google_api_key=api_key,
        temperature=0.1 
    )

def consult_and_fill(history, user_input):
    """
    ฟังก์ชันคุยกับ AI และพยายามดึงข้อมูลมาเติมลงฟอร์ม
    """
    llm = get_chat_llm()
    
    # ✅ แก้ไข Prompt: เพิ่มคำสั่งให้ AI พูดประโยคปิดท้ายตามที่ขอ
    system_prompt = """
    คุณคือ "AI Course Consultant" ผู้ช่วยวิเคราะห์ความต้องการในการฝึกอบรม
    
    หน้าที่ของคุณ:
    1. พูดคุยสอบถามผู้ใช้เพื่อรวบรวมข้อมูล 4 อย่างนี้ให้ครบ:
       - ตำแหน่งงาน/กลุ่มเป้าหมาย (Job Title)
       - ระยะเวลา (Duration)
       - ปัญหา/ทักษะที่ต้องการพัฒนา (Problem/Pain Points)
       - บริบทเพิ่มเติม (Context) : เครื่องมือ (Tools), โปรแกรม (Software), อุปกรณ์
       
    2. ถามทีละคำถาม อย่างเป็นกันเอง
    
    3. เมื่อผู้ใช้ให้ข้อมูล **ครบถ้วน** หรือ **ผู้ใช้บอกให้สรุป** ให้ปฏิบัติ 2 ขั้นตอน:
       A. พิมพ์ข้อความสรุปสั้นๆ และ **ต้องลงท้ายประโยคด้วยข้อความนี้เสมอ:**
          "ตรวจสอบและสร้างหลักสูตร ด้านล่างได้เลยครับ 👇"
       
       B. ต่อท้ายด้วย JSON Block ดังนี้ (เพื่อส่งข้อมูลไปกรอกฟอร์ม):
    
    ```json
    {{
      "job_title": "ระบุกลุ่มเป้าหมาย",
      "duration": "ระบุระยะเวลา",
      "problem": "ระบุปัญหาหรือทักษะที่ต้องการพัฒนา (ห้ามใช้คำว่า objectives)",
      "context": "ระบุบริบทเพิ่มเติม เครื่องมือ หรือโปรแกรมที่ใช้ (ห้ามตัดทิ้ง)"
    }}
    ```
    
    ข้อควรระวัง: 
    - ต้องใช้ Key ชื่อ "problem" เท่านั้น ห้ามใช้ "objectives"
    - ถ้ามีการกล่าวถึงโปรแกรมคอมพิวเตอร์ (เช่น Power BI, Excel) ต้องใส่มาใน context หรือ problem เสมอ
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    chain = prompt | llm
    
    response = chain.invoke({
        "history": history,
        "input": user_input
    })
    
    content = response.content
    extracted_data = None
    
    # 🕵️‍♂️ พยายามหา JSON Block ในคำตอบ
    json_match = re.search(r"```json\n(.*?)\n```", content, re.DOTALL)
    if json_match:
        try:
            json_str = json_match.group(1)
            extracted_data = json.loads(json_str)
            content = re.sub(r"```json\n(.*?)\n```", "", content, flags=re.DOTALL).strip()
        except:
            pass
            
    return content, extracted_data