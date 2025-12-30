import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: API Key tidak ditemukan di .env")

# Inisialisasi Client Baru
client = genai.Client(api_key=api_key)

def get_schema_from_prompt(user_prompt):
    print(f"🚀 Mengirim prompt ke Gemini (Model: gemini-2.5-flash): {user_prompt}")
    
    system_instruction = """
    Kamu adalah Data Engineer. Ubah request user menjadi JSON Schema.
    Format JSON:
    {"rows": 100, "columns": [{"name": "col_name", "type": "integer/float/categorical", "min": 0, "max": 100, "values": []}]}
    Pastikan type hanya boleh: 'integer', 'float', atau 'categorical'.
    """
    
    full_prompt = f"{system_instruction}\n\nUser Request: {user_prompt}"

    try:
        # Request ke Gemini 2.5 Flash
        response = client.models.generate_content(
            model='gemini-2.5-flash', # <--- KITA GANTI DI SINI
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                temperature=0.7
            )
        )
        
        # Parsing Hasil
        json_text = response.text
        
        # Bersihkan response
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]
            
        return json.loads(json_text)
        
    except Exception as e:
        print(f"❌ ERROR GEMINI: {e}")
        return None