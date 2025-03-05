import streamlit as st
import pandas as pd
from utils import load_data_from_sheets

# Konfigurasi Streamlit
st.set_page_config(
    page_title="Streamlit Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Informasi Spreadsheet
SPREADSHEET_ID = "1RIKxZ3s10YF4jBgkcanEy2op1JOUXLP6AkKqQpTSisU"  # Ganti dengan ID spreadsheet lo
RANGE_NAME = "Sheet1!A:T"  # Ganti dengan nama sheet dan range yang sesuai

# Load Data
df = load_data_from_sheets(SPREADSHEET_ID, RANGE_NAME)

# Sidebar
st.sidebar.header("Filter Data")

if df is not None:
    # Ubah tipe data kolom 'TANGGAL' menjadi datetime
    try:
        df['TANGGAL'] = pd.to_datetime(df['TANGGAL'])
    except:
        st.warning("Gagal mengubah format tanggal. Pastikan format tanggal di spreadsheet sudah benar.")

    # Filter Tanggal
    start_date = st.sidebar.date_input("Tanggal Mulai", df['TANGGAL'].min().date())
    end_date = st.sidebar.date_input("Tanggal Selesai", df['TANGGAL'].max().date())

    # Filter DataFrame
    df_filtered = df[
        (df['TANGGAL'].dt.date >= start_date) & (df['TANGGAL'].dt.date <= end_date)
    ]

    # Judul Aplikasi
    st.title("Streamlit Dashboard")

    # Metrik Utama
    col1, col2, col3 = st.columns(3)
    col1.metric("Jumlah Total Entri", len(df_filtered))
    col2.metric("Entri Terbaru", df_filtered['JUDUL'].iloc[-1], date=df_filtered['TANGGAL'].iloc[-1].strftime("%Y-%m-%d"))

    # Daftar Entri
    st.subheader("Daftar Entri")
    for index, row in df_filtered.iterrows():
        with st.expander(f"{row['JUDUL']} - {row['TANGGAL'].strftime('%Y-%m-%d')}"):
            st.write(f"**Penulis:** {row['PENULIS']}")
            st.write(f"**Kemenko:** {row['KEMENKO']}")
            st.write(f"**Tema:** {row['TEMA']}")
            st.write(f"**Sumber:** {row['SUMBER']}")
            st.write(f"**Nama:** {row['NAMA']}")
            st.write(f"**Link Video:** {row['LINK VIDEO']}")
            st.write(f"**Link Tiktok:** {row['Tiktok']}")
            st.write(f"**Link Snack Video:** {row['Snack Video']}")
            st.write(f"**Link Instagram:** {row['Instagram']}")

else:
    st.error("Gagal memuat data dari Google Sheets. Pastikan ID Spreadsheet dan nama range sudah benar, dan kredensial sudah terkonfigurasi dengan tepat.")
