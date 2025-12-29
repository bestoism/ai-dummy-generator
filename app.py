import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="AI Dummy Data Generator", layout="centered")

st.title("🤖 AI Dummy Data Generator")
st.write("Generate data dummy realistis dengan deskripsi bahasa alami.")

# Input Section
with st.form("input_form"):
    prompt = st.text_area(
        "Deskripsikan data yang kamu inginkan",
        placeholder="Contoh: Buatkan data 1000 siswa dengan umur, nilai matematika, tinggi badan, dan hobi...",
        height=150
    )

    # Kolom untuk input angka biar rapi
    col1, col2 = st.columns(2)
    with col1:
        rows = st.number_input(
            "Jumlah baris",
            min_value=1,
            max_value=100000,
            value=100,
            step=10
        )
    
    # Tombol Submit
    submitted = st.form_submit_button("Generate Data")

# Logic Placeholder
if submitted:
    if not prompt:
        st.warning("⚠️ Mohon isi deskripsi data terlebih dahulu.")
    else:
        st.info("🔄 Memproses permintaan... (Logic AI belum terhubung)")
        st.write(f"Prompt: {prompt}")
        st.write(f"Target Baris: {rows}")