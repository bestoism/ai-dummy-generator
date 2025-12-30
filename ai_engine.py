import os
import json
from google import genai
from google.genai import types
from groq import Groq
from dotenv import load_dotenv

# Load Environment
load_dotenv()

def get_schema_from_prompt(user_prompt, provider="gemini"):
    """
    Generate schema dari prompt user.
    Provider tersedia: 'gemini' atau 'groq'
    """

    print(f"🚀 Mengirim prompt ke {provider.upper()}...")

    # =======================
    # SYSTEM INSTRUCTION (TIDAK DIUBAH)
    # =======================
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
        json_text = ""

        # =======================
        # OPSI 1: GOOGLE GEMINI
        # =======================
        if provider == "gemini":
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return {"error": "❌ GEMINI_API_KEY tidak ditemukan di .env"}

            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.7
                )
            )

            json_text = response.text

        # =======================
        # OPSI 2: GROQ (LLAMA 3)
        # =======================
        elif provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                return {"error": "❌ GROQ_API_KEY tidak ditemukan di .env"}

            client = Groq(api_key=api_key)

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            json_text = completion.choices[0].message.content

        else:
            return {"error": "❌ Provider tidak dikenali. Gunakan 'gemini' atau 'groq'."}

        # =======================
        # CLEAN & PARSE JSON
        # =======================
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]

        return json.loads(json_text)

    except Exception as e:
        print(f"❌ ERROR {provider.upper()}: {e}")
        return None
