import streamlit as st
import pandas as pd
from generator import generate_dataframe
from ai_engine import get_schema_from_prompt

# 1. Config Halaman
st.set_page_config(page_title="AI Dummy Data Generator", layout="centered")

# 2. Inisialisasi Session State (Memori)
# Gunanya menyimpan data agar tidak hilang saat tombol download diklik
if "generated_df" not in st.session_state:
    st.session_state.generated_df = None
if "schema_preview" not in st.session_state:
    st.session_state.schema_preview = None

# --- SIDEBAR KONFIGURASI ---
with st.sidebar:
    st.header("⚙️ Konfigurasi AI")
    ai_provider = st.radio(
        "Pilih Provider:",
        ("Google Gemini", "Groq (Llama 3)")
    )
    
    if ai_provider == "Groq (Llama 3)":
        st.caption("⚡ Groq menggunakan model Llama-3. Sangat cepat & limit tinggi.")
    else:
        st.caption("🧠 Gemini adalah model asli dari Google.")

st.title("🤖 AI Dummy Data Generator")

# --- INPUT FORM ---
with st.form("input_form"):
    # Kita tidak perlu session state khusus untuk text_area karena ada di dalam form
    prompt = st.text_area(
        "Deskripsikan data yang kamu inginkan",
        placeholder="Contoh: Buatkan data 1000 karyawan startup dengan gaji...",
        height=150
    )
    
    col1, col2 = st.columns(2)
    with col1:
        row_override = st.number_input("Jumlah baris", min_value=1, max_value=100000, value=100)
    
    submitted = st.form_submit_button("Generate Data")

# --- LOGIC GENERATE (Hanya jalan saat tombol Generate diklik) ---
if submitted:
    if not prompt:
        st.warning("⚠️ Mohon isi deskripsi data.")
    else:
        # Tentukan provider
        provider_key = "gemini" if "Gemini" in ai_provider else "groq"
        
        with st.spinner(f"🤖 AI ({provider_key}) sedang berpikir..."):
            # Panggil AI
            schema = get_schema_from_prompt(prompt, provider=provider_key)
            
            if schema and "error" not in schema:
                # Override rows
                schema["rows"] = row_override
                
                # SIMPAN KE SESSION STATE (Supaya awet)
                st.session_state.schema_preview = schema
                
                try:
                    # Generate Data
                    df = generate_dataframe(schema)
                    # SIMPAN DATA KE SESSION STATE
                    st.session_state.generated_df = df
                    
                    st.success("✅ Berhasil generate data baru!")
                    
                except Exception as e:
                    st.error(f"Gagal generate data: {e}")
            elif schema and "error" in schema:
                st.error(f"Konfigurasi Salah: {schema['error']}")
            else:
                st.error("❌ AI gagal merespon. Cek koneksi atau API Key.")

# --- TAMPILAN HASIL (Jalan setiap rerun jika data sudah ada di memori) ---
if st.session_state.generated_df is not None:
    st.divider()
    st.subheader("📊 Hasil Data")
    
    # Tampilkan Schema (Optional)
    with st.expander("Lihat Schema JSON"):
        st.json(st.session_state.schema_preview)

    # Tampilkan Tabel
    st.dataframe(st.session_state.generated_df.head(50)) # Preview 50 baris
    
    # Tombol Download (Sekarang aman diklik karena data diambil dari session_state)
    csv = st.session_state.generated_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="dummy_data.csv",
        mime="text/csv"
    )