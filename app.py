import streamlit as st
import pandas as pd
from generator import generate_dataframe # Import fungsi yang baru kita buat

# Konfigurasi Halaman
st.set_page_config(page_title="AI Dummy Data Generator", layout="centered")

st.title("🤖 AI Dummy Data Generator")

# --- CONTOH SCHEMA (Nanti ini diganti output AI) ---
MOCK_SCHEMA = {
    "rows": 0, # Nanti di-override oleh input user
    "columns": [
        {"name": "id_siswa", "type": "integer", "min": 1000, "max": 9999},
        {"name": "nilai_ujian", "type": "float", "min": 0, "max": 100, "mean": 75},
        {"name": "jurusan", "type": "categorical", "values": ["IPA", "IPS", "Bahasa"]},
        {"name": "tinggi_badan", "type": "integer", "min": 150, "max": 180}
    ]
}
# ---------------------------------------------------

with st.form("input_form"):
    prompt = st.text_area(
        "Deskripsikan data yang kamu inginkan",
        placeholder="Contoh: Buatkan data 1000 siswa...",
        height=150
    )
    
    col1, col2 = st.columns(2)
    with col1:
        row_count = st.number_input("Jumlah baris", min_value=1, max_value=100000, value=100)
    
    submitted = st.form_submit_button("Generate Data")

if submitted:
    # Kita masih bypass prompt user dulu, langsung pakai MOCK_SCHEMA
    st.info("🔄 Generating dummy data (Mode Test: Menggunakan Schema Statis)...")
    
    # Update jumlah baris sesuai input user
    MOCK_SCHEMA["rows"] = row_count
    
    try:
        # Panggil Engine
        df = generate_dataframe(MOCK_SCHEMA)
        
        # Tampilkan Hasil
        st.success(f"✅ Berhasil membuat {len(df)} baris data!")
        st.dataframe(df.head(10)) # Tampilkan preview 10 baris aja biar enteng
        
        # Tombol Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="dummy_data.csv",
            mime="text/csv",
        )
        
    except Exception as e:
        st.error(f"Terjadi error: {e}")