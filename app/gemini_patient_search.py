# Python service to connect with Gemini and query FastAPI backend
import requests
import json

# === Cấu hình ===
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
BACKEND_API_URL = "http://localhost:8000/patients/search"

# === Prompt chuẩn yêu cầu Gemini sinh JSON ===
PROMPT_INSTRUCTION = '''
Bạn là trợ lý giúp người dùng truy vấn bệnh nhân trong bệnh viện.
Hãy trích xuất các tiêu chí từ câu hỏi sau và trả về dưới dạng JSON có định dạng như sau:

{
  "name": "search_patients",
  "arguments": {
    "first_name": "...",
    "last_name": "...",
    "medical_id": "...",
    "gender": "M|F|O",
    "year_of_birth": 1990,
    "address": "..."
  }
}

Nếu thông tin không có thì bỏ qua trường đó.
'''

def call_gemini(question: str) -> dict:
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT_INSTRUCTION + "\nCâu hỏi: " + question}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(GEMINI_URL, headers=headers, json=payload)
    result = response.json()

    try:
        raw_text = result['candidates'][0]['content']['parts'][0]['text']
        json_start = raw_text.find('{')
        parsed = json.loads(raw_text[json_start:])
        return parsed['arguments']
    except Exception as e:
        raise ValueError(f"Gemini response parse failed: {e}\nRaw: {result}")

def query_fastapi(arguments: dict):
    response = requests.get(BACKEND_API_URL, params=arguments)
    return response.json()

def natural_language_response(patients: list):
    if not patients:
        return "Không tìm thấy bệnh nhân nào phù hợp."
    messages = [f"\n✅ Tìm thấy {len(patients)} bệnh nhân phù hợp:"]
    for p in patients:
        messages.append(f"- {p['first_name']} {p['last_name']} (Mã: {p['medical_id']}, Năm sinh: {p['date_of_birth'][:4]})")
    return "\n".join(messages)

# === Luồng xử lý chính ===
def search_by_question(question: str):
    print("[1] Nhận câu hỏi người dùng:", question)
    args = call_gemini(question)
    print("[2] JSON truy vấn từ Gemini:", args)
    patients = query_fastapi(args)
    print("[3] Kết quả truy vấn:", patients)
    reply = natural_language_response(patients)
    return reply

# === Demo thử ===
if __name__ == "__main__":
    q = "Tìm bệnh nhân nữ tên Dung sinh năm 1993 ở Cần Thơ"
    print(search_by_question(q))
