import streamlit as st
import pandas as pd
import json
from generator import generate_dataframe
from ai_engine import get_schema_from_prompt

# 1. Config & Session State
st.set_page_config(page_title="AI Dummy Data Generator", layout="centered")

# Inisialisasi Memori
if "current_schema" not in st.session_state:
    st.session_state.current_schema = None # Menyimpan JSON Schema saat ini
if "generated_df" not in st.session_state:
    st.session_state.generated_df = None   # Menyimpan Tabel Data

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    ai_provider = st.radio("Provider AI:", ("Google Gemini", "Groq (Llama 3)"))
    st.caption("Gunakan Groq untuk kecepatan, Gemini untuk akurasi.")

st.title("🤖 AI Dummy Data Generator")

# ==========================================
# INPUT UTAMA (Prompt Natural)
# ==========================================
with st.form("main_form"):
    prompt = st.text_area(
        "Deskripsikan data:",
        placeholder="Buatkan data 500 siswa dengan nilai matematika, fisika, dan hobi...",
        height=100
    )
    col1, col2 = st.columns(2)
    with col1:
        initial_rows = st.number_input("Jumlah Baris:", min_value=1, max_value=100000, value=100)
    
    # Tombol Utama: Generate dari Prompt
    generate_new = st.form_submit_button("✨ Generate Data Baru")

# LOGIC 1: Generate Awal (Dari Prompt -> AI -> Data)
if generate_new:
    if not prompt:
        st.warning("Isi deskripsi dulu ya.")
    else:
        provider_key = "gemini" if "Gemini" in ai_provider else "groq"
        with st.spinner("AI sedang merancang & membuat data..."):
            # 1. AI bikin Schema
            schema = get_schema_from_prompt(prompt, provider=provider_key)
            
            if schema and "error" not in schema:
                schema["rows"] = initial_rows # Set jumlah baris
                
                # 2. Python bikin Data
                df = generate_dataframe(schema)
                
                # 3. Simpan ke Session State
                st.session_state.current_schema = schema
                st.session_state.generated_df = df
                st.success("✅ Data berhasil dibuat!")
            else:
                st.error("Gagal koneksi ke AI.")

# ==========================================
# HASIL & TUNING (Muncul jika ada data)
# ==========================================
if st.session_state.generated_df is not None:
    st.divider()
    
    # BAGIAN 1: DATA PREVIEW & DOWNLOAD
    st.subheader("📂 Preview Data")
    st.dataframe(st.session_state.generated_df.head(50))
    
    csv = st.session_state.generated_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="dummy_data.csv",
        mime="text/csv",
        type="primary"
    )

    st.markdown("---")

    # BAGIAN 2: TUNING / EDIT SCHEMA (Sesuai request kamu)
    st.subheader("🔧 Tuning Logic (Edit Schema)")
    
    with st.expander("Klik untuk mengedit Aturan / Schema JSON", expanded=False):
        st.info("Kamu bisa ubah 'min', 'max', atau aturan lainnya di sini, lalu Run Ulang.")
        
        # Konversi object JSON di memori jadi String biar bisa diedit di text area
        # Kita pakai JSON dari session_state agar sinkron
        schema_str_awal = json.dumps(st.session_state.current_schema, indent=2)
        
        updated_schema_str = st.text_area(
            "Editor JSON Schema:",
            value=schema_str_awal,
            height=300
        )
        
        col_tune_1, col_tune_2 = st.columns([1, 2])
        with col_tune_1:
            new_row_count = st.number_input("Update Jumlah Baris:", value=st.session_state.current_schema.get("rows", 100))
        
        # Tombol Run Ulang (Khusus edit manual)
        if st.button("🔄 Re-Generate dengan Editan Saya"):
            try:
                # 1. Parsing JSON hasil editan user
                new_schema = json.loads(updated_schema_str)
                new_schema["rows"] = new_row_count # Update rows dari input number baru
                
                # 2. Python bikin Data Ulang
                with st.spinner("Memproses aturan baru..."):
                    new_df = generate_dataframe(new_schema)
                    
                    # 3. Update Session State
                    st.session_state.current_schema = new_schema
                    st.session_state.generated_df = new_df
                    st.rerun() # Refresh halaman biar tabel di atas berubah
                    
            except json.JSONDecodeError:
                st.error("❌ JSON Error: Cek koma atau kurung kurawal kamu.")
            except Exception as e:
                st.error(f"Error: {e}")