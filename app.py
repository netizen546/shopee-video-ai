import streamlit as st
import whisper
import os
from moviepy.editor import VideoFileClip

# Set tampilan halaman browser
st.set_page_config(page_title="Shopee Video AI Optimizer", page_icon="🧡", layout="centered")

st.title("🧡 Shopee Video AI Metadata Optimizer")
st.write("Analisis video unboxing/review Anda langsung dari HP dan dapatkan caption SEO Shopee.")

# Input Form
product_name = st.text_input("Nama Produk:", placeholder="Contoh: Tempered Glass iPhone 17 Pro Max")
niche = st.selectbox("Kategori Shopee:", ["Elektronik & Gadget", "Fashion & Apparel", "Kecantikan & Rumah Tangga"])

# Upload File Video langsung dari galeri HP Android
uploaded_file = st.file_uploader("Pilih atau Rekam Video (.mp4, .mov)", type=["mp4", "mov", "avi"])

if uploaded_file is not None and product_name:
    if st.button("PROSES AI & GENERATE METADATA"):
        with st.spinner("AI sedang mendengarkan video Anda... Mohon tunggu..."):
            
            # Simpan file sementara di server
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.read())
                
            # 1. Ekstrak Audio
            video = VideoFileClip("temp_video.mp4")
            video.audio.write_audiofile("temp_audio.mp3", logger=None)
            video.close()
            
            # 2. Transkrip suara lewat Whisper AI
            model = whisper.load_model("base")
            result = model.transcribe("temp_audio.mp3", language="id")
            spoken_text = result["text"].strip()
            
            # Hapus file sampah sementara
            os.remove("temp_video.mp4")
            os.remove("temp_audio.mp3")
            
            # 3. Racik Caption Otomatis
            st.success("Analisis AI Selesai!")
            
            optimized_caption = (
                f"🔥 RACUN SHOPEE: {product_name.upper()} 🔥\n\n"
                f"Lagi cari {product_name} premium yang kualitasnya terbukti oke? "
                f"Tonton detail review-nya di video ini sampai habis! Produk ini punya spesifikasi "
                f"dan fungsi terbaik di kelasnya, worth it banget untuk jangka panjang.\n\n"
                f"🛒 Ambil harga promo sekarang dengan klik KERANJANG KUNING di kiri bawah! ✨\n\n"
                f"📌 HASHTAG REKOMENDASI ALGORITMA:\n"
                f"#RacunShopee #ShopeeVideo #{product_name.replace(' ', '')} #ShopeeHaul"
            )
            
            # Tampilkan di text area agar mudah di-copy di HP
            st.text_area("Salin Caption & Hashtag Ini:", value=optimized_caption, height=300)
                        
