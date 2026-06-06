
import streamlit as st
import pandas as pd
import requests

# Ambil input kata kunci pencarian dari pengguna di HP
keyword_input = st.text_input("Cari Produk Tren (Misal: Tempered Glass, TWS):", "Tempered Glass")

@st.cache_data(ttl=3600) # Hemat kuota API! Data disimpan 1 jam di memori
def fetch_rapidapi_shopee(keyword):
    # Masukkan alamat URL Endpoint dari RapidAPI yang Anda pilih
    url = "https://shopee-data-importer.p.rapidapi.com/search" 
    
    # Masukkan parameter pencarian (sesuaikan dengan dokumentasi API-nya)
    querystring = {"keyword": keyword, "region": "ID", "limit": "10"}
    
    # MASUKKAN API KEY GRATIS ANDA DI SINI
    headers = {
        "X-RapidAPI-Key": "8a8e528d12mshd7ed5243ffc3f97p1b8a42jsn5875a0d585d7",
        "X-RapidAPI-Host": "shopee-scraper-indonesia.p.rapidapi.com"
    }
    
    try:
        # Menembak server RapidAPI secara real-time
        response = requests.get(url, headers=headers, params=querystring)
        data_json = response.json()
        
        # Ekstrak data JSON menjadi tabel (struktur disesuaikan dengan respons asli API)
        items = data_json.get("products", [])
        
        list_produk = []
        for item in items:
            list_produk.append({
                "Nama Produk": item.get("title"),
                "Harga (Rp)": item.get("price"),
                "Penjualan (Bulanan)": item.get("historical_sold"),
                "Rating": item.get("rating"),
                "Toko": item.get("shop_name")
            })
            
        df = pd.DataFrame(list_produk)
        # Rumus Proyeksi GMV Otomatis
        df["Estimasi GMV (Rp)"] = df["Harga (Rp)"] * df["Penjualan (Bulanan)"]
        return df
        
    except Exception as e:
        # Jika kuota habis atau key salah, tampilkan pesan aman
        st.warning("Menampilkan data simulasi (Kuota API eksternal belum terhubung/habis).")
        # Balikkan data simulasi agar aplikasi tidak macet/blank merah
        mock_data = [
            {"Nama Produk": f"{keyword} Premium Furycube", "Harga (Rp)": 85000, "Penjualan (Bulanan)": 1420, "Rating": 4.9, "Estimasi GMV (Rp)": 120700000},
            {"Nama Produk": f"{keyword} OOTD Kasual", "Harga (Rp)": 125000, "Penjualan (Bulanan)": 650, "Rating": 4.8, "Estimasi GMV (Rp)": 81250000}
        ]
        return pd.DataFrame(mock_data)

# Panggil fungsi dan tampilkan di Streamlit
if st.button("MULAI RISET DATA"):
    df_hasil = fetch_rapidapi_shopee(keyword_input)
    st.dataframe(df_hasil, use_container_width=True)
