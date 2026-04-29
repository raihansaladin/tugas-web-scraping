import streamlit as st
import pandas as pd
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

from query_rdf import query_berita

st.set_page_config(page_title="Berita Politik Indonesia", layout="wide")
st.title("📰 Berita Politik Indonesia")
st.caption("Web Scraping → RDF (Turtle) → SPARQL Query → Streamlit")

# ── Sidebar ──────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Filter")

    sumber_pilihan = st.selectbox(
        "Filter Sumber",
        options=["Semua", "Detik News", "CNN Indonesia", "Antara News", "Kompas", "Republika"]
    )

    kata_kunci = st.text_input("🔍 Cari Judul", placeholder="ketik kata kunci...")

# ── Konten Utama ─────────────────────────────────
if os.path.exists("berita.ttl"):
    sumber = None if sumber_pilihan == "Semua" else sumber_pilihan
    data = query_berita(sumber=sumber)

    # Filter kata kunci
    if kata_kunci:
        data = [d for d in data if kata_kunci.lower() in d["Judul"].lower()]

    if data:
        df = pd.DataFrame(data)

        # Statistik
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Berita", len(df))
        col2.metric("Sumber Aktif", df["Sumber"].nunique())
        col3.metric("Kategori", df["Kategori"].nunique())

        st.divider()

        # Tabel dengan link clickable
        st.subheader(f"📋 Daftar Berita — {sumber_pilihan}")

        df_tampil = df.copy()
        df_tampil["URL"] = df_tampil["URL"].apply(
            lambda x: f'<a href="{x}" target="_blank">🔗 Buka</a>'
        )

        st.write(
            df_tampil.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
    else:
        st.warning("Tidak ada berita ditemukan.")
else:
    st.info("File berita.ttl belum ada. Jalankan scraper terlebih dahulu.")