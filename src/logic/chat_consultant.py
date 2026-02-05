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
        temperature=0.2
    )

def consult_and_fill(history, user_input):
    """
    ฟังก์ชันคุยกับ AI และพยายามดึงข้อมูลมาเติมลงฟอร์ม
    """
    llm = get_chat_llm()
    
    # ✅ แก้ไข: ใช้ {{ และ }} สำหรับ JSON เพื่อไม่ให้ LangChain สับสนว่าเป็นตัวแปร
    system_prompt = """
    คุณคือ "AI Course Consultant" ผู้ช่วยวิเคราะห์ความต้องการในการฝึกอบรม
    หน้าที่ของคุณ:
    1. พูดคุยสอบถามผู้ใช้เพื่อรวบรวมข้อมูล 4 อย่างนี้ให้ครบ:
       - ตำแหน่งงาน/กลุ่มเป้าหมาย (Job Title)
       - ระยะเวลา (Duration)
       - ปัญหา/ทักษะที่ต้องการพัฒนา (Pain Points)
       - บริบทเพิ่มเติม (Context)
    2. ถามทีละคำถาม อย่างเป็นกันเอง เหมือนเพื่อนร่วมงาน
    3. เมื่อผู้ใช้ให้ข้อมูล **ครบถ้วน** หรือ **ผู้ใช้บอกให้สรุป** ให้คุณพิมพ์ข้อความตอบกลับปกติ และ **ต่อท้าย** ด้วย JSON Block ดังนี้:
    
    ```json
    {{
      "job_title": "...",
      "duration": "...",
      "objectives": "...",
      "context": "..."
    }}
    ```
    
    ถ้าข้อมูลยังไม่ครบ ไม่ต้องส่ง JSON ให้ถามต่อไปเรื่อยๆ
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
            # ลบ JSON ออกจากข้อความที่จะโชว์ เพื่อไม่ให้รกตา
            content = re.sub(r"```json\n(.*?)\n```", "", content, flags=re.DOTALL).strip()
        except:
            pass
            
    return content, extracted_data