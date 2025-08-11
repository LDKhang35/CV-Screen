import os
import time
import json
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Lấy API key từ biến môi trường
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("⚠️ Missing GOOGLE_API_KEY in environment variables.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Prompt mẫu để trích xuất thông tin từ CV text
EXTRACTION_PROMPT = """
Bạn là một trợ lý AI có nhiệm vụ trích xuất thông tin từ CV dưới đây và trả về kết quả theo định dạng JSON với các trường:
- full_name
- applied_position
- gender
- dob
- email
- address
- phone
- skills
- experience
- university
- major
- gpa
- certifications

Nếu không có thông tin thì để trống.

CV:
"""

MAX_RETRIES = 5

def extract_cv_info_with_llm(cv_text):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = model.generate_content(EXTRACTION_PROMPT + cv_text)
            result = response.text

            # Nếu Gemini trả về nội dung không phải JSON thuần, cần làm sạch
            if "```json" in result:
                result = result.split("```json")[-1]
            if "```" in result:
                result = result.split("```")[-2]

            return json.loads(result)

        except ResourceExhausted as e:
            print(f"⚠️ Lỗi 429 - Quá giới hạn lần {attempt}/{MAX_RETRIES}. Đang chờ retry...")
            if attempt == MAX_RETRIES:
                print("❌ Dừng lại sau khi vượt quá số lần thử lại.")
                raise RuntimeError("LLM extraction failed due to rate limit.")

            wait_time = attempt * 30
            print(f"⏳ Đợi {wait_time} giây...")
            time.sleep(wait_time)

        except Exception as e:
            raise RuntimeError(f"LLM extraction failed: {e}")

def classify_cv_vs_jd(cv_text, jd_text, max_retries=3):
    prompt = f"""
        Bạn là chuyên gia về tuyển dụng nhân sự, dưới đây là nội dung CV và JD. Hãy đánh giá mức độ phù hợp của ứng viên với vị trí tuyển dụng theo thang điểm từ 0% đến 100% và phân loại theo 3 mức:
        - Phù hợp: 80–100%
        - Cân nhắc: 50–79%
        - Không phù hợp: 0–49%

        Chỉ trả về kết quả theo định dạng JSON như sau:

        {{
        "label": "Phù hợp | Cân nhắc | Không phù hợp",
        "score": số nguyên từ 0 đến 100,
        "comment": "Nhận xét 2 đến 3 dòng rõ ràng về lý do vì sao ứng viên đạt được đánh giá ở mức đó."
        }}

        JD:
        {jd_text}

        CV:
        {cv_text}
        """

    retries = 0
    while retries < max_retries:
        try:
            response = model.generate_content(prompt)
            result = response.text

            if "```json" in result:
                result = result.split("```json")[-1]
            if "```" in result:
                result = result.split("```")[-2]

            data = json.loads(result)
            return data["label"], data["comment"], data["score"]

        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                print(f"[RETRY] Gặp lỗi quota 429, đợi 30 giây...")
                time.sleep(30)
                retries += 1
            else:
                raise RuntimeError(f"LLM classification failed: {e}")

    raise RuntimeError("Exceeded max retries for Gemini classification.")
