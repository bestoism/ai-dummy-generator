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
    Kamu adalah Data Engineer Expert. Tugasmu adalah mengubah request user menjadi JSON Schema untuk generator data dummy.
    
    ATURAN PENTING:
    1. Output WAJIB JSON valid.
    2. Nama kolom (name) WAJIB format snake_case (contoh: 'jenis_kelamin', 'tinggi_badan', 'ipk').
    3. Tipe data hanya boleh: 'integer', 'float', 'categorical'.
    4. UNTUK DATA ANGKA (Integer/Float):
       - Tentukan 'min' dan 'max' yang masuk akal.
       - JIKA ITU DATA NILAI/SKOR/TINGGI/BERAT: Tambahkan field 'mean' (rata-rata) agar distribusi data terlihat normal (Bell Curve), bukan acak total.
       - Contoh: Untuk 'nilai_ujian', set min=0, max=100, mean=75.
    
    Format JSON:
    {
      "rows": 100,
      "columns": [
        {"name": "nama_kolom", "type": "...", "min": ..., "max": ..., "mean": ..., "values": [...]}
      ]
    }
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