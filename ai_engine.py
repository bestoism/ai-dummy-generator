import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_schema_from_prompt(user_prompt):
    """
    Menggunakan Google Gemini untuk mengubah prompt menjadi JSON Schema.
    """
    
    # Konfigurasi Model agar outputnya JSON
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json", # Fitur kunci Gemini untuk paksa JSON
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Model cepat & gratis
        generation_config=generation_config,
    )

    # System Prompt kita gabung di sini
    system_instruction = """
    Kamu adalah Data Engineer Expert. Tugasmu adalah mengubah request user menjadi JSON Schema.
    
    Struktur JSON yang WAJIB diikuti:
    {
      "rows": (integer, default 100),
      "columns": [
        {
          "name": (string, snake_case),
          "type": (pilih satu: "integer", "float", "categorical"),
          "min": (number, optional untuk numeric),
          "max": (number, optional untuk numeric),
          "mean": (number, optional untuk float),
          "values": (array string, wajib untuk categorical)
        }
      ]
    }
    Pastikan angka realistis.
    """
    
    full_prompt = f"{system_instruction}\n\nUser Request: {user_prompt}"

    try:
        response = model.generate_content(full_prompt)
        
        # Gemini kadang mengembalikan teks JSON langsung
        json_text = response.text
        
        # Bersihkan jika ada sisa markdown (biasanya gemini flash sudah bersih, tapi jaga-jaga)
        json_text = json_text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(json_text)
        
    except Exception as e:
        print(f"Error Gemini: {e}")
        return None