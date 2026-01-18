# 🏗️ DSD Course Architect (ระบบออกแบบหลักสูตรกรมพัฒนาฝีมือแรงงาน)

ระบบ AI อัจฉริยะสำหรับช่วยเจ้าหน้าที่และวิทยากรออกแบบหลักสูตรฝึกอบรม โดยตรวจสอบความสอดคล้องกับกฎระเบียบ กฎหมาย และมาตรฐานฝีมือแรงงานโดยอัตโนมัติ พร้อมระบบจัดทำเอกสารโครงการฝึกอบรม

![DSD Architect Cover](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red)

## ✨ ฟีเจอร์หลัก (Key Features)

### 👩‍💻 สำหรับผู้ใช้งานทั่วไป (User)
* **AI Course Designer:** ออกแบบหลักสูตรฝึกอบรมอัตโนมัติ ตามโจทย์ (ตำแหน่งงาน, เวลา, ปัญหา)
* **Smart Rule Checking:** ตรวจสอบและดึง **"กฎ/มาตรฐาน"** ที่เกี่ยวข้องมาแสดงในตารางกำหนดการให้อัตโนมัติ
* **Export to Word:** ดาวน์โหลดผลลัพธ์การออกแบบเป็นไฟล์ `.docx` พร้อมนำไปใช้งานต่อได้ทันที

### 🛠️ สำหรับผู้ดูแลระบบ (Admin)
* **Secure Login:** ระบบล็อกอินป้องกันการเข้าถึงส่วนจัดการ
* **AI Rule Extractor:** อัปโหลดไฟล์ PDF/TXT แล้วให้ AI ช่วยแกะกฎระเบียบออกมาเป็นข้อๆ ให้อัตโนมัติ
* **File Management:** ดูรายชื่อและ **"ลบ"** ไฟล์กฎระเบียบที่ไม่ต้องการออกจากระบบได้ทันที
* **Dynamic Knowledge Base:** ระบบสมอง AI (FAISS) ที่สามารถ Re-index เพื่อจดจำข้อมูลใหม่ได้ตลอดเวลา

---

## 🛠️ การติดตั้งและใช้งาน (Local Installation)

### 1. เตรียมเครื่องมือ
ต้องมี Python 3.9 ขึ้นไป และติดตั้ง Git

### 2. ติดตั้งโปรเจกต์
```bash
git clone [https://github.com/ช](https://github.com/ช)ื่อUserของคุณ/dsd-course-architect.git
cd dsd-course-architect

#3. สร้าง Environment และติดตั้งไลบรารี
# Windows
python -m venv .venv
.venv\Scripts\activate

# ติดตั้ง Library
pip install -r requirements.txt

#4. ตั้งค่า API Key
GOOGLE_API_KEY="AIzaSy... (ใส่คีย์ของคุณที่นี่)"


dsd-course-architect/
├── app.py                   # ไฟล์หลัก (Main Entry Point)
├── requirements.txt         # รายชื่อไลบรารีที่ต้องใช้
├── .env                     # (Local Only) เก็บ API Key
├── dsd_logo.png             # โลโก้หน่วยงาน
├── knowledge_base/          # 📂 โฟลเดอร์เก็บไฟล์กฎ (.txt) ที่ AI จะอ่าน
├── db_storage/              # 🧠 (Auto) สมองของ AI (FAISS Index)
└── src/
    ├── __init__.py
    ├── logic/               # 🧠 ส่วนประมวลผล (Backend Logic)
    │   ├── __init__.py
    │   ├── ai_engine.py     # คำสั่ง Prompt และการคุยกับ Gemini
    │   ├── data_manager.py  # ระบบจัดการฐานข้อมูล Vector (FAISS)
    │   └── doc_generator.py # ระบบสร้างไฟล์ Word (.docx)
    └── ui/                  # 🎨 ส่วนแสดงผล (Frontend UI)
        ├── __init__.py
        ├── admin_page.py    # หน้า Admin (จัดการไฟล์, แกะกฎ)
        └── user_page.py     # หน้า User (ออกแบบ, โหลดไฟล์)