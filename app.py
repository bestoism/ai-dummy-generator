import streamlit as st
import pandas as pd
from generator import generate_dataframe
from ai_engine import get_schema_from_prompt

st.set_page_config(page_title="AI Dummy Data Generator", layout="centered")

st.title("🤖 AI Dummy Data Generator")

# =========================
# SIDEBAR KONFIGURASI AI
# =========================
with st.sidebar:
    st.header("⚙️ Konfigurasi AI")
    
    ai_provider_ui = st.radio(
        "Pilih Provider:",
        ("Google Gemini", "Groq (Llama 3)")
    )

    if ai_provider_ui == "Groq (Llama 3)":
        st.caption("⚡ Groq menggunakan model Llama-3 dari Meta. Sangat cepat & limit tinggi.")
        ai_provider = "groq"
    else:
        st.caption("🧠 Gemini adalah model asli dari Google.")
        ai_provider = "gemini"

# =========================
# FORM INPUT USER
# =========================
with st.form("input_form"):
    prompt = st.text_area(
        "Deskripsikan data yang kamu inginkan",
        placeholder="Contoh: Buatkan data 100 karyawan startup dengan gaji, divisi, dan jam lembur...",
        height=150
    )
    
    col1, col2 = st.columns(2)
    with col1:
        row_override = st.number_input(
            "Jumlah baris (Override)",
            min_value=1,
            max_value=100000,
            value=100
        )
    
    submitted = st.form_submit_button("Generate Data")

# =========================
# PROSES GENERATE
# =========================
if submitted:
    if not prompt:
        st.warning("⚠️ Mohon isi deskripsi data terlebih dahulu.")
    else:
        with st.spinner(f"🤖 AI ({ai_provider.upper()}) sedang merancang skema data..."):
            
            # 1. Generate Schema via AI
            schema = get_schema_from_prompt(
                user_prompt=prompt,
                provider=ai_provider
            )
            
            if schema:
                # Override jumlah baris
                schema["rows"] = row_override
                
                # Tampilkan Schema
                with st.expander("📄 Lihat Schema JSON yang digenerate AI"):
                    st.json(schema)

                # 2. Generate Data
                try:
                    df = generate_dataframe(schema)
                    
                    st.success(f"✅ Berhasil membuat {len(df)} baris data!")
                    st.dataframe(df.head(10))
                    
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="dummy_data.csv",
                        mime="text/csv",
                    )
                except Exception as e:
                    st.error(f"❌ Gagal generate data dari schema: {e}")
            else:
                st.error("❌ AI gagal membuat schema. Coba deskripsi yang lebih jelas.")
